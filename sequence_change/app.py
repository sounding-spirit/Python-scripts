import os
import sys

import click

#Assume all file names are in the format ****-0123.jpg
def parse_book_name(file_name):
    return file_name.split(".")[0][:-4]

def parse_book_page(file_name):
    return int(file_name.split(".")[0][-4:])

def parse_book_extension(file_name):
    return '.'+file_name.split(".")[1]


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
print("Script dir:",SCRIPT_DIR)
sys.path.append(os.path.dirname(SCRIPT_DIR))

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("path", type=click.Path(dir_okay=True, exists=True))
@click.argument("pages", type=str)
def cli(path,pages):
    # pages to remove
    errant_pages = pages.split(",")
    print(errant_pages)

    # get all files in the target folder
    # pwd = os.getcwd()                       # current folder
    file_names = sorted(os.listdir(path))    # array of file names in sorted order

    index = parse_book_page(file_names[0])

    for file_name in file_names:
        book = parse_book_name(file_name)
        page = parse_book_page(file_name)
        ext = parse_book_extension(file_name)
        print(book,page,ext)
        
        # if page needs to be deleted
        if str(page) in errant_pages:
            # print(file_name,"removed")
            os.chmod(os.path.join(path,file_name), 0o777) # change the permission to avoid access denied problem
            os.remove(os.path.join(path,file_name))
        else:
            os.rename(os.path.join(path,file_name), os.path.join(path,book)+"{:04d}".format(index)+ext)
            index+=1  # increment index for next page

if __name__ == "__main__":
    cli()