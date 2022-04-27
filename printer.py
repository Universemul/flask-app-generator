import sys
from termcolor import colored, cprint

def error(message: str):
    cprint(message, "red", file=sys.stderr)

def info(message: str):
    cprint(message, "blue", file=sys.stdout)

def success(message: str):
    cprint(message, "green", file=sys.stdout) 