import xbmcgui
import xbmcplugin
import sys

HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]


def add_folder(name, params):
    url = BASE_URL + "?" + "&".join(
        f"{key}={value}" for key, value in params.items()
    )

    item = xbmcgui.ListItem(label=name)

    xbmcplugin.addDirectoryItem(
        handle=HANDLE,
        url=url,
        listitem=item,
        isFolder=True
    )


def add_stream(name, url):
    item = xbmcgui.ListItem(label=name)
    item.setProperty("IsPlayable", "true")

    xbmcplugin.addDirectoryItem(
        handle=HANDLE,
        url=url,
        listitem=item,
        isFolder=False
    )


params = dict()

if len(sys.argv) > 2 and sys.argv[2]:
    params = dict(
        pair.split("=", 1)
        for pair in sys.argv[2][1:].split("&")
        if "=" in pair
    )


# MENÚ PRINCIPAL
if not params:
    add_folder("News", {"folder": "news"})
    xbmcplugin.endOfDirectory(HANDLE)


# NEWS
elif params.get("folder") == "news":

    add_stream(
        "CBS News 24/7",
        "https://cbsn-us.cbsnstream.cbsnews.com/out/v1/55a8648e8f134e82a470f83d562deeca/master.m3u8"
    )

    xbmcplugin.endOfDirectory(HANDLE)
