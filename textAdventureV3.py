# Programmed by Kenneth Mallabo
# C15494052
# For the Lab Assessment Part 3 for the Software Development module
# This program is a small text adventure game

import random
from abc import ABC, abstractmethod
import json

# creating class structure for Equipment class
class Equipment(ABC):
    def __init__(self, d):
        self.difficulty = d

    @abstractmethod
    def calculateStat(self):
        pass

class Weapon(Equipment):
    # initialise with inheritance from Equipment class
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.attackValue = None

    # override abstract method
    def calculateStat(self):
        # normal difficulty
        if self.difficulty == 1:
            self.attackValue = 20
        # easy difficulty
        elif self.difficulty == 2:
            self.attackValue = 40

    def getAttack(self):
        return self.attackValue

class Armour(Equipment):
    # initialise with inheritance from Equipment class
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.healthValue = None

    # override abstract method
    def calculateStat(self):
        # normal difficulty
        if self.difficulty == 1:
            self.healthValue = 100
        # easy difficulty
        elif self.difficulty == 2:
            self.healthValue = 200

    def getHealth(self):
        return self.healthValue

class Game(Weapon, Armour):
    # initialise multiple inheritance derived from weapon and armour
    def __init__(self, cm, cn, d, w, h):
        # initialise the variables
        super().__init__(difficulty=d)
        self.combatMode = cm
        self.characterName = cn
        self.weaponStat = w
        self.healthStat = h

    # main menu selection function/mutator method
    def menuSelect(self):
        while True:
            print("Starting Game")
            value = input("Please enter 1 if you wish to get into a dialog scenario or 2 for just combat:\n")
            if value == "1":
                self.combatMode = 0
                print("You have chosen story mode")
                break
            elif value == "2":
                self.combatMode = 1
                print("You have chosen combat mode only")
                if self.difficulty == 1:
                    print("Reminder that you are playing on Normal difficulty")
                    print("Attack Value: " + str(self.weaponStat) + " Health: " + str(self.healthStat))
                    break
                elif self.difficulty == 2:
                    print("Reminder that you are playing on Easy difficulty")
                    print("Attack Value: " + str(self.weaponStat) + " Health: " + str(self.healthStat))
                    break
            else:
                print("Incorrect input detected, please choose 1 or 2")

    # function to add the character's name/mutator method
    def addName(self):
        tempCharacter = input("Enter your character's name:\n")
        # check if the entered name is empty, raise error if it is
        if bool(tempCharacter and not tempCharacter.isspace()) is False:
            raise EmptyInputError("Invalid name", "name must not be empty!")
        else:
            self.characterName = tempCharacter

class Scenario:
    # Implementing the 1:1 aggregation relationship between Scenario and Game classes
    def __init__(self, game):
        # initialise the variables
        self.Game = game
        self.talker = None
        self.noOfEnemy = None
        self.movement = None
        # a list enemy names and their health
        self.listEnemy = []

    # function to print statements out if you picked combat/dialog
    def startScenario(self):
        # dialog only
        if self.Game.combatMode == 0:
            print("Welcome to Fodlan, a continent recovering from a recent devastating war")
            print("Disillusioned soldiers have turned to banditry")
            print("Be careful whilst on your journey")
        # no dialog, all combat
        elif self.Game.combatMode == 1:
            print("Welcome to Fodlan, a continent that is experiencing complete societal collapse")
            print("A devastating plague has wiped out most of the population")
            print("The only survivors are deranged, prepare for unending struggle")

    # function on where to move/mutator method
    def moveScenario(self):
        while True:
            print("To the north is the savage mountains, filled with man eating heathens.")
            print("To the south lies the unforgiving desert where slavery has yet to be expelled.")
            print("To the west engulfs the seemingly endless seas, privateers and pirates are a dime a dozen here.")
            print("To the east where land is yet to be charted, here be dragons?")
            self.movement = input("Where do you want to venture forth?\n")

            if self.movement == "north":
                print(f"{self.Game.characterName} had trekked north in the snowy mountains")
                self.movement = "north"
                break
            elif self.movement == "south":
                print(f"{self.Game.characterName} had journeyed towards the sandy south")
                self.movement = "south"
                break
            elif self.movement == "west":
                print(f"{self.Game.characterName} had sailed the western seas")
                self.movement = "west"
                break
            elif self.movement == "east":
                print(f"{self.Game.characterName} have travelled to the far east")
                self.movement = "east"
                break
            else:
                print(f"Incorrect location has been inputted , what is {self.movement} anyway?")

    # function to create enemies to fight/mutator method
    def generateNumEnemy(self):
        # create up to 3 enemies
        self.noOfEnemy = random.randint(3, 4)  # Bug?: if used 1 to 5, sometimes 0 gets used
        print(self.noOfEnemy)
        for x in range(1, self.noOfEnemy):
            if self.movement == "north":
                self.enemyName = "Chaos Marauder"
                self.listEnemy.append([self.enemyName + str(x), 80])
            elif self.movement == "south":
                self.enemyName = "Slaver"
                self.listEnemy.append([self.enemyName + str(x), 20])
            elif self.movement == "west":
                self.enemyName = "Pirate"
                self.listEnemy.append([self.enemyName + str(x), 40])
            else:
                self.enemyName = "Ninja"
                self.listEnemy.append([self.enemyName + str(x), 60])
        self.noOfEnemy = self.noOfEnemy - 1

    # function to create npc/mutator method
    def generateNPC(self):
        if self.movement == "north":
            self.talker = "Greg the Chaos Marauder"
        elif self.movement == "south":
            self.talker = "Jack the Slaver"
        elif self.movement == "west":
            self.talker = "Buggy the Pirate"
        else:
            self.talker = "Nin the Ninja"

