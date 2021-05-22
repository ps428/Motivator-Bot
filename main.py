import discord
import os
import json
import requests
import random
from replit import db
from keep_alive import keep_alive

TOKEN = os.getenv('TOKEN')
client = discord.Client()

sad_words = [
    'bad', 'blue', 'brokenhearted', 'cast down', 'crestfallen', 'dejected',
    'depressed', 'despondent', 'disconsolate', 'doleful', 'down',
    'down in the mouth', 'downcast', 'downhearted', 'droopy', 'forlorn',
    'gloomy', 'glum', 'hangdog', 'heartbroken', 'heartsick', 'heartsore',
    'heavyhearted', 'inconsolable', 'joyless', 'low', 'low-spirited',
    'melancholic', 'melancholy', 'miserable', 'mournful', 'sad', 'saddened',
    'sorrowful', 'sorry', 'woebegone', 'woeful', 'wretched', 'exhausted'
]

starter_encouragements = [
    'Cheer up buddy!', 'Hang in there', 'Let if be', "It's gonna be alright",
    "Que sera sera"
]

if "responding" in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
    encouragements = db["encouragements"]

    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


# print("Hello there")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello Maddy!')

    if message.content.startswith('$hi'):
        await message.channel.send('Hi Peter!')

    if message.content.startswith('$yo'):
        await message.channel.send('Yo Jojo!')

    msg = message.content

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        # if True:;
        options = starter_encouragements
        if "encouragements" in db.keys():
            # options = options + db["encouragements"]
            #options.append(db["encouragements"])
            options.extend(db["encouragements"])

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))
            await message.channel.send("Here is a quote to boost you up: ")
            await message.channel.send(get_quote())

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send(
            "New enocuraging message added successfully!")

    if msg.startswith("$del"):
        encouragements = []

        if "encouragements" in db.keys():
            index = int(msg.split("$del ", 1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]

        await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on")

        else:
            db["responding"] = False
            await message.channel.send("Responding is off")


keep_alive()

client.run(TOKEN)
