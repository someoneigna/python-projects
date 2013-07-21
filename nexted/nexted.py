#!/usr/bin/python
from file import File
from gi.repository import Gtk

class Window:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("gui_nexted.GtkBuilder")
        self.window = builder.get_object("EditorWindow")
        self.textview = builder.get_object("textview")

        self.window.set_default_size(700,400)

        #Connect signals----- ENCAPSULATE -------
        signals = {'onFileNew': self.onFileNew,
                'onSaveFile': self.onSaveFile,
                'onOpenFile': self.onOpenFile,
                'onSaveAsFile': self.onSaveAsFile,
                'onQuit': self.onQuit,
                'onAboutInfo': self.onAboutInfo,
                'onUpdateTextPush': self.onUpdateTextPush,
                'onUpdateTextPop': self.onUpdateTextPop
        }
        builder.connect_signals(signals)

        #File-------------------------------------
        self.file_handle = File()
        self.current_filename = self.file_handle.get_name()
        #---------------------------------------

    def get_window(self):
        return self.window
    #----Encapsulate in class(ex: EventHandler)
    def onQuit(self, data):
        if self.file_handle.isOpen:
            self.save()
            self.file_handle.close()
        Gtk.Quit()
    def onAboutInfo(self, data):
        pass

    def onFileNew(self, data):
        if self.file_handle.isOpen:
            if self.file_handle.size() == 0 and \
                    self.current_filename == None:
                        return
            else:
                self.onSaveFile("fromFileNew")
        else:
            self.file_handle = File()

    def setCurrentFile(self, filename):
        if self.file_saved:
            self.file_handle.close()
        elif self.file_open:
            self.save()
            self.file_handle.close()

        self.file_handle = File(filename)
        self.current_filename = self.file_handle.get_name()
        self.set_title(self.current_filename)

    def save(self):
        text_buffer = self.textview.get_buffer()
        startIter, endIter = text_buffer.get_start_iter(),\
        text_buffer.get_end_iter()
        text = text_buffer.get_text(startIter, endIter, True)
        self.file_handle.save(text)



    def onSaveFile(self, data):
        self.save()

    def onSaveAsFile(self, data):
        dialog = Gtk.FileChooserDialog("Choose where to save", None,\
                                       Gtk.FileChooserAction.SAVE,\
                                       (Gtk.STOCK_CANCEL,\
                                        Gtk.ResponseType.CANCEL,\
                                        Gtk.STOCK_OPEN,\
                                        Gtk.ResponseType.OK))
        dialog.
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if self.file_handle.isOpen:
                self.save()
                self.file_handle.close()

    def onOpenFile(self, data):
        if self.file_handle.size() == 0:
            dialog = Gtk.FileChooserDialog("Choose file to open", None,\
                                       Gtk.FileChooserAction.OPEN,\
                                       (Gtk.STOCK_CANCEL,\
                                        Gtk.ResponseType.CANCEL,\
                                        Gtk.STOCK_OPEN,\
                                        Gtk.ResponseType.OK))
            response = dialog.run()
            self.file_handle = File(dialog.run())


        dialog = Gtk.Dialog("Do you wanna save this file?", None, Gtk.DIALOG_MODAL,\
                   (Gtk.STOCK_CANCEL, Gtk.RESPONSE_REJECT,\
                    Gtk.STOCK_OK, Gtk.RESPONSE_ACCEPT))
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if self.file_handle.isOpen:
                self.save()
                self.file_handle.close()





def main():
    win = Window()
    window = win.get_window()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
