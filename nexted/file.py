"""
File class of Nexted -- Python+PyGTK text editor
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
"""

import tempfile, os

#TODO: pass the tempfile data to the final chosed file
#      remove some unneded functions.

class File:
    """Handles opening, replacing and closing"""
    def __init__(self):
        self.file = None
        self.mode = None

    def open(self, filename, flag="READ"):
        if not filename:
            return(self.new())

        if not os.path.exists(filename) and flag == "CREATE":
            mode =  "w";
        elif not os.path.exists(filename) and flag== "READ":
            return "INEXISTANT"
        else:
            mode = "r+"

        try:
            self.file = open(filename, mode)#, encoding='utf-8')
            self.mode = mode

            if mode == "w":
                self.file.close()
                self.mode = "r+"
                self.file = open(filename, "r+")
            if not self.file.closed:
                return True
            return False
        except IOError:
            print("Couldnt open {file} file...\n".format(file=filename))


    def size(self):
        if self.file:
            return self.file.tell()
        else:
            return -1

    def new(self):
        """Creates a temporary file"""
        self.file = tempfile.TemporaryFile()
        self.mode = "r+"
        if self.file:
            return True
        return False


    def save_and_close(self, text):
        if self.file:
            self.save(text)
            self.file.close()
            self.file = None
            return True

        elif (not self.file):
            return False

    def has_changes(self):
        pass

    def get_name(self):
        if self.file:
            return self.file.name
        else:
            return None

    def replace(self, filename):
            os.remove(filename)
            self.file = open(filename, "w")
            self.file.close()
            self.file = open(filename, "r+")


    def save(self, text):
        if self.file and not self.file.closed:
            try:
                self.file.seek(0)
                self.file.write(text)
                self.file.flush()
                return True
            except IOError:
                print("Cant write to {0}!...\n".format(self.file.name))
        if not self.file or self.file.closed:
            return 'SELECT_FILE'

        return False


    def write(self, text):
        if not self.file.closed and self.file:
            self.file.write(text)
        else:
            print("The file is not open...\n")
            raise IOError

    def read(self):
        if self.file and not self.file.closed:
            return self.file.read()
        else:
            print("The file is not open...\n")
            raise IOError

    def close(self):
        if self.file and not self.file.closed:
            self.file.close()
            self.file = None
            return True
        else:
            return False

