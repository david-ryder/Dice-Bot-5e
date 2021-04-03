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

client = pymongo.MongoClient("mongodb+srv://mongobot:k495fAouRy802H5K@cluster0.wucup.mongodb.net/test?retryWrites=true&w=majority")

db = client.dndbot

characters = db.characters

@bot.event
async def on_ready():
    print('Hello!')

@bot.command()
async def roll(ctx, message):

    await clear(ctx, 1)

    if message == 'strength' or message == 'dexterity' or message == 'constitution' or message == 'intelligence' or message == 'wisdom' or message == 'charisma' or message == 'strsave' or message == 'dexsave' or message == 'consave' or message == 'intsave' or message == 'wissave' or message == 'chasave' or message == 'acrobatics' or message == 'animalhandling' or message == 'arcana' or message == 'athletics' or message == 'deception' or message == 'history' or message == 'insight' or message == 'intimidation' or message == 'investigation' or message == 'medicine' or message == 'nature' or message == 'perception' or message == 'performance' or message == 'persuasion' or message == 'religion' or message == 'sleightofhand' or message == 'stealth' or message == 'survival' or message == 'initiative':
        cursor = db.characters.find({'_id':str(ctx.message.author.id)})
        
        for characters in cursor:
            stat = characters[message]

        final_message = ctx.author.mention + '\n***Rolling ' + message + ':***   ('

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

        await ctx.channel.send(final_message)
        
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
    
    num_rolls = int(num_rolls)

    die_type = ''

    for a in range(d_index + 1, pm_index): # get die type
        die_type += message[a]
    
    die_type = int(die_type)

    addition = ''

    if plus:
        for a in range(pm_index + 1, len(message)):
            addition += message[a]
        addition = int(addition)
    elif minus:
        for a in range(pm_index + 1, len(message)):
            addition += message[a]
        addition = 0 - int(addition)
    else:
        addition = 0

    arr = []

    for a in range(num_rolls): # fill array with random values according to the die type
        arr.append((random.randint(1,die_type)) + addition)
    
    final_message = ctx.message.author.mention + '\n***Rolling ' + message + ':***   ('

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
    
    total = 0

    for x in range(int(num_rolls)): # calculate the total die roll
        total += arr[x]
    
    final_message += '\n***Total:***   ' + str(total)

    await ctx.send(final_message) # send final message

@bot.command()
async def rollhelp(ctx):

    await ctx.channel.purge(limit=1)

    message = ctx.author.mention + '```-- Roll command --\n\n'
    message += 'Simple die rolls - enter .roll <XdY> | example: .roll 2d20 will roll 2 20 sided dice\n\n'
    message += 'Modified rolls - enter .roll <XdY><+/-><value> | example: .roll 3d4+5 will roll 3 4 sided dice, and then add 5 to each result\n\n'
    message += 'Character rolls - enter .roll <stat> | example: .roll initiative will roll a 20 sided die and add your initiative modifier to the result\n\n'
    message += '- For saving throws, enter the first 3 letters of the associated stat, followed by save | example: .roll consave will roll a constitution saving throw\n'
    message += '- For skills/abilities, enter the name of the stat you want to roll, ignoring spaces | example: .roll animalhandling will roll an animal handling check```'
    await ctx.channel.send(message)

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

    attachment = ctx.message.attachments[0]
    site = attachment.url # get url to file from message

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url=site, headers=hdr)
    empty_pdf = urlopen(req).read()

    f = open('file.pdf', 'wb')
    f.write(empty_pdf)

    post_pdf = pdfshid.fileOpen('file.pdf')

    user_id = ctx.message.author.id

    pdfshid.fillSheet(post_pdf, user_id)

    f.close()

    post_pdf.close()

    os.remove(post_pdf.name)

    await clear(ctx, 2)

    final_message = ctx.author.mention + '\nCharacter succeddfully uploaded!'

    await ctx.channel.send(final_message)

@bot.command()
async def uploadhelp(ctx):

    await ctx.channel.purge(limit=1)

    message = ctx.author.mention + '```-- Upload command --\n\n'
    message += 'Upload your character sheet to Discord. When Discord asks you for a comment before sending, enter .upload\n\n'
    message += 'REQUIREMENTS:\n'
    message += '- Character sheet must be the official Wizards of the Coast 5e fillable pdf\n'
    message += '- All stat modifiers and ability scores must be filled - including initiative, saving throws, and skills\n'
    message += '- Every filled modifier must contain either a + or - before its value | example: +1 for performance skill\n\n'
    message += 'If upload successful, a message will be sent to confirm!```'
    await ctx.channel.send(message)


@bot.command()
async def help(ctx):
    
    final_message = ctx.author.mention + '```\n-- Available commands: --\n\n'
    final_message += '.roll | rolls dice\n'
    final_message += '.upload | uploads character sheet to database so it can be paired with .roll command\n\n'
    final_message += 'Enter .<command>help for help with a specific command | example: .rollhelp\n\n'
    final_message += 'If I do not respond with a message, then something went wrong!```'
    await ctx.channel.send(final_message)

bot.run(TOKEN)
