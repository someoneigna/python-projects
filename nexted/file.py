import tempfile, codecs, os

class File:
    def __init__(self):
        self.file = None
        self.mode = None

    def open(self, filename):
        if self.file and not self.file.closed:
            self.file.close()
            self.file = None
        self._open(filename, "r+")


    def _open(self, filename, mode):
        if not os.path.exists(filename):
            mode =  "w";
        try:
            self.file = open(filename, mode)#, encoding='utf-8')
            self.mode = mode

            if mode == "w":
                self.file.close()
                self.mode = "r+"
                self.file = open(filename, "r+")

        except IOError:
            print("Couldnt open %s file...\n" % filename)


    def size(self):
        if self.file:
            return self.file.tell()
        else:
            return -1

    def new(self, filename=None):
        if filename:
            self.file = tempfile.TemporaryFile()
            self.mode = "r+"

        else:
            self.file = self.open(filename)
            self.mode = "r+"


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

