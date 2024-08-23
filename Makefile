
.DEFAULT_GOAL := all


.PHONY: copy_challenges_js
copy_challenges_js:
	rm -rf ../js-challenges/dist
	mkdir -p ../js-challenges/dist
	bin/copy_challenges_js.py challenges/ ../js-challenges/dist/challenges
	cp -r tests/ ../js-challenges/dist/tests
	cd ../js-challenges/dist && zip -r challenges_tests.zip challenges tests && mv challenges_tests.zip ~/Yandex.Disk-docode.ru.localized/projects/cctest/challenges-js


.PHONY: copy_challenges_py
copy_challenges_py:
	rm -rf ../python-challenges/dist
	mkdir -p ../python-challenges/dist
	bin/copy_challenges_py.py challenges/ ../python-challenges/dist/challenges
	cp -r tests/ ../python-challenges/dist/tests
	cd ../python-challenges/dist && zip -r challenges_tests.zip challenges tests && mv challenges_tests.zip ~/Yandex.Disk-docode.ru.localized/projects/cctest/challenges-python
	echo "Archive created and copied to Yandex.Disk.localized-docode"




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