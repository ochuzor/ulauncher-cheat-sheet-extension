import json
import logging
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesUpdateEvent, PreferencesEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

from src.lib import SearchHandler, DataFactory


logger = logging.getLogger(__name__)

search_handler = SearchHandler.from_folder("~/cheat-sheets")

class FastTipsExtension(Extension):

    def __init__(self):
        super(FastTipsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        # items = []
        # logger.info('preferences %s' % json.dumps(extension.preferences))
        # for i in range(5):
        #     item_name = extension.preferences['item_name']
        #     data = {'new_name': '%s %s was clicked' % (item_name, i)}
        #     items.append(ExtensionResultItem(icon='images/icon.png',
        #                                      name='%s %s' % (item_name, i),
        #                                      description='Item description %s' % i,
        #                                      on_enter=ExtensionCustomAction(data, keep_app_open=True)))

        # return RenderResultListAction(items)

        qry = event.get_argument() or ''
        if not qry:
            return RenderResultListAction([])

        results = search_handler.make_search(qry)
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
                                                    on_enter=HideWindowAction())])


class PreferencesUpdateEventListener(EventListener):

    def on_event(self, event, extension):
        logger.info('####### PreferencesUpdateEventListener ########')
        data = DataFactory.load_data_from_folder("~/cheat-sheets")
        search_handler.set_data(data)


class PreferencesEventListener(EventListener):

    def on_event(self, event, extension):
        logger.info('####### PreferencesEventListener ########')
        data = DataFactory.load_data_from_folder("~/cheat-sheets")
        search_handler.set_data(data)


if __name__ == '__main__':
    FastTipsExtension().run()
