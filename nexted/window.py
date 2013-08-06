"""
Window class of Nexted -- Python+PyGTK text editor
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

from editor import Editor
from gi.repository import Gtk
import os

class Window:
    """Conects the signals to handle widgets and
        is connected to a Editor instance"""
    def __init__(self, start_file=None):
        #Read app xml file and prepare the window
        builder = Gtk.Builder()
        builder.add_from_file("gui_nexted.GtkBuilder")

        self.window = builder.get_object("EditorWindow")
        self.window.set_default_size(700, 400)
        self.title = self.window.get_title()

        #Contains a Editor

        #self.eb = Gtk.EventBox()
        self.textview = builder.get_object("textview")
        #self.eb.add(self.textview)
        #self.eb.modify_bg(Gtk.StateNormal, Gtk.gdk.color_parse("blue"))
        self.editor = Editor(self.textview)

        #And a statusbar
        self.statusbar = builder.get_object("statusbar")

        #Used for the title
        self.current_filename = None

        #Connect signals----- ENCAPSULATE -------
        signals = {
                'onFileNew': self.onFileNew,
                'onSaveFile': self.onSaveFile,
                'onOpenFile': self.onOpenFile,
                'onSaveAsFile': self.onSaveAsFile,
                'onQuit': Gtk.main_quit,
                'onAboutInfo': self.onAboutInfo,
                'hitCopy': self.onHitCopy,
                'hitBackspace': self.onHitBackspace,
                'hitCut': self.onHitCut,
                'onUpdateStatusTextPush': self.onUpdateStatusTextPush,
                'onUpdateStatusTextPop': self.onUpdateStatusTextPop,
                'onChooseFont': self.onChooseFont,
                'onChooseColor': self.onChooseColor
        }
        builder.connect_signals(signals)

        #Check passed commandline file
        self.startWithFile(start_file)

    def get_window(self):
        return self.window

    def setEditorColor(self, fg, bg):
        self.textview.modify_bg(Gtk.StateType.NORMAL, bg)
        self.textview.modify_fg(Gtk.StateType.NORMAL, fg)



    #----Encapsulate in class(ex: EventHandler)
    def onHitCut(self, data):
        pass
    def onHitBackspace(self, data):
        pass
    def onHitCopy(self, data):
        pass
    def onAboutInfo(self, data):
        dialog = Gtk.AboutDialog()
        dialog.set_authors("Ignacio Alvarez <someoneigna@gmail.com>")
        dialog.set_program_name("Nexted")
        dialog.set_version("0.1v")
        dialog.set_license(open("LICENSE", "r").read())
        dialog.set_website("https://github.com/someoneigna/python-projects/tree/master/nexted")
        dialog.set_website_label("Nexted github repository")
        dialog.run()
        dialog.destroy()

    def onChooseFont(self, data):
        dialog = Gtk.FontSelectionDialog("Choose a font")
        preview_text = "#include<stdio.h>\n"\
                "int main(){\n"\
                "    printf(\"Do you like this font?\\n\");\n"\
                "    return 0;\n}"
        dialog.set_preview_text(preview_text.decode('ascii'))
        response = dialog.run()
        dialog.destroy()

    def onFileInexistant(self, filename):
        """Warn about commandline passed file not existing"""
        file_basename = os.path.basename(filename)
        path = os.path.dirname(filename)
        message = ''.join('File: ' + file_basename + \
                '\nIn: ' + path + " doesn't exists.")

        dialog = Gtk.MessageDialog(
                None, 0,Gtk.MessageType.WARNING,
                Gtk.ButtonsType.OK, message
                )
        dialog.set_modal(True)
        dialog.run()
        dialog.destroy()
        self.current_filename = "Unnamed"
        self.update_title()

    def askReplace(self):
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL, "Do you really want to replace the file?")
        dialog.set_modal(True)
        response = dialog.run()
        dialog.destroy()
        return(response)

    def askToSave(self):
        if not self.editor.isFileSaved():
            dialog = Gtk.Dialog("Do you wanna save this file?", None,\
                    Gtk.DIALOG_MODAL, (Gtk.STOCK_CANCEL, Gtk.RESPONSE_REJECT,\
                        Gtk.STOCK_OK, Gtk.RESPONSE_ACCEPT))
            dialog.set_modal(True)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                if(self.editor.save() == 'SELECT_FILE'):
                    self.onSaveAsFile('TEMP')

    def update_title(self):
        filename = os.path.basename(self.current_filename)
        newtitle = ''.join(
                    self.title + '  --> '
                    + filename + ' <-- ' + self.current_filename + ' --'
                    )
        self.window.set_title(newtitle)

    def onFileNew(self, data):
        self.current_filename = "Unnamed"
        self.update_title()
        self.editor.new_file()

    def onSaveFile(self, data):
        #Save and check if we have an open file handle
        if self.editor.save() == 'SELECT_FILE':
            #No file is open, choose where to save
            self.onSaveAsFile('TEMP')

    def onSaveAsFile(self, data):
        dialog = Gtk.FileChooserDialog("Choose where to save", None,\
                                       Gtk.FileChooserAction.SAVE,\
                                       (Gtk.STOCK_CANCEL,\
                                        Gtk.ResponseType.CANCEL,\
                                        Gtk.STOCK_SAVE,\
                                        Gtk.ResponseType.OK))
        dialog.set_current_folder(os.getcwd())
        response = dialog.run()
        self.current_filename = dialog.get_filename()

        if response == Gtk.ResponseType.OK:
            if os.path.exists(self.current_filename):
                if self.askReplace() == Gtk.ResponseType.OK:
                    dialog.destroy()
                    self.editor.replace(self.current_filename)
                    return
            else:
                self.editor.save_as_file(self.current_filename)

        dialog.destroy()

    def startWithFile(self, filename):
        self.current_filename = filename

        #If a file was passed as arg
        if self.current_filename:
            #Open and show file
            status = self.editor.open_file(self.current_filename)
            if status == "INEXISTANT":
                self.onFileInexistant(self.current_filename)
            self.update_title()
        else:
            return

    def onChooseColor(self, data):
        color_fg, color_bg = 0, 0
        dialog = Gtk.ColorSelectionDialog("Choose editor foreground")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            color_fg = dialog.get_color_selection().get_current_color()

        dialog.destroy()

        dialog = Gtk.ColorSelectionDialog("Choose editor background")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            color_bg = dialog.get_color_selection().get_current_color()
        else:
            return


        dialog.destroy()

        self.setEditorColor(color_fg, color_bg)

    def onOpenFile(self, data):
        dialog = Gtk.FileChooserDialog("Choose file to open", None,\
                                    Gtk.FileChooserAction.OPEN,\
                                    (Gtk.STOCK_CANCEL,\
                                    Gtk.ResponseType.CANCEL,\
                                    Gtk.STOCK_OPEN,\
                                    Gtk.ResponseType.OK))

        dialog.set_current_folder(os.getcwd())
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.current_filename = dialog.get_filename()
            self.editor.new_file(self.current_filename)
        dialog.destroy()
        self.update_title()

    #TODO: find out the correct way to use Gtk.StatusBar
    def onUpdateStatusTextPush(self, data):
#        self.textview.get_buffer().set_modified(True)
#        text_buffer = self.textview.get_buffer()
#        chars = text_buffer.get_char_count()
#        lines = text_buffer.get_line_count()
#        text_info = "Lines:{lines} | Chars:{chars}".\
#        format(lines= lines, chars= chars)
#
#        statusbar_context =  self.statusbar.get_context()
#        self.statusbar.remove_all(statusbar_context)
#        self.statusbar.push(statusbar_context, text_info )
        pass

    def onUpdateStatusTextPop(self, data):
#        self.textview.get_buffer().set_modified(True)
#        text_buffer = self.textview.get_buffer()
#        chars = text_buffer.get_char_count()
#        lines = text_buffer.get_line_count()
#        text_info = "Lines:{lines} | Chars:{chars}".\
#        format(lines= lines, chars= chars)
#        statusbar_context =  self.statusbar.get_context()
#        self.statusbar.remove_all(statusbar_context)
#        self.statusbar.push(statusbar_context, text_info )
        pass

    def onQuit(self, data):
        self.editor.exit()
        raise "QUIT"







