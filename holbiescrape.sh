#!/usr/bin/env bash
# Run the Holberton project scraper on a link to a Holberton project
project="$1"
python2 /home/vagrant/utils/holbiescraper/holbieproject.py "$project"
python2 /home/vagrant/utils/holbiescraper/holbieread.py "$project"
