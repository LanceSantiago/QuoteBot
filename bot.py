# bot.py
import os
import discord
import random
import re

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


game=False
ans=""
response=""
origQuote=""
namelessQuote=""
global name_alias
name_alias = {"orange": ["nivy"], "iandur": ["lance", "lander"], "laptop monkey": ["kyo", "desktop monkey"], "emily w": ["emily", "goose"],
"blossom": ["naaz"], "onion": ["onion", "ritvik", "aipiox"], "jc": ["jerry"], "absurdism": ["krish"], "redvilder": ["nick"],"doomgooey": ["sergey", "doom"], "jonjonnho": ["jonathan"], "みお" : ["mio"],
"luciars": ["shiba", "lucas"], "garboguy": ["liam", "garbo" ,"mailman"], "dripbot": ["bolt"], "the-call-of-the-void": ["jessica", "obomo"], "voidlord": ["chonky","chonky birb", "StarLight "], "givemewater": ["water"], "kay911kay": ["broke&homeless", "broke", "daniel"], "salazareo": ["daniel", "salazar"], 
"riddle": ["kana"], "theraghavsharma": ["raghav", "kyo's butler"], "winghawk": ["georges","shanker"], "cluelessKimchi一IlirFan": ["kimchi", "kim"], "lukasz345": ["lukasz"], "starlight": ["chonky","chonky birb", "voidlord"],
"1!":["wan"], "iloveubb":["hans"]
}

def randquote():
    with open('quotes.txt', encoding="utf8") as f:
        lines=f.readlines()
        quote = random.randint(0, len(lines)-1)
        nospeakerWithQuoteNum = lines[quote].split("\" - ")[0]
        noSpeaker = (re.split(r'\#[0-9]*:', nospeakerWithQuoteNum)[1]) + "\""
        speakerWithNum = lines[quote].split("\" -")[1] 
        speaker = speakerWithNum.split("[")[0] 
        output = [noSpeaker, speaker, lines[quote]]
        return output

def setState(gameState,answerState,originalQuote, quote):
    global game
    game=gameState
    global ans
    ans=answerState
    global origQuote
    origQuote=originalQuote
    global namelessQuote
    namelessQuote=quote

def getState():
    return [game, ans, origQuote,namelessQuote]

@client.event
async def on_ready():
    game=False
    ans=""
    # Everything under here, the bot executes for "commands"
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if '-' in message.content:
        response=""
            # List of Commands
        if (message.content).lower() == '-help':
            response="**Guess Quote Commands!**\n **-guessquote** -> starts a quote guessing game! (short form -**gq**)\n **-giveup** -> Stops the game and reveals the answer!\n **-[username]** -> guessing that username for the current quote"
        
            # Prevents starting a new game if a game is on progress
        elif ((message.content).lower() == '-guessquote' or (message.content).lower() == '-gq') and getState()[0]: 
            response="Guess the previous quote! use -giveup to giveup"

            # Starting the Game
        elif ((message.content).lower() == '-guessquote' or (message.content).lower() == '-gq') and not getState()[0]:
            quote = randquote()
            response = quote[0]
            setState(True,quote[1].strip(),quote[2],quote[0])
            # re-prints the quote
        elif((message.content).lower() == '-quote') and getState()[0]:
            response=getState()[3]
            # Giving up
        elif (message.content).lower() == '-giveup' and getState()[0]:
            response = "Original quote:\n\n" + getState()[2]
            setState(False,"","","")

            # Giving up when no game is running
        elif ((message.content).lower() == '-giveup' or (message.content).lower() == '-quote') and not getState()[0]:
            reponse = "There is currently no game running!\nUse -guessquote to start a game!" 

            # Correct Guess
        elif getState()[0] and ((getState()[1]).lower() in (message.content).lower()) or (getState()[1].lower() in name_alias) and (message.content).lower()[1:] in (name_alias[getState()[1].lower()]):
            response = "**Correct!** \nOriginal quote:\n\n" + getState()[2]
            setState(False,"","","")

            # Wrong Guess
        elif getState()[0]:
            response = "Guess again or type -giveup to giveup." 
        if response != "":
            await message.channel.send(response)

client.run(TOKEN)
