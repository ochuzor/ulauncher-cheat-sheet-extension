from logging import log
import re
import subprocess
from os import path

import logging

logger = logging.getLogger(__name__)

class GrepSearchHandler:
    def __init__(self, texts_dir):
        self.texts_dir = path.expanduser(texts_dir)


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

            logger.info(f"cmd: {' '.join(cmd_ls)}")

            # resp = subprocess.run(cmd_ls, 
            #     stdout=subprocess.PIPE, 
            #     stderr=subprocess.PIPE, 
            #     check=True,
            #     shell=True,
            #     cwd=self.texts_dir)

            resp = subprocess.run(' '.join(cmd_ls), 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                check=True,
                shell=True,
                cwd=self.texts_dir)

            output_text = resp.stdout.decode("utf-8")
            if not output_text.strip():
                return []

            results = []
            for index, line in enumerate(output_text.splitlines()[:10]):
                ln = line.split(':', 1)[1]
                cmd, desc = ln.split(' - ')
                results.append({
                    "name": cmd,
                    "description": desc
                })
            
            return results

        except subprocess.CalledProcessError as exc:
            if exc.returncode == 1:
                # grep returns 1 if it didn't find anything: https://stackoverflow.com/a/28689969
                logger.info("grep didn't find anything.")
            else:
                err_msg = exc.stderr.decode("utf-8")
                msg = f"FAIL code: {exc.returncode} => {err_msg}"
                logger.error(msg)

            return []
