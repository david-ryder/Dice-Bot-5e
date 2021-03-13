import discord
import os
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()


def roll(a):
  num = random.randint(1, a)
  return num


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('.'): 
    length = len(message.content)

    pre = -1 # num characters before d

    plus = 0

    for x in range(length): # get index value of +, if there is one
      if message.content[x] == '+':
        plus = x

    if plus == 0: # if no + in input, default to length
      plus = length

    for x in range(length): # Gets number of characters before d
      if message.content[x] != 'd':
        pre += 1
      elif message.content[x] == 'd':
        break
    
    num_rolls = ''

    for x in range(1,pre+1): # get num_rolls
      num_rolls += message.content[x]
    
    post = length - pre - 2

    die_type = ''

    for x in range(length - post, plus): # get die_type
      die_type += message.content[x]

    addition = ''

    if plus != length: # get value to add to total later
      for x in range(plus, length):
        addition += message.content[x]

    if addition:
      addition = int(addition)
    else:
      addition = 0

    arr = []

    for x in range(int(num_rolls)): # execute die roll and store in array
      arr.append(roll(int(die_type)) + addition)

    query = message.content.replace('.','') # delete the command value from the input string

    final_message = message.author.mention + '\n***Rolling ' + query + ':***   ('

    for x in range(int(num_rolls)):
      if int(die_type) == 20 and arr[x] - addition == 20:
        final_message += '***'
      if x == int(num_rolls) - 1:
        final_message += str(arr[x]) + ')'
      else:
        final_message += str(arr[x]) + ', '
      if int(die_type) == 20 and arr[x] - addition == 20:
        final_message += '***'

    total = 0

    for x in range(int(num_rolls)):
      total += arr[x]
    
    final_message += '\n***Total:***   ' + str(total)

    await message.channel.send(final_message)


keep_alive()


client.run(os.getenv('TOKEN'))
