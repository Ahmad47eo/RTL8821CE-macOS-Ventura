# Roadmap

## 1. Hardware identification
- [ ] Confirm the Wi-Fi card's PCI vendor/device ID on the HP 250 G7.
- [ ] Confirm the adapter is PCIe RTL8821CE.
- [ ] Record macOS Ventura 13.7.8 build and OpenCore version.
- [ ] Collect sanitized hardware and boot logs.

## 2. Upstream research
- [ ] Review AirPort_RTW88 Ventura-specific docs and release assets.
- [ ] Review RTL88WiFi supported IDs, Ventura notes, and dependencies.
- [ ] Review RTW88-macOS package, daemon requirements, license, and IOMMU implications.
- [ ] Distinguish source archives from actual prebuilt binaries.
- [ ] Verify x86_64 architecture and macOS compatibility.

## 3. Candidate verification
- [ ] Verify repository owner, release tag, source provenance, and checksum.
- [ ] Inspect Info.plist bundle ID and PCI matching properties.
- [ ] Document all dependencies and kext load order.
- [ ] Document required OpenCore settings and security implications.
- [ ] Reject untrusted or incompatible binaries.

## 4. Safe testing
- [ ] Preserve a known-good EFI backup on USB.
- [ ] Make one reversible change at a time.
- [ ] Verify macOS boots before testing networking.
- [ ] Verify interface detection, network scanning, WPA2, DHCP, and DNS.
- [ ] Test reboot and sleep/wake.
- [ ] Record results with personal identifiers removed.

## 5. Release
- [ ] Publish reproducible instructions.
- [ ] Publish only binaries allowed by their licenses.
- [ ] Include source commit, build environment, checksum, and test matrix.
- [ ] Clearly label experimental and unverified builds.
