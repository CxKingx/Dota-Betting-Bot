import datetime

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
        self.dbObject = playerprofile()
        # Each Player list (id , Dire/Radiant, AmountBet)

    def CreateDatabases(self):
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS SessionTable (id integer PRIMARY KEY AUTOINCREMENT , 
            SessionID INT(50) , TitleMsgID, BetMsgID , TimeCreated , Status , GuildID , ChannelID)''')
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

    def UpdateSessionTable(self, message):
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        cur.execute(message)
        con.commit()
        con.close()

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
        embedTitle = 'Bet Session "' + str(SessionID) + '"'
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
        # embedVar = self.LoadBetters(SessionID)
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

    def CheckSessionExists(self, SessionID):
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

    def InsertSessionTable(self, SessionID, TitleMsgID, BetMsgID, TimeCreated, GuildID, ChannelID):
        updateHistory = '''INSERT INTO SessionTable ( SessionID ,TitleMsgID,BetMsgID,TimeCreated, Status, GuildID , ChannelID) VALUES(?,?,?,?,?,?,?)'''
        data_tuple = (SessionID, TitleMsgID, BetMsgID, TimeCreated, 'Open', GuildID, ChannelID)
        self.UpdateSessionTableTuple(updateHistory, data_tuple)
        return

    # OngoingBetters
    def SetTitleBetMessage(self, SessionID, message):
        self.titleMessage = message

    def GetTitleBetMessage(self):
        return self.titleMessage

    def SetBetUserMessage(self, SessionID, message):
        self.betUserMessage = message

    def GetBetUserMessage(self, SessionID):
        executeString = 'SELECT * FROM SessionTable WHERE SessionID ="' + str(SessionID) + '"'
        result = self.CustomOpenDBOngoingBetters(executeString)
        if len(result) == 0:
            return 0
        else:
            return result[0]
            # return result[0][3], result[0][6], result[0][7]

    def CountRadiantPoints(self, SessionID):
        executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '" and Side="radiant"'
        result = self.CustomOpenDBOngoingBetters(executeString)
        TempTotalPoints = 0
        if len(result) == 0:
            TempTotalPoints = 1
        else:

            for x in result:
                TempTotalPoints = TempTotalPoints + int(x[3])
        return TempTotalPoints

    def CountDirePoints(self, SessionID):
        executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '" and Side="dire"'
        result = self.CustomOpenDBOngoingBetters(executeString)
        TempTotalPoints = 0
        if len(result) == 0:
            TempTotalPoints = 1
        else:
            for x in result:
                TempTotalPoints = TempTotalPoints + int(x[3])
        return TempTotalPoints

    def CountTotalPointsBetted(self, SessionID):
        executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '"'
        result = self.CustomOpenDBOngoingBetters(executeString)
        TempTotalPoints = 0
        if len(result) == 0:
            print('No Value cuz no ppl Bet')
        else:

            for x in result:
                TempTotalPoints = TempTotalPoints + int(x[3])
        self.TotalPoints = TempTotalPoints
        return TempTotalPoints

    def GetTotalPointsBetted(self):
        return self.TotalPoints

    def LoadBetters(self, SessionID):
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
        RadiantTotalPoints = self.CountRadiantPoints(SessionID)
        DireTotalPoints = self.CountDirePoints(SessionID)
        RatioMsg = ''
        if RadiantTotalPoints > DireTotalPoints:
            RatioMsg = '' + str(round(float(RadiantTotalPoints / DireTotalPoints), 2)) + ' : ' + str(
                round(float(DireTotalPoints / DireTotalPoints), 2))
            # round(float(RadiantTotalPoints / DireTotalPoints), 2)
        else:
            RatioMsg = '' + str(round(float(DireTotalPoints / DireTotalPoints), 2)) + ' : ' + str(
                round(float(DireTotalPoints / RadiantTotalPoints), 2))

        descMsg = 'Radiant ' + str(RadiantTotalPoints) + ' Points and Dire ' + str(
            DireTotalPoints) + ' Points\n' + RatioMsg
        ThisSession = self.OpenSessionTable(SessionID)
        TitleMessage = "Betters " + "Session Status: " + ThisSession[0][5]
        bettersembed = discord.Embed(title=TitleMessage, description=descMsg, color=0xff00ae)
        bettersembed.add_field(name="Radiant Betters", value=RBetString, inline=True)
        bettersembed.add_field(name='Dire Betters', value=DBetString, inline=True)
        # bettersembed.add_field(name="Dire Betters", value='\u200b', inline=True)
        return bettersembed

    def AddUser(self, discordID, SessionID, Side, AmountBet):
        executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '" and DiscordID ="' + str(
            discordID) + '"'
        result = self.CustomOpenDBOngoingBetters(executeString)
        if len(result) == 0:
            InsertMessage = '''INSERT INTO OngoingBetters ( DiscordID, SessionID ,Side,Amount) VALUES(?,?,?,?)'''
            data_tuple = (str(discordID), str(SessionID), str(Side), str(AmountBet))
            self.UpdateDBOngoingBetters(discordID, InsertMessage, data_tuple)

            embedVar = self.LoadBetters(SessionID)

            # Uncomment this when ready
            self.dbObject.ReducePoints(discordID, AmountBet)
            return embedVar
        else:
            print('No add cuz exists')

    def RemoveUser(self, discordID, SessionID):
        executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '" and DiscordID ="' + str(
            discordID) + '"'
        result = self.CustomOpenDBOngoingBetters(executeString)
        if len(result) == 0:
            embedVar = discord.Embed(title="You have not bet in this session", description='\u200b', color=0xff00ae)
            updatestatus = False
        else:
            for user in result:
                self.dbObject.AddPoints(user[1], user[3])
            message = 'DELETE FROM OngoingBetters WHERE SessionID = "' + str(SessionID) + '" and DiscordID ="' + str(
                discordID) + '"'
            self.UpdateSessionTable(message)
            embedVar = self.LoadBetters(SessionID)
            updatestatus = True

        return embedVar, updatestatus

    def CheckUserinBet(self, discordID, SessionID):
        executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '" and DiscordID ="' + str(
            discordID) + '"'
        result = self.CustomOpenDBOngoingBetters(executeString)
        if len(result) == 0:
            return False
        else:
            return True

    def SessionTimerClose(self):
        today = datetime.datetime.today()  # 22:20
        # print(today)
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM SessionTable '
        cur.execute(executeString)
        result = cur.fetchall()
        con.close()
        EmbedUpdate = []
        if len(result) == 0:
            return EmbedUpdate
        else:
            for x in result:
                if today > datetime.datetime.strptime(x[4], '%Y-%m-%d %H:%M:%S.%f'):
                    print('found at Session ID ' + str(x[1]))
                    print('Guild = ' + str(x[6]) + ' Channel ' + str(x[7]) + ' msg at ' + str(x[3]))
                    UpdateString = "UPDATE SessionTable SET Status = 'Closed' WHERE SessionID = '" + str(x[1]) + "'"
                    self.UpdateSessionTable(UpdateString)
                    embedVar = self.LoadBetters(str(x[1]))
                    betmsgID = x[3]
                    datatuple = (betmsgID, embedVar, x[6], x[7])
                    EmbedUpdate.append(datatuple)
        # embedVar = self.LoadBetters(SessionID)

        return EmbedUpdate

    def CheckSessionOpen(self, SessionID):
        result = self.OpenSessionTable(SessionID)
        print(str(result[0][5]))
        if len(result) == 0:
            return True
        else:
            if result[0][5] == 'Open':
                return False
            else:
                return True

    def CleanDatabaseSession(self, SessionID):
        con = sqlite3.connect('OngoingBetters.db')
        cur = con.cursor()
        executeString = 'SELECT * FROM SessionTable WHERE SessionID ="' + str(SessionID) + '"'
        cur.execute(executeString)
        result = cur.fetchall()
        if len(result) == 0:
            message = 'nothing to delete'
        else:
            print('deleting')
            updatestring = 'DELETE FROM OngoingBetters WHERE SessionID = "' + str(SessionID) + '"'
            cur.execute(updatestring)
            con.commit()

            updatestring = 'DELETE FROM SessionTable WHERE SessionID = "' + str(SessionID) + '"'
            cur.execute(updatestring)
            con.commit()

            message = 'Deleted Sessions from Database'
        con.close()
        print(message)

        # embed = discord.Embed(description=message, color=0xda0b0b)
        # return embed
        return

    def WinManager(self, SessionID, Side):
        # Get Side Winners
        RadiantTotalPoints = self.CountRadiantPoints(SessionID)
        DireTotalPoints = self.CountDirePoints(SessionID)
        if Side == 'dire':
            WinRatio = round(float(RadiantTotalPoints / DireTotalPoints), 2)
            executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(
                SessionID) + '" and Side="dire"'
        else:
            WinRatio = (round(float(DireTotalPoints / RadiantTotalPoints), 2))
            executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(
                SessionID) + '" and Side="radiant"'

        Winners = self.CustomOpenDBOngoingBetters(executeString)
        print(Winners)
        for x in Winners:
            # Get Discord ID ,
            TotalWin = int(x[3]) + int(round(float(int(x[3]) * WinRatio), 0))
            self.dbObject.AddPoints(x[1], TotalWin)
        EachPageNumber = 6
        embedList = []
        print('Preparing Who Won List')
        for x in range(0, len(Winners), EachPageNumber):
            print('x ' + str(x))
            titleMsg = 'Session \"' + SessionID + '\" Winners'
            embed = discord.Embed(title=titleMsg, color=0xda0b0b)
            for y in range(0, EachPageNumber):
                try:
                    # print('y ' + str(y))
                    # print('xy ' + str(x + y))
                    print(Winners[x + y])

                    message = '<@!' + str(Winners[x + y][1]) + '> won ' + str(
                        int(round(float(int(Winners[x + y][3]) * WinRatio), 0))) + 'points '

                    print(message)
                    embed.add_field(value=message, name='\u200b', inline=False)
                except:
                    print('error')
                #
            embedList.append(embed)
            # print('loops: '+ embedlist[x]+' '+ embedlist[x+1]+ ' '+embedlist[x+2])
            # print(embedlist[x])
        print('adding points to winner ')
        print(embedList)
        return embedList

    def EndBetSession(self, SessionID, Side):
        message = "Ending " + SessionID + ' Winner is ' + Side
        WinEmbed = discord.Embed(title="Winner ", description=message, color=0xff00ae)
        embedList = self.WinManager(SessionID, Side)
        self.CleanDatabaseSession(SessionID)
        return embedList

    def CancelBetSession(self, discordID, SessionID):
        print('Cancelling n refunding')
        message = "Bet " + SessionID + " is Cancelled "
        executeString = 'SELECT * FROM OngoingBetters WHERE SessionID ="' + str(SessionID) + '"'

        # CancelEmbed = discord.Embed(title="Winner ", description=message, color=0xff00ae)
        result = self.CustomOpenDBOngoingBetters(executeString)
        if len(result) == 0:
            message = 'nothing to delete'
        else:
            for user in result:
                # print(user[1])
                # print(user[3])
                self.dbObject.AddPoints(user[1], user[3])

        self.CleanDatabaseSession(SessionID)
        return

    def GetOngoingBetSession(self):
        EachPageNumber = 6
        title = "Bet Sessions"
        print("Getting all Bet Session")
        executeString = 'SELECT * FROM SessionTable'
        result = self.CustomOpenDBOngoingBetters(executeString)
        embedList = []
        if len(result) == 0:
            print("No Session")
            embed = discord.Embed(title="No Active Bet Session", color=0xda0b0b)
            return embed
        else:
            print(" Session")
            for x in range(0, len(result), EachPageNumber):
                print('x ' + str(x))
                embed = discord.Embed(title=title, color=0xda0b0b)
                for y in range(0, EachPageNumber):
                    try:
                        # print('y ' + str(y))
                        # print('xy ' + str(x + y))
                        print(result[x + y])
                        message = 'Session "' + str(result[x + y][1]) + '" Status : ' + str(result[x + y][5])
                        embed.add_field(value=message, name='\u200b', inline=False)
                    except:
                        print('error')
                    #
                embedList.append(embed)
                # print('loops: '+ embedlist[x]+' '+ embedlist[x+1]+ ' '+embedlist[x+2])
                # print(embedlist[x])
            return embedList
