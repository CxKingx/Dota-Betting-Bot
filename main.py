import os
import discord
import asyncio
# import datetime,timedelta
from datetime import datetime, timedelta
# import pytz
# import time
from discord import reaction, message
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions, check

from betmanager import betmanager
from playerprofile import playerprofile

my_secret = os.environ['DISCORD_TOKEN']
bot = commands.Bot(command_prefix='*', intents=discord.Intents.all())

# Initialize the Important Variables
dbObject = playerprofile()
betObject = betmanager()


@bot.event
async def on_ready():
    print('We have logged in as  {0.user}'.format(bot))
    # Load Relevant Database # User and Points
    # Activity Save File
    CheckPeriodically.start()


@bot.command(name='test', help='Register Your Name in the Database to be able to bet')
async def test(ctx):
    mylist = "Alliance TA Tide Dazzle Centa Jug"
    all_words = mylist.split()
    first_word = all_words[0]
    print(first_word)
    all_words.remove(all_words[0])
    print(all_words)
    deez = await ctx.send(ctx.message.id)
    await ctx.send(deez.id)
    # betObject.TestUpdate()

    # msg = await ctx.fetch_message(1014895020882526320)
    # await msg.edit(content='buhbhe')
    thischannel = ctx.channel
    Bet_Starter = ctx.author
    # today = datetime.datetime.today()  # 22:20
    # MaxTimeRemove = today + timedelta(minutes=30)  # 22:45
    # await ctx.send(datetime.now())
    guild = bot.get_guild(683840883699089433)
    print(guild)
    channel = guild.get_channel(847409872324657153)
    print(channel)
    message = await channel.fetch_message(1019946780739252326)
    print(message)
    embedVar = discord.Embed(title="Current Q:",
                             description='Press the reaction to join ', color=0x00ff00)
    await message.edit(embed=embedVar)


# Guild = 683840883699089433 Channel 847409872324657153 msg at 1019936538760581172

@bot.command(name='signup', help='Register Your Name in the Database to be able to bet')
async def signup(ctx):
    print('Registering This Person')  # Take Discord ID , give Starting Points
    embedVar = dbObject.Register(ctx.author.id)
    await ctx.send(embed=embedVar)


@bot.command(name='deleteuser', help='Delete User')
async def deleteuser(ctx, user: discord.Member = None):
    if user:
        embedVar = dbObject.deleteUser(user.id)
        await ctx.send(embed=embedVar)
    else:  # not mention get self
        await ctx.send('No user to delete')


@bot.command(name='profile', help='Look at your profile ')
async def profile(ctx, user: discord.Member = None):
    if user:
        embedVar = dbObject.GetPlayerProfile(user.id)
        await ctx.send(embed=embedVar)
    else:  # not mention get self
        embedVar2 = dbObject.GetPlayerProfile(ctx.author.id)
        await ctx.send(embed=embedVar2)


