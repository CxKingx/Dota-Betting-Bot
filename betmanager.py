import discord
import sqlite3
from playerprofile import playerprofile


class betmanager:

    def __init__(self):
        print('Preparing')
        self.BetExists = False
        self.DireBetters = []
        self.RadiantBetters = []
        # Each Player list (id , Dire/Radiang, AmountBet)

    def GetBetExists(self):
        return self.BetExists

    def splitTitles(self, LongString):
        LongStringSplit = LongString.split()
        Title = LongStringSplit[0]
        # print(first_word)
        LongStringSplit.remove(Title)
        return Title, LongStringSplit

    def DireRadConvertor(self, RadiantSide, DireSide):
        direlist = ['dire', 'd']
        radiantlist =['radiant','rad','r']

        #if (any(x == RadiantSide.lower() for x in radiantlist)):

    def StartBetSession(self, RadiantSide, DireSide):
        self.BetExists = True
        embed = discord.Embed(title="Bet Session", color=0xff00ae)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/979033486340010015/1013430920935641148/871366.png")
        RadiantTeam, RadComposition = self.splitTitles(RadiantSide)
        RadDisplay = '[' + str(RadiantTeam) + ']\n' + ' '.join(RadComposition)
        embed.add_field(name="Radiant", value=RadDisplay, inline=True)
        DireTeam, DireComposition = self.splitTitles(DireSide)
        DireDisplay = '[' + str(DireTeam) + ']\n' + ' '.join(DireComposition)
        # embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name="Dire", value=DireDisplay, inline=True)

        # embed.add_field(name="Radiant Betters", value=str(RadiantSide), inline=True)
        # embed.add_field(name='\u200b', value='\u200b', inline=True)
        # embed.add_field(name="Dire Betters", value=str(DireSide), inline=True)

        return embed

    def AddDireBetters(self, discordID, Side, AmountBet):
        DataTuple = (discordID, Side, AmountBet)
        self.DireBetters.append(DataTuple)
        print('Added to Dire List')

    def AddRadBetters(self, discordID, Side, AmountBet):
        DataTuple = (discordID, Side, AmountBet)
        self.RadiantBetters.append(DataTuple)
        print('Added to Radiant List')

    def CheckUserinBet(self, discordID):
        print('Finding if duplicate')

    def EndBetSession(self):
        print("Ending")

    def CancelBetSession(self):
        print('Cancelling n refunding')
