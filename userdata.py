import discord
import sqlite3
import validators


class userdata:
    def __init__(self):
        self.discordID = 0
        self.betted_side = 'radiant'
        self.amount = 0

    def setDiscordID(self, discordID):
        self.discordID = discordID

    def getDiscordID(self):
        return self.discordID

    def setBetSide(self, side):
        self.betted_side = side

    def getBetSide(self):
        return self.betted_side

    def setAmount(self, amount):
        self.amount = amount

    def getAmount(self):
        return self.amount
