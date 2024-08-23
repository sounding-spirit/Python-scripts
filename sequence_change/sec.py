import os
import sys

import click

#Assume all file names are in the format ****-0123.ext
def parse_book_name(file_name):
    return file_name.split(".")[0][:-4]

def parse_book_page(file_name):
    return int(file_name.split(".")[0][-4:])

def parse_book_extension(file_name):
    return '.'+file_name.split(".")[1]

# get the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# get all files in the current folder
pwd = os.getcwd()                       # current folder
file_names = sorted(os.listdir(pwd))    # array of file names in sorted order
index = parse_book_page(file_names[0])  # starting index of the pages

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
def cli():
    while True:
        cmd_tokens = input("").split(" ")
        cmd = cmd_tokens[0]
        cmd_tokens.remove() # remove the command so that the rest are args

        if cmd == "drop":
            drop(cmd_tokens)
        elif cmd == "swap":
            swap(cmd_tokens)
        elif cmd == "exit":
            break
    reindex()

def drop(args):
    # pages to remove
    errant_pages = args.split(",")
    print(errant_pages)

    for file_name in file_names:
        book = parse_book_name(file_name)
        page = parse_book_page(file_name)
        ext = parse_book_extension(file_name)
        
        # if page needs to be deleted
        if str(page) in errant_pages:
            # print(file_name,"removed")
            os.chmod(file_name, 0o777) # change the permission to avoid access denied problem
            os.remove(file_name)

def reindex():
    index = parse_book_page(file_names[0])

    for file_name in file_names:
        book = parse_book_name(file_name)
        ext = parse_book_extension(file_name)
        os.rename(file_name, book+"{:04d}".format(index)+ext)
        index+=1  # increment index for next page

if __name__ == "__main__":
    cli()