# Driver research notes

Last updated: 2026-10-30

## Candidate comparison

| Project | Hardware claim | Ventura 13.7.8 evidence | Binary status | Caution |
|---|---|---|---|---|
| [AirPort_RTW88](https://github.com/xnoah222/Airport_RTW88) | Lists RTL8821CE PCIe | Documentation lists Ventura 13.7.7–13.7.8 | No confirmed ready-to-install release established here; Code > Download ZIP is source | Do not treat source ZIP as a kext |
| [RTL88WiFi](https://github.com/X1REN41L/RTL88WiFi) | Lists RTL8821CE IDs including `10ec:c821` | Ventura compatibility requires careful confirmation | Check upstream release assets | Follow only matching Ventura instructions |
| [RTL8821CE-macOS](https://github.com/Romeo352/RTL8821CE-macOS) | Targets RTL8821CE | Not independently verified on Ventura 13.7.8 HP 250 G7 | README advertises an RTW88 prebuilt package | README mentions IOMMU-related settings; understand DMA/security implications before use |

## What counts as verified

A candidate is not considered verified until all of the following are checked:

1. The actual card PCI ID matches the driver's supported device table.
2. The download is a real compiled x86_64 binary, not source code.
3. The release tag and source provenance are known.
4. The macOS version and kernel compatibility are documented.
5. All dependencies and required services are identified.
6. The license permits the intended use and redistribution.
7. The exact HP 250 G7 / Ventura 13.7.8 configuration is tested.

## Important technical distinction

A kext appearing in `kmutil showloaded` does not prove the driver matched the PCI device or created a usable Wi-Fi interface. Testing must separately confirm device matching, interface creation, scanning, association, DHCP, and internet access.

## Safety

Do not replace the entire EFI. Keep a known-good bootable EFI backup on a separate USB. Avoid changing SIP, Secure Boot, or IOMMU settings without a documented upstream requirement and a recovery plan. Never publish personal serial numbers, UUIDs, MAC addresses, or passwords.

## AirPort_RTW88 CI investigation (2026-10-30)

The current native-AirPort build attempt is blocked in upstream AWDL/P2P code, not by the bundle Info.plist. The upstream `AirportRTW88.hpp` includes `RTW88AWDLManager.hpp` and declares virtual-interface callbacks; `AirportRTW88.cpp` constructs and owns the AWDL manager, attaches AWDL/P2P virtual interfaces, and routes AWDL frames. Therefore, simply removing `AirportRTW88AWDL.cpp` from the Makefile is not a safe fix: the main driver has direct dependencies on those classes and callbacks.

The CI compiler errors seen in `AirportRTW88AWDL.cpp` involve Apple 802.11 SDK types that are unavailable/incompatible in the selected build SDK. A proper fix needs a source-level compatibility layer or a supported SDK/toolchain, followed by a successful clean x86_64 build. Do not ship a partially linked kext or label it Ventura-compatible until that succeeds.

The upstream repository currently has no official GitHub release asset for a ready-to-install Ventura binary. The user's repository workflow is a research build, not a validated installer. No EFI changes are required for this investigation.
