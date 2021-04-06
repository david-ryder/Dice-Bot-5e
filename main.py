import time
from replit import db
from keep_alive import keep_alive
import os
import random
import urllib
from urllib.request import Request, urlopen

import discord
import pymongo
from discord.ext import commands
from pymongo import MongoClient

import pdfshid

bot = discord.Client()

bot = commands.Bot(command_prefix='.', help_command=None)

client = pymongo.MongoClient("mongodb+srv://mongobot:k495fAouRy802H5K@cluster0.wucup.mongodb.net/test?retryWrites=true&w=majority")

db = client.dndbot

characters = db.characters

color_dict = {
    'red': discord.Color(16711680),
    'orange': discord.Color(16744192),
    'yellow': discord.Color(16641536),
    'green': discord.Color(65280),
    'teal': discord.Color.teal(),
    'blue': discord.Color(149502),
    'purple': discord.Color(10494192),
    'pink': discord.Color(16352485),
    'white': discord.Color.greyple(),
    'black': discord.Color.default()
}

class Weapon:
        def __init__(self, modifier, damage, type):
            self.modifier = modifier
            self.damage = damage
            self.type = type

# simple weapons
club = Weapon('strength', '1d4', 'bludgeoning')
dagger = Weapon('finesse', '1d4', 'piercing')
greatclub = Weapon('strength', '1d8', 'bludgeoning')
handaxe = Weapon('strength', '1d6', 'slashing')
javeline = Weapon('strength', '1d6', 'piercing')
lighthammer = Weapon('strength', '1d4', 'bludgeoning')
mace = Weapon('strength', '1d6', 'bludgeoning')
quarterstaff = Weapon('strength', '1d6', 'bludgeoning')
sickle = Weapon('strength', '1d4', 'slashing')
spear = Weapon('strength', '1d6', 'piercing')

# simple ranged weapons
lightcrossbow = Weapon('dexterity', '1d8', 'piercing')
dart = Weapon('finesse', '1d4', 'piercing')
shortbow = Weapon('dexterity', '1d6', 'piercing')
sling = Weapon('dexterity', '1d4', 'piercing')

# martial weapons
battleaxe = Weapon('strength', '1d8', 'slashing')
flail = Weapon('strength', '1d8', 'bludgeoning')
glaive = Weapon('strength', '1d10', 'slashing')
greataxe = Weapon('strength', '1d12', 'slashing')
greatsword = Weapon('strength', '2d6', 'slashing')
halberd = Weapon('strength', '1d10', 'slashing')
lance = Weapon('strength', '1d12', 'piercing')
longsword = Weapon('strength', '1d8', 'slashing')
maul = Weapon('strength', '2d8', 'bludgeoning')
morningstar = Weapon('strength', '1d8', 'piercing')
pike = Weapon('strength', '1d10', 'piercing')
rapier = Weapon('finesse', '1d8', 'piercing')
scimitar = Weapon('finesse', '1d6', 'slashing')
shortsword = Weapon('finesse', '1d6', 'piercing')
trident = Weapon('strength', '1d6', 'piercing')
warpick = Weapon('strength', '1d8', 'piercing')
warhammer = Weapon('strength', '1d8', 'bludgeoning')
whip = Weapon('finesse', '1d4', 'slashing')

# martial ranged weapons
blowgun = Weapon('dexterity', '1d1', 'piercing')
handcrossbow = Weapon('dexterity', '1d6', 'piercing')
heavycrossbow = Weapon('dexterity', '1d10', 'piercing')
longbow = Weapon('dexterity', '1d8', 'piercing')
net = Weapon('dexterity', '1d0', 'net')


toolrack = {}

toolrack['club'] = club
toolrack['dagger'] = dagger
toolrack['greatclub'] = greatclub
toolrack['handaxe'] = handaxe
toolrack['javeline'] = javeline
toolrack['lighthammer'] = lighthammer
toolrack['mace'] = mace
toolrack['quarterstaff'] = quarterstaff
toolrack['sickle'] = sickle
toolrack['spear'] = spear
toolrack['lightcrossbow'] = lightcrossbow
toolrack['dart'] = dart
toolrack['shortbow'] = shortbow
toolrack['sling'] = sling
toolrack['battleaxe'] = battleaxe
toolrack['flail'] = flail
toolrack['glaive'] = glaive
toolrack['greataxe'] = greataxe
toolrack['greatsword'] = greatsword
toolrack['halberd'] = halberd
toolrack['lance'] = lance
toolrack['longsword'] = longsword
toolrack['maul'] = maul
toolrack['morningstar'] = morningstar
toolrack['pike'] = pike
toolrack['rapier'] = rapier
toolrack['scimitar'] = scimitar
toolrack['shortsword'] = shortsword
toolrack['trident'] = trident
toolrack['warpick'] = warpick
toolrack['warhammer'] = warhammer
toolrack['whip'] = whip
toolrack['blowgun'] = blowgun
toolrack['handcrossbow'] = handcrossbow
toolrack['heavycrossbow'] = heavycrossbow
toolrack['longbow'] = longbow
toolrack['net'] = net 


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('.help'))
    print('Hello!')
    

