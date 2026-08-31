import xbmcgui
import xbmcplugin
import sys

HANDLE = int(sys.argv[1])


def add_link(name, url):
    item = xbmcgui.ListItem(label=name)
    item.setProperty("IsPlayable", "true")
    xbmcplugin.addDirectoryItem(
        handle=HANDLE,
        url=url,
        listitem=item,
        isFolder=False
    )


add_link("Google", "https://www.google.com")
add_link("Wikipedia", "https://www.wikipedia.org")
add_link("GitHub", "https://github.com")

xbmcplugin.endOfDirectory(HANDLE)
