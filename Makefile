PKG := compact_interval_set
PKG_VERS := 0.9
PKG_DEPS := \
	setup.cfg \
	$(PKG)/*.py

.PHONY: all
all: wheel

.PHONY: clean
clean:
	rm -rf dist $(PKG).egg-info build
	find . -name "*.pyc" | xargs rm
	find . -name __pycache__ | xargs rm -r

.PHONY: test
test: flake8 lint unittest

.PHONY: flake8
flake8:
	python3 -m flake8 $(PKG)

.PHONY: lint
lint:
	pylint -j2 $(PKG)

.PHONY: unittest
unittest:
	python3 -m unittest

.PHONY: wheel
wheel: dist/$(PKG)-$(PKG_VERS)-py3-none-any.whl

.PHONY: install
install: wheel
	sudo pip3 uninstall -y $(PKG)
	sudo pip3 install dist/$(PKG)-$(PKG_VERS)-py3-none-any.whl

.PHONY: uninstall
uninstall:
	sudo pip3 uninstall $(PKG)

.PHONY: publish
publish: all
	 python3 -m twine upload \
		dist/$(PKG)-$(PKG_VERS)-py3-none-any.whl \
		dist/$(PKG)-$(PKG_VERS).tar.gz

dist/$(PKG)-$(PKG_VERS)-py3-none-any.whl: $(PKG_DEPS) Makefile test
	python3 -m build
	python3 -m twine check $@