@bot.command()
async def roll(ctx, message):

    await ctx.channel.purge(limit=1)

    user = db.characters.find_one({'_id':str(ctx.message.author.id)})

    try:
      user_color = color_dict[user['color']]
    except:
      user_color = color_dict['black']

    try:
      name = user['name']
    except:
      name = ctx.author.name

    embed = discord.Embed(title=('-- ' + name + ' rolls ' + message + ' --'), color=user_color)

    if message == 'strength' or message == 'dexterity' or message == 'constitution' or message == 'intelligence' or message == 'wisdom' or message == 'charisma' or message == 'strsave' or message == 'dexsave' or message == 'consave' or message == 'intsave' or message == 'wissave' or message == 'chasave' or message == 'acrobatics' or message == 'animalhandling' or message == 'arcana' or message == 'athletics' or message == 'deception' or message == 'history' or message == 'insight' or message == 'intimidation' or message == 'investigation' or message == 'medicine' or message == 'nature' or message == 'perception' or message == 'performance' or message == 'persuasion' or message == 'religion' or message == 'sleightofhand' or message == 'stealth' or message == 'survival' or message == 'initiative':
        
        if user == None:
            await ctx.send(ctx.author.mention + '\nSorry! Looks like you haven\'t uploaded a character sheet yet!')
            return
        try:
          stat = user[message]
        except:
          await ctx.send(ctx.author.mention + '\nSorry! Looks like you haven\'t uploaded a character sheet yet!')
          return

        final_message = '('

        crit1 = False
        crit2 = False

        roll1 = random.randint(1,20)
        if roll1 == 1 or roll1 == 20:
          crit1 = True

        roll2 = random.randint(1,20)
        if roll2 == 1 or roll2 == 20:
          crit2 = True



        if '+' in stat:
            index = stat.find('+')

            total1 = roll1 + int(stat[index:])

            if crit1:
                final_message += '***'

            final_message += str(total1)

            if crit1:
                final_message += '***'

            final_message += ', '

            total2 = roll2 + int(stat[index:])

            if crit2:
                final_message += '***'

            final_message += str(total2)

            if crit2:
                final_message += '***'

            final_message += ')'

        elif '-' in stat:
            index = stat.find('-')
            
            subtraction = 0 - int(stat[index:])

            total1 = roll1 - subtraction

            if crit1:
                final_message += '***'

            final_message += str(total1)

            if crit1:
                final_message += '***'

            final_message += ', '

            total1 = roll2 - subtraction

            if crit2:
                final_message += '***'

            final_message += str(total2)

            if crit2:
                final_message += '***'

            final_message += ')'

        else:

            total1 = roll1

            if crit1:
                final_message += '***'

            final_message += str(total1)

            if crit1:
                final_message += '***'

            final_message += ', '

            total2 = roll2

            if crit2:
                final_message += '***'

            final_message += str(total2)

            if crit2:
                final_message += '***'

            final_message += ')'
        
        embed.add_field(name='Result:', value=final_message)

        await ctx.channel.send(embed=embed)
        
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
        await ctx.send(ctx.author.mention + '\nWhoops! That was an invalid entry')
        return

    die_type = ''

    for a in range(d_index + 1, pm_index): # get die type
        die_type += message[a]
    
    try:
        die_type = int(die_type)
    except ValueError:
        await ctx.send(ctx.author.mention + '\nWhoops! That was an invalid entry')
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
            await ctx.send(ctx.author.mention + '\nWhoops! That was an invalid entry')
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
    
    embed.add_field(name=('Result:'), value=final_message, inline=False)
    
    total = 0

    for x in range(int(num_rolls)): # calculate the total die roll
        total += arr[x]

    embed.add_field(name='Total:', value=str(total))

    await ctx.send(embed=embed) # send final message


