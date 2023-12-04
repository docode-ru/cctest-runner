#!/usr/bin/env python
import os
import glob
import argparse
from googletrans import Translator

def translate_text(text, src_lang='en', dest_lang='ru'):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

def translate_comments_and_strings(content, src_lang='en', dest_lang='ru'):
    lines = content.split('\n')
    translated_lines = []

    inside_comment = False

    for line in lines:
        if line.strip().startswith('#'):
            inside_comment = True
            translated_lines.append(translate_text(line.strip(), src_lang=src_lang, dest_lang=dest_lang))
        elif inside_comment and (not line.strip() or not line.lstrip().startswith('#')):
            inside_comment = False
        elif inside_comment:
            translated_lines.append(translate_text(line, src_lang=src_lang, dest_lang=dest_lang))
        else:
            translated_lines.append(line)

    return '\n'.join(translated_lines)

def process_file(file_path, src_lang='en', dest_lang='ru'):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    translated_content = translate_comments_and_strings(content, src_lang=src_lang, dest_lang=dest_lang)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(translated_content)

def traverse_directory(directory_path, src_lang='en', dest_lang='ru'):
    for file_path in glob.iglob(os.path.join(directory_path, '**/*.py'), recursive=True):
        process_file(file_path, src_lang=src_lang, dest_lang=dest_lang)
        print(f'Translated comments and strings in: {file_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate comments and strings in Python files.')
    parser.add_argument('directory_path', help='Path to the directory containing Python files.')
    parser.add_argument('--src_lang', default='en', help='Source language (default: en).')
    parser.add_argument('--dest_lang', default='ru', help='Destination language (default: ru).')

    args = parser.parse_args()

    directory_path = args.directory_path
    src_lang = args.src_lang
    dest_lang = args.dest_lang

    if not os.path.isdir(directory_path):
        print(f'Error: {directory_path} is not a valid directory.')
        exit(1)

    traverse_directory(directory_path, src_lang=src_lang, dest_lang=dest_lang)
