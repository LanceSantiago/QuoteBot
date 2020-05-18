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

def randquote():
    with open('testFile.txt', encoding="utf8") as f:
        lines=f.readlines()
        quote = random.randint(0, len(lines)-1)
        nospeakerWithQuoteNum = lines[quote].split("\" - ")[0]
        noSpeaker = (re.split(r'\#[0-9]*:', nospeakerWithQuoteNum)[1]) + "\""
        speakerWithNum = lines[quote].split("\" -")[1] 
        speaker = speakerWithNum.split("[")[0] 
        output = [noSpeaker, speaker, lines[quote]]
        return output

def setState(gameState,answerState,originalQuote):
    global game
    game=gameState
    global ans
    ans=answerState
    global origQuote
    origQuote=originalQuote

def getState():
    return [game, ans, origQuote]

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
        if (message.content).lower() == '-guessquote':
            quote = randquote()
            response = quote[0]
            setState(True,quote[1].strip(),quote[2])
        elif (message.content).lower() == '-giveup':
            response = "Original quote:\n\n" + getState()[2]
            setState(False,"","")
        elif getState()[0] and ((getState()[1]).lower() in (message.content).lower()):
            response = "**Correct!** \nOriginal quote:\n\n" + getState()[2] 
            setState(False,"","")
        elif getState()[0]:
            response = "No. Guess again." 
        if response != "":
            await message.channel.send(response)

client.run(TOKEN)




# orange: -guessquote
# bot: Guess who said this!
# bot: "Hello"
# orange: -iandur
# bot: Correct! Quote: #123: "Hello"  etc
