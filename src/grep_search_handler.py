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
    # note https://stackoverflow.com/a/36300197
    # def get_result_parts(self, result_str):
    #     src = ":".join(tokens[:2])
    #     line = tokens[2]

    def map(self, result_string):
        # /home/chinedu/cheat-sheets/vim-commands.txt:1:Ctrl + y - move screen up one line (without moving cursor)
        # print(f"res => {result_string}")

        file_loc, line_num, text = result_string.split(":", 2)

        text_parts = text.split(" - ")
        cmd = text_parts[0].strip()
        description = text_parts[1].strip() if len(text_parts) > 1 else cmd

        src = path.basename(file_loc).split("-")[0]
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
            "dest": "",
            "term": ""
        }

        if first_token.startswith('#'):
            query_object["dest"] = first_token[1:].lower()
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


class GrepSearchHandler:
    def __init__(self, grep_wrapper, search_query_mapper, search_results_mapper):
        self.grep_wrapper = grep_wrapper
        self.search_query_mapper = search_query_mapper
        self.search_results_mapper = search_results_mapper

    def make_search(self, search_term):
            query = self.search_query_mapper.map(search_term)
            term = query["term"]
            dest = query["dest"]
            if not term and not dest:
                return []

            res_iter = self.grep_wrapper.search_iter(term)
            MAX_RESULT_COUNT = 10
            result_list = ResultList()

            for res_str in chain.from_iterable(res_iter):
                res = self.search_results_mapper.map(res_str)
                if res["name"] or res["description"]:
                    result_list.add(res)
                if result_list.count() >= MAX_RESULT_COUNT:
                    break

            return result_list.to_list()

    @classmethod
    def from_directory(cls, texts_dir):
        _dir = path.expanduser(texts_dir)
        return cls(GrepWrapper(_dir), 
            SearchQueryMapper(), 
            SearchResultMapper())
