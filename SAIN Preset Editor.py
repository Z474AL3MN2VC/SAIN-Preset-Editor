import os
import re
import json
from glob import glob

"""
### Get the file names and locations to work with. ###
# TODO: Have the script prompt for the name of the preset to modify.

# Get an array of the default bot files to modify including the file locations.
myBotFiles = []
myBotDir= glob("./SAIN-*/BepInEx/plugins/SAIN/Presets/AiSB/BotSettings/*")
myBotDir.sort()
for botFiles in myBotDir:
    myBotFiles.append(botFiles)

# Get the bot names out of the bot file locations.
defaultBotNames = []
for botNames in myBotFiles:
    extractBotName = re.search("([\\w\\s]+)\\.json", botNames)
    defaultBotNames.append(extractBotName.group(1))

# Get an array of the personality files to modify including the file locations.

myPersonalityFiles = []
myPersonalityDir= glob("./SAIN-*/BepInEx/plugins/SAIN/Presets/AiSB/Personalities/*")
myPersonalityDir.sort()
for personalityFiles in myPersonalityDir:
    myPersonalityFiles.append(personalityFiles)

# Get the personality names out of the personality file locations.
defaultPersonalityNames = []
for personalityNames in myPersonalityFiles:
    extractPersonalityNName = re.search("([\\w\\s]+)\\.json", personalityNames)
    defaultPersonalityNames.append(extractPersonalityName.group(1))    
"""


### Hard code stuff for now. ### 
myPresetDir = "./Presets/AiSB/BotSettings/"
defaultBotDir = "./Default Bot Config Values/"
fileExtension = ".json"


### Define bot tiers. ###

# Low Tier: Scavs
tierScav = ["Crazy Scav Event", "Scav Group", "Scav", "Tagged and Cursed Scav"]
# Medium Tier: PMCs
tierPMC = ["Bear", "Usec"]
# High Tier: Rogues, Raiders, Boss Guards
tierElite = ["Bloodhound", "Cultist", "Gluhar Guard Assault", "Gluhar Guard Scout", "Gluhar Guard Security", "Gluhar Guard Snipe", "Kaban Guard Close 1", "Kaban Guard Close 2", "Kaban Guard", "Kaban Sniper", "Kolontay Assault", "Kolontay Security", "Raider", "Rashala Guard", "Rogue", "Sanitar Guard", "Shturman Guard", "Tagilla Guard"]
# High Tier: Bosses
tierBoss = ["BigPipe","BirdEye","Cultist Priest", "Gluhar", "Kaban", "Killa", "Knight", "Kolontay", "Partisan", "Rashala", "Sanitar", "Shturman", "Tagilla"]


### Prompt for user input. ###

# Select the tier and set the array to use.
print("Select Tier: Scav, PMC, Elite, Boss")
userInput = input()
if userInput == "Scav":
    theTier = tierScav
elif userInput == "PMC":
    theTier = tierPMC
elif userInput == "Elite":
    theTier = tierElite
elif userInput == "Boss":
    theTier = tierBoss
else:
    print("ERROR")
    exit()

# Select the difficulty.
# Universal difficulty level for all Elite and Boss types.
if theTier in (tierElite, tierBoss):
    print("Universal difficulty level for all Elite and Boss types.")
else:
    print("Select Difficulty: easy, normal, hard, impossible")
    theDifficulty = input()
    if theDifficulty == "easy":
        "OK"
    elif theDifficulty == "normal":
        "OK"
    elif theDifficulty == "hard":
        "OK"
    elif theDifficulty == "impossible":
        "OK"
    else:
        print("ERROR")
        exit()

# Select the property types.
print("Select Property Type: Core, Difficulty, Grenade")
thePropertyType = input()
if thePropertyType == "Core":
    print("Select Property:")
    print("VisibleAngle float, VisibleDistance float, AccuratySpeed float")
elif thePropertyType == "Difficulty":
    print("Select Property:")
    print("VisibleDistCoef float, GainSightCoef float, ScatteringCoef float, HearingDistanceCoef float, AggressionCoef float, PrecisionSpeedCoef float, AccuracySpeedCoef float")
elif thePropertyType == "Grenade":
    print("Select Property:")
    print("TimeSinceSeenBeforeThrow float, ThrowGrenadeFrequency float, ThrowGrenadeFrequency_MAX float, GrenadePrecision float")
else:
    print("ERROR")
    exit()
theProperty = input()

# Get the default value for the selected property.
# No default value exists for Difficulty object, print the current values instead.
for filetoEdit in theTier:
    if thePropertyType != "Difficulty":
        theFileName = defaultBotDir+filetoEdit+fileExtension
    else:
        theFileName = myPresetDir+filetoEdit+fileExtension
    with open(theFileName, "r") as file:
        data = json.load(file)
        print("Default:", filetoEdit)
        if theTier in (tierElite, tierBoss):
            print(data["Settings"]["impossible"][thePropertyType][theProperty])
        else:
            print(data["Settings"][theDifficulty][thePropertyType][theProperty])
# Set the property value.
print("Enter your modified value.")
theValue = input()
theValue = float(theValue)


### Proceed to modify files. ###

# Iterate through the tier files.
for filetoEdit in theTier:
    theFileName = myPresetDir+filetoEdit+fileExtension
    with open(theFileName, "r") as file:
        data = json.load(file)
        # Universal difficulty level for all Elite and Boss types.
        if theTier in (tierElite, tierBoss):
            # Print the file that is being edited.
            print("Editing: "+filetoEdit+" - Universal Difficulty"+"- Property: "+theProperty)
            # Print the existing property value.
            print("From: ")
            print(data["Settings"]["impossible"][thePropertyType][theProperty])
            # Print the modified property value.
            print("To: ")
            data["Settings"]["easy"][thePropertyType][theProperty] = theValue
            data["Settings"]["normal"][thePropertyType][theProperty] = theValue
            data["Settings"]["hard"][thePropertyType][theProperty] = theValue
            data["Settings"]["impossible"][thePropertyType][theProperty] = theValue
            print(data["Settings"]["impossible"][thePropertyType][theProperty])  
        else:
            # Print the file that is being edited.
            print("Editing: "+filetoEdit+" - Selected Difficulty: "+theDifficulty+" - Property: "+theProperty)
            # Print the existing property value.
            print("From: ")
            print(data["Settings"][theDifficulty][thePropertyType][theProperty])
            # Print the modified property value.
            print("To: ")
            data["Settings"][theDifficulty][thePropertyType][theProperty] = theValue
            print(data["Settings"][theDifficulty][thePropertyType][theProperty])
    # Save files.
    with open (theFileName, "w") as file:
        json.dump(data, file, indent=2)
        

### The bot properties to adjust. ###

# botName.json - Settings.(easy|normal|hard|impossible).Difficulty.$theProperty
#   VisibleDistCoef float
#   GainSightCoef float
#   ScatteringCoef float
#   HearingDistanceCoef float
#   AggressionCoef float
#   PrecisionSpeedCoef float
#   AccuracySpeedCoef float

# botName.json - Settings.(easy|normal|hard|impossible).Core.$theProperty
#   VisibleAngle float
#   VisibleDistance float
#   AccuratySpeed float

# botName.json - Settings.(easy|normal|hard|impossible).Grenade.$theProperty
#   TimeSinceSeenBeforeThrow float
#   ThrowGrenadeFrequency float
#   ThrowGrenadeFrequency_MAX float
#   GrenadePrecision float

### The personality properties to adjust. ###

# personalityName.json
#   Assignment.CanBeRandomlyAssigned true/false
#   Assignment.RandomlyAssignedChance float