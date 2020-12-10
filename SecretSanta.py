# Title - Secret Santa Generator
# Author - Andrew Knapp
# 
# Goal - Generate Secret Santa Pairings
# without given excluded pairs

import os
import shutil
import random
from copy import deepcopy

# Takes in a list of participants and a dictionary of excluded pairs
# the pairs are in the form
# { "name1": ["name2", "name3"]}
def generatePairs(participants, excludedPairs):
    random.seed()
    # Randomizes order of participants
    random.shuffle(participants) 

    pairings = {}
    successfullyGeneratedPairings = False

    # Attempts to create a successful pairing, if one
    # is not made it will try again. This is a faux depth 
    # first search in that decisions are randomized each attempt
    # without taking into account previous attempted pairings
    while not successfullyGeneratedPairings:

        peopleLeft = deepcopy(participants)
        attemptNumber = 0
        index = 0
        successfullyAddedPair = False
        currentRecipient = ""
        for person in participants:

            successfullyAddedPair = False
            attemptNumber = 0
            while not successfullyAddedPair:
                # Protection against infinite loops
                if (attemptNumber > len(peopleLeft * 2)):
                    successfullyGeneratedPairings = False
                    break
                attemptNumber += 1
                index = random.randint(0, len(peopleLeft) - 1)
                currentRecipient = peopleLeft[index]
                # If the possible currentRecipient is not the current person
                # If the possible currentRecipient is not in the person's excluded pairs
                # If the possible currentRecipient is not already the Secret Santa for the current person
                if not (currentRecipient == person) and not (person in excludedPairs and (currentRecipient in excludedPairs[person])) and not (currentRecipient in pairings and pairings[currentRecipient] == person):
                    # Set the current person as the secret santa to the currentRecipient
                    pairings[person] = currentRecipient
                    peopleLeft.remove(currentRecipient)
                    successfullyAddedPair = True
                    # If all pairings have been made exit loop.
                    if (len(pairings.keys()) == len(participants)):
                        successfullyGeneratedPairings = True
    
    return pairings


# Read participants from people.txt
# output: a list of all participants
def readParticipants():
    participants = open("people.txt").read()

    participantList = []
    currentPerson = ""
    for x in range(len(participants)):
        if not (participants[x] == "\n"):
            currentPerson += participants[x]
        else:
            participantList.append(currentPerson)
            currentPerson = ""

    return participantList

# Reads the pairs that should not be assigned to one another
# output: a dictionary in the form
# { "name1": ["name2", "name3"]}
def readExcludedPairs():
    excludedPairs = open("excludedPairs.txt").read()
    excludedPairList = {}
    currentPerson = ""
    currentPair = []
    for x in range(len(excludedPairs)):
        if excludedPairs[x] == " ":
            currentPair.append(currentPerson)
            currentPerson = ""
        elif excludedPairs[x] == "\n":
            currentPair.append(currentPerson)
            if currentPerson in excludedPairList:
                excludedPairList[currentPair[1]].append(currentPair[0])
                if currentPair[0] in excludedPairList:
                    excludedPairList[currentPair[0]].append(currentPair[1])
            else:
                excludedPairList[currentPair[0]] = [currentPair[1]]
                excludedPairList[currentPair[1]] = [currentPair[0]]
            currentPair = []
            currentPerson = ""
        else:
            currentPerson += excludedPairs[x]

    return excludedPairList

# Write the pairings to separate txt files
def recordPairings(pairings):

    path = "./pairings"
    
    shutil.rmtree(path, True)
    os.mkdir(path)

    for secretSanta in pairings:
        pairFile = open(os.path.join(path, secretSanta), "w")
        pairFile.write("You are the secret santa for " + pairings[secretSanta])


def main():
    participants = readParticipants()

    excludedPairs = readExcludedPairs()
   
    pairs = generatePairs(participants, excludedPairs)

    recordPairings(pairs)

    print("Your pairings have been created\nMake sure to not peek at yours!")

main()