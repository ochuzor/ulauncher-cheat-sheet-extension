from logging import log
import re
import subprocess
from os import path
from itertools import chain
from collections import OrderedDict

import logging

from attr import __description__

logger = logging.getLogger(__name__)


class SearchResultMapper:

    def map(self, result_string):
        # /home/chinedu/cheat-sheets/vim-commands.txt:1:Ctrl + y - move screen up one line (without moving cursor)
        # print(f"res => {result_string}")

        file_loc, line_num, text = result_string.split(":", 2)

        text_parts = text.split(" - ")
        cmd = text_parts[0].strip()
        description = text_parts[1].strip() if len(text_parts) > 1 else cmd

        src = path.basename(file_loc).split("-")[0].lower()
        id = f"{file_loc}:{line_num}"
        name = f"[{src}] {cmd}" if cmd else ""
        
        return {
            "id": id,
            "name": name,
            "description": description,
            "src": src,
            "cmd": cmd
        }


class SearchQueryMapper:
    def map(self, search_str):
        tokens = ' '.join(search_str.split()).strip().split(' ')
        
        # python string split guarantees there's at least a single item in the list
        first_token = tokens[0]

        query_object = {
            "src": "",
            "term": ""
        }

        if first_token.startswith('#'):
            query_object["src"] = first_token[1:].lower()
            query_object["term"] = " ".join(tokens[1:])

        else:
            query_object["term"] = " ".join(tokens)

        return query_object


class GrepWrapper:
    def __init__(self, texts_dir):
        self.texts_dir = texts_dir

    def grep(self, str_pattern):
        try:
            # cmd_ls = ["grep", "-i", search_term, 'vim-commands.txt', 'git-command.txt']
            # https://stackoverflow.com/a/35280826
            # grep -r -i --include=\*.txt 'searchterm' ./
            cmd_ls = ["grep", "-r", "-i", "-n", '--include="*.txt"', 
                f"'{str_pattern}'",
                self.texts_dir]
            cmd_str = ' '.join(cmd_ls)
            # logger.info(f"cmd: {cmd_str}")

            resp = subprocess.run(cmd_str,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                check=True,
                shell=True,
                cwd=self.texts_dir)

            output_text = resp.stdout.decode("utf-8")
            if not output_text.strip():
                return []
            
            return output_text.splitlines()
        except subprocess.CalledProcessError as exc:
            if exc.returncode == 1:
                # grep returns 1 if it didn't find anything: https://stackoverflow.com/a/28689969
                logger.info(f"grep didn't find anything")
            else:
                err_msg = exc.stderr.decode("utf-8")
                msg = f"FAIL code: {exc.returncode} => {err_msg}"
                logger.error(msg)

            return []

    def search_iter(self, text):
        yield self.grep(text)
        while text.count(' ') > 0:
            text = text.replace(' ', '.*', 1)
            yield self.grep(text)



class ResultList:
    def __init__(self):
        self.__ls_results = OrderedDict()

    def add(self, result):
        id = result["id"]
        if id not in self.__ls_results:
            self.__ls_results[id] = result

    def count(self):
        return len(self.__ls_results)

    def to_list(self):
        return self.__ls_results.values()


class HistoryList:
    def __init__(self, result_list = [], max_items_count = 50):
        self.__result_list = result_list
        self.__max_items_count = max_items_count
    
    def add(self, data):
        ls = self.__result_list[:self.__max_items_count - 1]
        self.__result_list = [i for i in ls if i["id"] != data["id"]]
        self.__result_list.insert(0, data)

    def to_list(self):
        return self.__result_list


class GrepSearchHandler:
    def __init__(self, max_result_count, grep_wrapper, search_query_mapper, search_results_mapper, history_list):
        self.grep_wrapper = grep_wrapper
        self.search_query_mapper = search_query_mapper
        self.search_results_mapper = search_results_mapper
        self.history_list = history_list
        self.max_result_count = max_result_count

    def make_search(self, search_term):
            query = self.search_query_mapper.map(search_term)
            term = query["term"]
            src_query = query["src"]

            if not term:
                ls = self.history_list.to_list()
                if not src_query:
                    return ls
                return [item for item in ls if item["src"] == src_query]

            res_iter = self.grep_wrapper.search_iter(term)
            result_list = ResultList()

            for res_str in chain.from_iterable(res_iter):
                res = self.search_results_mapper.map(res_str)
                
                if res["name"] or res["description"]:
                    if src_query:
                        if res["src"] == src_query:
                            result_list.add(res)
                    else:
                        result_list.add(res)

                if result_list.count() >= self.max_result_count:
                    break

            return result_list.to_list()

    @classmethod
    def from_directory(cls, texts_dir, max_result_count, history_list):
        _dir = path.expanduser(texts_dir)
        return cls(max_result_count,
            GrepWrapper(_dir), 
            SearchQueryMapper(), 
            SearchResultMapper(),
            history_list)
