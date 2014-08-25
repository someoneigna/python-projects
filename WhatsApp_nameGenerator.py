'''
    Generates WhatsApp names from files modification timestamp.

    Made in order to make WindowsPhone WhatsApp photos match Android WhatsApp format.

    The MIT License (MIT)

    Copyright (c) 2014 Ignacio Alvarez - someoneigna@gmail.com

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

'''
import sys
import os
import glob
import stat
import datetime
import shutil

type_dict = dict()
PROGRAM_NAME = 'WhatsApp_nameGenerator.py'

def get_filetype(file):
    ''' Return a tuple of (prefix, filetype) from the filename '''
    
    parts = file.split('.')
    result = None
    extension = ''
    prefix = "UNKNOWN"

    if (len(parts) > 1):
        extension = parts[1]
    
        if extension in type_dict:
            prefix = type_dict[extension]
            
    result = (prefix, extension)
    
    return result


def get_name(prefix, time_str, number, extension):
    ''' Return PREFIX - time - WAxxxx . extension
        ej: (IMG-20140612-WA0000.jpg)                 '''
    
    return prefix + '-' + time_str + '-' + 'WA' +  number + extension


def get_timestamp(filename):
    return os.stat(filename).st_mtime
    
    
def main(args):
    rename_files = False
    show_info = False
    
    # If got from input a list of (filetype:prefix), ej(jpg:IMG, mp4:VID)
    if (len(args) > 1 and len(args[1]) > 0) :
        if len(args) > 2:
            if 'r' in args[2]:
                rename_files = True
            if 'v' in args[2]:
                show_info = True
            
            
        # Generate the dictionary of filetype->prefix (ej: jpg->IMG)
        for pair in args[1].split(','):
            key_pair = pair.split(':')
            type_dict[key_pair[0]] = key_pair[1]
            
        # For filtering file input, make a list of valid extensions
        valid_format = type_dict.keys()
            
    else:
        print('Specify valid formats for filename conversion:'\
        '   Input: {0} jpg:IMG, mp4:VID.'\
        'As a optional argument you can specify \'-r\' to rename'\
        'instead of copying files. And you can specify \'-v\' to print the log.'.format(PROGRAM_NAME))
        
        sys.exit(0)

    last_repeated_date = None 
    repetitions = 0
    results = []
    
    files = []
    # Generate a list of valid files on the current dir
    for type in valid_format:
        files.extend(glob.glob('*.' + type))

    # Sort input files by the timestamp
    files = sorted(files, key=lambda x: get_timestamp(x), reverse=True)

    # For each file timestamp generate the prefix + time string + current day number
    for file in files:

        # If it's already a WhatsApp filename skip
        if ('WA' in file):
            continue
        
        time_str = str(datetime.date.fromtimestamp(get_timestamp(file))).replace('-', '')

        # To generate WAXYZ number
        # check if previous date was the same, then add to the
        # suffix WA000
        if (last_repeated_date == time_str):
            repetitions += 1
        else:
            repetitions = 0
            last_repeated_date = time_str

        number = '{:04d}'.format(repetitions)
        
        # Get prefix,filetype tuple from file
        type_pair = get_filetype(file)

        # The prefix corresponding for the passed filetype
        prefix = str(type_pair[0])

        # File extension
        extension = str(type_pair[1])
        extension = '.' + extension
        
        new_filename = get_name(prefix, time_str, number, extension)

        # Skip if the file is already generated
        if os.path.exists(new_filename):
            continue

        # If renaming files enabled (-r passed)
        if rename_files:
            os.rename(file, new_filename)
        else:
            shutil.copy2(file, new_filename)

        # If log is enabled (-v passed)
        if show_info:
            results.append(file + ' -> ' + new_filename)

    for result in results:
        print (result)
        
if __name__ == '__main__':
    main(sys.argv)
