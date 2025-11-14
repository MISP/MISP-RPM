# MISP-RPM

This RPMs work with a clean Red Hat installation. There are no external repositories like EPEL, Remi PHP or others needed. They only rely on optional official RHEL repositories and software collections - you'll obviously need a valid RedHat subscription attached. Due to external dependencies in [MISP-Modules](https://github.com/MISP/misp-modules) this project can't control, we'll not provide a RPM for the modules. Just a single MISP instance is provided.

If you want to use a full fletched MISP version with all available features like misp-modules, see [https://github.com/amuehlem/MISP-RPM/](https://github.com/amuehlem/MISP-RPM/). For this installation you'll need additional external repositories like EPEL and Remi PHP.

## Install

See [INSTALL.md](INSTALL.md) for this specific RPM install on RedHat and refer
to upstream MISP documentation for anything MISP related and/or upgrade paths.

**As RHEL8 is officially end of life, we recommend to upgrade to RHEL9 or RHEL10**

## Reporting issues
Any issues regarding setting up a MISP instance using this RPMs, can be reported here.

Issues with [MISP](https://github.com/MISP/MISP/) itself (application problems unrelated to the RPM) should be reported to the original developers.

## History
### Nov 14
- version 2.5.25 for RHEL8/9/10

### Nov 4
- version 2.5.24 for RHEL8/9/10
- version 2.4.216 for RHEL8

### Oct 15
- version 2.5.23 for RHEL8/9/10

### Oct 6
- version 2.5.22 for RHEL8/9/10

### Sep 12
- cleaning up branches and simplifying the SPECS
 - the master branch is used to create RPMS for RHEL8/9/10
 - the rhel79 branch is just to keep the history for RHEL7

### Sep 2
- releas 2.5.20-el9
- renaming misp-php82-* packages to misp-php-* (this simplifies the build process to create this RPMs)

### Aug 9
- release 2.5.19-el8

### Aug 8
- release 2.5.18-el8

### Aug 5
- release 2.5.17-el8
- release 2.4.215-el8

### Jul 15
- release 2.5.16-el8
- release 2.4.214-el8

### Jun 22
- release 2.5.15-el8
- release 2.4.213-el8

### Jun 19
- release 2.5.14-el8

### Jun 16 2025
- release 2.5.13-el8
- release 2.4.211-el8

### May 14 2025
- release 2.5.11-el8
- release 2.5.12-el8
- release 2.4.10-el8

### Apr 9 2025
- release 2.5.10-el8

### Feb 24 2025
- release 2.5.7-1-el8 and 2.4.205-1-el8

### Feb 6 2025
- release 2.4.204-1-el8 for RHEL8 with PHP74

### Feb 3 2025
- release 2.5.1-1-el8
- release 2.5.2-1-el8
- release 2.5.3-1-el8
- release 2.5.4-1-el8
- release 2.5.5-1-el8
- release 2.5.6-1-el8

### Aug 29
- release 2.5.19-el9

### Aug 9
- release 2.5.18-el9

### Aug 5
- release 2.5.17-el9

### Jul 15
- release 2.5.16-el9

### Jun 22
- release 2.5.15-el9

### Jun 19
- release 2.5.14-el9

### Jun 16
- release 2.5.13-el9

### May 14
- release 2.5.11-el9
- release 2.5.12-el9

### Apr 9 2025
- release 2.5.10-el9

### Feb 24 2025
- release 2.5.7-1-el9

### Feb 6 2025
- release 2.5.0-1-el9
- release 2.5.1-1-el9
- release 2.5.2-1-el9
- release 2.5.3-1-el9
- release 2.5.4-1-el9
- release 2.5.5-1-el9
- release 2.5.6-1-el9