class Combat(Scenario):
    # initialise with inheritance from Scenario class
    def __init__(self, playerHealth, playerAttack, characterName, listEnemy):
        super().__init__(playerHealth)
        self.user = characterName
        self.listEnemies = [listEnemy]
        self.playerAttack = playerAttack
        self.playerHealth = playerHealth
        self.aliveEnemies = len(self.listEnemies[0])  # using built in function len to get length of list
        self.scoreNumEnemies = len(self.listEnemies[0])  # using built in function len to get length of list
        self.scoreEnemyType = self.listEnemies[0][0][0]
        self.scoreList = []

    # accessor method to get scoreNumEnemies
    def getScoreNumEnemies(self):
        return self.scoreNumEnemies

    # accessor method to get aliveEnemies for printing
    def getEnemy(self):
        print(self.aliveEnemies)
        for x in range(0, self.aliveEnemies):
            print(f"Enemy: {self.listEnemies[0][x][0]} Health: {self.listEnemies[0][x][1]}\n")

    # function to attack enemies/ mutator method
    def attack(self):
        enemyCounter = self.aliveEnemies
        while True:
            target = input("Who to attack? (Choose number)\n")
            target = int(target) - 1
            try:
                if self.listEnemies[0][target][1] > 0:
                    self.listEnemies[0][int(target)][1] = self.listEnemies[0][int(target)][1] - self.playerAttack
                    print(f"{self.listEnemies[0][target][0]}'s health has dropped to {self.listEnemies[0][target][1]}!")
                    break
                else:
                    print(f"{self.listEnemies[0][target][0]} is already dead!")
            except:
                print("Incorrect target has been chosen")

        # check if the target is dead
        if self.listEnemies[0][target][1] <= 0:
            print(f"{self.listEnemies[0][target][0]} has died!")

        # check if all enemies are dead
        for x in range(0, self.aliveEnemies):
            if self.listEnemies[0][x][1] <= 0:
                enemyCounter = enemyCounter - 1
                if enemyCounter == 0:
                    print("All enemies has been slayed!")
                    self.aliveEnemies = 0

    # function for the all of the enemies to attack the player/ mutator method
    def enemyAttack(self):
        for x in range(0, len(self.listEnemies[0])):
            if self.listEnemies[0][x][1] > 0:
                self.playerHealth = self.playerHealth - 10
                print(f"{self.listEnemies[0][x][0]} has attacked {self.user}")
                print(f"{self.user}'s health has dropped to {self.playerHealth}!")
        # check if the player runs out of health, exit program if true
        if self.playerHealth <= 0:
            print(f"{self.user} has died!")
            exit()

    # function to calculate score depending on type of enemy and store in list
    def calculateScore(self):
        print(f"Number of dead enemies: {self.scoreNumEnemies}")
        score = self.scoreNumEnemies * 10
        if self.scoreEnemyType == "Chaos Marauder1":
            for x in range(self.getScoreNumEnemies()):
                score = score * 8
                self.scoreList.append(score)
        elif self.scoreEnemyType == "Slaver1":
            for x in range(self.getScoreNumEnemies()):
                score = score * 2
                self.scoreList.append(score)
        elif self.scoreEnemyType == "Pirate1":
            for x in range(self.getScoreNumEnemies()):
                score = score * 4
                self.scoreList.append(score)
        elif self.scoreEnemyType == "Ninja1":
            for x in range(self.getScoreNumEnemies()):
                score = score * 6
                self.scoreList.append(score)
        return self.scoreList

    # override string method to show the status of the player
    def __str__(self):
        return f"Hero:{self.user}, Health:{self.playerHealth}"

    # override less than method to compare between combat objects
    def __lt__(self, otherPlayer):
        return self.getScoreNumEnemies() < otherPlayer.getScoreNumEnemies()  # using number of enemies to compare combat objects

    # override greater than method to compare between combat objects
    def __gt__(self, otherPlayer):
        return self.getScoreNumEnemies() > otherPlayer.getScoreNumEnemies()  # using number of enemies to compare combat objects

    # override equal to method to compare between combat objects
    def __eq__(self, otherPlayer):
        return self.getScoreNumEnemies() == otherPlayer.getScoreNumEnemies()  # using number of enemies to compare combat objects

