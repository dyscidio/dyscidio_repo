import xbmc
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
    },
    {
        "name": "Euronews Español",
        "url": "https://jmp2.uk/rok-8acb4f9b8a255216966db355daaa1749.m3u8",
        "icon": "eurosp.png"
    },
    {
        "name": "Euronews World",
        "url": "https://jmp2.uk/rok-dafd06b712a35fbe9935d4c04c2e8b53.m3u8",
        "icon": "euroen.png"
    },
    {
        "name": "N+ Univision 24/7",
        "url": "https://jmp2.uk/rok-5a28fbf15c135b51b3638e8bd02d6577.m3u8",
        "icon": "univision.png"
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


REPOSITORIES = [
    {
        "name": "Balandro",
        "url": "https://repobal.github.io/base/",
        "icon": "icon.png"
    },
    {
        "name": "Alfa",
        "url": "https://alfa-addon.com/alfa/",
        "icon": "icon.png"
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


def add_external_link(name, url, icon):
    item = xbmcgui.ListItem(label=name)

    item.setArt({
        "thumb": icon,
        "icon": icon
    })

    xbmcplugin.addDirectoryItem(
        handle=HANDLE,
        url=build_url({"open": url}),
        listitem=item,
        isFolder=False
    )


def show_channels(channels):

    for channel in channels:

        icon = channel["icon"]

        if not icon.startswith(("http://", "https://")):
            icon = os.path.join(
                MEDIA_PATH,
                icon
            )

        add_stream(
            channel["name"],
            channel["url"],
            icon
        )

    xbmcplugin.endOfDirectory(HANDLE)


def show_repositories():

    for repository in REPOSITORIES:

        icon = os.path.join(
            MEDIA_PATH,
            repository["icon"]
        )

        add_external_link(
            repository["name"],
            repository["url"],
            icon
        )

    xbmcplugin.endOfDirectory(HANDLE)


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

if len(sys.argv) < 3 or not sys.argv[2]:

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
# RESTO DEL MENÚ
# ============================================================

else:

    params = dict(
        parse_qsl(sys.argv[2][1:])
    )

    # --------------------------------------------------------
    # ABRIR ENLACE EXTERNO CON CHROME
    # --------------------------------------------------------

    if params.get("open"):

        url = params["open"]

        xbmc.executebuiltin(
            'StartAndroidActivity(com.android.chrome,android.intent.action.VIEW,,%s)'
            % url
        )

        xbmcplugin.endOfDirectory(HANDLE)


    # --------------------------------------------------------
    # LINKS
    # --------------------------------------------------------

    elif params.get("folder") == "links":

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

        add_folder(
            "Repositorios",
            "repositories",
            os.path.join(MEDIA_PATH, "icon.png")
        )

        xbmcplugin.endOfDirectory(HANDLE)


    # --------------------------------------------------------
    # NEWS
    # --------------------------------------------------------

    elif params.get("folder") == "news":

        show_channels(NEWS_CHANNELS)


    # --------------------------------------------------------
    # SPORTS
    # --------------------------------------------------------

    elif params.get("folder") == "sports":

        show_channels(SPORTS_CHANNELS)


    # --------------------------------------------------------
    # TV-FILMS
    # --------------------------------------------------------

    elif params.get("folder") == "tvfilms":

        show_channels(TV_FILMS_CHANNELS)


    # --------------------------------------------------------
    # REPOSITORIOS
    # --------------------------------------------------------

    elif params.get("folder") == "repositories":

        show_repositories()
