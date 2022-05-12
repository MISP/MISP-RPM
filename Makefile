.PHONY: misp.rpm
misp.rpm:
	rpmbuild --buildroot $(PWD)/BUILDROOT/ --define '_topdir .' -ba SPECS/misp.spec