class Dialog(Scenario):
    # initialise with inheritance from Scenario class
    def __init__(self, movement, NPC, characterName):
        super().__init__(movement)
        self.user = characterName
        self.location = movement
        self.talker = NPC
        self.loot = {}              # dictionary of loot, for assignment 3

    # function to print out statements depending on who the NPC is and attempt to steal from them
    def npcDialog(self):
        print("You will now attempt to steal in order to survive")
        if self.talker == "Greg the Chaos Marauder":
            print(f"{self.talker}: Hello there {self.user}, you wish to die?")
            attemptSteal = random.randint(0, 1)
            self.loot['Chance to Steal'] = '50%'
        elif self.talker == "Jack the Slaver":
            print(f"{self.talker}: You look like you will fetch a good price...")
            attemptSteal = random.randint(0, 2)
            self.loot['Chance to Steal'] = '66%'
        elif self.talker == "Buggy the Pirate":
            print(f"{self.talker}: Give me your money or your life!")
            attemptSteal = random.randint(0, 3)
            self.loot['Chance to Steal'] = '75%'
        else:
            print(f"{self.talker}: ...")
            attemptSteal = random.randint(0, 4)
            self.loot['Chance to Steal'] = '80%'

        # check if user succeeds and prints out result
        if attemptSteal == 0:
            self.loot['Loot'] = 0
            print(f"{self.talker} has caught {self.user} trying to steal!")
            #print(f"Statistic: {self.loot}")
            print("Game over")
        else:
            print(f"{self.user} has successfully stolen from {self.talker}!")
            lootScore = random.randint(0, 100)
            self.loot['Loot'] = lootScore
            #print(f"Statistic: {self.loot}")
            print("Congratulations")
        # write dictionary to json file
        with open("stealStats.json", "w") as outfile:
            json.dump(self.loot, outfile)

class PlayerList:
    # Implementing the 1:0..M aggregation relationship between Combat and PlayerList
    def __init__(self):
        self.combats = []

    # function to add more players into the list
    def addPlayer(self, Combat):
        self.combats.append(Combat)

    # function to check if the player is in the list or not
    def searchForPlayer(self, Combat):
        if Combat in self.combats:
            return True
        else:
            return False

    # function to sort player names
    def sortPlayerName(self):
        self.combats.sort()

    # function to use sorted player names in reverse
    def sortedPlayerName(self):
        return sorted(self.combats, reverse=True)

    # function to sort player scores with lambda function
    def sortPlayerScore(self):
        self.combats.sort(key=lambda score: score.calculateScore())

    # function to use sorted player scores in reverse with lambda function
    def sortedPlayerScore(self):
        return sorted(self.combats, key=lambda score: score.calculateScore(), reverse=True)

    # override string method to seperate list of player names
    def __str__(self):
        playerNames = ''
        for s in self.combats:
            playerNames += s.user + ';'
        return playerNames

class EmptyInputError(Exception):
    """Exception raised for errors in the input.

        Attributes:
            expression -- input expression in which the error occurred
            message -- explanation of the error
        """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    # override string method to seperate expression and message
    def __str__(self):
        return self.expression + " | " + self.message

difficultyChoice = input("Enter 1 for normal mode or any other key for easy mode\n")
if difficultyChoice == "1":
    characterAttack = Weapon(1)  # create characterAttack object
    characterHealth = Armour(1)  # create characterHealth object
else:
    characterAttack = Weapon(2)  # create characterAttack object
    characterHealth = Armour(2)  # create characterHealth object
# run functions from Weapon and Armour class
characterAttack.calculateStat()
characterHealth.calculateStat()

game1 = Game(None, None, characterHealth.difficulty, characterAttack.getAttack(),
             characterHealth.getHealth())  # creates game1 object
# run functions from Game class
game1.addName()
game1.menuSelect()

comScenario = Scenario(game1)  # creates comScenario1 object
# run functions from Scenario class
comScenario.startScenario()
comScenario.moveScenario()
comScenario.generateNumEnemy()

