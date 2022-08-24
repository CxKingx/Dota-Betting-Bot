import os
import discord

# import datetime,timedelta
from datetime import datetime, timedelta
# import pytz
# import time
from discord import reaction
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from playerprofile import playerprofile

my_secret = os.environ['DISCORD_TOKEN']
bot = commands.Bot(command_prefix='*', intents=discord.Intents.all())

# Initialize the Important Variables
DefaultAmount = 15
dbObject = playerprofile()


# Make the Bet Objects
# Class 1 the User Database Storage

# Class 2 the Bet Functions
# await ctx.channel.send('a')
@bot.event
async def on_ready():
    print('We have logged in as  {0.user}'.format(bot))
    # Load Relevant Database # User and Points
    # Activity Save File


@bot.command(name='signup', help='Register Your Name in the Database to be able to bet')
async def signup(ctx):
    # Check if User has Existed in the Database
    # If Registered Message You have been registered, you can bet
    # if Not Register
    print('Registering This Person')  # Take Discord ID , give Starting Points
    embedVar = dbObject.Register(ctx.author.id)
    await ctx.send(embed=embedVar)


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
    if user:
        if amount:
            embedVar = dbObject.AddPoints(user.id,int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

@addPoints.error
async def addPoints_error(ctx, error):
    print('encounter eror')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permission to add Points <:kizunaai:683869090204614658>.")

@bot.command(name='reducePoints', help='Reduce Points to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def reducePoints(ctx, amount, user: discord.Member = None):
    if user:
        if amount:
            embedVar = dbObject.ReducePoints(user.id,int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')


@bot.command(name='addWins', help='Add Wins to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def addWins(ctx, amount, user: discord.Member = None):
    if user:
        if amount:
            embedVar = dbObject.AddWins(user.id,int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')


@bot.command(name='reduceWins', help='Reduce Wins to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def reduceWins(ctx, amount, user: discord.Member = None):
    if user:
        if amount:
            embedVar = dbObject.ReduceWins(user.id,int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

@bot.command(name='addLosses', help='Add Losses to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def addLosses(ctx, amount, user: discord.Member = None):
    if user:
        if amount:
            embedVar = dbObject.AddLosses(user.id,int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')


@bot.command(name='reduceLosses', help='Reduce Losses to a certain user')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
async def reduceLosses(ctx, amount, user: discord.Member = None):
    if user:
        if amount:
            embedVar = dbObject.ReduceLosses(user.id,int(amount))
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

    else:  # not mention get self
        await ctx.send(embed='Failed to add points cuz wrong syntax addPoints xamount @User')

# Inputs
@bot.command(name='bet', help='Bet in a ongoing game , Default bet is 20 points')
async def bet(ctx):
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
    print(
        'Invalid Inputs, please use "bet Session_Number Amount_to_Bet/Leave_it_Blank(Default = ' + DefaultAmount + ')"\n')


# Inputs
@bot.command(name='startbet', help='Start Betting Session 1')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin', 'Goblin king', 'Goblin giants')
# async def startbet(ctx , radiant , dire ):
async def startbet(ctx):
    thischannel = ctx.channel
    Bet_Starter = ctx.author

    def radiant(m):
        return m.channel == thischannel and m.author == Bet_Starter

    def dire(m):
        return m.channel == thischannel and m.author == Bet_Starter

    await ctx.send('Please Specify Radiant Side')
    Radiant_msg = await bot.wait_for('message', check=radiant)
    # if Not Registered
    await ctx.send(str(Radiant_msg.content))

    await ctx.send('Please Specify Dire Side')
    Dire_msg = await bot.wait_for('message', check=dire)
    # if Not Registered
    await ctx.send(str(Dire_msg.content))

    Title = str('Radiant Side = ' + Radiant_msg.content + '\nVS\nDire Side = ' + str(Dire_msg.content))
    await ctx.send(Title)

    # Setup Embed Message
    # Send Title to Bet Function Class
    # Let that function setup the things time limited to bet , setup the temp cache for ppl storage
    # Bet Status = True
    # Get Embed message from them
    # await ctx.send(embed = embed)


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


@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)

    split_message = user_message.split()
    channel = str(message.channel.name)
    channelID = str(message.channel.id)
    # channel_nsfw = message.channel.is_nsfw()
    print(f'{username}: {user_message} ({channel}) (ID: {channelID})')

    #Dont Delete This
    await bot.process_commands(message)


bot.run(my_secret)
