import xbmcgui
import xbmcplugin
import xbmcaddon
import sys
import os
from urllib.parse import parse_qsl


HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")

MEDIA_PATH = os.path.join(ADDON_PATH, "resources", "media")


# Canales de News
CHANNELS = [
    {
        "name": "BBC World News",
        "url": "https://vs-hls-push-ww-live.akamaized.net/x=4/i=urn:bbc:pips:service:bbc_news_channel_hd/t=3840/v=pv14/b=5070016/main.m3u8",
        "icon": "bbc.png"
    },
    {
        "name": "CBS News 24/7",
        "url": "https://cbsn-us.cbsnstream.cbsnews.com/out/v1/55a8648e8f134e82a470f83d562deeca/master.m3u8",
        "icon": "cbs.png"
    },
    {
        "name": "CNN International",
        "url": "https://jmp2.uk/stvp-GBBD8000016N",
        "icon": "cnn.png"
    },
    {
        "name": "NBC News NOW",
        "url": "https://xumo-drct-nbcnn-ir8ze.fast.nbcuni.com/live/master.m3u8",
        "icon": "nbc.png"
    }
]


def build_url(params):
    return BASE_URL + "?" + "&".join(
        f"{key}={value}" for key, value in params.items()
    )


def add_folder(name, icon):
    item = xbmcgui.ListItem(label=name)

    item.setArt({
        "thumb": icon,
        "icon": icon
    })

    xbmcplugin.addDirectoryItem(
        handle=HANDLE,
        url=build_url({"folder": "news"}),
        listitem=item,
        isFolder=True
    )


def add_stream(name, url, icon):
    item = xbmcgui.ListItem(label=name)

    item.setProperty("IsPlayable", "true")

    item.setArt({
        "thumb": icon,
        "icon": icon
    })

    xbmcplugin.addDirectoryItem(
        handle=HANDLE,
        url=url,
        listitem=item,
        isFolder=False
    )


# MENÚ PRINCIPAL

if len(sys.argv) < 3 or not sys.argv[2]:

    news_icon = os.path.join(MEDIA_PATH, "cnn.png")

    add_folder(
        "News",
        news_icon
    )

    xbmcplugin.endOfDirectory(HANDLE)


# NEWS

else:

    params = dict(
        parse_qsl(sys.argv[2][1:])
    )

    if params.get("folder") == "news":

        for channel in CHANNELS:

            icon = os.path.join(
                MEDIA_PATH,
                channel["icon"]
            )

            add_stream(
                channel["name"],
                channel["url"],
                icon
            )

        xbmcplugin.endOfDirectory(HANDLE)
