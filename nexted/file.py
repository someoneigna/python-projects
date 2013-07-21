import tempfile

class File:
    def __init__(self):
        try:
            self.file = tempfile.TemporaryFile()
            self.isTemp = True
            self.mode = "w+"
            self.init()
        except IOError:
            print("Could create a file...\n")

    def open(self, mode, filename):
        try:
            self.file = open(filename, mode)
            self.mode = mode
            self.filename = filename
        except IOError:
            print("Could open %s file...\n" % filename)

    def init(self):
        self.isOpen = True
        self.saved = False
        self.name = self.file.name

    def size(self):
        return self.file.tell()

    def save_and_close(self, text):
        if self.isOpen and self.file:
            self.file.write(text)
            self.file.close()
            self.file.isOpen = False
            self.file.saved = True
            self.file = None
            return True

        elif (not self.isOpen):
            return False

    def has_changes(self):
        pass

    def get_name(self):
        if self.isOpen:
            return self.name
        else:
            return None

    def save(self, text):
        if self.isOpen and self.mode == "w+":
            try:
                self.file.write(text)
                self.saved = True
                return True
            except IOError:
                print("Cant write to file!...\n")
        elif self.mode == "r":
            self.file.close()
            try:
                self.file = open(self.filename, "w+")
                self.mode = "w+"
                return True
            except IOError:
                print("Can't reopen %s in write mode...\n" % self.filename)
        else:
           return False


    def write(self, text):
        if not self.file.closed and self.file:
            self.file.close()
            self.file = open(self.filename, "w+")
            self.file.write(text)
            self.file.close()
            self.file = open(self.filename, "r")
        else:
            print("The file is not open...\n")
            raise IOError

    def read(self):
        if file.isOpen:
            return self.file.read()
        else:
            print("The file is not open...\n")
            raise IOError

    def close(self):
        if self.file:
            self.file.close()
            return True
        else:
            return False

