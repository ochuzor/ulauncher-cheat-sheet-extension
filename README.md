# Demo Extension

A cheat sheet extension for [ulauncher](https://github.com/Ulauncher/Ulauncher).

## setup and usage
Ensure that [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) is installed in your machine before using this extension:
pip install fuzzywuzzy[speedup]

Save your cheat sheets into .txt files in the form:
command - description

The files should be saved into the ```~/cheat-sheets``` folder. Each files should be named [filter]-whatever.txt . The 'filter' part is used to filter the search results later. For example, you can save all your [vim](https://www.vim.org/) commands into a file ```vim-commands.txt```. And when you search for commands you can type ```#vim <the rest of your search texts>```.
