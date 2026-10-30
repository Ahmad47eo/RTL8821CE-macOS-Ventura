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
# The public MacKernelSDK declares apple80211_scan_result as the 152-byte
# public prefix. The upstream 1164-byte assertion incorrectly treats the
# private kernel allocation size as the public C type size. All accesses in
# fillScanResultFromBSS are through declared fields and cap IE copies at
# sizeof(d->asr_ie_data), so retain the public-prefix implementation.
source = Path("AirPort_RTW88/src/kext/AirportRTW88.cpp")
cpp = source.read_text()
abi_assert = '    static_assert(sizeof(apple80211_scan_result) == 1164, "Ventura CURRENT_NETWORK ABI changed");\n'
if abi_assert not in cpp:
    raise SystemExit("expected CURRENT_NETWORK size assertion not found; refusing patch")
cpp = cpp.replace(
    abi_assert,
    '    /* Public MacKernelSDK exposes the 152-byte scan-result prefix; the\n'
    '     * private Ventura allocation is larger. Only declared prefix fields\n'
    '     * are written, and IE copies are bounded by sizeof(asr_ie_data). */\n',
    1,
)
source.write_text(cpp)
print("Removed invalid private-allocation-size assertion; public fields remain bounded.")

print("Patched optional AWDL/P2P private-ABI dispatcher; STA path retained.")
