#!/bin/bash

help=false
list=false
remove=false
file_name=""
file_extension=".txt"
category_name=""

while [ -n "$1" ]; do # while loop starts

    case "$1" in

    -n)
        file_name="$2"
        if [ "$file_name" = "" ] ; then
            file_name="main"
        fi
        shift
        ;;

    -c)
        category_name="$2"
        if [ "$category_name" = "" ] ; then
            category_name="General"
        fi
        shift
        ;;

    -e)
        file_extension="$2"
        shift
        ;;

    -r)
        remove=true
        ;;

    -l)
        list=true
        ;;

    --help)
        help=true
        ;;

    *) echo "Option $1 not recognized" ;;

    esac

    shift

done

if [ "$help" = true ] ; then
    python3 $HOME/Personal/Projects/Note-Automation/notes.py "true false false none none none"
elif [ "$list" = true ] ; then
    python3 $HOME/Personal/Projects/Note-Automation/notes.py "false true false $category_name none none"
elif [ "$remove" = true ] ; then
    python3 $HOME/Personal/Projects/Note-Automation/notes.py "false false true $category_name $file_name $file_extension"
else
    python3 $HOME/Personal/Projects/Note-Automation/notes.py "false false false $category_name $file_name $file_extension"
fi
