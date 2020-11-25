import requests
import lxml.html as lh
import pandas as pd
import os
import sys

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
}

missionData = {
    "__comment1": "All data scraped from: https://payday.fandom.com/wiki/Category:PAYDAY_2_heists#Heists and https://payday.fandom.com/wiki/PAYDAY:_The_Heist#Heists"
}

doubleNames = {
    "Bank Heist": ["Bank Heist: Deposit", "Bank Heist: Cash", "Bank Heist: Gold", "Bank Heist: Random"],
    "Transport": [
        "Transport: Crossroads",
        "Transport: Downtown",
        "Transport: Harbor",
        "Transport: Park",
        "Transport: Underpass",
    ],
}


def HandlePayday2Heists():
    print("Parsing Payday 2 Heists...")
    page = requests.get("https://payday.fandom.com/wiki/Category:PAYDAY_2_heists#Heists", headers=headers)
    doc = lh.fromstring(page.content)
    trElements = doc.xpath("//tr")[5:]
    bEscape = True

    for tableRow in trElements:

        index = 0
        for trElement in tableRow:
            name = trElement.text_content()
            if name == "\n    v·d·e\n    PAYDAY 2 Heists\n":
                bEscape = True
                break
            rows = name.split("\n")
            print(rows[0])
            index += 1

        if bEscape:
            break


def HandlePayday1Heists():
    pass


HandlePayday2Heists()
HandlePayday1Heists()
