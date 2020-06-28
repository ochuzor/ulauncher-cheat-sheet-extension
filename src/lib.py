from os import path, makedirs
import glob

import fuzzywuzzy
from fuzzywuzzy import process

from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


def ensure_dir(DIR):
    if not path.exists(DIR):
        makedirs(DIR)


def get_file_paths(folder_path):
    return glob.glob(path.join(folder_path, "*.txt"))


def get_texts_from_file(file_path):
    texts = []
    with open(file_path) as f:
        for ln in f.readlines():
            line = ln.strip()
            if line:
                texts.append(line)
    return texts


def get_data(file_paths):
    text_list = []
    for file in file_paths:
        source = path.splitext(path.basename(file))[0]
        source = source.split("-")[0]

        for text in get_texts_from_file(file):
            line = "#{} {}".format(source, text)
            text_list.append(line)
    return text_list


def make_search_result(query_result):
    return query_result[0].split(' ', 1)[1]


class QueryHandler:
    def __init__(self, data):
        self.data = data

    def make_search(self, search_string, limit=5):
        results = process.extract(search_string, self.data, limit=limit)
        return list(map(make_search_result, results))

    @classmethod
    def from_folder(cls, folder_path):
        _folder_path = path.expanduser(folder_path)
        ensure_dir(_folder_path)
        file_paths = get_file_paths(_folder_path)
        data = get_data(file_paths)
        return cls(data)


def main():
    folder_path = "~/cheat-sheets"
    query_handler = QueryHandler.from_folder(folder_path)
    search_string = "last command"
    print(query_handler.make_search(search_string))


if __name__ == '__main__':
    main()
