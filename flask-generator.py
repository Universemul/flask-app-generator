import jinja2
import os
import shutil
import subprocess

import argparse as ap
from pathlib import Path

import printer

DB_CHOICES = ['mysql', 'postgresql', 'sqlite']
BASE_TEMPLATES_DIR = "templates/base"

def main():
    parser = ap.ArgumentParser()
    parser.add_argument('--name', help='Name of your project')
    parser.add_argument('--db', help='Name of the database by default', required=False, choices=DB_CHOICES)
    parser.add_argument('--directory', help="The base directory where you want to create your app", default="/tmp/")
    parser.add_argument('--python', help="Define the python version", default="3.9.1")
    args = parser.parse_args()  
    directory = create_structure(args.name, args.directory)
    create_virtualenv(directory, args)
    create_requirements(directory, args)
    create_python_files(directory, args)
    print(f"CREATION OF {args.name} FINISHED. DON'T FORGET TO INSTALL THE REQUIREMENTS.TXT")

def create_structure(app_name: str, directory: str):
    full_directory = os.path.join(directory, app_name)
    if os.path.exists(full_directory):
        shutil.rmtree(full_directory)
    #if os.path.isdir(full_directory):
    #    printer.error(f"The directory {full_directory} already exists. Make a different choice")
    #    shutil.rmtree(full_directory)
    #    exit(-1)
    shutil.copytree("structure", full_directory)
    return full_directory

def create_requirements(directory: str, args: ap.Namespace):
    file_loader = jinja2.FileSystemLoader('templates')
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template('requirements.fg')
    output = template.render(database=args.db)
    write_file(os.path.join(directory, "requirements.txt"), output)

def create_virtualenv(directory: str, args: ap.Namespace):
    printer.info(f"pyenv virtualenv {args.python} {args.name}")
    process = subprocess.Popen(f'pyenv virtualenv {args.python} {args.name}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    printer.info(f'Creating or using virtual environment {args.name}')
    process.wait()
    if process.returncode == 0:
        printer.success(f'Virtual environment {args.name} created.')
        write_file(os.path.join(directory, ".python-version"), args.name)
        return
    error = str(process.stderr.read())
    if "already exists" in error:
        printer.info(f"Do you want to continue with the {args.name} virtualenv (yes or no)")
        continue_with_venv = input(f"").lower()
        if continue_with_venv in ["y", "yes"]:
            write_file(os.path.join(directory, ".python-version"), args.name)
            return
        else:
            printer.error(f"Installation stopped for {args.name}")
            exit(0)
    printer.error(f"Virtual environment creation failed: {error}")
    exit(-1)

def create_python_files(directory: str, args: ap.Namespace):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(BASE_TEMPLATES_DIR) for f in filenames if not f.startswith('.')]
    for _f in files:
        f_directory = os.path.dirname(_f).replace(f"{BASE_TEMPLATES_DIR}", "")
        if f_directory.startswith('/'):
            f_directory = f_directory[1:]
        render_template(_f, f"{directory}/{f_directory}", args)

def render_template(filename: str, to_directory: str, args: ap.Namespace):
    file_loader = jinja2.FileSystemLoader('')
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template(filename)
    output = template.render(database=args.db)
    _file = filename.split('/')[-1].replace('.fg', '.py')
    write_file(f"{to_directory}/{_file}", output)

def write_file(filename: str, content: str):
    output = Path(filename)
    printer.info(f"CREATING file {filename}")
    output.parent.mkdir(exist_ok=True, parents=True)
    output.write_text(content)

if __name__ == "__main__":
    main()
    
