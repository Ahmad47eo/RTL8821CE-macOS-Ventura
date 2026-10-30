#!/usr/bin/env python3
"""Disable only the optional AWDL/P2P private-ABI ioctl dispatcher.

The public MacKernelSDK intentionally forward-declares several private
apple80211 payloads. Referencing their layouts is unsafe and prevents a
portable Ventura build. Infrastructure Wi-Fi remains implemented elsewhere.
"""
from pathlib import Path
import re
p = Path("AirPort_RTW88/src/kext/AirportRTW88AWDL.cpp")
s = p.read_text()
start = s.find("SInt32 AirportRTW88::apple80211VirtualRequest(")
if start < 0:
    raise SystemExit("AWDL dispatcher signature not found; refusing patch")
end_marker = "\n}\n\nstatic int rtw88SendActionFrame"
end = s.find(end_marker, start)
if end < 0:
    raise SystemExit("AWDL dispatcher end marker not found; refusing patch")
stub = """SInt32 AirportRTW88::apple80211VirtualRequest(UInt request_type, int request_number,
                                               IO80211VirtualInterface *interface,
                                               void *data)
{
    (void)request_type;
    (void)request_number;
    (void)interface;
    (void)data;
    /* AWDL/P2P selectors use private Apple ABI layouts absent from the
     * public SDK. Do not guess their structure sizes or claim success. */
    return kIOReturnUnsupported;
}
"""
s = s[:start] + stub + s[end+2:]
p.write_text(s)
if "return kIOReturnUnsupported;" not in s[start:start+700]:
    raise SystemExit("stub verification failed")
# The public MacKernelSDK scan-result structure is 152 bytes and its
# asr_ie_data member is a POINTER, not an inline byte array. The upstream
# 1164-byte assertion is invalid for this public declaration, and writing
# IE bytes through the zeroed pointer would crash. Keep the safe scalar
# scan-result fields and report no IE payload until a valid owner/lifetime
# contract is implemented.
source = Path("AirPort_RTW88/src/kext/AirportRTW88.cpp")
cpp = source.read_text()
abi_assert = '    static_assert(sizeof(apple80211_scan_result) == 1164, "Ventura CURRENT_NETWORK ABI changed");\\n'
if abi_assert not in cpp:
    raise SystemExit("expected CURRENT_NETWORK size assertion not found; refusing patch")
cpp = cpp.replace(
    abi_assert,
    '    static_assert(sizeof(((apple80211_scan_result *)0)->asr_ie_data) == sizeof(void *),\\n'
    '                  "apple80211_scan_result IE member must be a pointer");\\n',
    1,
)
ie_start = '    const size_t ieLength = b.ies_len > sizeof(b.ies) ? sizeof(b.ies) : b.ies_len;\\n'
ie_end = '    }\\n'
start = cpp.find(ie_start)
if start < 0:
    if 'IE payload intentionally omitted' not in cpp:
        raise SystemExit("scan-result IE block not found; refusing patch")
else:
    end = cpp.find(ie_end, cpp.find('        /* Preserve the already-working Ventura SCAN_RESULT contract:', start))
    if end < 0:
        raise SystemExit("scan-result IE block end not found; refusing patch")
    end += len(ie_end)
    safe_ie = ('    /* asr_ie_data is a pointer in this SDK, not inline storage.\\n'
               '     * Do not copy into the NULL pointer after bzero(). IE payloads\\n'
               '     * are omitted until their allocation/ownership contract is\\n'
               '     * implemented for Ventura. */\\n'
               '    d->asr_ie_len = 0;\\n'
               '    d->asr_ie_data = nullptr;\\n')
    cpp = cpp[:start] + safe_ie + cpp[end:]
source.write_text(cpp)
print("Removed invalid ABI size assertion and unsafe IE pointer writes.")

print("Patched optional AWDL/P2P private-ABI dispatcher; STA path retained.")