@bot.command()
async def rollhelp(ctx):

    await ctx.channel.purge(limit=1)

    user = db.characters.find_one({'_id':str(ctx.message.author.id)})

    if user == None or user['color'] == None:
        embed = discord.Embed(title='-- Roll command help --')
    else:
        embed = discord.Embed(title='-- Roll command help --', color=color_dict[user['color']])

    embed.add_field(name='Simple die rolls', value='Enter .roll XdY\n- example: .roll 2d20 will roll 2 20 sided dice', inline=False)
    embed.add_field(name='Modified rolls', value='Enter .roll XdY(+/-)number\n- example: .roll 3d4+5 will roll 3 4 sided dice, and then add 5 to each result', inline=False)
    embed.add_field(name='Character rolls', value='Enter .roll stat\n- example: .roll initiative will roll an initiative check at advantage\n\nFor saving throws, enter the first 3 letters of the associated stat, followed by save\n- example: .roll consave will roll a constitution saving throw at advantage\n\nFor skills/abilities, enter the name of the stat you want to roll, ignoring spaces\n- example: .roll animalhandling will roll an animal handling check at advantage', inline=False)
    embed.add_field(name='Critical success/failures', value='These values will be bolded')

    await ctx.channel.send(embed=embed)


@bot.command()
async def clear(ctx, num):

    if ctx.message.author.id != 391638053367840771:
        return

    num = int(num)

    await ctx.channel.purge(limit=num)

    return


@bot.command()
async def upload(ctx):

    await ctx.channel.purge(limit=1)

    try:
        attachment = ctx.message.attachments[0]
    except IndexError:
        await ctx.send(ctx.author.mention + '\nOops! You forgot to send your attachment sheet before running the upload command!')
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
        await ctx.send(ctx.author.mention + '\nSomething is wrong with the uploaded file!')
        return

    f.close()

    post_pdf.close()

    os.remove(post_pdf.name)

    user = db.characters.find_one({'_id':str(ctx.message.author.id)})

    if user == None:
        await ctx.send(ctx.author.mention + '\nWhoops! Something went wrong!')
        return

    final_message = ctx.author.mention + '\nSuccessfully uploaded ' + user['name'] + '\'s character sheet!'

    await ctx.channel.send(final_message)

    return


@bot.command()
async def uploadhelp(ctx):

    await ctx.channel.purge(limit=1)

    user = db.characters.find_one({'_id':str(ctx.message.author.id)})

    if user == None or user['color'] == None:
        embed = discord.Embed(title='-- Upload command help --')
    else:
        embed = discord.Embed(title='-- Upload command help --', color=color_dict[user['color']])

    embed.add_field(name='Instructions', value=('1. Character sheet must be the official Wizards of the Coast 5e fillable pdf:\n' + 'https://media.wizards.com/2016/dnd/downloads/5E_CharacterSheet_Fillable.pdf' + '\n2.  Upload your character sheet to Discord\n3.  When Discord asks you for a comment before sending, enter .upload\n\n'), inline=False  )
    embed.add_field(name='Requirements', value=('\n- Character name,stat modifiers, initiative, saving throws, and skills must all be filled on the character sheet\n- Every filled modifier must contain a + or - before its value'), inline=False)
    embed.add_field(name='If upload is successful:', value='A message will be sent to confirm!', inline=False)
    await ctx.channel.send(embed=embed)


@bot.command()
async def color(ctx, message):
    
    await ctx.channel.purge(limit=1) # delete input message
    
    user = db.characters.find_one({'_id':str(ctx.message.author.id)}) # find user_id

    # if user not in system
    if user == None:

        # create entry
        dict1 = {}
        
        # assign id
        dict1['_id'] = str(ctx.author.id)
        # assign color
        if message in color_dict:
            dict1['color'] = message
            await ctx.send(ctx.author.mention + '\nYour bot messages will now be ' + message + '!')
        else:
            await ctx.send(ctx.author.mention + '\nInvalid color option! Try a different color!')
            return

        
        characters.insert_one(dict1) # upload entry

    # user in system
    else:

        if message in color_dict:
            dict1 = user
            dict1['color'] = message
            characters.remove(spec_or_id=dict1['_id'])
            characters.insert_one(dict1)
            await ctx.send(ctx.author.mention + '\nYour bot messages will now be ' + message + '!')
        else:
            await ctx.send(ctx.author.mention + '\nInvalid color option! Try a different color!')
            return        


@bot.command()
async def colorhelp(ctx):

    await ctx.channel.purge(limit=1)

    user = db.characters.find_one({'_id':str(ctx.message.author.id)})

    if user == None or user['color'] == None:
        embed = discord.Embed(title='-- Color command help --')
    else:
        embed = discord.Embed(title='-- Color command help --', color=color_dict[user['color']])
    
    embed.add_field(name='Instructions', value='1.  Enter .color _______\n- example: .color purple\n2.  Wait for bot to send another message to confirm your selection', inline=False)
    embed.add_field(name='Available colors', value='- red\n- orange\n- yellow\n- green\n- teal\n- blue\n- purple\n- pink\n- white\n- black', inline=False)
    
    await ctx.send(embed=embed)


