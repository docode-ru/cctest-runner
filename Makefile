
.DEFAULT_GOAL := all

.PHONY: copy_challenges_py
copy_challenges_py:
	mkdir -p dist
	bin/copy_challenges_py.py challenges/ dist/challenges

.PHONY: copy_challenges_js
copy_challenges_js:
	mkdir -p dist
	bin/copy_challenges_js.py challenges/ dist/challenges



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
	ln -s ../python-challenges/tests


.PHONE: symlink_python
symlink_python: rm_symlinks symlink_python_challenges


# create symbolic links to js challenges
.PHONY: symlink_js_challenges
symlink_js_challenges:
	ln -s ../js-challenges/challenges
	ln -s ../js-challenges/tests


.PHONY: symlink_js
symlink_js: rm_symlinks symlink_js_challenges

# check if there are symlinks and remove them
.PHONE : rm_symlinks
rm_symlinks:
	if [ -L challenges ] || [ -L tests ]; then rm challenges; rm tests; fi


# create symbolic links to java challenges
.PHONY: symlink_java_challenges
symlink_java_challenges:
	ln -s ../java-challenges/challenges

# create symbolic links to java test
.PHONY: symlink_java_tests
symlink_java_tests:
	ln -s ../java-challenges/tests

.PHONY: symlink_java
symlink_java: symlink_java_challenges symlink_java_tests