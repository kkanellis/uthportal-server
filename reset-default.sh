#!/bin/bash

#COLORS
KNRM="\x1B[0m"
KRED="\x1B[31m"
KGRN="\x1B[32m"
KYEL="\x1B[33m"
KBLU="\x1B[34m"
KMAG="\x1B[35m"
KCYN="\x1B[36m"
KWHT="\x1B[37m"

DATABASE="uthportal"
CONFIG="config.json"

printf "\n$KRED\t\t***WARNING***$KNRM\n"
printf "This script will DROP the mongo database named \"uthportal\".\n"
printf "All configuration and settings files will be deleted too.\n"
printf "$KRED\t***THIS IS IRREVERSIBLE!!!***$KNRM\n"
while true; do
    read -p "Are you sure you want to continue? [y/n]: " CONTINUE
    case $CONTINUE in
        [Yy]* )
            mongo $DATABASE --eval "db.dropDatabase()" > /dev/null
            printf "Databse $KCYN""<$DATABASE>$KNRM wiped.\n"
            [ -f $CONFIG ] && rm $CONFIG #if the config file is existant, remove it
            printf "Removed $KCYN""config.json$KNRM"".\n"
            break
            ;;
        [Nn]* )
            printf "Aborting...\n"
            break
            ;;
        * )
            printf "\nInvalid input $KRED[$CONTINUE]$KNRM!\n"
            printf "Please enter $KGRN[Y/y]$KNRM for yes, or $KGRN[N/n]$KNRM for no! \n"
            ;;
    esac
done
printf "$KYEL""Bye :)$KNRM\n"
