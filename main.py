import os
import discord
import pymongo
from discord.ext import commands
import random
import pdfshid
import urllib
from urllib.request import Request, urlopen

bot = discord.Client()

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Hello!')

@bot.command()
async def roll(ctx, message):

    await clear(ctx, 1)
    
    d_index = 0

    pm_index = len(message)

    plus = False
    minus = False

    length = len(message)

    for a in range(len(message)): # parse the input string for d, +/-
        if message[a] == 'd':
            d_index = a 
        if message[a] == '+':
            pm_index = a
            length -= pm_index
            plus = True
        elif message[a] == '-':
            pm_index = a
            length -= pm_index
            minus = True

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
        if int(die_type) == 20 and arr[x] - addition == 20:
            final_message += '***'
        if x == int(num_rolls) - 1:
            final_message += str(arr[x]) + ')'
        else:
            final_message += str(arr[x]) + ','
        if int(die_type) == 20 and arr[x] - addition == 20:
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

    pdfshid.fillSheet(post_pdf)

    f.close()

    post_pdf.close()

    os.remove(post_pdf.name)
    
bot.run(TOKEN)
