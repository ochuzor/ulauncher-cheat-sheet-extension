from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.client.EventListener import EventListener

import logging

from .grep_search_handler import GrepSearchHandler

logger = logging.getLogger(__name__)

DEFAULT_CHEAT_SHEETS_DIR = "~/cheat-sheets"
search_handler = GrepSearchHandler.from_directory(DEFAULT_CHEAT_SHEETS_DIR)

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        qry_str = event.get_argument() or ''
        results = search_handler.make_search(qry_str)
        items = []
        for data in results:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                            name=data['name'],
                                            description=data['description'],
                                            on_enter=ExtensionCustomAction(data, keep_app_open=True)))
        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                    name=data['name'],
                                                    description=data['description'],
                                                    on_enter=CopyToClipboardAction(data["cmd"]))])
