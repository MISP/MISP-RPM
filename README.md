# MISP RPM

~~Fork of https://github.com/amuehlem/MISP-RPM/~~

## Update: 8. Dec 2023
I'm taking over the task of creating this RPMS and might put it together with my origional repository https://github.com/amuehlem/MISP-RPM/. For this I've unforked this repository and will manage it as a standalone repository.
This will need some cleanup work first ;-)

---

Thanks a million times to Andreas Muehlemann and SWITCH, their initial work was
a great help in writing this RHEL7.x specific branch

RPM packages built with this branch shouldn't require any external non RedHat
repository (EPEL, Remi PHP, ...) and only rely on optional official RHEL repo
and Software Collections - you'll obviously need a valid RedHat subscription
attached.

## Build

See [BUILD.md](BUILD.md)

## Install

See [INSTALL.md](INSTALL.md) for this specific RPM install on RedHat and refer
to upstream MISP documentation for anything MISP related and/or upgrade paths.

## Reporting issues

Please report issues on this branch to https://github.com/MISP/MISP-RPM and not
the original developers.
