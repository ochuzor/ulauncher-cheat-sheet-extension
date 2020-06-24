from os import path
import glob


def get_texts_from_file(file_path):
    texts = []
    with open(file_path) as f:
        for ln in f.readlines():
            line = ln.strip()
            if line:
                texts.append(line)
    return texts


def get_data_from_text(text):
    ls = text.split(' - ', 1)

    if len(ls) == 1:
        return {"cmd": '', "desc": ls[0]}
    return {"cmd": ls[0], "desc": ls[1]}


class FileHandler:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data = []

    def get_file_paths(self):
        return glob.glob(path.join(self.folder_path, "*.txt"))

    def get_data(self):
        file_paths = self.get_file_paths()
        for file in file_paths:
            source = path.splitext(path.basename(file))[0]
            source = source.split("-")[0]

            for text in get_texts_from_file(file):
                data = get_data_from_text(text)
                data['source'] = source
                self.data.append(data)
        return self.data


def main():
    folder_path = path.expanduser("../.data")
    file_handler = FileHandler(folder_path)
    file_paths = file_handler.get_file_paths()
    print('files: ' + ''.join(file_paths))
    texts_items = file_handler.get_data()
    for dd in texts_items[10:20]:
        print(dd)


if __name__ == '__main__':
    main()
