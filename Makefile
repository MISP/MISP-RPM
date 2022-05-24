.PHONY: clean prepare

arch=$(shell uname -p)

clean:
	rm -rf BUILD BUILDROOT RPMS SRPMS

/usr/bin/rpmbuild:
	sudo yum install -y rpm-build

/usr/bin/yum-builddep:
	sudo yum install -y yum-utils

%.rpm: SPECS/%.spec /usr/bin/rpmbuild /usr/bin/yum-builddep
	if [ $@ = 'faup.rpm' ]; then \
		sudo rpm -U --replacepkgs RPMS/$(arch)/gtcaca-devel-*.rpm; \
	fi
	sudo yum-builddep $<
	rpmbuild --buildroot $(PWD)/BUILDROOT/ --define '_topdir .' -ba $<

faup.rpm: gtcaca.rpm

misp.rpm: faup.rpm

prepare:
	sudo subscription-manager register --auto-attach
	sudo yum-config-manager --enable rhel-server-rhscl-7-rpms
	sudo subscription-manager repos --enable rhel-7-server-optional-rpms
	sudo yum install -y scl-utils ca-certificates
