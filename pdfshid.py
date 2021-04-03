import pymongo
import json
import os

# opens character sheet
def fileOpen (filename): # opens the entered file name
    f = open(filename, 'r', encoding='utf8', errors='ignore')
    return f

# extracts the desired substring from a larger string
def filter(my_str, sub):
    index = my_str.find(sub)
    return my_str[index:]

# connects and uploads info from text doc to mongodb
def uploadSheet(text_doc):
    
    client = pymongo.MongoClient("mongodb+srv://mongobot:k495fAouRy802H5K@cluster0.wucup.mongodb.net/test?retryWrites=true&w=majority")

    db = client.dndbot

    characters = db.characters

    dict1 = {}

    # converts text_doc to a json file
    with text_doc as f:
        for line in f:
            attribute, value = line.strip().split()
            dict1[attribute] = value.strip()

    characters.remove(spec_or_id=dict1['_id'])

    characters.insert_one(dict1)


# parses character sheet for rollable information
def fillSheet(input_file, user_id):
    
    substring = 'CharacterName)/Type/Annot/V(' # get character name

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    filename = matched_line + '.txt'

    out_file = open(filename, 'w')

    out_file.write('_id ' + str(user_id) + '\n')

    substring = 'STRmod)/Type/Annot/V(' # get STR mod

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break

    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('strength ' + matched_line + '\n')

    substring = 'DEXmod )/Type/Annot/V(' # get DEX mod

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break

    matched_line = filter(matched_line, substring)
    
    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('dexterity ' + matched_line + '\n')

    substring = 'CONmod)/Type/Annot/V(' # get CON mod

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('constitution ' + matched_line + '\n')

    substring = 'INTmod)/Type/Annot/V(' # get INT mod

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break

    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('intelligence ' + matched_line + '\n')

    substring = 'WISmod)/Type/Annot/V(' # get WIS mod

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('wisdom ' + matched_line + '\n')

    substring = 'CHamod)/Type/Annot/V(' # get CHA mod

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('charisma ' + matched_line + '\n')

    input_file.seek(0)

    substring = 'ST Strength)/Type/Annot/V(' # get STR save

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('ssave ' + matched_line + '\n')

    substring = 'ST Dexterity)/Type/Annot/V(' # get DEX save

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('dsave ' + matched_line + '\n')

    substring = 'ST Constitution)/Type/Annot/V(' # get CON save

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('csave ' + matched_line + '\n')

    substring = 'ST Intelligence)/Type/Annot/V(' # get INT save

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('isave ' + matched_line + '\n')

    substring = 'ST Wisdom)/Type/Annot/V(' # get WIS save

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('wsave ' + matched_line + '\n')

    substring = 'ST Charisma)/Type/Annot/V(' # get CHA save

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('csave ' + matched_line + '\n')

    input_file.seek(0)

    substring = 'Acrobatics)/Type/Annot/V(' # get Acrobatics skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('acrobatics ' + matched_line + '\n')

    substring = 'Animal)/Type/Annot/V(' # get Animal Handling skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('animalhandling ' + matched_line + '\n')

    substring = 'Arcana)/Type/Annot/V(' # get Arcana skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('arcana ' + matched_line + '\n')

    input_file.seek(0)

    substring = 'Athletics)/Type/Annot/V(' # get Athletics skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('athletics ' + matched_line + '\n')

    substring = 'Deception )/Type/Annot/V(' # get Deception skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('deception ' + matched_line + '\n')

    substring = 'History )/Type/Annot/V(' # get History skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('history ' + matched_line + '\n')

    substring = 'Insight)/Type/Annot/V(' # get Insight skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('insight ' + matched_line + '\n')

    substring = 'Intimidation)/Type/Annot/V(' # get Intimidation skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('intimidation ' + matched_line + '\n')

    substring = 'Investigation )/Type/Annot/V(' # get Investigation skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('investigation ' + matched_line + '\n')

    substring = 'Medicine)/Type/Annot/V(' # get Medicine skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('medicine ' + matched_line + '\n')

    input_file.seek(0)

    substring = 'Nature)/Type/Annot/V(' # get Nature skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('nature ' + matched_line + '\n')

    input_file.seek(0)

    substring = 'Perception )/Type/Annot/V(' # get Perception skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('perception ' + matched_line + '\n')

    substring = 'Performance)/Type/Annot/V(' # get Performance skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('performance ' + matched_line + '\n')

    substring = 'Persuasion)/Type/Annot/V(' # get Persuasion skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('persuasion ' + matched_line + '\n')

    input_file.seek(0)

    substring = 'Religion)/Type/Annot/V(' # get Religion skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('religion ' + matched_line + '\n')

    substring = 'SleightofHand)/Type/Annot/V(' # get Sleight of hand skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('sleightofhand ' + matched_line + '\n')

    input_file.seek(0)

    substring = 'Stealth )/Type/Annot/V(' # get Stealth skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('stealth ' + matched_line + '\n')

    substring = 'Survival)/Type/Annot/V(' # get Survival skill

    matched_line = ''

    for line in input_file:
        if substring in line:
            matched_line = line
            break
    
    matched_line = filter(matched_line, substring)

    matched_line = matched_line.replace(substring, '')

    matched_line = matched_line.replace(')>>\n', '')

    out_file.write('survival ' + matched_line + '\n')

    out_file.close()

    again = open(filename, 'r')

    uploadSheet(again)

    again.close()

    os.remove(filename)
