import webbrowser
import uuid
import json
from datetime import datetime


if __name__ == "__main__":
    '''url = 'http://vk.com/feed'

    # Open URL in a new tab, if a browser window is already open.
    # webbrowser.open_new_tab(url)

    # Open URL in new window, raising the window if possible.
    webbrowser.open_new(url)'''

    with open("devs/try.json", "r") as try_data:
        try_d = json.load(try_data)
    try_d["list"].append("e")
    print(try_d)
    with open("devs/try.json", "w") as try_data:
        json.dump(try_d, try_data)
    print(str(datetime.now()))
