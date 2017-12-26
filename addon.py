# -*- coding: utf-8 -*-

import sys
import urlparse
from resources.lib.common import Common
from resources.lib.client import Client
from resources.lib.parser import Parser

handle_ = int(sys.argv[1])
url_ = sys.argv[0]

plugin = Common(
    addon_handle=handle_,
    addon_url=url_
)
client = Client(plugin)
parser = Parser(plugin=plugin)

def router(paramstring):

    args = dict(urlparse.parse_qs(paramstring))
    mode = args.get('mode', ['rails'])[0]
    title = args.get('title', [''])[0]
    id_ = args.get('id', ['home'])[0]
    params = args.get('params', [''])[0]

    if mode == 'rails':
        parser.rails_items(client.rails(id_, params), id_)
    elif 'rail' in mode:
        parser.rail_items(client.rail(id_, params), mode)
    elif 'epg' in mode:
        date = params
        if id_ == 'date':
            date = plugin.get_date()
        parser.epg_items(client.epg(date), date, mode)
    elif mode == 'play':
        parser.playback(client.playback(id_))
    elif mode == 'play_context':
        parser.playback(client.playback(id_), title, True)
    elif mode == 'is_settings':
        plugin.open_is_settings()

if __name__ == '__main__':
    if plugin.get_setting('startup') == 'true':
        device_id = plugin.uniq_id()
        if device_id:
            client.startUp(device_id)
            playable = plugin.start_is_helper()
            if client.TOKEN and playable:
                plugin.set_setting('startup', 'false')

    if client.TOKEN and client.DEVICE_ID:
        router(sys.argv[2][1:])