#!/usr/bin/python
'''
Python 2.x compliant (change <> to != for Python3)
File organizer by type/time/name

Copyright (C) 2013 Ignacio Alvarez <someoneigna@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import sys, os, time, glob, re
import shutil, filecmp

DEBUG_MODE = 0

#TODO: Make the arg parsing prettier, (using argparse maybe?).
#      - Add the posibility to save a list of file moved.
#      - Implement sorting by date.
def main(args):
    '''Main program entry point'''

    arguments = check_args(args, len(args))

    if arguments == "INVALID" or not arguments:
        print(" Invalid arguments...\n  Use \'-h\' for help.")
        return

    if arguments == "HELP":
        print_help()
        return

    directory = args[3]
    if not directory or not os.path.exists(directory):
        print(" Invalid directory...")
        return


    if arguments == "VALID":
        filetypes = get_filetypes(args[2])
        classificate_dir(args[1], filetypes, directory)
        return

    if arguments == "GET_DATES":
        dates, mode = get_dates(args[1])
        classificate_dir(mode, filetypes, directory, dates)
        return


def change_dir(directory):
    '''Changes current dir and returns it'''
    if directory <> ".":
        try:
            os.chdir(directory)

        except IOError:
            print("Cant access {0}...\n".format(directory))

        return os.getcwd()
    else:
        return directory


def check_for_file(fname):
    '''Checks if it's a valid file'''

    return not(os.path.islink(fname) or \
            os.path.isdir(fname) or \
            (fname == sys.argv[0]))


def fix_repeated(file_a, file_b, directory):
    '''Reacts on existing files, removing or saving with a different name.'''

    # If the files are the exact same remove it
    if filecmp.cmp(file_a, file_b):
        os.remove(file_a)
    else:
        # else we save rename and append -diff in route/'filename + diff'
        backup_filename = file_a + "-diff"
        fullroute = directory + backup_filename

        print("Saving as: {fullroute}\n".format(fullroute=fullroute))
        os.rename(file_a, backup_filename)
        shutil.move(backup_filename, fullroute)


def move_file(fname, directory):
    '''Move a file into specified dir, and checks for existing files'''

    try:
        if DEBUG_MODE:
            print("Moving \'{origin}\' ----> \'{destiny}\'".format(origin=fname, destiny=directory + fname))
        shutil.move(fname, directory)

    except shutil.Error:
        fullpath = directory + fname
        print("{fullpath} already exists, skipping...\n".format(fullpath=fullpath))
        fix_repeated(fname, fullpath, directory)


def organize_by_symbols(filetypes, directory):
    '''Organize files starting with "(,),-,_[]'''

    start_dir = os.getcwd()

    if os.path.exists(os.path.relpath(directory)):
        current_dir = change_dir(directory)

    files_processed = 0

    for filetype in filetypes:

        match = ''.join(' [][()$-_=]*' + '.' + filetype)

        # For matched file in dir
        for fname in glob.iglob(match):

            files_processed += 1

            # If folder for current letter doesn't exists
            if not os.path.exists("#misc-symbols" + "/"):
                os.mkdir("#misc-symbols")

            move_file(fname, "#misc-symbols" + "/")

    if current_dir <>  start_dir:
        change_dir(start_dir)

    return files_processed


def organize_by_name(filetypes, directory):
    '''Organize by name mode used in (-n and -n+)'''
    start_dir = os.getcwd()

    if os.path.exists(os.path.relpath(directory)):
        current_dir = change_dir(directory)

    files_processed = 0

    # For every chosen filetype
    for filetype in filetypes:

        # For every file on dir
        match = ''.join("^[A-Za-z0-9]*" + "." + filetype)

        for fname in glob.iglob(match):
            files_processed += 1

            # If folder for current letter doesn't exists
            dir_letter = fname[0].upper()
            directory = dir_letter + "/"

            if not os.path.exists(directory):
                os.mkdir(dir_letter)

            move_file(fname, directory)

    if current_dir <> start_dir:
        change_dir(start_dir)

    return files_processed


#def organize_by_date(mode, filetypes, directory, dates):
#    """Organize by date PENDING"""
#    return 0"""


