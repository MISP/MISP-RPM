# MISP-RPM

This RPMs work with a clean Red Hat installation. There are no external repositories like EPEL, Remi PHP or others needed. They only rely on optional official RHEL repositories and software collections - you'll obviously need a valid RedHat subscription attached.

If you want to use a full fletched MISP version with all available features like misp-modules, see [https://github.com/amuehlem/MISP-RPM/](amuehlem/MISP-RPM/). For this installation you'll need additional external repositories like EPEL and Remi PHP.

## Install

See [INSTALL8.md](INSTALL8.md) for this specific RPM install on RedHat and refer
to upstream MISP documentation for anything MISP related and/or upgrade paths.

## Reporting issues

Please report issues on this branch to https://github.com/MISP/MISP-RPM and not
to the original developers.

## History
### Feb 3 2025
- release 2.5.1-1-el8
- release 2.5.2-1-el8
- release 2.5.3-1-el8
- release 2.5.4-1-el8
- release 2.5.5-1-el8
- release 2.5.6-1-el8

### Jan 29 2025
- release 2.5.0-1-el8, misp for RHEL8 with PHP82

### Sep 20 2024
- release 2.4.198-1-el8, first version for RHEL8 systems

### Jul 11 2024
- release 2.4.194-1

### Apr 23 2024
- release 2.4.191-1

### Apr 2 2024
- release 2.4.188-1

### Feb 23 2024
- release 2.4.185-1

#### Feb 9 2024
- release 2.4.183-1
- release 2.4.184-1

#### Dec 19 2023
- release 2.4.182-1

#### Dec 12 2023
- release 2.4.181-1

#### Dec 8 2023
- Taking over the task to create this RPMS
- unforked the repository from https://github.com/amuehlem/MISP-RPM/
- lots of cleanup and adaption to the automated build environment
