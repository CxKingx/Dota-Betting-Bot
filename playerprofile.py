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
            '''CREATE TABLE IF NOT EXISTS PlayerProfile (id integer PRIMARY KEY AUTOINCREMENT , DiscordID , 
            Points INT(50), Wins INT(50), Lose INT(50) )''')
        con.commit()
        con.close()

        con = sqlite3.connect('ActivityHistory.db')
        cur = con.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS ActivityHistory (id integer PRIMARY KEY AUTOINCREMENT , DiscordID , Points, Wins , Lose)''')
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

    def deleteUser(self, discordID):
        result = self.OpenDBPlayerProfile(discordID)
        if (len(result) == 0):
            message = 'nothing to delete'
        else:
            print('deleting')
            updatestring = 'DELETE FROM PlayerProfile WHERE DiscordID = "' + str(discordID) + '"'
            self.UpdateDBPlayerProfile(discordID, updatestring)
            message = 'Deleted ID'
        embed = discord.Embed(description=message, color=0xda0b0b)
        return embed


    def CheckUserExists(self, discordID):
        result = self.OpenDBPlayerProfile(discordID)
        if (len(result) == 0):
            return False
        else:
            return True

    def CheckBetableStatus(self, discordID, bet_amount):
        result = self.OpenDBPlayerProfile(discordID)
        if (len(result) == 0):
            return False
        else:
            if int(bet_amount) > int(result[0][2]):
                return False
            else:
                return True

    def GetUserMoney(self, discordID):
        result = self.OpenDBPlayerProfile(discordID)
        if len(result) == 0:
            return False
        else:
            return result[0][2]

    def GetPlayerProfile(self, discordID):
        print('GetPlayerProfile')
        result = self.OpenDBPlayerProfile(discordID)
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

    def OpenDBPlayerProfile(self, discordID):
        print('OpenDB')
        con = sqlite3.connect('PlayerProfile.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM PlayerProfile WHERE DiscordID ="' + str(discordID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        con.close()
        return result

    def UpdateDBPlayerProfile(self, discordID, message):
        print('UpdateDB')
        con = sqlite3.connect('PlayerProfile.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM PlayerProfile WHERE DiscordID ="' + str(discordID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        cur.execute(message)
        con.commit()
        con.close()
        return

    def UpdateHistory(self, discordID, message, data_tuple):
        print('updating History')
        con = sqlite3.connect('ActivityHistory.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM ActivityHistory WHERE DiscordID ="' + str(discordID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        cur.execute(message, data_tuple)
        con.commit()
        con.close()
        return

    #

    # Manual Just in Case Functions
    def AddPoints(self, discordID, amount):
        print('Adding Points')
        result = self.OpenDBPlayerProfile(discordID)
        if len(result) == 0:
            message = 'Something went Wrong'
            embed = discord.Embed(description=message, color=0xda0b0b)
            return embed
        else:
            addCounter = int(result[0][2]) + int(amount)
            updatestring = "UPDATE PlayerProfile SET Points = '" + str(addCounter) + "' WHERE DiscordID = '" + str(
                discordID) + "'"
            self.UpdateDBPlayerProfile(discordID, updatestring)
            # Update History
            updateHistory = '''INSERT INTO ActivityHistory ( DiscordID, Points ,Wins,Lose) VALUES(?,?,?,?)'''
            data_tuple = (str(discordID), str(amount), '0', '0')
            self.UpdateHistory(discordID, updateHistory, data_tuple)

        message = '<@!' + str(discordID) + '> has been added ' + str(amount) + 'points'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    def ReducePoints(self, discordID, amount):
        print('Reducing Points')
        result = self.OpenDBPlayerProfile(discordID)
        if len(result) == 0:
            message = 'Something went Wrong'
            embed = discord.Embed(description=message, color=0xda0b0b)
            return embed
        else:
            addCounter = int(result[0][2]) - int(amount)
            updatestring = "UPDATE PlayerProfile SET Points = '" + str(addCounter) + "' WHERE DiscordID = '" + str(
                discordID) + "'"
            self.UpdateDBPlayerProfile(discordID, updatestring)
            # Update History
            updateHistory = '''INSERT INTO ActivityHistory ( DiscordID, Points ,Wins,Lose) VALUES(?,?,?,?)'''
            reducestring = '-'+str(amount)
            data_tuple = (str(discordID), str(reducestring), '0', '0')
            self.UpdateHistory(discordID, updateHistory, data_tuple)

        message = '<@!' + str(discordID) + '> has been reduced ' + str(amount) + 'points'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    def AddWins(self, discordID, amount):
        print('Adding Wins')
        result = self.OpenDBPlayerProfile(discordID)
        if len(result) == 0:
            message = 'Something went Wrong'
            embed = discord.Embed(description=message, color=0xda0b0b)
            return embed
        else:

            addCounter = int(result[0][3]) + int(amount)
            updatestring = "UPDATE PlayerProfile SET Wins = '" + str(addCounter) + "' WHERE DiscordID = '" + str(
                discordID) + "'"
            self.UpdateDBPlayerProfile(discordID, updatestring)
            # Update History
            updateHistory = '''INSERT INTO ActivityHistory ( DiscordID, Points ,Wins,Lose) VALUES(?,?,?,?)'''
            data_tuple = (str(discordID), '0', str(amount), '0')
            self.UpdateHistory(discordID, updateHistory, data_tuple)

        message = '<@!' + str(discordID) + '> has been added ' + str(amount) + 'win'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    def ReduceWins(self, discordID, amount):
        print('Reducing Wins')
        result = self.OpenDBPlayerProfile(discordID)
        if len(result) == 0:
            message = 'Something went Wrong'
            embed = discord.Embed(description=message, color=0xda0b0b)
            return embed
        else:
            addCounter = int(result[0][3]) - int(amount)
            updatestring = "UPDATE PlayerProfile SET Wins = '" + str(addCounter) + "' WHERE DiscordID = '" + str(
                discordID) + "'"
            self.UpdateDBPlayerProfile(discordID, updatestring)
            # Update History
            updateHistory = '''INSERT INTO ActivityHistory ( DiscordID, Points ,Wins,Lose) VALUES(?,?,?,?)'''
            data_tuple = (str(discordID), '0', str(-amount), '0')
            self.UpdateHistory(discordID, updateHistory, data_tuple)

        message = '<@!' + str(discordID) + '> has been reduced ' + str(amount) + 'win'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    def AddLosses(self, discordID, amount):
        print('Adding Losses')
        result = self.OpenDBPlayerProfile(discordID)
        if len(result) == 0:
            message = 'Something went Wrong'
            embed = discord.Embed(description=message, color=0xda0b0b)
            return embed
        else:
            addCounter = int(result[0][4]) + int(amount)
            updatestring = "UPDATE PlayerProfile SET Lose = '" + str(addCounter) + "' WHERE DiscordID = '" + str(
                discordID) + "'"
            self.UpdateDBPlayerProfile(discordID, updatestring)
            # Update History
            updateHistory = '''INSERT INTO ActivityHistory ( DiscordID, Points ,Wins,Lose) VALUES(?,?,?,?)'''
            data_tuple = (str(discordID), '0', '0', str(amount))
            self.UpdateHistory(discordID, updateHistory, data_tuple)
        message = '<@!' + str(discordID) + '> has been added ' + str(amount) + 'losses'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    def ReduceLosses(self, discordID, amount):
        print('Reduce Losses')
        result = self.OpenDBPlayerProfile(discordID)
        if len(result) == 0:
            message = 'Something went Wrong'
            embed = discord.Embed(description=message, color=0xda0b0b)
            return embed
        else:
            addCounter = int(result[0][4]) - int(amount)
            updatestring = "UPDATE PlayerProfile SET Lose = '" + str(addCounter) + "' WHERE DiscordID = '" + str(
                discordID) + "'"
            self.UpdateDBPlayerProfile(discordID, updatestring)
            # Update History
            updateHistory = '''INSERT INTO ActivityHistory ( DiscordID, Points ,Wins,Lose) VALUES(?,?,?,?)'''
            data_tuple = (str(discordID), '0', '0', str(-amount))
            self.UpdateHistory(discordID, updateHistory, data_tuple)

        message = '<@!' + str(discordID) + '> has been reduced ' + str(amount) + 'losses'
        embed = discord.Embed(title="", description=message, color=0xda0b0b)
        return embed

    # End of The Manual Functions for Backup
    def CustomOpenPlayerProfile(self, executeString):
        print('OpenDB')
        con = sqlite3.connect('PlayerProfile.db')
        cur = con.cursor()
        cur.execute(executeString)
        result = cur.fetchall()
        con.close()
        return result

    # Get Top 5
    def GetTopFive(self):
        # message = 'Top 5 Winners is: '
        message = 'The fattest 5'
        executeString = "SELECT * FROM PlayerProfile ORDER BY Points DESC"
        result = self.CustomOpenPlayerProfile(executeString)

        embed = discord.Embed(title=message, color=0xda0b0b)
        firstfive = result[0:5]
        for x in firstfive:
            message = '<@!' + str(x[1]) + '>:\n  ***' + str(x[2]) + '*** points , ' + str(x[3]) + 'W ' + str(x[4]) + 'L'
            embed.add_field(value=message, name='\u200b', inline=False)
            print()
        return embed

    def GetBotFive(self):
        # message = 'Top 5 Losers is: '
        message = 'The African Child'
        executeString = "SELECT * FROM PlayerProfile ORDER BY Points ASC"
        result = self.CustomOpenPlayerProfile(executeString)

        embed = discord.Embed(title=message, color=0xda0b0b)
        botfive = result[0:5]
        for x in botfive:
            message = '<@!' + str(x[1]) + '>:\n  ***' + str(x[2]) + '*** points, ' + str(x[3]) + 'W ' + str(x[4]) + 'L'
            embed.add_field(value=message, name='\u200b', inline=False)

        return embed

    def GetTopWins(self):
        # message = 'Top 5 Winners is: '
        message = 'The fattest 5'
        executeString = "SELECT * FROM PlayerProfile ORDER BY Wins DESC"
        result = self.CustomOpenPlayerProfile(executeString)

        embed = discord.Embed(title=message, color=0xda0b0b)
        firstfive = result[0:5]
        for x in firstfive:
            message = '<@!' + str(x[1]) + '>:\n  ***' + str(x[2]) + '*** points , ' + str(x[3]) + 'W ' + str(x[4]) + 'L'
            embed.add_field(value=message, name='\u200b', inline=False)
            print()
        return embed

    def GetTopLose(self):
        # message = 'Top 5 Winners is: '
        message = 'The fattest 5'
        executeString = "SELECT * FROM PlayerProfile ORDER BY Lose DESC"
        result = self.CustomOpenPlayerProfile(executeString)

        embed = discord.Embed(title=message, color=0xda0b0b)
        firstfive = result[0:5]
        for x in firstfive:
            message = '<@!' + str(x[1]) + '>:\n  ***' + str(x[2]) + '*** points , ' + str(x[3]) + 'W ' + str(x[4]) + 'L'
            embed.add_field(value=message, name='\u200b', inline=False)
            print()
        return embed

    def Leaderboard(self):
        EachPageNumber = 6
        title = 'Leaderboard'
        executeString = "SELECT * FROM PlayerProfile ORDER BY Points DESC"
        result = self.CustomOpenPlayerProfile(executeString)
        embed = discord.Embed(title=title, color=0xda0b0b)
        # embedlist=['a','b','c','d','e','f','g','h','i','j']
        embedList = []
        for x in range(0, len(result), EachPageNumber):
            print('x ' + str(x))
            embed = discord.Embed(title=title, color=0xda0b0b)
            for y in range(0, EachPageNumber):
                try:
                    # print('y ' + str(y))
                    # print('xy ' + str(x + y))
                    print(result[x + y])
                    message = '<@!' + str(result[x + y][1]) + '>:\n  ***' + str(
                        result[x + y][2]) + '*** points, ' + str(result[x + y][3]) + 'W ' + str(
                        result[x + y][4]) + 'L'
                    embed.add_field(value=message, name='\u200b', inline=False)
                except:
                    print('error')
                #
            embedList.append(embed)
            # print('loops: '+ embedlist[x]+' '+ embedlist[x+1]+ ' '+embedlist[x+2])
            # print(embedlist[x])
        return embedList
