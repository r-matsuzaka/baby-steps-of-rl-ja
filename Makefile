PACKAGE_DIR=.

format:
	isort $(PACKAGE_DIR)
	black $(PACKAGE_DIR)

lint:
	pylint -d C,R,fixme $(PACKAGE_DIR)

test:
	pytest