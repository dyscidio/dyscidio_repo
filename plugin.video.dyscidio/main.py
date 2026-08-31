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


# -------------------------
# MENÚ PRINCIPAL
# -------------------------

if len(sys.argv) < 3 or not sys.argv[2]:

    news_icon = os.path.join(MEDIA_PATH, "cnn.png")

    add_folder(
        "News",
        news_icon
    )

    xbmcplugin.endOfDirectory(HANDLE)


# -------------------------
# NEWS
# -------------------------

else:

    params = dict(
        parse_qsl(sys.argv[2][1:])
    )

    if params.get("folder") == "news":

        # CNN International Europe
        add_stream(
            "CNN International",
            "https://cnn-cnninternational-1-eu.rakuten.wurl.com/manifest/playlist.m3u8",
            os.path.join(MEDIA_PATH, "cnn.png")
        )

        # CBS News 24/7
        add_stream(
            "CBS News 24/7",
            "https://cbsn-us.cbsnstream.cbsnews.com/out/v1/55a8648e8f134e82a470f83d562deeca/master.m3u8",
            os.path.join(MEDIA_PATH, "cbs.png")
        )

        # Euronews Español
        add_stream(
            "Euronews Español",
            "https://rakuten-euronews-4-es.samsung.wurl.tv/manifest/playlist.m3u8",
            os.path.join(MEDIA_PATH, "euronews.png")
        )

        xbmcplugin.endOfDirectory(HANDLE)
