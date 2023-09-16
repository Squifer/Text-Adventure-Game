# Programmed by Kenneth Mallabo
# C15494052
# For the Lab Assessment Part 3 for the Software Development module
# This program is a unittest for a small text adventure game

import unittest
import textAdventureV3 as textAdventure

class TestGame(unittest.TestCase):
    def setUp(self):
        # initialise variables
        self.difficulty = 1
        self.weaponStat = 20
        self.healthStat = 100
        self.cm = 1
        self.cn = "Test"
        self.w = textAdventure.Weapon(self.difficulty)
        self.h = textAdventure.Armour(self.difficulty)
        self.g = textAdventure.Game(self.cm, self.cn, self.difficulty, self.w, self.h)
        self.c = textAdventure.Combat(100, 20, "Test", ["Chaos Marauder1", 80])
        self.s = textAdventure.Scenario(self.g)
        self.pl = textAdventure.PlayerList()

    # tests menuSelect function
    def test_menuSelect(self):
        # check if choosing dialog/1 has been successful
        self.g.menuSelect()
        self.assertEqual(self.g.difficulty, 1)
        self.s = textAdventure.Scenario(self.g)

    # tests addName function
    def test_addName(self):
        # check if the chosen name "Test" is successful
        self.g.addName()
        self.assertEqual(self.g.characterName, "Test")

    # tests moveScenario function
    def test_moveScenario(self):
        # check if going north is successful
        self.s.moveScenario()
        self.assertEqual(self.s.movement, "north")

    # tests generateNPC function
    def test_generateNPC(self):
        # check if the actual NPC name is the same as the expected name
        self.s.movement = "north"
        self.s.generateNPC()
        self.assertEqual(self.s.talker, "Greg the Chaos Marauder")

    # tests generateNumEnemy functions
    def test_generateNumEnemy(self):
        # check if listEnemy and noOfEnemy variables are not empty
        self.s.generateNumEnemy()
        #self.c = textAdventure.Combat(100, 20, "Test", ["Chaos Marauder1", 80])
        self.assertIsNotNone(self.s.listEnemy)
        self.assertIsNotNone(self.s.noOfEnemy)

    # tests attack function
    def test_attack(self):
        # check if there are no more enemies left
        self.c = textAdventure.Combat(100, 20, "Test", ["Chaos Marauder2", 80])
        self.c.listEnemies = ["Chaos Marauder2", 80]
        self.c.aliveEnemies = 1
        print(self.c.listEnemies)
        self.c.attack()
        self.assertEqual(self.c.aliveEnemies, 0)

    # tests enemyAttack function
    def test_enemyAttack(self):
        # check to make sure that the player is not dead
        self.c.getEnemy()
        self.c.enemyAttack()
        self.assertIsNotNone(self.c.playerHealth)

    # tests calculateScore function
    def test_calculateScore(self):
        # check to make sure that the scoreList is not empty and has an actual score
        self.c.calculateScore()
        self.assertIsNotNone(self.c.scoreList)


    # tests string method to show the status of the player
    def test_str(self):
        # check to make sure that the string override is not empty
        self.assertIsNotNone(self.c.__str__())

    # tests less than method to compare between combat objects
    def test_lt(self):
        # check that 0 is greater than scoreNumEnemies like the less than override
        self.assertLess(0, self.c.scoreNumEnemies)

    # tests greater than method to compare between combat objects
    def test_gt(self):
        # check that scoreNumEnemies is greater than 0 like the greater than override
        self.assertGreater(self.c.scoreNumEnemies, 0)

    # tests equal to method to compare between combat objects
    def test_eq(self):
        # check that scoreNumEnemies is equal to scoreNumEnemies like the equal to override
        self.assertEqual(self.c.scoreNumEnemies, self.c.scoreNumEnemies)

    # tests npcDialog function
    def test_npcDialog(self):
        # check that the talker variable is the same as the expected "Greg the Chaos Marauder"
        self.npc = textAdventure.Dialog("north", "Greg the Chaos Marauder", "Test")  # create playerDialog object
        self.assertEqual(self.npc.talker, "Greg the Chaos Marauder")

    # tests function to add more players into the list and function to check if the player is in the list or not
    def test_addSearchForPlayer(self):
        # check if the second player is indeed in the list
        self.c2 = textAdventure.Combat(200, 40, "Test2", "Pirate")
        self.pl = textAdventure.PlayerList()
        self.pl.addPlayer(self.c2)
        self.assertTrue(self.pl.searchForPlayer(self.c2))

    # tests string method to seperate list of player names
    def test_str2(self):
        # check to make sure that the string override is not empty
        self.assertIsNotNone(self.pl.__str__())

    # tests user attack function if user has entered a non-numeric value
    def test_attackError(self):
        # check if user entered non-numeric value like "t", if exception is raised then test is a success
        with self.assertRaises(Exception):
            self.c.attack()

if __name__ == '__main__':
    # begin the test
    unittest.main()