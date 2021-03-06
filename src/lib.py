from os import path, makedirs
import glob
import re

import fuzzywuzzy
from fuzzywuzzy import process


def ensure_dir(DIR):
    if not path.exists(DIR):
        makedirs(DIR)


def get_file_paths(folder_path):
    return glob.glob(path.join(folder_path, "*.txt"))


def get_texts_from_file(file_path):
    texts = []
    with open(file_path, "r") as f:
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
        ''' query_result is a tuple of the form ('text', search_score) '''
        text = query_result[0]
        cheat_sheet_src, result_str = text.split(' ', 1)
        result_tokens = result_str.split(' - ', 1)

        if len(result_tokens) == 1:
            return {
                'name': f'[{cheat_sheet_src}] {result_str}',
                'description': ''
            }

        return {
            'name': f'[{cheat_sheet_src}]: {result_tokens[0]}',
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


def filter_by_source(src_str, texts):
    return list(filter(lambda str_val: str_val.startswith(src_str + ' '), texts))

def get_search_object(search_string):
    ss = " ".join(search_string.split())
    first_token, *tokens = ss.split(' ')

    filter_str = ""
    search_string = ""

    if first_token.startswith('#') and len(first_token) > 1:
        filter_str = first_token
        search_string = " ".join(tokens)

    elif first_token == '#':
        search_string = ' '.join(tokens)

    else:
        search_string = ss

    return {
        "filter_str": filter_str,
        "search_string": search_string
    }



class SearchHandler:
    def __init__(self, data, search_result_mapper):
        self.__data = data
        self.search_result_mapper = search_result_mapper

    def make_search(self, query_string, limit=5):        
        search_object = get_search_object(query_string)
        filter_str = search_object["filter_str"]
        search_string = search_object["search_string"]

        data = filter_by_source(filter_str, self.__data) if filter_str else self.__data
        results = process.extract(search_string, data, scorer=fuzzywuzzy.fuzz.partial_token_sort_ratio, limit=limit) if search_string else []
        return list(map(self.search_result_mapper.map, results))

    def set_data(self, data):
        self.__data = data

    @classmethod
    def from_folder(cls, folder_path):
        data = DataFactory.load_data_from_folder(folder_path)
        return cls(data, SearchResultMapper())