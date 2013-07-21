#!/usr/bin/python
""" Python 2.x compliant (change <> to != for Python3)
    File organizer by type/time/name"""

import sys, string, os, time, glob
import shutil, filecmp

DEBUG_MODE = 0

def main(args):
    """Main program entry point"""

    arguments = check_args(args, len(args))

    if arguments == "INVALID":
        print(" Invalid arguments...\n  Use \'-h\' for help.")
        return

    if arguments == "HELP":
        print_help()
        return

    directory = args[3]

    if arguments == "VALID":
        filetypes = get_filetypes(args[2])
        classificate_dir(args[1], filetypes, directory)
        return


    if arguments == "GET_DATES":
        dates, mode = get_dates(args[1])
        classificate_dir(mode, filetypes, directory, dates)
        return

def change_dir(directory):
    """Changes current dir and returns it"""
    if directory <> ".":
        try:
            os.chdir(directory)
        except IOError:
            print("Cant access %s...\n" % directory)
    return os.getcwd()

def optimize(orig_filetypes):
    """For current dir scan valid filetypes
        return a list of valid filetypes"""

    #Phase 1: remove repeated, skip if "*"
    if orig_filetypes == "*":
        return orig_filetypes
    filetypes = []
    for filetype in orig_filetypes:
        if filetype not in filetypes:
            filetypes.append(filetype)

    return filetypes



def append_delimiter(words, delimiter):
    """Append delimiter in word list"""

    # Used if organize_x() was called skipping get_filetypes(arg)
    if delimiter not in words:
        for i, word in enumerate(words):
            words[i] = "." + word[i]


def check_for_file(fname):
    """Checks if it's a valid file"""

    return not(os.path.islink(fname) or \
            os.path.isdir(fname) or \
            (fname == sys.argv[0]))


def get_dict_list(mode):
    """Generates a dictionary with a mode to valid keys to match"""

    letters = string.ascii_lowercase
    numbers_plus_letters = string.digits + string.ascii_lowercase

    mode_to_container = {"-n":letters, "-n+":numbers_plus_letters}
    return mode_to_container[mode]


def fix_repeated(file_a, file_b, directory):
    """Reacts on existing files, removing or saving with a different name """

    # If the files are the exact same remove it
    if filecmp.cmp(file_a, file_b):
        os.remove(file_a)
    else:
        # else we save rename and append -diff in route/'filename + diff'
        backup_filename = file_a + "-diff"
        print("Saving as: %s\n" %(directory + backup_filename))
        os.rename(file_a, backup_filename)
        shutil.move(backup_filename, directory + backup_filename)


def move_file(fname, directory):
    """Move a file into specified dir, and checks for existing files"""

    try:
        if DEBUG_MODE:
            print("Moving \'%s\' ----> \'%s\'" %(fname, directory + fname))
        shutil.move(fname, directory)

    except shutil.Error:
        print("%s already exists, skipping...\n" % (directory + fname))
        fix_repeated(fname, directory + fname, directory)


def organize_by_symbols(orig_filetypes, directory):
    """Organize files starting with "(,),-,_" """

    current_dir = change_dir(directory)

    filetypes = optimize(orig_filetypes)

    files_processed = 0
    valid = "$()=-_"

    for char in valid:
        for filetype in filetypes:
            # For matched file in dir
            for fname in glob.glob(char + "*." + filetype):

                files_processed += 1

                # If folder for current letter doesn't exists
                if os.path.exists("#misc-symbols" + "/") == False :
                    os.mkdir("#misc-symbols")

                move_file(fname,"#misc-symbols" + "/")

    if current_dir <> directory:
        change_dir("..")

    return files_processed


def organize_by_name(orig_filetypes, mode, directory):
    """Organize by name mode (-n and -n+)"""

    current_dir = change_dir(directory)

    filetypes = optimize(orig_filetypes)
    files_processed = 0


    mode_dict = get_dict_list(mode)
    mode_folders = mode_dict.upper()
    alphanumeric = mode_dict + mode_folders

    if not(mode_dict) or not(mode_folders):
        print("Invalid letters for comparision\n")
        raise IndexError


    # For every chosen filetype
    for filetype in filetypes:
        # For every letter
        for letter in alphanumeric:
            # For every file on dir
            for fname in glob.glob(letter + "*." + filetype):
                files_processed += 1

                # If folder for current letter doesn't exists
                if os.path.exists(letter.upper() + "/") == False:
                    os.mkdir(letter.upper())

                move_file(fname, letter.upper() + "/")

    if current_dir <> directory:
        change_dir("..")

    return files_processed


#def organize_by_date(mode, filetypes, directory, dates):
#    """Organize by date PENDING"""
#    return 0"""


def organize_by_filetype(orig_filetypes, directory):
    """Organize by filetype mode (-f)"""

    filetypes = optimize(orig_filetypes)

    files_processed = 0

    current_dir = change_dir(directory)

    for ftype in filetypes:
        for fname in glob.glob("*." + ftype):

            files_processed += 1
            if filetypes == "*":
                if DEBUG_MODE:
                    print(fname.rsplit(".")[1] + "\n")

                # If folder for current file filetype doesn't exists
                if os.path.exists( fname.rsplit(".")[1] + "/") == False :
                    os.mkdir( fname.rsplit(".")[1] )
                move_file(fname, fname.rsplit(".")[1] + "/")

            else:
                # If folder for current filetype doesn't exists
                if os.path.exists( ftype + "/") == False :
                    os.mkdir( ftype )
                move_file(fname, ftype + "/")

        #for end
    # for end
    if current_dir <> directory:
        os.chdir("..")

    return files_processed


def classificate_dir(mode, filetypes, directory, dates=0):
    """Calls the corresponding function to sort files in selected mode"""

    files_classified = 0
    init_time = time.ctime()

    if mode == "-n" or mode == "-n+":
        files_classified = organize_by_name(filetypes, mode, directory)

        if mode == "-n+":
            files_classified += organize_by_symbols(filetypes, directory)

    elif mode == "-tf" or mode == "-te": # time frame and time exact date modes
        #files_classified = organize_by_date(mode, filetypes, directory, dates)
        pass

    elif mode == "-f":
        files_classified = organize_by_filetype(filetypes, directory)

    if files_classified == 0:
        print("No files were organized. Ending...")
    else:
        if(files_classified > 1):
            file_str = "file"
        else:
            file_str = "files"

        print("""\
        \n %d %s were organized.\n\n  \
                Started at:\n\t%s\n  \
                Ended at:\n\t%s\n""" \
                % (files_classified, file_str, init_time, time.ctime()))


def print_help():
    """Print help string"""

    indent = "\t  "
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

    print(help_string % (indent, indent, indent, indent))


def check_args(argv, args):
    """Checks and validates arguments"""

    global DEBUG_MODE
    valid_args = ("-n", "-n+", "-t", "-f", "-h")

    if args == 1 or argv[1] not in valid_args:
        return "INVALID"

    #argv[1] is valid then check for debug mode
    if "d" in argv[1]:
        DEBUG_MODE = 1

    if(args < 4 or argv[1] == "-h"):
        return "HELP"

    if(argv[1] == "-t"):
        return "GET_DATES"

    return "VALID"


def get_filetypes(arg):
    """Parses filetypes from third argument"""

    if arg == "*":
        return "*"

    else:
        filetype_list = []
        filetypes = arg.split(",")

        for element in filetypes:
            filetype_list.append(element)

    return filetype_list


def get_dates(line):
    """Gets date and mode"""

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


