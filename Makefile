
.DEFAULT_GOAL := all

.PHONY: copy_challenges
copy_challenges:
	mkdir -p dist
	bin/copy_challenges.py challenges/ dist/challenges


.PHONY: translate_comments
translate_comments:
	bin/translate_comments.py dist/challenges

# copy tests to dist
.PHONY: copy_tests
copy_tests:
	mkdir -p dist
	cp -r tests/ dist/tests

.PHONY: clean
clean:
	rm -rf dist

.PHONY: archive_python_challenges
archive_python_challenges:
	cd dist && zip -r challenges_tests.zip challenges tests && mv challenges_tests.zip ~/Yandex.Disk.localized/python-challenges
	echo "Archive created and copied to Yandex.Disk.localized"


.PHONY: all_ru
all_ru: copy_challenges translate_comments copy_tests archive_python_challenges

.PHONY: all
all: copy_challenges copy_tests archive_python_challenges

# create symbolic links to challenges
.PHONY: symlink_python_challenges
symlink_python_challenges:
	ln -s ../python-challenges/challenges

# create symbolic links to tests
.PHONY: symlink_python_tests
symlink_python_tests:
	ln -s ../python-challenges/tests

.PHONE: symlink_python
symlink_python: symlink_python_challenges symlink_python_tests