# checks if this is combat only
if comScenario.Game.combatMode == 1:
    playerCombat = Combat(comScenario.Game.healthStat, comScenario.Game.weaponStat, comScenario.Game.characterName,
                          comScenario.listEnemy)  # creates playerCombat object
    # continue to loop if there is at least 1 enemies alive
    while playerCombat.aliveEnemies > 0:
        # run functions from Combat class
        playerCombat.getEnemy()
        try:
            playerCombat.attack()
        # if user has entered a non-numeric value
        except ValueError:
            print(f"{playerCombat.user} has clumsily hit the ground!")
        playerCombat.enemyAttack()
        print(playerCombat)  # print the overridden string to show player name and current health
    print(f"Total score: {playerCombat.calculateScore()}")
    highestScore = max(playerCombat.calculateScore())  # built-in function max
    print(f"Highest score: {highestScore}")
    playerList = PlayerList()  # create playerList object
    print("Is " + playerCombat.user + "here? " + str(
        playerList.searchForPlayer(playerCombat)))  # check if playerList is here or not
    playerList.addPlayer(playerCombat)  # add player to the playerList
    print("Is " + playerCombat.user + " here? " + str(
        playerList.searchForPlayer(playerCombat)))  # check if playerList is here or not

    # two-player multiplayer, the other player may get to play their turn
    print("Congratulations! Is there another player that wants to play?")
    choice = input("1 for yes or any other key for no\n")
    if choice == "1":
        difficultyChoice = input("Enter 1 for normal mode or any other key for easy mode\n")
        if difficultyChoice == "1":
            characterAttack2 = Weapon(1)  # create characterAttack object
            characterHealth2 = Armour(1)  # create characterHealth object
        else:
            characterAttack2 = Weapon(2)  # create characterAttack object
            characterHealth2 = Armour(2)  # create characterHealth object
        # run functions from Weapon and Armour class
        characterAttack2.calculateStat()
        characterHealth2.calculateStat()
        game2 = Game(None, None, characterHealth2.difficulty, characterAttack2.getAttack(),
                     characterHealth2.getHealth())  # creates game2 object
        # run functions from Game class
        game2.addName()
        game2.menuSelect()
        comScenario2 = Scenario(game2)  # creates comScenario2 object
        # run functions from Scenario class
        comScenario2.moveScenario()
        comScenario2.generateNumEnemy()

        if comScenario2.Game.combatMode == 1:
            playerCombat2 = Combat(comScenario2.Game.healthStat, comScenario2.Game.weaponStat,
                                   comScenario2.Game.characterName,
                                   comScenario2.listEnemy)  # creates playerCombat2 object
            # continue to loop if there is at least 1 enemies alive
            while playerCombat2.aliveEnemies > 0:
                # run functions from Combat class
                playerCombat2.getEnemy()
                try:
                    playerCombat2.attack()
                # if user has entered a non-numeric value
                except ValueError:
                    print(f"{playerCombat2.user} has clumsily hit the ground!")
                playerCombat2.enemyAttack()
                print(playerCombat2)
            print(f"All scores: {playerCombat2.calculateScore()}")
            highestScore = max(playerCombat2.calculateScore())  # built-in function max
            print(f"Highest score: {highestScore}")
            print("Is " + playerCombat2.user + " here? " + str(
                playerList.searchForPlayer(playerCombat2)))  # check if playerList is here or not
            playerList.addPlayer(playerCombat2)  # add player to the playerList
            playerList.sortPlayerName()  # sort players' names in alphabetical order
            print(playerList)  # check for players
            for s in playerList.sortedPlayerName():
                print(s.user)  # print sorted players' names

            # compare if the first player has killed more than the second
            if playerCombat > playerCombat2:
                print(f"{playerCombat.user}'s enemies killed is greater than {playerCombat2.user}")
            # compare if the first player has killed less than the second
            elif playerCombat < playerCombat2:
                print(f"{playerCombat.user}'s enemies killed is greater than {playerCombat2.user}")
            # compare if the first and second player has killed equally the same number
            else:
                print(f"{playerCombat.user}'s enemies killed is equal to {playerCombat2.user}")

        # checks if this is dialog only
        elif comScenario2.Game.combatMode == 0:
            comScenario2.generateNPC()  # run function to create NPC depending on location
            playerDialog = Dialog(comScenario2.movement, comScenario2.talker,
                                  comScenario2.Game.characterName)  # create playerDialog object
            playerDialog.npcDialog()  # run function to print out dialog
            # opening json file to print it out
            with open("stealStats.json", "r") as openfile:
                # reading from json file
                json_object = json.load(openfile)
            print(json_object)
# checks if this is dialog only
elif comScenario.Game.combatMode == 0:
    comScenario.generateNPC()  # run function to create NPC depending on location
    playerDialog = Dialog(comScenario.movement, comScenario.talker,
                          comScenario.Game.characterName)  # create playerDialog object
    playerDialog.npcDialog()  # run function to print out dialog# opening json file to print it out
    with open("stealStats.json", "r") as openfile:
        # reading from json file
        json_object = json.load(openfile)
    print(json_object)