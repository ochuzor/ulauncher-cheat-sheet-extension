from logging import log
import re
import subprocess
from os import path

import logging

logger = logging.getLogger(__name__)


class SearchResultMapper:
    def map(self, result_string):
        line = result_string.strip().split(':', 1)[1]
        tokens = line.split(' - ')
        
        return {
            "name": tokens[0],
            "description": tokens[1] if len(tokens) > 1 else ''
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


class GrepSearchHandler:
    def __init__(self, texts_dir, search_query_mapper, search_results_mapper):
        self.texts_dir = texts_dir
        self.search_query_mapper = search_query_mapper
        self.search_results_mapper = search_results_mapper


    def make_search(self, search_term):
        try:
            if not search_term.strip():
                return []

            # cmd_ls = ["grep", "-i", search_term, 'vim-commands.txt', 'git-command.txt']
            # https://stackoverflow.com/a/35280826
            # grep -r -i --include=\*.txt 'searchterm' ./
            cmd_ls = ["grep", "-r", "-i", '--include="*.txt"', 
                f"'{search_term}'",
                self.texts_dir]
            cmd_str = ' '.join(cmd_ls)
            logger.info(f"cmd: {cmd_str}")

            resp = subprocess.run(cmd_str,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                check=True,
                shell=True,
                cwd=self.texts_dir)

            output_text = resp.stdout.decode("utf-8")
            if not output_text.strip():
                return []

            ls = output_text.splitlines()[:10]
            map_itr = map(self.search_results_mapper.map, ls)
            return list(map_itr)

        except subprocess.CalledProcessError as exc:
            if exc.returncode == 1:
                # grep returns 1 if it didn't find anything: https://stackoverflow.com/a/28689969
                logger.info("grep didn't find anything.")
            else:
                err_msg = exc.stderr.decode("utf-8")
                msg = f"FAIL code: {exc.returncode} => {err_msg}"
                logger.error(msg)

            return []

    @classmethod
    def from_directory(cls, texts_dir):
        return cls(path.expanduser(texts_dir), 
            SearchQueryMapper(), 
            SearchResultMapper())
