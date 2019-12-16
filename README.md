# Notes

Notes is a simple note taking app created for linux terminal enviroment.
It is designed to make it easier to take notes directly from terminal.

## Setup

## Add alias for notes to your .bashrc file

1. Go to your HOME directory
2. Open .bashrc file in your favorite editor (`$ nano ~/.bashrc`)
3. Add `alias note=PATH/TO/NOTES/notes.sh` to the end of file and replace PATH/TO/NOTES with path to where you installed the repository
4. Save file and type `$ . ~/.bashrc` to reload it and apply the alias.
5. You can now use notes (`$ note`)

## Change notes to use your preferred editor

Default editor for notes is *nano*, but it can be changed in notes.ini file

1. Go to your installation directory of Linux-Notes/
2. Navigate to *notes.ini* and change `EDITOR` value to whatever editor you use (use the terminal call for editor not just the name)

## Save notes to other location

Default notes location is *~/Personal/Notes*, but it can be changed in *notes.ini* file

1. Go to your installation directory Linux-Notes/
2. Navigate to *notes.ini* and change `NOTES_LOCATION` value to whatever location you want

## Usage

Show help
`$ note --help`

Open main note file
`$ note`

Open main note file for specific category
`$ note -c [Category]`

Open specific note in category
`$ note -c [Category] -n [Note name]`

Remove specific note
`$ note -r -c [Category] - n [Note name]`

Remove whole category
`$ note -r -c [Category]`

Remove all notes
`$ note -r`

Show note list
`$ note -l {-c [Category]}`
