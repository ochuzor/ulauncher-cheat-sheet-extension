from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.client.EventListener import EventListener

import logging

logger = logging.getLogger(__name__)

class KeywordQueryEventListener(EventListener):

    def __init__(self, search_handler):
        self.search_handler = search_handler

    def on_event(self, event, extension):
        qry_str = event.get_argument() or ''
        results = self.search_handler.make_search(qry_str)
        items = []
        for data in results:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                            name=data['name'],
                                            description=data['description'],
                                            on_enter=ExtensionCustomAction(data, keep_app_open=True)))
        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def __init__(self, history_list):
        self.history_list = history_list

    def on_event(self, event, extension):
        data = event.get_data()
        self.history_list.add(data)
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                    name=data['name'],
                                                    description=data['description'],
                                                    on_enter=CopyToClipboardAction(data["cmd"]))])
