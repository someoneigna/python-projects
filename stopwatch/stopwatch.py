'''Simple stopwatch with PyGTK3'''
import time

try:
    from gi.repository import Gtk, GObject
except:
    print('You need PyGTK3 libraries to run this.')
    raise


class SaveDialog(GObject.GObject):
    '''Pop-up window'''
    def __init__(self, filename=None, data=None):
        self.data = data
        self.filename = filename

        #Get a builder to reach GUI widgets
        builder = Gtk.Builder()
        builder.add_from_file("stopwatch_saveDialog.GtkBuilder")

        #Define signals
        signals = {
                'onAccept': self.onAccept,
                'onCancel': self.onCancel,
        }

        #Get parent
        self.window = builder.get_object("saveDialog")

        #Get input field
        self.inputField = builder.get_object('inputField')

        #Connect signals
        builder.connect_signals(signals)

    def get_window(self):
        return self.window

    def get_text(self, textView):
            """Gets the text inside the TextView and returns it"""
            textbuffer = textView.get_buffer()
            startIter, endIter = textbuffer.get_start_iter(),\
                                textbuffer.get_end_iter()
            text = textbuffer.get_text(startIter, endIter, True)
            return text

    def onAccept(self, widget):
        if self.filename:
            saveFile = open(self.filename, 'w')
            textInput = self.get_text(self.inputField)
            saveFile.write('Description: ' + textInput + '\n' + self.data)
            saveFile.close()
        self.window.destroy()

    def onCancel(self, widget):
        self.window.destroy()

class StopWatch():
    '''Main window of StopWatch'''
    def __init__(self):

        self.counting = False
        self.startTime = 0
        self.endTime = 0

        #Get a builder to reach GUI widgets
        builder = Gtk.Builder()
        builder.add_from_file("stopwatch.GtkBuilder")

        #Get parent
        self.window = builder.get_object("stopwatch")

        #Define all signals
        signals = {
                'onStart': self.onStart,
                'onSave': self.onSave
        }

        #Gui widgets
        self.startField = builder.get_object("startField")
        self.endField = builder.get_object("endField")
        self.differenceField = builder.get_object("differenceField")
        self.start_stop_Button = builder.get_object("Start/Stop")

        #Connect signals
        builder.connect_signals(signals)

    def onStart(self, widget):
        if self.counting:
            self.endTime = time.time()
            self.counting = False
            self.start_stop_Button.set_label('Start')
            self.setFields('END')
            self.setFields('DIFF')

        else:
            self.counting = True
            self.startTime = time.time()
            if(self.startTime <> 0):
                self.endTime = 0
                self.setFields('END')
                self.setFields('DIFF')

            self.start_stop_Button.set_label('Stop')
            self.setFields('START')

    def setFields(self, field):
        if field == 'START':
            self.startField.set_text(time.ctime().split()[3])

        elif field == 'END':
            if self.endTime == 0:
                self.endField.set_text('')
            else:
                self.endField.set_text(time.ctime().split()[3])

        elif field == 'DIFF':
            if self.endTime == 0:
                self.differenceField.set_text('')
            else:
                timeElapsed = '{0:.3f}'.format((self.endTime - self.startTime))
                self.differenceField.set_text(timeElapsed)

    def onSave(self, widget):
        if self.endTime:
            startTimeStr = self.startField.get_text()
            endTimeStr = self.endField.get_text()
            timeElapsed = '{0:.3f}'.format((self.endTime - self.startTime))
            filename = endTimeStr + '.StopWatch'


            info = 'Start:{0} End:{1} Diff:{2}'.format(startTimeStr, endTimeStr, timeElapsed)
            saveDialog = SaveDialog(filename, info)

            window = saveDialog.get_window()
            window.show_all()

    def get_window(self):
        return self.window

def main():
    stopWatch = StopWatch()
    window = stopWatch.get_window()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
