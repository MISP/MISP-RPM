.PHONY: clean prepare release

arch=$(shell uname -p)
prereq_tmpdir=/tmp/misp-rpm-prereq
prereq_dir=./RPMS-PREREQ

epel_release_rpm=https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

prepare: /etc/yum.repos.d/epel.repo
	sudo subscription-manager register --auto-attach
	sudo yum-config-manager --enable rhel-server-rhscl-7-rpms
	sudo subscription-manager repos --enable rhel-7-server-optional-rpms
	sudo yum install -y scl-utils ca-certificates git

/etc/yum.repos.d/epel.repo:
	sudo yum install -y $(epel_release_rpm)

release: RPMS
	mkdir -p release
	cp RPMS/*/* release/
	cp RPMS-PREREQ-*/* release/

/usr/bin/rpmbuild:
	sudo yum install -y rpm-build

/usr/bin/yum-builddep:
	sudo yum install -y yum-utils

%.rpm: SPECS/%.spec /usr/bin/rpmbuild /usr/bin/yum-builddep
	if [ $@ = 'faup.rpm' ]; then \
		sudo rpm -U --replacepkgs RPMS/$(arch)/gtcaca-devel-*.rpm; \
	fi
	if [ $@ = 'misp.rpm' ]; then \
		sudo yum remove -y epel-release; \
	fi
	sudo yum-builddep -y $<
	rpmbuild --buildroot $(PWD)/BUILDROOT/ --define '_topdir .' -ba $<

gtcaca.rpm: prereq-cmake3 prereq-libcaca-devel

faup.rpm: gtcaca.rpm

misp.rpm: faup.rpm prereq-ssdeep-devel

$(prereq_tmpdir):
	mkdir -p $@

$(prereq_dir)-%:
	mkdir -p $@

prereq-%: $(prereq_tmpdir) $(prereq_dir)-%
	sudo yum install --downloadonly --downloaddir=$(prereq_tmpdir) $* | \
		sed -n '/^Installing:/,/^Transaction Summary/p' | \
		sort -u | \
		awk '$$4 == "epel" { print $$1 }' | \
		xargs -I _RPM_FILE_ sh -c 'cp -v $(prereq_tmpdir)/_RPM_FILE_*.rpm $(prereq_dir)-$*/'
	sudo yum install -y $(prereq_dir)-$*/*.rpm || sudo yum reinstall -y $(prereq_dir)-$*/*.rpm

clean:
	#sudo yum remove -y libcaca imlib2 rhash libzstd libuv cmake3 ssdeep-libs
	rm -rf BUILD BUILDROOT RPMS SRPMS
