#!/usr/bin/env python3

import random

def generatePairs():

    pairCandidates = {
        "Mohamad Jammoul": "Austin",
        "Mary Wheeler": "Austin",
        "Chris Green": "CSIRO",
        "James Gunning": "CSIRO",
        "Samuel Jackson": "CSIRO",
        "Andrew Wilkins": "CSIRO",
        "Dennis Voskov": "Delft",
        "Michiel Wapperom": "Delft",
        "Florian Doster": "Herriot-Watt",
        "Sebastian Geiger": "Herriot-Watt",
        "Satish Karra": "LANL",
        "Hari Viswanathan": "LANL",
        "Jacques Franc": "Stanford",
        "Holger Class": "Stuttgart",
        "Dennis Gläser": "Stuttgart",
    }

    observerCandidates = {
        "Meissam Bahlali": "Imperial",
        "Matthew Jackson": "Imperial",
        "Carl Jacquemyn": "Imperial",
        "Geraldine Regnier": "Imperial",
        "Pablo Salinas": "Imperial",
        "Youssef AbdAllah": "Melbourne",
        "Stephan Matthai": "Melbourne",
    }

    finished = False
    idx = 1
    while not finished:
        person1, group1 = random.choice(list(pairCandidates.items()))
        person2, group2 = random.choice(list(pairCandidates.items()))

        if person1 == person2 or group1 == group2:
            continue

        if observerCandidates:
            observer, group = random.choice(list(observerCandidates.items()))

        print(f'Pair {idx}: {person1} ({group1}) and {person2} ({group2}), Observer: {observer} ({group})')
        idx += 1
        del pairCandidates[person1]
        del pairCandidates[person2]
        del observerCandidates[observer]

        if len(pairCandidates) < 2:
            finished = True

if __name__ == "__main__":
    generatePairs()
