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

bot = commands.Bot(command_prefix='.')

TOKEN = 'ODIxNjAyOTE0MTE1NTE4NDc1.YFGHVw.oNUSOFoqEaQRj6BcWKe7aZpTyVs'

client = pymongo.MongoClient("mongodb+srv://mongobot:k495fAouRy802H5K@cluster0.wucup.mongodb.net/test?retryWrites=true&w=majority")

db = client.dndbot

characters = db.characters

@bot.event
async def on_ready():
    print('Hello!')

@bot.command()
async def roll(ctx, message):

    await clear(ctx, 1)

    if message == 'strength' or message == 'dexterity' or message == 'constitution' or message == 'intelligence' or message == 'wisdom' or message == 'charisma' or message == 'strsave' or message == 'dexsave' or message == 'consave' or message == 'intsave' or message == 'wissave' or message == 'chasave' or message == 'acrobatics' or message == 'animalhandling' or message == 'arcana' or message == 'athletics' or message == 'deception' or message == 'history' or message == 'insight' or message == 'intimidation' or message == 'investigation' or message == 'medicine' or message == 'nature' or message == 'perception' or message == 'performance' or message == 'persuasion' or message == 'religion' or message == 'sleightofhand' or message == 'stealth' or message == 'survival':
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
async def clear(ctx, num):
    num = int(num)
    await ctx.channel.purge(limit=num)

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



bot.run(TOKEN)
