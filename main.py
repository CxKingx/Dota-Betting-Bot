import os
import discord
# import datetime,timedelta
from datetime import datetime, timedelta
# import pytz
# import time
from discord import reaction
from discord.ext import commands, tasks

my_secret = os.environ['DISCORD_TOKEN']
bot = commands.Bot(command_prefix='*', intents=discord.Intents.all())

# Initialize the Important Variables
DefaultAmount = 15


# Make the Bet Objects
#Class 1 the User Database Storage

#Class 2 the Bet Functions
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


# Inputs
@bot.command(name='bet', help='Bet in a ongoing game , Default bet is 20 points')
async def bet(ctx):
    # Check if Bet is Online
    # Yes Continue
        # Check if User has Existed in the Database
        # If Registered
            # Check the player remaining points, if it is sufficient to bet
            #If  Sufficient
                # Start Managing the Bet
            # Else Not Sufficient
                # You have no more Bet Points , Please bet with a smaller value
        # Else not Registered
            # You have not sign up for us, please use signup

    #Else No Bets are Ongoing
        #print('No Bets are ongoing right now
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

    Title = str('Radiant Side = '+Radiant_msg.content + '\nVS\nDire Side = '+ str(Dire_msg.content))
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
    print('mesg')
    await bot.process_commands(message)


bot.run(my_secret)
