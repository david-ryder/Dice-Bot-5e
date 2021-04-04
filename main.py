import time
from replit import db
from keep_alive import keep_alive
import os
import discord
import pymongo
from pymongo import MongoClient
from discord.ext import commands
import random
import pdfshid
import urllib
from urllib.request import Request, urlopen

bot = discord.Client()

bot = commands.Bot(command_prefix='.', help_command=None)

TOKEN = 'ODIxNjAyOTE0MTE1NTE4NDc1.YFGHVw.Bbrjq8hb7EOlQwevjgkKdleQ71M'

client = pymongo.MongoClient("mongodb+srv://mongobot:k495fAouRy802H5K@cluster0.wucup.mongodb.net/test?retryWrites=true&w=majority")

db = client.dndbot

characters = db.characters

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('.help'))
    print('Hello!')
    

@bot.command()
async def roll(ctx, message):

    await ctx.channel.purge(limit=1)

    user = db.characters.find_one({'_id':str(ctx.message.author.id)})

    embed = discord.Embed(title=('-- Rolling ' + message + ' --'), color=65535)

    if message == 'strength' or message == 'dexterity' or message == 'constitution' or message == 'intelligence' or message == 'wisdom' or message == 'charisma' or message == 'strsave' or message == 'dexsave' or message == 'consave' or message == 'intsave' or message == 'wissave' or message == 'chasave' or message == 'acrobatics' or message == 'animalhandling' or message == 'arcana' or message == 'athletics' or message == 'deception' or message == 'history' or message == 'insight' or message == 'intimidation' or message == 'investigation' or message == 'medicine' or message == 'nature' or message == 'perception' or message == 'performance' or message == 'persuasion' or message == 'religion' or message == 'sleightofhand' or message == 'stealth' or message == 'survival' or message == 'initiative':
        
        if user == None:
            await ctx.send(ctx.author.mention + '\nSorry! Looks like you haven\'t uploaded a character sheet yet!')
            return

        stat = user[message]

        final_message = '('

        if '+' in stat:
            index = stat.find('+')

            result = random.randint(1,20)

            total = result + int(stat[index:])

            if result == 20 or result == 1:
                final_message += '***'

            final_message += str(total)

            if result == 20 or result == 1:
                final_message += '***'

            final_message += ')'

        elif '-' in stat:
            index = stat.find('-')

            result = random.randint(1,20)
            
            subtraction = 0 - int(stat[index:])

            total = result - subtraction

            if result == 20 or result == 1:
                final_message += '***'

            final_message += str(total)

            if result == 20 or result == 1:
                final_message += '***'
                
            final_message += ')'

        else:
            result = random.randint(1,20)

            total = result

            if result == 20 or result == 1:
                final_message += '***'

            final_message += str(total)

            if result == 20 or result == 1:
                final_message += '***'

            final_message += ')'
        
        embed.add_field(name='Result', value=final_message)

        await ctx.channel.send(ctx.author.mention, embed=embed)
        
        return


    d_index = message.find('d')

    pm_index = len(message)

    plus = False
    minus = False

    length = len(message)

    if '+' in message:
        pm_index = message.find('+')
        plus = True
        length -= pm_index

    if '-' in message:
        pm_index = message.find('-')
        minus = True
        length -= pm_index

    num_rolls = ''

    for a in range(d_index): # get number of rolls
        num_rolls += message[a]
    
    try:
        num_rolls = int(num_rolls)
    except ValueError:
        await ctx.send(ctx.author.mention + '\nWhoops! That\'s an invalid entry')
        return

    die_type = ''

    for a in range(d_index + 1, pm_index): # get die type
        die_type += message[a]
    
    try:
        die_type = int(die_type)
    except ValueError:
        await ctx.send(ctx.author.mention + '\nWhoops! That\'s an invalid entry')
        return

    addition = ''

    if plus:
        try:
            for a in range(pm_index + 1, len(message)):
                addition += message[a]
            addition = int(addition)
        except ValueError:
            await ctx.send(ctx.author.mention + '\nWhoops! That\'s an invalid entry')
            return
    elif minus:
        try:
            for a in range(pm_index + 1, len(message)):
                addition += message[a]
            addition = 0 - int(addition)
        except ValueError:
            await ctx.send(ctx.author.mention + '\nWhoops! That\'s an invalid entry')
            return
    else:
        addition = 0

    arr = []

    for a in range(num_rolls): # fill array with random values according to the die type
        arr.append((random.randint(1,die_type)) + addition)
    
    final_message = '('

    for x in range(int(num_rolls)): # build final message, bold crits
        if (int(die_type) == 20 and arr[x] - addition == 20) or (int(die_type) == 20 and arr[x] - addition == 1):
            final_message += '***'
        if x == int(num_rolls) - 1:
            final_message += str(arr[x]) + ')'
        else:
            final_message += str(arr[x]) + ','
        if (int(die_type) == 20 and arr[x] - addition == 20) or (int(die_type) == 20 and arr[x] - addition == 1):
            final_message += '***'
        final_message += ' '
    
    embed.add_field(name=('Result'), value=final_message, inline=False)
    
    total = 0

    for x in range(int(num_rolls)): # calculate the total die roll
        total += arr[x]

    embed.add_field(name='Total', value=str(total))

    await ctx.send(ctx.message.author.mention, embed=embed) # send final message