@bot.command(name='addPoints', help='Add Points to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def addPoints(ctx, amount, user: discord.Member = None):
    print('addPoints')
    if user:
        if amount:
            embedVar = dbObject.AddPoints(user.id, int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')


@addPoints.error
async def addPoints_error(ctx, error):
    print('addPoints_error')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission to add Points <:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


@bot.command(name='reducePoints', help='Reduce Points to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def reducePoints(ctx, amount, user: discord.Member = None):
    print('reducePoints')
    if user:
        if amount:
            embedVar = dbObject.ReducePoints(user.id, int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')


@reducePoints.error
async def reducePoints_error(ctx, error):
    print('reducePoints_error ')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission to Reduce Points <:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


@bot.command(name='addWins', help='Add Wins to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def addWins(ctx, amount, user: discord.Member = None):
    print('addWins')
    if user:
        if amount:
            embedVar = dbObject.AddWins(user.id, int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')


@addWins.error
async def addWins_error(ctx, error):
    print('addWins_error ')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission to add Wins <:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


@bot.command(name='reduceWins', help='Reduce Wins to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def reduceWins(ctx, amount, user: discord.Member = None):
    print('reduceWins')
    if user:
        if amount:
            embedVar = dbObject.ReduceWins(user.id, int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')


@reduceWins.error
async def reduceWins_error(ctx, error):
    print('reduceWins_error ')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission to reduce Wins <:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


@bot.command(name='addLosses', help='Add Losses to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def addLosses(ctx, amount, user: discord.Member = None):
    print('addLosses')
    if user:
        if amount:
            embedVar = dbObject.AddLosses(user.id, int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')


@addLosses.error
async def addLosses_error(ctx, error):
    print('addLosses_error ')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission to add Losses <:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


@bot.command(name='reduceLosses', help='Reduce Losses to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def reduceLosses(ctx, amount, user: discord.Member = None):
    print('reduceLosses')
    if user:
        if amount:
            embedVar = dbObject.ReduceLosses(user.id, int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')


@reduceLosses.error
async def reduceLosses_error(ctx, error):
    print('reduceLosses_error')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission to reduce Losses <:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


# Inputs
@bot.command(name='bet', help='Bet in a ongoing game')
async def bet(ctx):
    thischannel = ctx.channel
    Bet_author = ctx.author
    msg_list = []

    def SessionReply(m):
        return m.channel == thischannel and m.author == Bet_author

    def SideReply(m):
        return m.channel == thischannel and m.author == Bet_author

    def AmountReply(m):
        return m.channel == thischannel and m.author == Bet_author

    userexists = dbObject.CheckUserExists(ctx.author.id)
    if userexists:
        CurrentMoney = dbObject.GetUserMoney(ctx.author.id)

        # Check Bet if Online
        SessionAsk = await ctx.send('Please Specify Session Number')
        msg_list.append(SessionAsk)
        try:
            Session_msg = await bot.wait_for('message', timeout=30, check=SessionReply)
            if SessionAsk:
                if betObject.CheckSessionExists(Session_msg.content):
                    msg_list.append(Session_msg)
                else:
                    await ctx.send('No Bet Session Exists')
                    return
                # await ctx.send(str(Radiant_msg.content))

        except asyncio.TimeoutError:
            await ctx.send('too long, try again')
            return

        if betObject.CheckUserinBet(ctx.author.id, Session_msg.content):
            await ctx.send('You Have Betted in this match')
            return

        if betObject.CheckSessionOpen(Session_msg.content):
            await ctx.send('Session is not available / Closed')
            return

        BetQuestion = await ctx.send('Your funds is: ' + str(CurrentMoney) + '\nPlease Give Amount for Bet')
        msg_list.append(BetQuestion)
        try:
            Amount_msg = await bot.wait_for('message', timeout=30, check=AmountReply)
            if AmountReply:
                try:
                    if isinstance(int(Amount_msg.content), int):
                        msg_list.append(Amount_msg)
                        if dbObject.CheckBetableStatus(ctx.author.id, int(Amount_msg.content)):
                            AmountSufficientMsg = await ctx.send('Next Step')
                            msg_list.append(AmountSufficientMsg)
                        else:
                            await ctx.send('Not enough points to bet')
                            return
                except:
                    await ctx.send('Invalid Input')
                    return
            else:
                await ctx.send('Invalid Input')
        except asyncio.TimeoutError:
            await ctx.send('too long, try again')
            return

        SideQuestion = await ctx.send('Please Pick a side Radiant/Dire')
        msg_list.append(SideQuestion)
        TranslatedMessage = ''
        try:
            Side_msg = await bot.wait_for('message', timeout=30, check=SideReply)
            if SideReply:
                msg_list.append(Side_msg)
                TranslatedMessage = betObject.DireRadConvertor(Side_msg.content.lower())
                if TranslatedMessage == 'dire' or TranslatedMessage == 'radiant':
                    BetProcessMsg = await ctx.send('Processing Bet (Not actually up yet)')
                    msg_list.append(BetProcessMsg)
                else:
                    await ctx.send('Invalid choice, please choose \'radiant\' or \'dire\' ')
                    return

        except asyncio.TimeoutError:
            await ctx.send('too long, try again')
            return

        for x in msg_list:
            await x.delete()
        print('done')

        betMsgObjectID = betObject.GetBetUserMessage(Session_msg.content)
        # betMsgObject = await ctx.fetch_message(betMsgObjectID)
        if betMsgObjectID == 0:
            await ctx.send('0 Result')
        else:

            guild = bot.get_guild(int(betMsgObjectID[6]))
            channel = guild.get_channel(int(betMsgObjectID[7]))
            betMsgObject = await channel.fetch_message(int(betMsgObjectID[3]))
            # await message.edit(embed=betMsgObjectID[1])

            embedVar = betObject.AddUser(ctx.author.id, Session_msg.content, TranslatedMessage, Amount_msg.content)
            await betMsgObject.edit(embed=embedVar)

            Title = str('You have betted **' + Amount_msg.content + '** for **' + str(TranslatedMessage) + '** side')
            await ctx.send(Title)

    else:
        await ctx.send('No Account Registered , use *signup')
        return

    # Check if Bet is Online
    # Yes Continue
    # Check if User has Existed in the Database
    # If Registered
    # Check the player remaining points, if it is sufficient to bet
    # If  Sufficient
    # Start Managing the Bet
    # Else Not Sufficient
    # You have no more Bet Points , Please bet with a smaller value
    # Else not Registered
    # You have not sign up for us, please use signup

    # Else No Bets are Ongoing
    # print('No Bets are ongoing right now
    # No Display Error Message


# @bet.error
# async def bet_error(ctx, error):
#     print('bet_error')
#     if isinstance(error, commands.MissingAnyRole):
#         await ctx.send("You don't have permission<:kizunaai:683869090204614658>.")
#     else:
#         await ctx.send("something went wrong")
#

@bot.command(name='cancelbet', help='Bet in a ongoing game , Default bet is 20 points')
async def cancelbet(ctx):
    thischannel = ctx.channel
    Bet_Starter = ctx.author
    msg_list = []
    msg_list.append(ctx.message)

    def session(m):
        return m.channel == thischannel and m.author == Bet_Starter

    SessionAsk = await ctx.send('Please Specify Session Number to remove your bet')
    msg_list.append(SessionAsk)
    try:
        Session_msg = await bot.wait_for('message', timeout=30, check=session)
        if Session_msg:
            if betObject.CheckSessionExists(Session_msg.content):
                msg_list.append(Session_msg)

            else:
                await ctx.send('Bet Session Does not Exists')
                return

        else:
            await ctx.send('Invalid Input')
    except asyncio.TimeoutError:
        await ctx.send('too long, try again')
        return

    if betObject.CheckSessionOpen(Session_msg.content):
        await ctx.send('Session is not available / Closed')
        return

    betMsgObjectID = betObject.GetBetUserMessage(Session_msg.content)
    #betMsgObject = await ctx.fetch_message(betMsgObjectID)
    guild = bot.get_guild(int(betMsgObjectID[6]))
    channel = guild.get_channel(int(betMsgObjectID[7]))
    betMsgObject = await channel.fetch_message(int(betMsgObjectID[3]))

    embedVar, Status = betObject.RemoveUser(ctx.author.id, Session_msg.content)
    await betMsgObject.edit(embed=embedVar)
    if Status:
        await ctx.send('You Have been removed from bet')
    else:
        await ctx.send('You have not bet in this session')


@tasks.loop(minutes=1)
async def CheckPeriodically():
    print('checkin')
    embedlist = betObject.SessionTimerClose()
    if len(embedlist) == 0:
        return
    else:
        for x in embedlist:
            guild = bot.get_guild(int(x[2]))
            channel = guild.get_channel(int(x[3]))
            message = await channel.fetch_message(int(x[0]))
            await message.edit(embed=x[1])


# Inputs
@bot.command(name='startSession', help='Start Betting Session 1')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
# async def startSession(ctx , radiant , dire ):
async def startSession(ctx):
    thischannel = ctx.channel
    Bet_Starter = ctx.author
    msg_list = []
    msg_list.append(ctx.message)

    # print(msg_list)
    def radiant(m):
        return m.channel == thischannel and m.author == Bet_Starter

    def dire(m):
        return m.channel == thischannel and m.author == Bet_Starter

    def session(m):
        return m.channel == thischannel and m.author == Bet_Starter

    SessionAsk = await ctx.send('Please Specify Session Number')
    msg_list.append(SessionAsk)
    try:
        Session_msg = await bot.wait_for('message', timeout=30, check=session)
        if Session_msg:
            if betObject.CheckSessionExists(Session_msg.content):
                await ctx.send('Bet Session Exists')
                return
            else:
                # await ctx.send(str(Radiant_msg.content))
                msg_list.append(Session_msg)
        else:
            await ctx.send('Invalid Input')
    except asyncio.TimeoutError:
        await ctx.send('too long, try again')
        return
    # await ctx.send('Please Specify Session ID

    reply1 = await ctx.send('Please Specify Radiant Side. Format : TeamName hero hero hero hero hero')
    msg_list.append(reply1)
    try:
        Radiant_msg = await bot.wait_for('message', timeout=30, check=radiant)
        if Radiant_msg:
            # await ctx.send(str(Radiant_msg.content))
            msg_list.append(Radiant_msg)
    except asyncio.TimeoutError:
        await ctx.send('too long, try again')
        return

    reply2 = await ctx.send('Please Specify Dire Side. Format : TeamName hero hero hero hero hero')
    msg_list.append(reply2)
    try:
        Dire_msg = await bot.wait_for('message', timeout=30, check=dire)
        if Dire_msg:
            # await ctx.send(str(Dire_msg.content))
            msg_list.append(Dire_msg)
    except asyncio.TimeoutError:
        await ctx.send('too long, try again')
        return

    Title = str('Session Number ' + str(
        Session_msg.content) + '\nRadiant Side = ' + Radiant_msg.content + '\nVS\nDire Side = ' + str(Dire_msg.content))
    await ctx.send(Title)

    for x in msg_list:
        await x.delete()
    print('done')

    embedBet, embedBetters = betObject.StartBetSession(Session_msg.content, Radiant_msg.content, Dire_msg.content)
    TitleBetMessage = await ctx.send(embed=embedBet)
    # betObject.SetTitleBetMessage(Session_msg, TitleBetMessage.id)
    BettersMessage = await ctx.send(embed=embedBetters)

    # betObject.SetBetUserMessage(Session_msg, BettersMessage.id)
    today = datetime.now()  # 22:20
    MaxTimeRemove = today + timedelta(minutes=15)  # 22:45
    # ctx.message.guild.id ctx.message.channel.id
    betObject.InsertSessionTable(Session_msg.content, TitleBetMessage.id, BettersMessage.id, MaxTimeRemove,
                                 ctx.message.guild.id, ctx.message.channel.id)
    # UpdateStatusEmbed = betObject.LoadBetters(Session_msg.content)
    # await BettersMessage.edit(embed=UpdateStatusEmbed)


# @startbet.error
# async def startbet_error(ctx, error):
#     print('startbet_error')
#     if isinstance(error, commands.MissingAnyRole):
#         await ctx.send("You don't have permission <:kizunaai:683869090204614658>.")
#     else:
#         await ctx.send("something went wrong")

@bot.command(name='cancelSession', help='cancel Betting Session')
@commands.has_any_role('MOD', 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def cancelSession(ctx):
    # Delete Message
    thischannel = ctx.channel
    Bet_Starter = ctx.author
    msg_list = []
    msg_list.append(ctx.message)

    def session(m):
        return m.channel == thischannel and m.author == Bet_Starter

    SessionAsk = await ctx.send('Please Specify Session Number to End')
    msg_list.append(SessionAsk)
    try:
        Session_msg = await bot.wait_for('message', timeout=30, check=session)
        if Session_msg:
            if betObject.CheckSessionExists(Session_msg.content):
                msg_list.append(Session_msg)

            else:
                await ctx.send('Bet Session Does not Exists')
                return

        else:
            await ctx.send('Invalid Input')
    except asyncio.TimeoutError:
        await ctx.send('too long, try again')
        return

    for x in msg_list:
        await x.delete()

    betObject.CancelBetSession(ctx.author.id, Session_msg.content)
    message = "Bet " + Session_msg.content + " is Cancelled "
    CancelEmbed = discord.Embed(title=message, description='Player Funds have been refunded', color=0xff00ae)
    await ctx.send(embed=CancelEmbed)


@bot.command(name='endSession', help='end Betting Session 1')
@commands.has_any_role('MOD', 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def endSession(ctx):
    thischannel = ctx.channel
    Bet_Starter = ctx.author
    msg_list = []
    msg_list.append(ctx.message)

    def SideReply(m):
        return m.channel == thischannel and m.author == Bet_Starter

    def session(m):
        return m.channel == thischannel and m.author == Bet_Starter

    SessionAsk = await ctx.send('Please Specify Session Number to End')
    msg_list.append(SessionAsk)
    try:
        Session_msg = await bot.wait_for('message', timeout=30, check=session)
        if Session_msg:
            if betObject.CheckSessionExists(Session_msg.content):
                msg_list.append(Session_msg)

            else:
                await ctx.send('Bet Session Does not Exists')
                return

        else:
            await ctx.send('Invalid Input')
    except asyncio.TimeoutError:
        await ctx.send('too long, try again')
        return

    SideQuestion = await ctx.send('Please Choose which side won Radiant/Dire')
    msg_list.append(SideQuestion)
    TranslatedMessage = ''
    try:
        Side_msg = await bot.wait_for('message', timeout=30, check=SideReply)
        if SideReply:
            msg_list.append(Side_msg)
            TranslatedMessage = betObject.DireRadConvertor(Side_msg.content.lower())
            if TranslatedMessage == 'dire' or TranslatedMessage == 'radiant':
                BetProcessMsg = await ctx.send('Processing Bet')
                msg_list.append(BetProcessMsg)
            else:
                await ctx.send('Invalid choice, please choose \'radiant\' or \'dire\' ')
                return

    except asyncio.TimeoutError:
        await ctx.send('too long, try again')
        return

    for x in msg_list:
        await x.delete()

    WinProcessMsg = 'Ending Session ' + Session_msg.content + ' with ' + TranslatedMessage + ' as winners'
    WinEmbed = discord.Embed(title=WinProcessMsg, description='\u200b', color=0xff00ae)
    await ctx.send(embed=WinEmbed)

    embedVar = betObject.EndBetSession(Session_msg.content, Side_msg.content)
    if len(embedVar) == 0:
        await ctx.send('No Winners')
    elif len(embedVar) > 0:
        for x in embedVar:
            await ctx.send(embed=x)

    # await ctx.send(embed=embedVar)

@bot.command(name='activeSession', help='end Betting Session 1')
async def activeSession(ctx):
    embedVar = d


@bot.command(name='top', help='end Betting Session 1')
async def top5(ctx):
    embedVar = dbObject.GetTopFive()
    await ctx.send(embed=embedVar)


@top5.error
async def top5_error(ctx, error):
    print('top5_error')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission <:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


@bot.command(name='bot', help='end Betting Session 1')
async def bot5(ctx):
    embedVar = dbObject.GetBotFive()
    await ctx.send(embed=embedVar)


@bot5.error
async def bot5_error(ctx, error):
    print('bot5_error')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission<:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


@bot.command(name='topwin', help='end Betting Session 1')
async def topwins(ctx):
    embedVar = dbObject.GetTopWins()
    await ctx.send(embed=embedVar)


@topwins.error
async def topwins_error(ctx, error):
    print('topwins_error')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission to reduce Losses <:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


@bot.command(name='toplose', help='end Betting Session 1')
async def toplose(ctx):
    embedVar = dbObject.GetTopLose()
    await ctx.send(embed=embedVar)


@toplose.error
async def toplose_error(ctx, error):
    print('toplose_error')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission to reduce Losses <:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


@bot.command(name='leaderboard', help='end Betting Session 1')
async def Leaderboard(ctx):
    embedVar = dbObject.Leaderboard()
    for x in embedVar:
        await ctx.send(embed=x)


@Leaderboard.error
async def Leaderboard_error(ctx, error):
    print('Leaderboard_error')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission<:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)

    split_message = user_message.split()
    channel = str(message.channel.name)
    channelID = str(message.channel.id)
    # channel_nsfw = message.channel.is_nsfw()
    print(f'{username}: {user_message} ({channel}) (ID: {channelID})')

    # Dont Delete This
    await bot.process_commands(message)


bot.run(my_secret)
