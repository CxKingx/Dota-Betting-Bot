import discord
import sqlite3
import validators


class playerprofile:
    def __init__(self):
        self.startAmount = 250
        print('Initiating')
        self.CreateDatabases()

    def CreateDatabases(self):
        con = sqlite3.connect('PlayerProfile.db')
        cur = con.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS PlayerProfile (id integer PRIMARY KEY AUTOINCREMENT , DiscordID , Points , Wins , Lose)''')
        con.commit()
        con.close()

    def Register(self, discordID):
        con = sqlite3.connect('PlayerProfile.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM PlayerProfile WHERE DiscordID ="' + str(discordID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        if (len(result) == 0):
            cur.execute(
                '''INSERT INTO PlayerProfile ( DiscordID, Points , Wins , Lose  ) VALUES(?,?,?,?)''',
                [str(discordID), str(self.startAmount), '0', '0'])

            con.commit()
            con.close()
            message = 'You are registered in the database, you can now bet'
            embed = discord.Embed(description=message, color=0xda0b0b)
            return embed
        else:
            con.close()
            message = 'You Have a account signed up , use *profile to check'
            embed = discord.Embed(description=message, color=0xda0b0b)
            return embed

    def CheckUserExists(self, discordID):
        con = sqlite3.connect('PlayerProfile.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM PlayerProfile WHERE DiscordID ="' + str(discordID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        if (len(result) == 0):
            return False
        else:
            return True

    def GetPlayerProfile(self, discordID):
        print('GetPlayerProfile')
        con = sqlite3.connect('PlayerProfile.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM PlayerProfile WHERE DiscordID ="' + str(discordID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        if (len(result) == 0):
            message = '<@!' + str(discordID) + '> has not Registered , you can use *signup to register'
            embed = discord.Embed(description=message, color=0xda0b0b)
            return embed
        else:
            titlemsg = '<@!' + str(discordID) + '> \'s Profile'
            message = '**' + str(result[0][2]) + '** points'
            embed = discord.Embed(title="", description=titlemsg, color=0xda0b0b)
            embed.add_field(name="Points Left", value=message, inline=False)
            embed.add_field(name="Wins", value=result[0][3], inline=False)
            embed.add_field(name="Losses", value=result[0][4], inline=False)

            return embed

    def AddPoints(self, discordID, amount):
        message = '<@!' + str(discordID) + '> has been added ' + str(amount) + 'points'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    def ReducePoints(self, discordID, amount):
        message = '<@!' + str(discordID) + '> has been reduced ' + str(amount) + 'points'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    def AddWins(self, discordID, amount):
        message = '<@!' + str(discordID) + '> has been added ' + str(amount) + 'win'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    def ReduceWins(self, discordID, amount):
        message = '<@!' + str(discordID) + '> has been reduced ' + str(amount) + 'win'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    def AddLosses(self, discordID, amount):
        message = '<@!' + str(discordID) + '> has been added ' + str(amount) + 'losses'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    def ReduceLosses(self, discordID, amount):
        message = '<@!' + str(discordID) + '> has been reduced ' + str(amount) + 'losses'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed
