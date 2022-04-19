import argparse as ap
import jinja2
import os
import shutil
import subprocess

###
# Virtual env
# Comment gerer l'imports des views?
# Gerer postgresql/mysql et sqlite connection
###

DB_CHOICES = ['mysql', 'postgresql', 'sqlite']

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
    create_run(directory, args)
    create_python_files(directory, args)

def create_structure(app_name: str, directory: str):
    full_directory = os.path.join(directory, app_name)
    if os.path.exists(full_directory):
        shutil.rmtree(full_directory)
    #if os.path.isdir(full_directory):
    #    print(f"The directory {full_directory} already exists. Make a different choice")
    #    shutil.rmtree(full_directory)
    #    exit(-1)
    shutil.copytree("templates/structure", full_directory)
    return full_directory

def create_requirements(directory: str, args: ap.Namespace):
    file_loader = jinja2.FileSystemLoader('templates')
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template('misc/requirements.fg')
    output = template.render(database=args.db)
    write_file(os.path.join(directory, "requirements.txt"), output)

def create_virtualenv(directory: str, args: ap.Namespace):
    print(f"pyenv virtualenv {args.python} {args.name}")
    process = subprocess.Popen(f'pyenv virtualenv {args.python} {args.name}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('Creating virtual environment')
    process.wait()
    if process.returncode == 0:
        print('Virtual environment created.')
        write_file(os.path.join(directory, ".python-version"), args.name)
        return
    error = str(process.stderr.read())
    if "already exists" in error:
        print(f"Do you want to continue with the {args.name} virtualenv (yes or no)")
        continue_with_venv = input(f"").lower()
        if continue_with_venv in ["y", "yes"]:
            write_file(os.path.join(directory, ".python-version"), args.name)
            return
    print(f"Virtual environment creation failed: {error}")
    exit(-1)

def create_run(directory: str, args: ap.Namespace):
    file_loader = jinja2.FileSystemLoader('templates')
    env = jinja2.Environment(loader=file_loader)
    for _file in ['wsgy', 'app']:
        template = env.get_template(f'misc/{_file}.fg')
        output = template.render(database=args.db)
        write_file(os.path.join(directory, f"{_file}.py"), output)

def create_python_files(directory: str, args: ap.Namespace):
    for _file in [
        "config/__init__", "config/settings", 
        "models/__init__", "views"
    ]:
        file_loader = jinja2.FileSystemLoader('templates')
        env = jinja2.Environment(loader=file_loader)
        template = env.get_template(f'python_files/{_file}.fg')
        output = template.render(database=args.db)
        write_file(os.path.join(directory, f"{_file}.py"), output)

def write_file(filename: str, content: str):
    print(filename)
    with open(filename, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
    
