#!/usr/bin/python
from file import File
from gi.repository import Gtk
import os

class Window:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("gui_nexted.GtkBuilder")
        self.window = builder.get_object("EditorWindow")
        self.textview = builder.get_object("textview")
        self.statusbar = builder.get_object("statusbar")
        self.window.set_default_size(700,400)

        #Connect signals----- ENCAPSULATE -------
        signals = {'onFileNew': self.onFileNew,
                'onSaveFile': self.onSaveFile,
                'onOpenFile': self.onOpenFile,
                'onSaveAsFile': self.onSaveAsFile,
                'onQuit': Gtk.main_quit,
                'onAboutInfo': self.onAboutInfo,
                'onUpdateStatusTextPush': self.onUpdateStatusTextPush,
                'onUpdateStatusTextPop': self.onUpdateStatusTextPop
        }
        builder.connect_signals(signals)

        #File-------------------------------------
        self.file_handle = File()
        self.current_filename = None
        #---------------------------------------

        #Textview--------------------------------
        self.textview.get_buffer().set_modified(False)
        #-------------------------------------------
    def clean_buffer(self):
        buff = self.textview.get_buffer()
        startIter, endIter = buff.get_start_iter(), buff.get_end_iter()
        buff.delete(startIter, endIter)

    def update_buffer(self):
        buff = self.textview.get_buffer()
        buff.set_text(self.file_handle.read())

    def get_window(self):
        return self.window

    def file_saved(self):
        return not self.textview.get_buffer().get_modified()

    #----Encapsulate in class(ex: EventHandler)

    def onAboutInfo(self, data):
        pass

    def onUpdateStatusTextPush(self, data):
        self.textview.get_buffer().set_modified(True)
        text_buffer = self.textview.get_buffer()
        chars = text_buffer.get_char_count()
        lines = text_buffer.get_line_count()
        text_info = "Lines:{lines} | Chars:{chars}".\
        format(lines= lines, chars= chars)

        statusbar_context =  self.statusbar.get_context()
        self.statusbar.remove_all(statusbar_context)
        self.statusbar.push(statusbar_context, text_info )
        pass

    def onUpdateStatusTextPop(self, data):
        self.textview.get_buffer().set_modified(True)
        text_buffer = self.textview.get_buffer()
        chars = text_buffer.get_char_count()
        lines = text_buffer.get_line_count()
        text_info = "Lines:{lines} | Chars:{chars}".\
        format(lines= lines, chars= chars)

        statusbar_context =  self.statusbar.get_context()
        self.statusbar.remove_all(statusbar_context)
        self.statusbar.push(statusbar_context, text_info )
        pass

    def onQuit(self, data):
        if not self.file_saved:
            self.save()
        self.file_handle.close()
        raise "QUIT"

    def askReplace(self):
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL, "Do you really want to replace the file?")
        response = dialog.run()
        dialog.destroy()
        return(response)

    def askToSave(self, tempfile):
        if not self.file_saved():
            dialog = Gtk.Dialog("Do you wanna save this file?", None,\
                    Gtk.DIALOG_MODAL, (Gtk.STOCK_CANCEL, Gtk.RESPONSE_REJECT,\
                        Gtk.STOCK_OK, Gtk.RESPONSE_ACCEPT))
            dialog.set_modal(True)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                if not self.file_saved and not tempfile:
                    self.save()
                    self.file_handle.close()
                else:
                    self.onSaveAsFile('TEMP')
            dialog.destroy()


    def onFileNew(self, data):
        if not self.file_saved():
            self.askToSave()
        else:
            self.file_handle.new()
            self.textview.get_buffer().set_modified(False)

    def setCurrentFile(self, filename):
        if not self.file_saved():
            self.save()
        self.file_handle.close()
        self.file_handle.open(filename)

        self.current_filename = self.file_handle.get_name()
        self.set_title(self.current_filename)

    def save(self):
        """Get textbuffer data and send it to File.save(text)"""
        text_buffer = self.textview.get_buffer()
        startIter, endIter = text_buffer.get_start_iter(),\
        text_buffer.get_end_iter()
        text = text_buffer.get_text(startIter, endIter, True)

        #Check if we dont have a opened file handle
        if(self.file_handle.save(text) == "SELECT_FILE"):
            #If not file is open select one and retry save
            self.onSaveAsFile('TEMP')
            self.file_handle.save(text)



    def onSaveFile(self, data):
        if not self.file_saved():
            self.file_handle.replace(self.current_filename)
            self.save()

    def onSaveAsFile(self, data):
        dialog = Gtk.FileChooserDialog("Choose where to save", None,\
                                       Gtk.FileChooserAction.SAVE,\
                                       (Gtk.STOCK_CANCEL,\
                                        Gtk.ResponseType.CANCEL,\
                                        Gtk.STOCK_OPEN,\
                                        Gtk.ResponseType.OK))
        dialog.set_current_folder(os.getcwd())
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            if os.path.exists(filename):
                if self.askReplace() == Gtk.ResponseType.OK:
                    dialog.destroy()
                    self.file_handle.replace(filename)
                    self.save()
                    return

            else:
                self.file_handle.open(dialog.get_filename())
                self.save()

            if data == 'SELECT_FILE':
                self.file_handle.open(dialog.get_filename())

        dialog.destroy()


    def onOpenFile(self, data):
        dialog = Gtk.FileChooserDialog("Choose file to open", None,\
                                    Gtk.FileChooserAction.OPEN,\
                                    (Gtk.STOCK_CANCEL,\
                                    Gtk.ResponseType.CANCEL,\
                                    Gtk.STOCK_OPEN,\
                                    Gtk.ResponseType.OK))
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.current_filename = dialog.get_filename()
            if not self.file_saved():
                self.save()
            self.file_handle.close()
            self.file_handle.open(self.current_filename)
            self.clean_buffer()

            self.update_buffer()

        dialog.destroy()






def main():
    win = Window()
    window = win.get_window()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
