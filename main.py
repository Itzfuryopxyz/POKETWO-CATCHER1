import re, os, asyncio, random, string, keep_alive
from discord.ext import commands, tasks

version = 'v2.0'

prefix = "!"  
allowed_user_id = 1076116730620940298  
user_token = os.environ['user_token']
logs_id = os.environ['logs_id']
user_id = os.environ['user_id']
#removed catch_id = os.environ['catch_id'] 
#removed guild_id = os.environ['guild_id']

with open('data/pokemon','r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('data/legendary','r') as file:
    legendary_list = file.read()
with open('data/mythical','r') as file:
    mythical_list = file.read()
with open('data/level','r') as file:
    to_level = file.readline()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0

prefix = "!"  
main = 1076116730620940298
poketwo = 716390085896962058
client = commands.Bot(command_prefix='prefix')
intervals = [3.0, 2.2, 2.4, 2.6, 2.8]

def solve(message):
    hint = []
    for i in range(15,len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''
    for i in hint:
        hint_string += i
    hint_replaced = hint_string.replace('_', '.')
    solution = re.findall('^'+hint_replaced+'$', pokemon_list, re.MULTILINE)
    return solution

#removed @spam.before_loop
@client.event
async def on_ready():
    print(f'Logged into account: {client.user.name}')

@client.event
async def on_message(message):
    channel = message.channel
    if message.guild.id != 1034016979725582347:
            if message.embeds:
                embed_title = message.embeds[0].title
                if 'wild pokémon has appeared!' in embed_title:
                    #spam.cancel()
                    await asyncio.sleep(4)
                    await channel.send('<@716390085896962058> h')
                elif "Congratulations" in embed_title:
                    embed_content = message.embeds[0].description
                    if 'now level' in embed_content:
                        split = embed_content.split(' ')
                        a = embed_content.count(' ')
                        level = int(split[a].replace('!', ''))
                        if level == 100:
                            await channel.send(f".s {to_level}")
                            with open('data/level', 'r') as fi:
                                data = fi.read().splitlines(True)
                            with open('data/level', 'w') as fo:
                                fo.writelines(data[1:])
            else:
                content = message.content
                if 'The pokémon is ' in content:
                    if not len(solve(content)):
                        print('Pokemon not found.')
                    else:
                        for i in solve(content):
                            await asyncio.sleep(2)
                            await channel.send(f'<@716390085896962058> c {i}')

                elif 'Congratulations' in content:
                    global shiny
                    global legendary
                    global num_pokemon
                    global mythical
                    num_pokemon += 1
                    split = content.split(' ')
                    pokemon = split[7].replace('!','')
                    if 'seem unusual...' in content:
                        shiny += 1
                        print(f'Shiny Pokémon caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                    elif re.findall('^'+pokemon+'$', legendary_list, re.MULTILINE):
                        legendary += 1
                        print(f'Legendary Pokémon caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                    elif re.findall('^'+pokemon+'$', mythical_list, re.MULTILINE):
                        mythical += 1
                        print(f'Mythical Pokémon caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                    else:
                        print(f'Total Pokémon Caught: {num_pokemon}')
                if 'human' in content:
                    await channel.send(f"<@{main}> bot kicked please Solve captcha") 
                    await message.author.kick()

#------------------------------SHINY LOGGING-----------------------------#

@client.event
async def on_message(message):
    channel = client.get_channel(int(logs_id))
    content = message.content
    if 'seem unusual...' in content:
        await channel.send(f"Hey <@{main}>, i just caught a shiny✨ pokemon Arent you happy? to check your shiny use  !shiny ") 

keep_alive.keep_alive()
client.run(f"{user_token}")
