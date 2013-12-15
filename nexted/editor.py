"""
Editor class of Nexted -- Python+PyGTK text editor
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

from gi.repository import Gtk, Gdk
from file import File

class Editor:
    """Handles the Gtk.Textview and interacts a File"""
    def __init__(self, textview):
        self.textview = textview
        self.textbuffer = self.textview.get_buffer()
        self.file_handle = File()
        self.textbuffer.set_modified(False)

    def set_font(self, font):
        pass

    def clean_buffer(self):
        startIter, endIter = self.textbuffer.get_start_iter(),\
                             self.textbuffer.get_end_iter()
        self.textbuffer.delete(startIter, endIter)

    def save_as_file(self, filename):
        self.file_handle.close()
        self.file_handle.open(filename, flag="CREATE")
        self.save()

    def open_file(self, filename, flag="READ"):
        state = self.file_handle.open(filename, flag)
        if state == "INEXISTANT":
            return "INEXISTANT"
        elif state == True:
            self.update_editor()
        else:
            print("Failed to open: {file}".format(file=filename))

    def new_file(self, filename=None):
        self.file_handle.close()
        self.file_handle.open(filename)
        self.clean_buffer()
        self.update_editor()

    def replace_file(self, filename):
        self.file_handle.replace(filename)
        self.save()

    def update_editor(self):
        self.textbuffer.set_text(self.file_handle.read())

    def isFileSaved(self):
        return not self.textbuffer.get_modified()

    def get_text(self):
        """Gets the text inside the TextView and returns it"""
        startIter, endIter = self.textbuffer.get_start_iter(),\
                             self.textbuffer.get_end_iter()
        text = self.textbuffer.get_text(startIter, endIter, True)
        return text

    def _set_text(self, text):
        self.textbuffer.set_text(text)

    def save(self):
        """Get textbuffer data and send it to File.save(text)"""

        #Check if we dont have a opened file handle
        if(self.file_handle.save(self.get_text()) == "SELECT_FILE"):
            #If not file is open select one and retry save
            return 'SELECT_FILE'
        else:
            self.textbuffer.set_modified(False)

    def save_and_close(self):
        """Saves and closes without caring about file existance"""
        if self.isFileSaved():
            self.file_handle.close()
        else:
            self.file_handle.save_and_close(self.get_text())
            self.textbuffer.set_modified(False)

    def exit(self):
        if not self.isFileSaved():
            self.save()
        self.file_handle.close()
