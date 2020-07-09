import json
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent

from src.event_listeners import ItemEnterEventListener, KeywordQueryEventListener

class CheatSheetExtension(Extension):

    def __init__(self):
        super(CheatSheetExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


if __name__ == '__main__':
    CheatSheetExtension().run()
