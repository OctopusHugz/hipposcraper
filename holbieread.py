#!/usr/bin/env python2
"""Main entry point for holbieread

Usage:
    `./holbieread.py https://intranet.hbtn.io/projects/232`
"""
from scrapers import *


def get_args():
    """Method that grabs argv

    Returns:
        link (str): argv[1]
    """
    arg = sys.argv[1:]
    count = len(arg)

    if count > 1:
        print("[ERROR] Too many arguments (must be one)")
        sys.exit()
    elif count == 0:
        print("[ERROR] Too few arguments (must be one)")
        sys.exit()

    link = sys.argv[1]
    return link


def holbieread():
    """Entry point for hipporeader

    Scrapes for specific text to create a README automatically.
    """

    link = get_args()

    print("\nHolbiescraper version 2.0")
    print("Creating README.md file:")
    parse_data = BaseParse(link)

    project_type = parse_data.project_type_check()
    sys.stdout.write("  -> Scraping information... ")
    # Creating scraping object
    r_scraper = ReadScraper(parse_data.soup, project_type)

    print("done")

    # Writing to README.md with scraped data
    r_scraper.open_readme()
    r_scraper.write_title()
    r_scraper.write_tasks()
    if "interview" not in project_type:
        r_scraper.write_rsc()
        r_scraper.write_info()

    author = str(parse_data.json_data["author_name"])
    user = str(parse_data.json_data["github_username"])
    git_link = str(parse_data.json_data["github_profile_link"])

    r_scraper.write_footer(author, user, git_link)

    print("README.md all set!")


if __name__ == "__main__":
    holbieread()
