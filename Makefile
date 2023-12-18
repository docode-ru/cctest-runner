
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

.PHONY: archive_challenges
archive_challenges:
	cd dist && zip -r challenges.zip challenges && zip -r tests.zip tests


.PHONY: all_ru
all_ru: copy_challenges translate_comments copy_tests archive_challenges

.PHONY: all
all: copy_challenges copy_tests archive_challenges