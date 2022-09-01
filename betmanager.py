import discord
import sqlite3
from playerprofile import playerprofile


class betmanager:

    def __init__(self):
        print('Preparing')
        self.BetExists = False
        self.DireBetters = []
        self.RadiantBetters = []
        self.titleMessage = 0
        self.betUserMessage = 0
        self.TotalPoints = 0
        self.CreateDatabases()
        # Each Player list (id , Dire/Radiant, AmountBet)

    def CreateDatabases(self):
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS SessionTable (id integer PRIMARY KEY AUTOINCREMENT , 
            SessionID INT(50) , TitleMsgID, BetMsgID )''')
        con.commit()
        con.close()

        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS OngoingBetters (id integer PRIMARY KEY AUTOINCREMENT , DiscordID , 
             Side, Amount, SessionID INT(50) )''')
        con.commit()
        con.close()

    def OpenDBOngoingBetters(self, discordID):
        print('OpenDB')
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM OngoingBetters WHERE DiscordID ="' + str(discordID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        con.close()
        return result

    def CustomOpenDBOngoingBetters(self, message):
        print('OpenDB')
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        # executeString = 'SELECT * FROM OngoingBetters WHERE DiscordID ="' + str(discordID) + '"'
        cur.execute(message)
        result = cur.fetchall()
        con.close()
        return result

    # For Inserting and Deleting
    def UpdateDBOngoingBetters(self, discordID, message, data_tuple):
        print('UpdateDB')
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM OngoingBetters WHERE DiscordID ="' + str(discordID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        cur.execute(message, data_tuple)
        con.commit()
        con.close()
        return

    def GetBetExists(self):
        return self.BetExists

    def splitTitles(self, LongString):
        LongStringSplit = LongString.split()
        Title = LongStringSplit[0]
        # print(first_word)
        LongStringSplit.remove(Title)
        return Title, LongStringSplit

    def DireRadConvertor(self, message):
        direlist = ['dire', 'd']
        radiantlist = ['radiant', 'rad', 'r']
        if (any(x == message for x in direlist)):
            DireChoice = 'dire'
            return DireChoice
        elif (any(x == message for x in radiantlist)):
            RadChoice = 'radiant'
            return RadChoice
        else:
            notChoice = 'Not chosen'
            return notChoice

        # if (any(x == RadiantSide.lower() for x in radiantlist)):

    def StartBetSession(self, SessionID, RadiantSide, DireSide):
        self.CleanDatabaseSession(1)
        self.BetExists = True
        embedTitle = 'Bet Session ' + str(SessionID)
        embed = discord.Embed(title=embedTitle, color=0xff00ae)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/979033486340010015/1013430920935641148/871366.png")
        RadiantTeam, RadComposition = self.splitTitles(RadiantSide)
        RadDisplay = '[' + str(RadiantTeam) + ']\n' + ' '.join(RadComposition)
        embed.add_field(name="Radiant", value=RadDisplay, inline=True)
        DireTeam, DireComposition = self.splitTitles(DireSide)
        DireDisplay = '[' + str(DireTeam) + ']\n' + ' '.join(DireComposition)
        # embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name="Dire", value=DireDisplay, inline=True)

        bettersembed = discord.Embed(title="Betters ", color=0xff00ae)
        bettersembed.add_field(name="Radiant Betters", value='\u200b', inline=True)
        bettersembed.add_field(name="Dire Betters", value='\u200b', inline=True)

        return embed, bettersembed

    def OpenSessionTable(self, SessionID):
        print('OpenDB')
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM SessionTable WHERE SessionID ="' + str(SessionID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        con.close()
        return result

    def UpdateSessionTable(self, message):
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        # executeString = 'SELECT * FROM SessionTable WHERE SessionID ="' + str(SessionID) + '"'
        cur.execute(message)
        # result = cur.fetchall()
        con.commit()
        con.close()
        return

    def UpdateSessionTableTuple(self, message, data_tuple):
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        cur.execute(message, data_tuple)
        con.commit()
        con.close()
        return

    def CheckSessionExists(self,SessionID):
        result = self.OpenSessionTable(SessionID)
        if len(result) == 0:
            return False
        else:
            return True

    def TestUpdate(self):
        updateHistory = '''INSERT INTO SessionTable ( SessionID ,TitleMsgID,BetMsgID) VALUES(?,?,?)'''
        data_tuple = (1, 3123123, 1312314)
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        # executeString = 'SELECT * FROM OngoingBetters WHERE DiscordID ="' + str(discordID) + '"'
        # cur.execute(executeString)
        result = cur.fetchall()
        cur.execute(updateHistory, data_tuple)
        con.commit()
        con.close()

    def InsertSessionTable(self, SessionID, TitleMsgID, BetMsgID):
        updateHistory = '''INSERT INTO SessionTable ( SessionID ,TitleMsgID,BetMsgID) VALUES(?,?,?)'''
        data_tuple = (SessionID, TitleMsgID, BetMsgID)
        self.UpdateSessionTableTuple(updateHistory, data_tuple)
        return

    # OngoingBetters
    def SetTitleBetMessage(self, SessionID, message):
        self.titleMessage = message

    def GetTitleBetMessage(self):
        return self.titleMessage

    def SetBetUserMessage(self, SessionID, message):
        self.betUserMessage = message

    def GetBetUserMessage(self,SessionID):
        executeString = 'SELECT * FROM SessionTable WHERE SessionID ="' + str(SessionID) + '"'
        result = self.CustomOpenDBOngoingBetters(executeString)
        if len(result) == 0:
            return 0
        else:
            return result[0][3]

    def CountTotalPointsBetted(self, SessionID):
        executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '"'
        result = self.CustomOpenDBOngoingBetters(executeString)
        if len(result) == 0:
            print('No Value cuz no ppl Bet')
        else:
            TempTotalPoints = 0
            for x in result:
                TempTotalPoints = TempTotalPoints + int(x[3])

            self.TotalPoints = TempTotalPoints
        return

    def GetTotalPointsBetted(self):
        return self.TotalPoints

    def LoadBetters(self,SessionID):
        print('Load Bet n Update')
        # Load Radiant and put in list
        RadexecuteString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '" and Side="radiant"'
        self.RadiantBetters = self.CustomOpenDBOngoingBetters(RadexecuteString)
        # Load Dire and put in list
        DireexecuteString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '" and Side="dire"'
        self.DireBetters = self.CustomOpenDBOngoingBetters(DireexecuteString)

        print(self.RadiantBetters)
        print(self.DireBetters)
        RBetString = '-'
        DBetString = '-'
        for x in self.RadiantBetters:
            # RBetString = str(RBetString) + ' ' + str(x[])
            RBetString = RBetString + '<@!' + str(x[1]) + '>: ' + str(x[3]) + ' points\n-'
            # print(' ' + str(x[0]) + ' ' + str(x[1]) + ' ' + str(x[2]) + ' ' + str(x[3]) + ' ' + str(x[4]))
        for x in self.DireBetters:
            # RBetString = str(RBetString) + ' ' + str(x[])
            DBetString = DBetString + '<@!' + str(x[1]) + '>: ' + str(x[3]) + ' points\n-'
            # print(' ' + str(x[0]) + ' ' + str(x[1]) + ' ' + str(x[2]) + ' ' + str(x[3]) + ' ' + str(x[4]))
        # Return
        self.CountTotalPointsBetted(SessionID)
        # print(RBetString)
        # print(DBetString)
        # embedVar = discord.Embed(title="Current Q: " + str(len(self.ParticipantDict)) + '/' + str(self.QueLimit),
        # description='Press the reaction to join ', color=0x00ff00)
        descMsg = '' + str(self.TotalPoints) + ' Points Total'
        bettersembed = discord.Embed(title="Betters ", description=descMsg, color=0xff00ae)
        bettersembed.add_field(name="Radiant Betters", value=RBetString, inline=True)
        bettersembed.add_field(name='Dire Betters', value=DBetString, inline=True)
        # bettersembed.add_field(name="Dire Betters", value='\u200b', inline=True)
        return bettersembed

    def AddUser(self, discordID,SessionID, Side, AmountBet):
        executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '" and DiscordID ="'+str(discordID)+'"'
        result = self.CustomOpenDBOngoingBetters(executeString)
        if len(result) == 0:
            InsertMessage = '''INSERT INTO OngoingBetters ( DiscordID, SessionID ,Side,Amount) VALUES(?,?,?,?)'''
            data_tuple = (str(discordID), str(SessionID), str(Side), str(AmountBet))
            self.UpdateDBOngoingBetters(discordID, InsertMessage, data_tuple)

            embedVar = self.LoadBetters(SessionID)
            return embedVar
        else:
            print('No add cuz exists')

    def AddDireBetters(self, discordID, Side, AmountBet):
        DataTuple = (discordID, Side, AmountBet)
        self.DireBetters.append(DataTuple)
        print('Added to Dire List')

    def AddRadBetters(self, discordID, Side, AmountBet):
        DataTuple = (discordID, Side, AmountBet)
        self.RadiantBetters.append(DataTuple)
        print('Added to Radiant List')

    def UpdateBettedUsers(self):
        print('Updating')
        # self.betUserMessage

    def CheckUserinBet(self, discordID):
        print('Finding if duplicate')

        result = self.OpenDBOngoingBetters(discordID)
        if len(result) == 0:
            return True
        else:
            return False

    def CleanDatabaseSession(self, SessionID):
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        if len(result) == 0:
            message = 'nothing to delete'
        else:
            print('deleting')
            updatestring = 'DELETE FROM OngoingBetters WHERE SessionID = "' + str(SessionID) + '"'
            cur.execute(updatestring)
            con.commit()

            message = 'Deleted Sessions from Database'
        con.close()
        print(message)


        # embed = discord.Embed(description=message, color=0xda0b0b)
        # return embed
        return

    def EndBetSession(self):
        print("Ending")

    def CancelBetSession(self):
        print('Cancelling n refunding')