@bot.command()
async def mysheet(ctx):
    
    # delete function call
    await ctx.channel.purge(limit=1)

    user = db.characters.find_one({'_id':str(ctx.message.author.id)})
    
    # check if user has sheet in system
    try:
        user_test = user['strength']
    except:
        await ctx.send(ctx.author.mention + '\nWhoops! You need to upload a character sheet before you can do tha!')
        return
    
    if user == None or user['color'] == None:
        embed = discord.Embed(title='Character sheet for:')
    else:
        embed = discord.Embed(title='Character sheet for:', color=color_dict[user['color']])

    tempdict = user
    tempdict.pop('_id')
    tempdict.pop('color')
    charactername = tempdict['name']
    tempdict.pop('name')

    message = (str(tempdict)).replace(',', '\n').replace('\'', '').replace('{', '').replace('}', '')
    embed.add_field(name=charactername, value=message)
    await ctx.send(embed=embed)


@bot.command()
async def attack(ctx, message):

    # delete function call
    await ctx.channel.purge(limit=1)

    # get user
    user = db.characters.find_one({'_id':str(ctx.message.author.id)})

    # does user have a character sheet
    try:
       strength = user['strength']
       dexterity = user['dexterity']
       name = user['name']
    except:
        await ctx.send(ctx.author.mention + '\nWhoops! You need to upload a character sheet before you can make attack rolls!')
        return

    try:
        color = color_dict[user['color']]
    except:
        color = color_dict['black']
    
    # is user's message in the toolrack
    if message in toolrack:
        
        embed = discord.Embed(title=('-- ' + name + ' attacks with ' + message + ' --'), color=color)

        crit1 = False
        crit2 = False

        roll1 = random.randint(1,20)
        if roll1 == 1 or roll1 == 20:
            crit1 = True

        roll2 = random.randint(1,20)
        if roll2 == 1 or roll2 == 20:
            crit2 = True

        weapon = toolrack[message]
        bonus = weapon.modifier

        if bonus == 'finesse':
            if user['strength'] > user['dexterity']:
                bonus = 'strength'
            else:
                bonus = 'dexterity'


        if '+' in user[bonus]:
            roll1 += int(user[bonus].replace('+', ''))
            roll2 += int(user[bonus].replace('+', ''))

        if '-' in user[bonus]:
            roll1 -= int(user[bonus].replace('-', ''))
            roll2 -= int(user[bonus].replace('-', ''))

        message = '('

        if crit1:
            message += '***' + str(roll1) + '***, '
        else:
            message += str(roll1) + ','

        if crit2:
            message += '***' + str(roll2) + '***)'
        else:
            message += str(roll2) + ')'

        # get string from weapon description
        string = weapon.damage

        new_message = '('

        total = 0

        if len(string) <= 3:
            try:
                # loop for number of dice to roll
                for x in range(int(string[0])):
                    total += random.randint(1, int(string[2]))

                if '+' in user[bonus]:
                    total += int(user[bonus].replace('+', ''))

                if '-' in user[bonus]:
                    total -= int(user[bonus].replace('-', ''))
            except:
                total = 0
        else:
            try:
                # loop for number of dice to roll
                for x in range(int(string[0])):
                    total += random.randint(1, int(string[2] + string[3]))

                if '+' in user[bonus]:
                    total += int(user[bonus].replace('+', ''))

                if '-' in user[bonus]:
                    total -= int(user[bonus].replace('-', ''))
            except:
                total = 0


        new_message += str(total) + ')'

        embed.add_field(name='To hit:', value=message)
        embed.add_field(name=(weapon.damage + user[bonus] + ' ' + weapon.type + ' damage:'), value=new_message, inline=False)

        await ctx.send(embed=embed)
    else:
      await ctx.send(ctx.author.mention + '\nWhoops! That was an invalid weapon name! Try again!')


@bot.command()
async def help(ctx):

    await ctx.channel.purge(limit=1)

    user = db.characters.find_one({'_id':str(ctx.message.author.id)})

    if user == None or user['color'] == None:
        embed = discord.Embed(title='-- Available commands --')
    else:
        embed = discord.Embed(title='-- Available commands --', color=color_dict[user['color']])

    embed.add_field(name='.roll', value='Rolls dice in XdY format, or rolls dice straight from character sheet\n.rollhelp for more info', inline=False)
    embed.add_field(name='.upload', value='Uploads character sheet so .roll command can use your character\'s stats\n.uploadhelp for more info', inline=False)
    embed.add_field(name='.attack', value='Makes an attack roll using stats from your character sheet\nEnter .attack weaponname to make an attack with a weapon\n- example: .attack longsword to attack with a longsword')
    embed.add_field(name='.mysheet', value='Sends message containing all of your character\'s stats', inline=False)
    embed.add_field(name='.color', value='Changes the color that your bot messages will be sent in\n.colorhelp for more info', inline=False)
    
    await ctx.channel.send(embed=embed)


keep_alive()

bot.run(os.getenv('TOKEN'))
