import os
import sys

import click
import re
import shutil


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
cwd = os.getcwd()

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def cpy(path, target, regex):
    file_names = sorted(os.listdir(path))
    for file_name in file_names:
        if os.path.isdir(os.path.join(path,file_name)):
            cpy(os.path.join(path,file_name),target,regex)
        elif os.path.isfile(os.path.join(path,file_name)):
            if regex.match(file_name):
                shutil.copyfile(os.path.join(path,file_name),os.path.join(os.path.join(cwd,target),file_name))
                print(file_name+" moved to "+target)
        else:
            print(os.path.join(path,file_name)+" is not a file or dir")

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("path", type=click.Path(dir_okay=True, exists=True))
@click.argument("target", type=click.Path(dir_okay=True, exists=True))
@click.argument("regex", default=".*-0000.*",type=str)
def cli(path, target, regex):
    pattern = re.compile(regex)
    cpy(path,target,pattern)


if __name__ == "__main__":
    cli()