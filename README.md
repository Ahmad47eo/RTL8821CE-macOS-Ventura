# RTL8821CE macOS Ventura Wi-Fi

Research project for investigating Realtek RTL8821CE Wi-Fi support on Intel Hackintosh systems, with a target of **macOS Ventura 13.7.8** and OpenCore.

> **Status: experimental research. No driver in this repository is currently verified as working on the target HP 250 G7.**

## Target hardware

- Laptop: HP 250 G7
- Wi-Fi: Realtek RTL8821CE PCIe
- Expected PCI ID: `10ec:c821` (confirm on the actual machine; do not assume)
- CPU: Intel Core i3-1005G1 (Ice Lake)
- macOS: Ventura 13.7.8
- Bootloader: OpenCore

## Project goals

1. Find a genuine prebuilt x86_64 driver compatible with Ventura.
2. Confirm the exact PCI device ID and supported hardware.
3. Document dependencies and OpenCore configuration.
4. Test safely with a known-good EFI backup.
5. Publish only binaries that may legally be redistributed and have clear provenance.

## Upstream projects to investigate

These are independent projects; this repository is not affiliated with their authors.

- [AirPort_RTW88](https://github.com/xnoah222/Airport_RTW88) — its documentation lists RTL8821CE and Ventura 13.7.7–13.7.8. A source ZIP is not a prebuilt kext; check Releases and build instructions carefully.
- [RTL88WiFi](https://github.com/X1REN41L/RTL88WiFi) — documents RTL8821CE PCI IDs including `10ec:c821`; check its Ventura-specific compatibility notes and dependencies.
- [RTL8821CE-macOS](https://github.com/Romeo352/RTL8821CE-macOS) — advertises a prebuilt RTW88 package. Its README describes a daemon and Ethernet-style interface and mentions IOMMU-related configuration. Treat this as experimental and review security implications before use.

## Safety first

- Keep a known-good, bootable OpenCore EFI backup on a separate USB.
- Never replace the entire EFI folder to install one driver.
- Do not mix kexts or configuration instructions from different projects.
- Verify release source, version, architecture, dependencies, checksum, and license.
- Do not disable SIP or change IOMMU/DMA settings unless the upstream project clearly requires it and the risks are understood.
- Never publish personal serial numbers, MLB, SystemUUID, ROM, MAC addresses, Wi-Fi names, or passwords.
- Do not redistribute third-party binaries unless their license allows it.
- A loaded kext does not by itself prove that Wi-Fi works.

## Current status

- [ ] Confirm the actual PCI vendor/device ID.
- [ ] Record the exact macOS build and OpenCore version.
- [ ] Identify a real prebuilt Ventura-compatible binary.
- [ ] Verify dependencies and release provenance.
- [ ] Review Ventura-specific OpenCore configuration.
- [ ] Test with a recoverable EFI backup.
- [ ] Confirm Wi-Fi interface appears and scans for networks.
- [ ] Test WPA2 connection, DHCP, DNS, reboot, and sleep/wake.
- [ ] Publish reproducible results.

## Contributing

Include the exact adapter PCI ID, macOS build, OpenCore version, kext versions, and sanitized logs. Do not upload personal EFI folders or identifying configuration values.

## Disclaimer

Independent community research. Not affiliated with Apple or Realtek. Compatibility is not guaranteed until tested on the stated hardware and macOS version.
