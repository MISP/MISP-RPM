# MISP RPM

Fork of https://github.com/amuehlem/MISP-RPM/ 

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
