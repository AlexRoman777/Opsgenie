class WriteFile:
    def __init__(self, mode, filepath):
        self.mode = mode
        self.filepath = filepath

    def write_to_txt(self, data):
        with open(self.filepath, self.mode) as file:
            file.write(data)

    def write_to_markdown(self, data):
        with open(self.filepath, self.mode) as file:
            file.write(data)
