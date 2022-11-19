# Build Script
Build script is a simple tool that you can use to write scripts that build your applications.

It is easy to learn along with being pretty powerful
# Basics
To run a simple command, make a .buildscript file and type in `run python`

When you run the file using python buildscript/main.py (name of your file).buildscript,
the python terminal should open.

You can already use the run function to perform many tasks liek compiling a C program.
Building an Electron app.
Using py-installer to package your python program.
And even more!

There are also additonal commands like sleep, which waits a duritation.
if, which checks if something is true or not.
log, which prints something to the screen, it can also take in different levels of logging like debug, warn, and error!

Here is a example of a simple Build Script program.
```run g++ -fdiagnostics-color=always -g main.cpp -o main.exe
variable log = output
io write log.txt log
```