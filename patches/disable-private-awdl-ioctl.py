#!/usr/bin/env python3
"""Apply conservative Ventura compatibility patches to upstream AirPort_RTW88."""
from pathlib import Path

awdl = Path("AirPort_RTW88/src/kext/AirportRTW88AWDL.cpp")
s = awdl.read_text()
sig = "SInt32 AirportRTW88::apple80211VirtualRequest("
start = s.find(sig)
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
s = s[:start] + stub + s[end + 2:]
awdl.write_text(s)

source = Path("AirPort_RTW88/src/kext/AirportRTW88.cpp")
cpp = source.read_text()
bad_assert = '    static_assert(sizeof(apple80211_scan_result) == 1164, "Ventura CURRENT_NETWORK ABI changed");\n'
if bad_assert not in cpp:
    raise SystemExit("expected CURRENT_NETWORK size assertion not found; refusing patch")
good_assert = """    static_assert(sizeof(((apple80211_scan_result *)0)->asr_ie_data) == sizeof(void *),
                  "apple80211_scan_result IE member must be a pointer");
"""
cpp = cpp.replace(bad_assert, good_assert, 1)

# The public SDK declares asr_ie_data as void*. bzero() makes it NULL, so
# memcpy through it is invalid. Do not expose IE data until a real allocation
# and lifetime contract is implemented.
ie_start = cpp.find("    const size_t ieLength =")
if ie_start < 0:
    if "IE payload intentionally omitted" not in cpp:
        raise SystemExit("scan-result IE block not found; refusing patch")
else:
    ie_end_marker = "\n}\n\nIOReturn AirportRTW88::handleSCAN_RESULT"
    ie_end = cpp.find(ie_end_marker, ie_start)
    if ie_end < 0:
        raise SystemExit("scan-result function boundary not found; refusing patch")
    safe_ie = """    /* asr_ie_data is a pointer in this SDK, not inline storage.
     * Do not copy into the NULL pointer after bzero(). IE payloads are
     * omitted until their allocation/ownership contract is implemented. */
    d->asr_ie_len = 0;
    d->asr_ie_data = nullptr;
"""
    cpp = cpp[:ie_start] + safe_ie + cpp[ie_end:]
source.write_text(cpp)
print("Applied AWDL stub, corrected scan-result ABI assertion, and removed unsafe IE pointer writes.")
