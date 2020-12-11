#!/usr/bin/env python2
"""Module for WebScraper"""
from scrapers import *


class WebScraper:
    """WebScraper class

    High-Level_Programming project scraper.

    Args:
        soup (obj): BeautifulSoup obj containing parsed link

    Attributes:
        py_flag (int): For write_checker()
        py_js (int): For write_checker()
    """
    py_flag = 0
    js_flag = 0
    html_flag = 0
    css_flag = 0

    def __init__(self, soup):
        self.soup = soup
        self.file_names = self.find_files()
        self.prototypes_list = self.find_prototypes()

    def find_prototypes(self):
        """Method to scrape python prototypes

        Has a failsafe incase there are non-python files in scraped data.
        """
        res = []
        find_protos = self.soup.find_all(string=re.compile("Prototype: "))
        for item in find_protos:
            py_proto = item.next_sibling.text
            find_py = py_proto.find(":")
            if find_py != 1:
                res.append(py_proto)
            else:
                pass
        return res

    def find_files(self):
        """Method to scrape for python file names"""
        return self.soup.find_all(string=re.compile("File: "))

    def html_skeleton(self, file_name):
        html_string = ('<!DOCTYPE html>\n<html lang="en">\n'
                       '<head>\n'
                       '\t<meta charset="UTF-8">\n'
                       '\t<meta name="viewport" '
                       'content="width=device-width, initial-scale=1.0">\n'
                       '\t<title>Document</title>\n'
                       '</head>\n<body>\n\n'
                       '</body>\n</html>\n')
        with open(file_name, "w") as f:
            f.write(html_string)

    def write_files(self):
        """Method to write/create python files

        Has a function that creates directories if found in `file_name`.
        Last function creates required files in additional directory.
        """

        new_dir_files = []
        file_idx = 0
        one_dir_check = 0
        folder_name = None

        sys.stdout.write("  -> Creating task files... ")
        for item in self.file_names:
            text_file = item.next_sibling.text
            if "images" in text_file:
                os.mkdir("images")
                continue
            try:
                find_pyfile = text_file.find(".py")
                find_comma = re.search('(.+?),', text_file)

                # Creating sub directories if exists
                if find_comma is not None:
                    find_folder = re.search(', (.+?)/', text_file)
                else:
                    find_folder = re.search('(.+?)/', text_file)
                find_dir_file = re.search('/(.+?)$', text_file)
                if find_dir_file is not None:
                    new_dir_files.append(str(find_dir_file.group(1)))
                if find_folder is not None and one_dir_check is 0:
                    folder_name = str(find_folder.group(1))
                    os.mkdir(folder_name)
                    one_dir_check += 1

                # Handling multiple files
                if "," in text_file:
                    create_name = str(find_comma.group(1))
                    make_comma = open(create_name, "w+")
                    make_comma.close()
                elif "." not in text_file and one_dir_check is not 1:
                    os.mkdir(text_file)
                else:
                    w_file_name = open(text_file, "w+")
                    if ".py" in text_file:
                        self.py_flag = 1
                        w_file_name.write("#!/usr/bin/python3\n")
                    elif ".sh" in text_file:
                        w_file_name.write("#!/bin/bash\n")
                    elif ".js" in text_file:
                        self.js_flag = 1
                        w_file_name.write("#!/usr/bin/node\n")
                    elif ".html" in text_file:
                        self.html_flag = 1
                        self.html_skeleton(text_file)
                    elif ".css" in text_file:
                        self.css_flag = 1
                        w_file_name.write("{\n\t;\n}")
                    else:
                        pass
                    # Creating prototypes in parallel with files
                    if find_pyfile != -1:
                        w_file_name.write(self.prototypes_list[file_idx])
                        file_idx += 1
                    else:
                        pass
                    w_file_name.close()
            except AttributeError:
                sys.stdout.write("[ERROR] Failed to create ")
                sys.stdout.write("task file %s\n" % text_file)
                sys.stdout.write("                        ... ")
                continue
            except IOError:
                sys.stdout.write("[ERROR] Failed to make file, passing\n")
                sys.stdout.write("                        ... ")
                pass
            except IndexError:
                pass

        # Check if new dir created, insert files if there is
        if folder_name is not None and one_dir_check is 1:
            os.chdir(folder_name)
            for item in new_dir_files:
                if "," in item:
                    item_obj = re.search('/(.+?)$', text_file)
                    item = str(item_obj.group(1))
                dir_file = open(item, "w+")
                dir_file.close()
            os.chdir("..")
        self.write_checker()
        print("done")

    def write_checker(self):
        with open("check.sh", "w+") as f:
            f.write("#!/usr/bin/env bash\n")
            if self.js_flag == 1:
                f.write("semistandard --fix ")
            elif self.py_flag == 1:
                f.write("pep8 ")
            elif self.html_flag == 1 or self.css_flag == 1:
                f.write("/home/vagrant/utils/W3C-Validator/w3c_validator.py ")
            else:
                print("What kind of files do we have here?")
            if self.file_names:
                for i in self.file_names:
                    f.write('"%s" ' % i.next_sibling.text)
            f.write("\n")
