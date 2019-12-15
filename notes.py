#!/bin/python3
from sys import argv
import os
from getpass import getuser

NOTES_DIR = os.path.expanduser('~/Personal/Notes')

params = argv[1].split(' ')

show_help = params[0]
listing = params[1]
remove = params[2]
category = params[3]
file_name = params[4]
extension = params[5]

ignore = False

if extension[0] == '.':
    extension = extension[1:]
elif extension == '':
    extension = 'txt'

def print_listing(path):
    if os.path.exists(path):
        os.system(f'ls {path}')
    else:
        print(f'No notes found under category: {category}')

def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def create_note(category, file_name, extension):
    path = os.path.join(NOTES_DIR, category)
    ensure_dir(path)
    path = os.path.join(path, f'{file_name}.{extension}')
    if not os.path.exists(path):
        print('Creating new note..')
        os.mknod(path)
    return path

def open_note(path):
    print(f'Opening {file_name}.{extension} in category {category}')
    os.system(f'gedit {path}')

def remove_note(category, file_name, extension):
    if category != '':
        if file_name != '':
            path = os.path.join(NOTES_DIR, category, f'{file_name}.{extension}')
            if os.path.exists(path):
                while True:
                    remove = input(f'Remove note: {category}/{file_name}.{extension}? (Y/N): ').lower()
                    if remove == 'y':
                        os.remove(path)
                        print(f'Removed note {category}/{file_name}.{extension}')
                        break
                    elif remove == 'n':
                        print('User Aborted')
                        break
            else:
                print('No such note')
        else:
            path = os.path.join(NOTES_DIR, category)
            if os.path.isdir(path):
                while True:
                    remove = input(f'Remove CATEGORY: {category}? (Y/N): ').lower()
                    if remove == 'y':
                        os.system(f'rm -r {path}')
                        print(f'Removed category {category}')
                        break
                    elif remove == 'n':
                        print('User Aborted')
                        break
            else:
                print('No such caregory')
    else:
        if os.path.isdir(NOTES_DIR):
            while True:
                remove = input(f'Remove ALL NOTES? (Y/N): ').lower()
                if remove == 'y':
                    while True:
                        remove = input(f'Are you sure (you are removing all saved notes)? (Y/N): ').lower()
                        if remove == 'y':
                            os.system(f'rm -r {NOTES_DIR}')
                            print('Removed all saved notes')
                            break
                        elif remove == 'n':
                            print('User Aborted')
                            break
                    break
                elif remove == 'n':
                    print('User Aborted')
                    break
        else:
            print('There are no saved notes to remove')

def print_help():
    print('\nUSAGE:')
    print(' -n [filename]         set the filename')
    print(' -c [category]         specify the category the note is in')
    print(' -e [extension]        specify the file extension of note ')
    print(' -l                    for listing (can be  combined with -c for category specific')

if getuser() == 'root':
    if remove == 'false' or (remove == 'true' and category != ''):
        print('Warning, the command was executed as root, this is not advised, please switch to non-root user.')
        print('In order to remove effects of this command and all root\'s saved notes, use "sudo note -r"\n')
    else:
        print('Removing all root\'s saved notes')
        os.system(f'rm -r {NOTES_DIR}')
        ignore = True

if not ignore:
    if show_help == 'true':
        print_help()
    elif remove == 'true':
        remove_note(category, file_name, extension)
    else:
        if category == '':
            category = 'General'

        ensure_dir(NOTES_DIR)
        path = os.path.join(NOTES_DIR, category)

        if listing == 'true':
            print_listing(path)
        else:
            if file_name == '':
                file_name = 'main'
                extension = '__init__.txt'
                print('Main')
            path = create_note(category, file_name, extension)
            open_note(path)