def organize_by_filetype(filetypes, directory):
    '''Organize by filetype mode (-f)'''

    files_processed = 0

    start_dir = os.getcwd()

    if os.path.exists(os.path.relpath(directory)):
        current_dir = change_dir(directory)


    for ftype in filetypes:
        for fname in glob.glob("*." + ftype):

            files_processed += 1

            #Get filetype from filename
            filetype = fname.partition(".")[2]

            # If folder for current file filetype doesn't exists
            dirname = filetype + "/"

            if not os.path.exists(dirname):
                os.mkdir(filetype)
            move_file(fname, dirname)
        #for end
    #for end
    if current_dir <> start_dir:
        change_dir(start_dir)

    return files_processed

#TODO: Refactor this mess
def classificate_dir(mode, filetypes, directory, dates=0):
    '''Calls the corresponding function to sort files in selected mode'''

    files_classified = 0
    init_time = time.ctime()

    if "-n" in mode:
        files_classified = organize_by_name(filetypes, directory)

        if mode == "-n+":
            files_classified += organize_by_symbols(filetypes, directory)

    elif mode == "-tf" or mode == "-te": # time frame and time exact date modes
        #files_classified = organize_by_date(mode, filetypes, directory, dates)
        print("Not implemented yet... Sorry")
        return

    elif mode == "-f":
        files_classified = organize_by_filetype(filetypes, directory)

    else:
        print("Mode inexistant, exiting....")
        return


    if files_classified == 0:
        print("No files were organized. Ending...")

    else:
        file_str = "files" if(files_classified > 1) else "file"

        entries = {
                    'quantity': files_classified, 'files': file_str,
                    'start': init_time, 'end': time.ctime()
                  }

        #I really have to improve this
        message = """\n {0} {1} were organized.\n\n\
                Started at:\n\t{2}\n  \
                Ended at:\n\t{3}\n""".format(files_classified, file_str, init_time, time.ctime()) #I wish passing 'entries' would be possible :'(
        print(message)


def print_help():
    '''Print help string'''

    indent = "\t  "

    #Improve this calamity xD
    help_string = """nforg.py - A file organizer in python -\n\
            Arguments: nforg.py <mode> <filetypes> <dir>\n\
            Example: nforg.py -n \"pdf,png,txt\" .\n\n\
    Organizing mode:\n\t\t-n: by name\n\t\t-n+: by name (including numbers and symbols)\
            \n\t\t-t: by time\n\t\t-f: by filetype\n\n    Using \"-t\" time mode:\n\
    \n%sLooking for jpg files with the two specified dates, moving them to\n%sfolders with that specified date.\
    \n\n\t\tnforg.py -t \"12/05/2010+5/06/2012\" \"jpg\" .\
    \n\n%sLooking for ugly .doc files in a time frame and moving into\n%sfiles with the file day/month/year.\
    \n\n\t\tnforg.py -t \"12/04/2008 8/06/2009\" \"doc\" .\n\
    """

    print(help_string.format(indent, indent, indent, indent))


def check_args(argv, args):
    '''Checks and validates arguments'''

    global DEBUG_MODE
    valid_args = {"-n", "-n+", "-t", "-f", "-h"}

    #argv[1] is valid then check for debug mode
    if "d" in argv[1]:
        DEBUG_MODE = 1
        argv[1] = argv[1].replace('d', '')

    if args <= 1 or argv[1] not in valid_args:
        return "INVALID"


    if(args < 4 or argv[1] == "-h"):
        return "HELP"

    if(argv[1] == "-t"):
        return "GET_DATES"

    return "VALID"


def get_filetypes(arg):
    '''Parses filetypes from third argument'''

    if arg == "*":
        return "*"

    else:
        filetypes = arg.strip() #Remove possible whitespace input example: "pdf, png, tar"
        filetypes = {x for x in filetypes.split(",")} #Split "pdf,png,tar" into a set -> {pdf, png, tar}
        return filetypes

    return "ERROR"


def get_dates(line):
    '''Gets date and mode'''

    dates = []

    if "+" in line:
        dates = line.split("+")
        mode = "-te" #Exact date mode

    elif " " in line:
        dates = line.split(" ")
        mode = "-tf" #Time frame date mode

    return (dates, mode)


if __name__ == "__main__":
    main(sys.argv)


