#!/bin/python3
import configparser
import os
from getpass import getuser
from shutil import rmtree
from sys import argv


parser = configparser.RawConfigParser()
parser.read('notes.ini')


NOTES_DIR = os.path.expanduser(parser.get('SETTINGS', 'NOTES_LOCATION'))

for sect in parser.sections():
    print('1')
    print(sect)


class Static(object):
    def __init__(self, show_help, listing, remove, category, filename, extension):
        self.Note = Note(category, filename, extension)
        if getuser() == 'root':
            print(
                'Warning, you are using root account for notes. This is not recommended')
            print(
                'Use "note -r" to remove all root\'s saved notes and use non-root account for notes.')
        if not len(self.Note.raw_category.split('/..') + self.Note.raw_category.split('../')) > 2:
            if show_help:
                Static.show_help()
            elif listing:
                self.show_listing()
            elif remove:
                self.remove()
            else:
                self.open()
        else:
            print(
                f'The category cannot point above parent directory ({self.Note.raw_category} -> {self.Note.full_raw_category_path})')

    @staticmethod
    def show_help():
        print('\nUSAGE:')
        print(' -n [filename]         set the filename')
        print(' -c [category]         specify the category the note is in')
        print(' -e [extension]        specify the file extension of note ')
        print(
            ' -l                    for listing (can be  combined with -c for category specific')

    def show_listing(self):
        if os.path.exists(self.Note.full_raw_category_path):
            os.system(f'ls --color=auto {self.Note.full_raw_category_path}')
        else:
            if not self.Note.raw_category == '':
                print(
                    f'No notes found under category: {self.Note.raw_category}')
            else:
                print('No notes found')

    def remove(self):
        if self.Note.raw_category == '' and self.Note.raw_filename == '':
            # Remove all notes
            if os.path.isdir(NOTES_DIR):
                if Static.ask_for_confirmation('REMOVE ALL NOTES?'):
                    if Static.ask_for_confirmation('Are you sure (will remove ALL saved notes)?'):
                        Static.remove_all_notes()
                        return True
                print('User-Canceled')
            else:
                print('You have no saved notes (nothing to remove)')
            return False
        elif self.Note.raw_filename == '':
            # Remove whole category
            if os.path.isdir(self.Note.full_category_path):
                category = self.Note.category
                if Static.ask_for_confirmation(f'Will fully remove category {category} with all its notes'):
                    self.Note.remove_category()
                    return True
                print('User-Canceled')
            else:
                print(f'No such category ({self.Note.category})')
            return False
        else:
            # Remove single note
            if os.path.exists(self.Note.full_path):
                path = self.Note.relative_path
                if Static.ask_for_confirmation(f'Will remove note {path}'):
                    self.Note.remove()
                    return True
                print('User-Canceled')
            else:
                print(f'No such note ({self.Note.relative_path})')
            return False

    def open(self):
        if not os.path.exists(self.Note.full_path):
            self.Note.create()
        self.Note.open()

    @staticmethod
    def ask_for_confirmation(text):
        while True:
            confirmation = input(f'{text} (Y/N): ').lower()
            if confirmation == 'y':
                return True
            elif confirmation == 'n':
                return False
            else:
                continue

    @staticmethod
    def remove_all_notes():
        # TODO: Change remove method
        rmtree(NOTES_DIR)
        # // os.system(f'rm -r {NOTES_DIR}')
        print('All notes has been removed')

    @staticmethod
    def ensure_dir():
        if not os.path.isdir(NOTES_DIR):
            print('Creating main notes directory')
            os.makedirs(NOTES_DIR)


class Note(Static):
    def __init__(self, category, filename, extension):
        self.raw_category = category
        # Set default category
        if self.raw_category == '':
            self.category = 'General'
        else:
            self.category = self.raw_category

        self.raw_filename = filename
        # Set default filename
        if self.raw_filename == '':
            self.filename = 'main'
        else:
            self.filename = self.raw_filename

        # Remove first dot in extension or default it to txt
        if extension != '':
            if extension[0] == '.':
                self.extension = extension[1:]
            else:
                self.extension = extension
        else:
            self.extension = 'txt'

        # Set some paths
        self.relative_path = os.path.join(
            self.category, f'{self.filename}.{self.extension}')
        self.full_path = os.path.join(NOTES_DIR, self.relative_path)
        self.full_category_path = os.path.join(NOTES_DIR, self.category)
        self.full_raw_category_path = os.path.join(
            NOTES_DIR, self.raw_category)

    def open(self):
        print(f'Opening {self.relative_path}')
        editor = parser.get('SETTINGS', 'EDITOR')
        os.system(f'{editor} {self.full_path}')

    def create(self):
        if not os.path.isdir(self.full_category_path):
            self.create_category()
        print(f'Creating {self.relative_path}')
        os.mknod(self.full_path)

    def create_category(self):
        Static.ensure_dir()
        print(f'Creating Category {self.category}')
        os.mkdir(self.full_category_path)

    def remove(self):
        print(f'Removing {self.relative_path}')
        os.remove(self.full_path)

    def remove_category(self):
        print(f'Removing category {self.category}')
        # TODO: Change remove method
        rmtree(self.full_category_path)
        # // os.system(f'rm -r {self.full_category_path}')


if __name__ == '__main__':
    try:
        params = argv[1].split(' ')

        show_help = params[0]
        if show_help == 'true':
            show_help = True
        else:
            show_help = False
        show_listing = params[1]
        if show_listing == 'true':
            show_listing = True
        else:
            show_listing = False
        remove = params[2]
        if remove == 'true':
            remove = True
        else:
            remove = False
        category = params[3]
        filename = params[4]
        extension = params[5]

        S = Static(show_help, show_listing, remove,
                   category, filename, extension)
    except IndexError:
        print('File can\'t be run directly use notes.sh instead')
