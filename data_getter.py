import requests
import json
import os
import certifi

CURRENT_YEAR = 2024

def get_data(day):
    if not (os.path.exists("data/")):
        os.mkdir("data")
         
    if (os.path.exists(f"data/day_{day}.txt")):
        with open(f"data/day_{day}.txt", "r") as f:
            data = f.read()
        return data
    else:
        with open('defaults.json','r') as f:
            defaults = json.load(f)

        URL = "https://adventofcode.com/" + str(CURRENT_YEAR) + "/day/" + str(day) + "/input"
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        token = defaults["token"]

        headers = {'User-Agent': USER_AGENT}
        cookies = {"session": token}

        page = requests.get(URL, cookies=cookies, headers=headers, verify=certifi.where())

        page_lines = page.text.splitlines()
        data = []
        for line in page_lines:
            data.append(line)

        # First we save as txt
        with open("data/day_" + str(day) + ".txt", "w") as f:
            f.write('\n'.join(data))
        # Then we re-load the data from the text
        # This just helps keep performance consistent
        with open(f"data/day_{day}.txt", "r") as f:
            data = f.read()
        return data