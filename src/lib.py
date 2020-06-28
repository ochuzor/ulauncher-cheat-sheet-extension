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


class SearchResultMapper:

    def map(self, query_result):
        result_str = query_result[0].split(' ', 1)[1]
        result_tokens = result_str.split(' - ', 1)

        if len(result_tokens) == 1:
            return {
                'name': result_str,
                'description': ''
            }

        return {
            'name': result_tokens[0],
            'description': result_tokens[1]
        }


class DataFactory:

    @staticmethod
    def load_data_from_folder(folder_path):
        _folder_path = path.expanduser(folder_path)
        ensure_dir(_folder_path)
        file_paths = get_file_paths(_folder_path)
        data = get_data(file_paths)
        return data


class SearchHandler:
    def __init__(self, data, search_result_mapper):
        self.__data = data
        self.search_result_mapper = search_result_mapper

    def make_search(self, search_string, limit=5):
        results = process.extract(search_string, self.__data, limit=limit)
        return list(map(self.search_result_mapper.map, results))

    def set_data(self, data):
        self.__data = data

    @classmethod
    def from_folder(cls, folder_path):
        data = DataFactory.load_data_from_folder(folder_path)
        return cls(data, SearchResultMapper())