# MISP-RPM

This project will deliver you with a simple and reproducable way to install [MISP](https://github.com/MISP/MISP) on a Red Hat based system. Each release will contain a specific version of the software and will give you reproducable installations on dev, test, acceptance or prod systems.

# Two flavors

**This step is very important**

We provide two different flavors of RPMs for MISP. You should decide for one of them and stick to it for as long as possible. We don't provide any help to change between one or the other, a fresh installation is recommended to change from one to the other.

## RHEL only installation

This RPMs work with a clean Red Hat installation. There are no external repositories like EPEL, Remi PHP or others needed. They only rely on optional official RHEL repositories and software collections - you'll obviously need a valid RedHat subscription attached. Due to external dependencies in [MISP-Modules](https://github.com/MISP/misp-modules) this project can't control, we'll not provide a RPM for the modules. Just a single MISP instance is provided.
Files for this option will be provided in the [releases section](https://github.com/MISP/MISP-RPM/releases) of this project. Please make sure you use the correct version for your RHEL base system.

### Installation
See [INSTALL.md](INSTALL.md) for this specific RPM install on RedHat and refer
to upstream MISP documentation for anything MISP related and/or upgrade paths.

**As RHEL8 is officially end of life, we recommend to upgrade to RHEL9 or RHEL10**


## Full MISP installation with modules
If you want to use a full fletched MISP version with all available features like misp-modules, you can use the 2nd flavor of RPMs. You'll need to use EPEL, Remi PHP and other external repositories to solve dependency issues.
see [https://github.com/amuehlem/MISP-RPM/](https://github.com/amuehlem/MISP-RPM/). For this installation you'll need additional external repositories like EPEL and Remi PHP. The packages will be delivered through our own MISP repository.

### Installtion

See [INSTALL_full.md](INSTALL_full.md) for the full installation with modules and external repositories. For more information about MISP, check the official upstream MISP documentation for anything MISP related and/or upgrade paths.

**As RHEL8 is officially end of life, we recommend to upgrade to RHEL9 or RHEL10**

## Reporting issues
Any issues regarding setting up a MISP instance using the provided RPMs, can be reported here.

Issues with [MISP](https://github.com/MISP/MISP/) itself (application problems unrelated to the RPM) should be reported to the original developers.

## History
### NOV XX 2026
- Merging with [amuehlem/MISP-RPM](https://github.com/amuehlem/MISP-RPM/)

### Oct 12 2026
- misp-2.5.50 (2.5.49 was skipped in [MISP](https://www.github.com/MISP/MISP/)

### Sep 29 2026
- misp-2.5.48

### Sep 17 2026
- misp-2.5.47

### Sep 5 2026
- misp-2.5.46

### Aug 26 2026
- misp-2.5.45

### Jul 13 2026
- misp-2.5.44

### Jul 10 2026
- misp-2.5.43

### Jun 22 2026
- misp-2.5.42

### Jun 17 2026
- misp-2.5.41

### Jun 15 2026
- misp-2.5.40

### Jun 5 2026
- misp-2.5.39

### May 21 2026
- misp-2.5.38

### Apr 29 2026
- misp-2.5.37

### Apr 4 2026
- misp-2.5.36

### Mar 23 2026
- misp-2.5.35

### Mar 10 2026
- misp-2.5.34

### Mar 2 2026
- misp-2.5.33

### Jan 15 2026
- misp-2.5.32

### Dec 23
- misp-2.5.31

### Dec 12
- misp 2.5.28

### Dec 1
- misp 2.5.27

### Nov 20
- misp 2.5.26

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
