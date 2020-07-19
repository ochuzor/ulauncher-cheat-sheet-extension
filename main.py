from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent

from src.event_listeners import ItemEnterEventListener, KeywordQueryEventListener
from src.grep_search_handler import GrepSearchHandler, HistoryList

MAX_RESULT_COUNT = 10

history_list = HistoryList(list(), MAX_RESULT_COUNT)
search_handler = GrepSearchHandler.from_directory(MAX_RESULT_COUNT, history_list)

class CheatSheetExtension(Extension):

    def __init__(self):
        super(CheatSheetExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener(search_handler))
        self.subscribe(ItemEnterEvent, ItemEnterEventListener(history_list))


if __name__ == '__main__':
    CheatSheetExtension().run()
