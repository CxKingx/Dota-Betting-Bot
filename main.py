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


@bot.command(name='test', help='Register Your Name in the Database to be able to bet')
async def test(ctx):
    mylist = "Alliance TA Tide Dazzle Centa Jug"
    all_words = mylist.split()
    first_word = all_words[0]
    print(first_word)
    all_words.remove(all_words[0])
    print(all_words)


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
@bot.command(name='bet', help='Bet in a ongoing game , Default bet is 20 points')
async def bet(ctx):
    # amount = 2
    # await ctx.send(str(amount))
    # await ctx.send(str(-amount))
    thischannel = ctx.channel
    Bet_author = ctx.author
    msg_list = []

    def SideReply(m):
        return m.channel == thischannel and m.author == Bet_author and isinstance(m.content, str)

    def AmountReply(m):
        return m.channel == thischannel and m.author == Bet_author and isinstance(int(m.content), int)

    userexists = dbObject.CheckUserExists(ctx.author.id)
    if userexists:
        CurrentMoney = dbObject.GetUserMoney(ctx.author.id)

        # Check Bet if Online
        if betObject.GetBetExists():

            BetQuestion = await ctx.send('Your funds is: ' + str(CurrentMoney) + '\nPlease Give Amount for Bet')
            msg_list.append(BetQuestion)
            try:
                Amount_msg = await bot.wait_for('message', timeout=30, check=AmountReply)
                if AmountReply:
                    msg_list.append(Amount_msg)
                    if dbObject.CheckBetableStatus(ctx.author.id, int(Amount_msg.content)):
                        AmountSufficientMsg = await ctx.send('Next Step')
                        msg_list.append(AmountSufficientMsg)
                    else:
                        await ctx.send('Not enough points to bet')
                        return

            except asyncio.TimeoutError:
                await ctx.send('too long, try again')
                return

            SideQuestion = await ctx.send('Please Pick a side Radiant/Dire')
            msg_list.append(SideQuestion)
            try:
                Side_msg = await bot.wait_for('message', timeout=30, check=SideReply)
                if SideReply:
                    msg_list.append(Side_msg)
                    if Side_msg.content.lower() == 'dire' or Side_msg.content.lower() == 'radiant':
                        BetProcessMsg = await ctx.send('Processing Bet (Not actually up yet)')
                        msg_list.append(BetProcessMsg)
                    else:
                        await ctx.send('Invalid choice, please choose \'radiant\' or \'dire\' ')
                        return

            except asyncio.TimeoutError:
                await ctx.send('too long, try again')
                return

            Title = str('You have betted **' + Amount_msg.content + '** for **' + str(Side_msg.content) + '** side')
            await ctx.send(Title)

            for x in msg_list:
                await x.delete()
            print('done')
        else:
            await ctx.send('No Bet Session is Ongoing')
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


@bet.error
async def bet_error(ctx, error):
    print('bet_error')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission<:kizunaai:683869090204614658>.")
    else:
        await ctx.send("something went wrong")


# Inputs
@bot.command(name='startbet', help='Start Betting Session 1')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
# async def startbet(ctx , radiant , dire ):
async def startbet(ctx):
    thischannel = ctx.channel
    Bet_Starter = ctx.author
    msg_list = []
    msg_list.append(ctx.message)

    # print(msg_list)
    def radiant(m):
        return m.channel == thischannel and m.author == Bet_Starter

    def dire(m):
        return m.channel == thischannel and m.author == Bet_Starter

    reply1 = await ctx.send('Please Specify Radiant Side')
    msg_list.append(reply1)
    try:
        Radiant_msg = await bot.wait_for('message', timeout=30, check=radiant)
        if Radiant_msg:
            # await ctx.send(str(Radiant_msg.content))
            msg_list.append(Radiant_msg)
    except asyncio.TimeoutError:
        await ctx.send('too long, try again')
        return

    reply2 = await ctx.send('Please Specify Dire Side')
    msg_list.append(reply2)
    try:
        Dire_msg = await bot.wait_for('message', timeout=30, check=dire)
        if Dire_msg:
            # await ctx.send(str(Dire_msg.content))
            msg_list.append(Dire_msg)
    except asyncio.TimeoutError:
        await ctx.send('too long, try again')
        return

    Title = str('Radiant Side = ' + Radiant_msg.content + '\nVS\nDire Side = ' + str(Dire_msg.content))
    await ctx.send(Title)

    for x in msg_list:
        await x.delete()
    print('done')

    embedBet = betObject.StartBetSession(Radiant_msg.content, Dire_msg.content)
    await ctx.send(embed=embedBet)
    # Setup Embed Message
    # Send Title to Bet Function Class
    # Let that function setup the things time limited to bet , setup the temp cache for ppl storage
    # Bet Status = True
    # Get Embed message from them
    # await ctx.send(embed = embed)


# @startbet.error
# async def startbet_error(ctx, error):
#     print('startbet_error')
#     if isinstance(error, commands.MissingAnyRole):
#         await ctx.send("You don't have permission <:kizunaai:683869090204614658>.")
#     else:
#         await ctx.send("something went wrong")

@bot.command(name='cancelbet', help='cancel Betting Session 1')
@commands.has_any_role('MOD', 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def cancelbet(ctx):
    # Delete Message
    await ctx.channel.send('Cancelling Bet Session')
    await ctx.channel.send('a')


@bot.command(name='endbet', help='end Betting Session 1')
@commands.has_any_role('MOD', 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def endbet(ctx):
    # Delete Message
    await ctx.channel.send('Ending Bet Session')
    await ctx.channel.send('a')


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
