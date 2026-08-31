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


# ============================================================
# CONTENIDO
# ============================================================

NEWS_CHANNELS = [
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


SPORTS_CHANNELS = [
    {
        "name": "Sky Sports F1",
        "url": "http://stream.bottledesk.net/p/AwZGQwwEZA/index.m3u8",
        "icon": "skysportsf1.png"
    }
]


TV_FILMS_CHANNELS = [
    {
        "name": "Syfy US",
        "url": "http://23.237.104.106:8080/USA_SYFY/index.m3u8",
        "icon": "syfyus.png"
    }
]


# ============================================================
# FUNCIONES
# ============================================================

def build_url(params):
    return BASE_URL + "?" + "&".join(
        f"{key}={value}" for key, value in params.items()
    )


def add_folder(name, folder, icon):
    item = xbmcgui.ListItem(label=name)

    item.setArt({
        "thumb": icon,
        "icon": icon
    })

    xbmcplugin.addDirectoryItem(
        handle=HANDLE,
        url=build_url({"folder": folder}),
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


def show_channels(channels):
    for channel in channels:

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


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

if len(sys.argv) < 3 or not sys.argv[2]:

    # Icono provisional para Links
    links_icon = os.path.join(
        MEDIA_PATH,
        "cnn.png"
    )

    add_folder(
        "Links",
        "links",
        links_icon
    )

    xbmcplugin.endOfDirectory(HANDLE)


# ============================================================
# SUBMENÚ LINKS
# ============================================================

else:

    params = dict(
        parse_qsl(sys.argv[2][1:])
    )

    folder = params.get("folder")


    # --------------------------------------------------------
    # LINKS
    # --------------------------------------------------------

    if folder == "links":

        add_folder(
            "News",
            "news",
            os.path.join(MEDIA_PATH, "bbc.png")
        )

        add_folder(
            "Sports",
            "sports",
            os.path.join(MEDIA_PATH, "skysportsf1.png")
        )

        add_folder(
            "TV-Films",
            "tvfilms",
            os.path.join(MEDIA_PATH, "syfyus.png")
        )

        xbmcplugin.endOfDirectory(HANDLE)


    # --------------------------------------------------------
    # NEWS
    # --------------------------------------------------------

    elif folder == "news":

        show_channels(NEWS_CHANNELS)


    # --------------------------------------------------------
    # SPORTS
    # --------------------------------------------------------

    elif folder == "sports":

        show_channels(SPORTS_CHANNELS)


    # --------------------------------------------------------
    # TV-FILMS
    # --------------------------------------------------------

    elif folder == "tvfilms":

        show_channels(TV_FILMS_CHANNELS)
