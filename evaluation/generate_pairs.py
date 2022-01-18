#!/usr/bin/env python3
import random

def generatePairs():
    pairCandidates = {
        "Mojdeh Delshad": "Austin",
        "Mohamad Jammoul": "Austin",
        "Mary Wheeler": "Austin",
        "Chris Green": "CSIRO",
        "Samuel Jackson": "CSIRO",
        "Denis Voskov": "Delft",
        "Michiel Wapperom": "Delft",
        "Sebastian Geiger": "Herriot-Watt",
        "Satish Karra": "LANL",
        "Hari Viswanathan": "LANL",
        "Jacques Franc": "Stanford",
        "Holger Class": "Stuttgart",
        "Dennis Gläser": "Stuttgart",
        "Stephan Matthai": "Melbourne",
    }

    observerCandidates = {
        "Meissam Bahlali": "Imperial",
        "Matthew Jackson": "Imperial",
        "Carl Jacquemyn": "Imperial",
        "Geraldine Regnier": "Imperial",
        "Pablo Salinas": "Imperial",
        "Qi Shao": "Melbourne",
        "Luat Khoa Tran": "Melbourne",
        "Youssef AbdAllah": "Melbourne",
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

        if group == group1 or group == group2:
            continue

        print(f'Pair {idx}: {person1} ({group1}) and {person2} ({group2}), Observer: {observer} ({group})')
        idx += 1
        del pairCandidates[person1]
        del pairCandidates[person2]
        del observerCandidates[observer]

        if len(pairCandidates) < 2:
            finished = True

if __name__ == "__main__":
    generatePairs()
