import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import pytest

from grep_search_handler import SearchResultMapper

@pytest.fixture
def search_result_mapper_sut():
    """ Returns a basic search result mapper """
    return SearchResultMapper()

def test_map(search_result_mapper_sut):
    assert search_result_mapper_sut.map("/home/bee/cee/vim-cds.txt:2:cmd - desc om") == {
        "name": "[vim] cmd", 
        "description": "desc om", 
        "id": "/home/bee/cee/vim-cds.txt:2",
        "src": "vim",
        "cmd": "cmd"
    }

    assert search_result_mapper_sut.map("vim-cmds.txt:1:cmd arg - desc om") == {
        "name": "[vim] cmd arg", 
        "description": "desc om", 
        "id": "vim-cmds.txt:1",
        "src": "vim",
        "cmd": "cmd arg"
    }

    assert search_result_mapper_sut.map("/vim-cmds.txt:3:cmd - description") == {
        "name": "[vim] cmd", 
        "description": "description", 
        "id": "/vim-cmds.txt:3",
        "src": "vim",
        "cmd": "cmd"
    }

    assert search_result_mapper_sut.map("home/git-commands.txt:10:command one - some text") == {
        "name": "[git] command one", 
        "description": "some text", 
        "id": "home/git-commands.txt:10",
        "src": "git",
        "cmd": "command one"
    }

    assert search_result_mapper_sut.map("home/bash-cds.txt:34:kp -i - desc om") == {
        "name": "[bash] kp -i", 
        "description": "desc om", 
        "id": "home/bash-cds.txt:34",
        "src": "bash",
        "cmd": "kp -i"
    }

    assert search_result_mapper_sut.map("home/vi-cds.txt:36:cmd- desc om") == {
        "name": "[vi] cmd- desc om", 
        "description": "cmd- desc om", 
        "id": "home/vi-cds.txt:36",
        "src": "vi",
        "cmd": "cmd- desc om"
    }

    assert search_result_mapper_sut.map("/c/vim-cds.txt:40:cmd -desc om") == {
        "name": "[vim] cmd -desc om", 
        "description": "cmd -desc om", 
        "id": "/c/vim-cds.txt:40",
        "src": "vim",
        "cmd": "cmd -desc om"
    }

    assert search_result_mapper_sut.map("/python-cds.txt:99:") == {
        "name": "", 
        "description": "", 
        "id": "/python-cds.txt:99",
        "src": "python",
        "cmd": ""
    }

    assert search_result_mapper_sut.map("home/vim-cds.txt:38:   ") == {
        "name": "", 
        "description": "", 
        "id": "home/vim-cds.txt:38",
        "src": "vim",
        "cmd": ""
    }

    assert search_result_mapper_sut.map("home/bash-cds.txt:12:    cmd - desc om") == {
        "name": "[bash] cmd", 
        "description": "desc om", 
        "id": "home/bash-cds.txt:12",
        "src": "bash",
        "cmd": "cmd"
    }

    assert search_result_mapper_sut.map("home/vim-cds.txt:93:    cmd  ") == {
        "name": "[vim] cmd", 
        "description": "cmd", 
        "id": "home/vim-cds.txt:93",
        "src": "vim",
        "cmd": "cmd"
    }

    assert search_result_mapper_sut.map("home/vim-cds.txt:3:one-word") == {
        "name": "[vim] one-word", 
        "description": "one-word", 
        "id": "home/vim-cds.txt:3",
        "src": "vim",
        "cmd": "one-word"
    }

    assert search_result_mapper_sut.map("home/vscode-cds.txt:903:something") == {
        "name": "[vscode] something", 
        "description": "something", 
        "id": "home/vscode-cds.txt:903",
        "src": "vscode",
        "cmd": "something"
    }
