import discord
import os
import json
import requests
import random

TOKEN=os.getenv('TOKEN')
client = discord.Client()

sad_words = ['sad','unhappy','depresed','angry','miserable','depressing','tired','exhausted']

starter_encouragements = [
  'Cheer up buddy!',
  'Hang in there',
  'Let if be',
  "It's gonna be alright",
  "Que sera sera"
]
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

# print("HEllo teher")

print(TOKEN)

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

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  msg = message.content
  
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

client.run(TOKEN)
