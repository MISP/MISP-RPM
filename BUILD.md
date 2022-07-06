# Building the RPMs on RHEL 7

RHEL 7.9 fully tested (build and deployment)

## Prerequesites

RHEL must be registered and attached as we need Software collections for at
least PHP 7.3 (rh-php73)

`make prepare` should take care of this subscription-manager step and install a
small set of pre requirements

Be aware some external dependencies will be fetched from EPEL (check
`Makefile`) but that `epel-release` package and references are going to be
removed right before building the MISP RPM (see *Output* for those external
dependencies).

## Build

`make misp.rpm` should then cake care of all the remaining installation
components and the actual RPMs build

### Version bumping

Please check spec files in `SPECS/`, field `Version:` and `Release:`

Packages are using a given release or upstream git commit id as RPM versioning;
please keep in mind semver / version comparison, especially for packages with
no upstream versioning. Example is `gtcaca` which doesn't have any upstream
version nor tag and for which we set up an arbitrary version (1.0). If you
decide to change the commit id (cid) you'll have to bump the version which will
be used in the output RPM package.

## Output

Results should be found in the `RPMS/` and `RPMS-PREREQ-*/` directories.

`make release` will create directory `release` will all built and prerequesites
packages


Example release:

```bash
$ ls -1 release/
cmake3-3.17.5-1.el7.x86_64.rpm
cmake3-data-3.17.5-1.el7.noarch.rpm
faup-1.6.0+8e81b17-1.el7.x86_64.rpm
faup-devel-1.6.0+8e81b17-1.el7.x86_64.rpm
gtcaca-1.0+98c7aa8-2.el7.x86_64.rpm
gtcaca-devel-1.0+98c7aa8-2.el7.x86_64.rpm
imlib2-1.4.5-9.el7.x86_64.rpm
imlib2-devel-1.4.5-9.el7.x86_64.rpm
libcaca-0.99-0.40.beta20.el7.x86_64.rpm
libcaca-devel-0.99-0.40.beta20.el7.x86_64.rpm
libuv-1.44.1-1.el7.x86_64.rpm
libzstd-1.5.2-1.el7.x86_64.rpm
misp-2.4.159-1.el7.x86_64.rpm
misp-pear-crypt-gpg-2.4.159-1.el7.x86_64.rpm
misp-pecl-rdkafka-2.4.159-1.el7.x86_64.rpm
misp-pecl-redis-2.4.159-1.el7.x86_64.rpm
misp-pecl-ssdeep-2.4.159-1.el7.x86_64.rpm
misp-php-brotli-2.4.159-1.el7.x86_64.rpm
misp-python-virtualenv-2.4.159-1.el7.x86_64.rpm
rhash-1.3.4-2.el7.x86_64.rpm
ssdeep-devel-2.14.1-1.el7.x86_64.rpm
ssdeep-libs-2.14.1-1.el7.x86_64.rpm
```

## Cleanup

Normally subsequent `make misp.rpm` run should rebuild everything.

`make clean` will remove the artifacts and the build environment. Run this in
case of issue and/or if you want to rebuild everything from scratch.


**CAUTION** **CAUTION**

See comments in the `spec` files, especially regarding side effect on the
system being used for the build (`misp.spec`) - this build suite **will alter
the host system** by installing RedHat PHP Software collection. Therefore it
isn't recommended to run this on a production system nor the target host where
you plan to install MISP.

```
# we need to use the PHP environment installed with Redhat Software collection (scl)
# this seems quite a challenge to install *inside* the RPM build root
# so for some PHP extension we may already have the .so file present
# which is loaded by PECL right before trying to perform install/upgrade
# seems PECL segfaults in this case, thus the ugly hack to rename .ini file
# right before a `pecl install` call
```
