#!/usr/bin/env bash
# Run the Holberton project scraper on a link to a Holberton project
project="$1"
python2 /home/vagrant/utils/holbiescraper/holbieproject.py "$project"
project_return=$(echo "$?")
if [[ "$project_return" -ne 1 ]];
then python2 /home/vagrant/utils/holbiescraper/holbieread.py "$project"
else echo "Looks like there was an error running holbieproject, so I won't run holbieread. Exiting..."
fi
