import requests
import lxml.html as lh
import json
import os

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
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

classics = [
    "Diamond Heist",
    "First World Bank",
    "Green Bridge",
    "Heat Street",
    "No Mercy",
    "Panic Room",
    "Slaughterhouse",
    "Counterfeit",
    "Undercover",
]


def HandlePayday2Heists():
    print("Parsing Payday 2 Heists...")

    page = requests.get("https://payday.fandom.com/wiki/Category:PAYDAY_2_heists#Heists", headers=headers)
    doc = lh.fromstring(page.content)
    scrapedHeists = {}
    tableContent = doc.xpath("//table[@class='navbox']")[0][0].text_content().replace("\n\n", "===SEP===\n")

    for x in tableContent.split("===SEP==="):
        x = x.replace("\n", "")
        if "•" not in x:
            continue
        x = (
            x.replace("Hector: Firestarter", "• Firestarter")
            .replace("The Continental: Brooklyn 10-10", " •  Brooklyn 10-10")
            .replace("NightmareBasic: Flash Drive", "Nightmare • Flash Drive")
            .replace("Other: Safe House Raid", " • Safe House Raid")
            .replace("Watchdogs Jimmy:", "Watchdogs •")
            .replace("Event: Cursed", " • Cursed")
            .replace("The Butcher: ", " ")
        )

        for heist in x.split("•"):
            heist = heist.strip().rstrip()
            if heist in classics:
                heist += " (Payday 2)"
            print(f"Requesting heist: {heist}")
            heistPage = requests.get(f"https://payday.fandom.com/wiki/{heist}", headers=headers)
            heistDoc = lh.fromstring(heistPage.content)
            # div -> table -> tbody
            heistTable = heistDoc.xpath("//div[@class='mw-parser-output']")[0]

            for foo in heistTable:
                if (
                    foo.get("style")
                    == "background-color:#131313; width:309px; float:right; clear:right; margin-left:.5em; font-size:smaller; line-height:1.5em; color:white"
                ):
                    heistTable = foo[0]
                    break

            contractor = heistTable[3][1].text_content().replace("\n", "")  # Who gives the heist out
            length = int(heistTable[4][1].text_content().replace("\n", ""))  # Length of heist in days
            loudOrStealth = heistTable[5][1].text_content().replace("\n", "").split(" / ")  # Loud, Stealth
            print(f'Found heist "{heist}" from {contractor} of length {length} day(s) ({loudOrStealth})')

            loudable = loudOrStealth[0] == "✔"
            stealthable = loudOrStealth[1] == "✔"

            if heist in doubleNames:
                for doubleName in doubleNames[heist]:
                    scrapedHeists.update(
                        {
                            doubleName: {
                                "contractor": contractor,
                                "days": length,
                                "stealthable": stealthable,
                                "loudable": loudable,
                            }
                        }
                    )
            else:
                scrapedHeists.update(
                    {
                        heist: {
                            "contractor": contractor,
                            "days": length,
                            "stealthable": stealthable,
                            "loudable": loudable,
                        }
                    }
                )
    return scrapedHeists


def HandlePayday2Gear():
    print("Parsing Payday 2 Weapons...")

    # Melee needs to be handled differently.
    typeToLink = {
        "Primary": "https://payday.fandom.com/wiki/Category:Primary_weapons_(Payday_2)",
        "Secondary": "https://payday.fandom.com/wiki/Category:Secondary_weapons_(Payday_2)",
        "Throwable": "https://payday.fandom.com/wiki/Category:Throwable_weapons",
    }
    weaponTypes = {"Primary": [], "Secondary": [], "Throwable": [], "Melee": []}

    for wepType in typeToLink:
        page = requests.get(typeToLink[wepType], headers=headers)
        if not page:
            return
        doc = lh.fromstring(page.content)
        for link in doc.xpath("//a[@class='category-page__member-link']"):
            wepName = link.text_content().replace("\n", "").replace(" (Payday 2)", "").replace("\u2019", "'")
            if ".png" in wepName or "Category:" in wepName or "File:" in wepName:
                continue
            print(f"Parsing gun: {wepName}")
            weaponTypes[wepType] += [wepName]

    # Now to handle melee
    page = requests.get("https://payday.fandom.com/wiki/Category:Melee", headers=headers)
    if not page:
        return
    doc = lh.fromstring(page.content)
    trElements = doc.xpath("//tr")[5:]
    for tableRow in trElements:
        meleeName = tableRow[0].text_content().replace("\n", "").replace("\u00B4", "'")

        print(f"Parsing melee weapon: {meleeName}")
        weaponTypes["Melee"] += [meleeName]
    return weaponTypes


# Hardcoded lol
heists = {
    "__comment1": "All data scraped from: https://payday.fandom.com/wiki/Category:PAYDAY_2_heists#Heists and https://payday.fandom.com/wiki/PAYDAY:_The_Heist#Heists",
    "Payday2": {},
    "Payday1": {
        "First World Bank": {"contractor": "Bain", "days": 1, "stealthable": True, "loudable": True},
        "Heat Street": {"contractor": "Bain", "days": 1, "stealthable": False, "loudable": True},
        "Panic Room": {"contractor": "Bain", "days": 1, "stealthable": False, "loudable": True},
        "Green Bridge": {"contractor": "Bain", "days": 1, "stealthable": False, "loudable": True},
        "Diamond Heist": {"contractor": "Bain", "days": 1, "stealthable": True, "loudable": True},
        "Slaughterhouse": {"contractor": "Bain", "days": 1, "stealthable": False, "loudable": True},
        "Undercover": {"contractor": "Bain", "days": 1, "stealthable": False, "loudable": True},
        "Counterfeit": {"contractor": "Bain", "days": 1, "stealthable": False, "loudable": True},
        "No Mercy": {"contractor": "Bain", "days": 1, "stealthable": False, "loudable": True},
    },
}

heists["Payday2"] = HandlePayday2Heists()

with open("../js/data/heists.json", "w") as outfile:
    json.dump(heists, outfile, indent=4)

# Hardcoded cause its not like Payday 1 is getting updated lol
gear = {
    "Payday2": {},
    "Payday1": {
        "Primary": [
            "AMCAR-4",
            "Reinbeck",
            "M308",
            "Brenner 21",
            "AK-47",
            "Mark 11",
            "Locomotive 12G",
            "Compact-5",
            "GL40",
        ],
        "Secondary": ["B9-S", "Bronco .44", "Crosskill .45", "STRYK"],
        "Melee": ["Knife"],
    },
}
gear["Payday2"] = HandlePayday2Gear()

with open("../js/data/gear.json", "w") as outfile:
    json.dump(gear, outfile, indent=4)
