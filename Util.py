import os
import sys
import subprocess

RESET = '\033[0m'
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
def print_color(text, r, g, b):
    print(get_color_escape(r, g, b) 
      + text
      + RESET)
def clear():
    print("\033[H\033[J", end="")
    sys.stdout.flush()