@bot.command()
async def rollhelp(ctx):

    await ctx.channel.purge(limit=1)

    embed = discord.Embed(title='-- Roll command --', color=discord.Color(65535))
    embed.add_field(name='Simple die rolls', value='Enter .roll XdY\nExample: .roll 2d20 will roll 2 20 sided dice', inline=False)
    embed.add_field(name='Modified rolls', value='Enter .roll XdY(+/-)number\nExample: .roll 3d4+5 will roll 3 4 sided dice, and then add 5 to each result', inline=False)
    embed.add_field(name='Character rolls', value='Enter .roll stat\nExample: .roll initiative will roll a 20 sided die and add your initiative modifier to the result\n\nFor saving throws, enter the first 3 letters of the associated stat, followed by save\n- Example: .roll consave will roll a constitution saving throw\n\nFor skills/abilities, enter the name of the stat you want to roll, ignoring spaces\n- Example: .roll animalhandling will roll an animal handling check', inline=False)
    embed.add_field(name='Critical success/failures', value='These values will be bolded')

    await ctx.channel.send(embed=embed)

@bot.command()
async def clear(ctx, num):

    if ctx.message.author.id != 391638053367840771:
        return

    await ctx.channel.purge(limit=1)

    num = int(num)

    await ctx.channel.purge(limit=num)

    return

@bot.command()
async def upload(ctx):

    await clear(ctx, 0)

    try:
        attachment = ctx.message.attachments[0]
    except IndexError:
        await ctx.send(ctx.author.mention + '\nWhoops! Something went wrong!')
        return

    site = attachment.url # get url to file from message

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url=site, headers=hdr)
    empty_pdf = urlopen(req).read()

    f = open('file.pdf', 'wb')
    f.write(empty_pdf)

    post_pdf = pdfshid.fileOpen('file.pdf')

    user_id = ctx.message.author.id

    try:
        pdfshid.fillSheet(post_pdf, user_id)
    except ValueError:
        await ctx.send(ctx.author.mention + '\nSomething is wrong with the file!')
        return

    f.close()

    post_pdf.close()

    os.remove(post_pdf.name)

    user = db.characters.find_one({'_id':str(ctx.message.author.id)})

    if user == None:
        await ctx.send(ctx.author.mention + '\nWhoops! Something went wrong!')
        return

    final_message = ctx.author.mention + '\nCharacter successfully uploaded!'

    await ctx.channel.send(final_message)

    return

@bot.command()
async def uploadhelp(ctx):

    await ctx.channel.purge(limit=1)

    embed = discord.Embed(title='-- Upload command --', color=discord.Color(65535))
    embed.add_field(name='Instructions', value=('1. Character sheet must be the official Wizards of the Coast 5e fillable pdf:\n' + 'https://media.wizards.com/2016/dnd/downloads/5E_CharacterSheet_Fillable.pdf' + '\n2.  Upload your character sheet to Discord\n3.  When Discord asks you for a comment before sending, enter .upload\n\n'), inline=False  )
    embed.add_field(name='Requirements', value=('\n- All stat modifiers and ability scores must be filled including initiative, saving throws, and skills\n- Every filled modifier must contain either a + or - before its value\nexample: +1 for performance skill'), inline=False)
    embed.add_field(name='If upload is successful:', value='A message will be sent to confirm!', inline=False)
    await ctx.channel.send(embed=embed)

@bot.command()
async def attack(ctx, weapon):

    user = db.characters.find_one({'_id':str(ctx.message.author.id)})

    if user == None:
        await ctx.send(ctx.author.mention + '\nSorry! Looks like you haven\'t uploaded a character sheet yet!')
        return

@bot.command()
async def help(ctx):

    await ctx.channel.purge(limit=1)

    embed = discord.Embed(title='-- Available commands --', color=discord.Color(65535))
    embed.add_field(name='.roll', value='Rolls dice', inline=False)
    embed.add_field(name='.upload', value='Uploads character sheet so .roll command can use your character\'s stats', inline=False)
    embed.add_field(name='.commandhelp', value='Replace \'command\' with the name of the command you want to learn about\nexample: .rollhelp', inline=False)
    embed.add_field(name='Important!', value='If I do not respond with a message, then something went wrong!')

    await ctx.channel.send(embed=embed)

keep_alive()

bot.run(os.getenv('TOKEN'))
