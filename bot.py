import os
import random
import requests
import json
import urllib.request
import asyncio
from PIL import Image

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#client = discord.Client()
bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())





@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Nutrition and Yoga Club! '\
        'By joining, you automatically confirm a blood oath swearing that your whole bloodline will be members of the club!'
    )

    
@bot.event
async def on_message(message):
    if 'ewb' in message.content:
        await message.channel.send('JOIN YOU BITCH')
        await message.channel.send(file = discord.File('flowcode.png'))

    if message.author.id == 144613357679411200:
        num = random.random()

        if num <= .20:
            await message.reply(file = discord.File('mr_swift.png'))

    if 'swift' in message.content.lower() and 'swifted' not in message.content.lower():
        await message.channel.send(file = discord.File('mr_swift.png'))
    
    # if message.author.id == 310602518092840962:
    #     await message.reply("I ain't reading allat but we :speaking_head::up::bangbang::bangbang::fire:")

    if len(message.content) > 120:
        await message.reply("I ain't reading allat but we :speaking_head::up::bangbang::bangbang::fire:")
    
    #if num < 0.05:
       #await message.channel.send(file = discord.File('selfie.jpg'))
        #await message.channel.send("Had to do it to 'em")
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if message.author.id == 988934440875069460:
        await message.channel.send(file = discord.File('deepfried.jpg'))
        await message.channel.send('GET SWIFTED :dash:')


    
@bot.command(name='numgame',
        brief='Guess a number between 1 and 100 (Enter -1 to quit)',
        pass_context=True)
async def numgame(context):
    number = random.randint(1,100)
    attempt = -1
    guesses = 0
    await context.send('Guess a number between 1 and 100 (Enter -1 to quit)')
    while attempt != number:
        guesses+=1
        msg = await bot.wait_for('message', check=checknum(context.author), timeout=30)
        attempt = int(msg.content)
        
        if attempt == -1:
            await context.send('You suck!')
            break
        if attempt > number:
            await context.send('Go lower')
            
        elif attempt < number:
            await context.send('Go higher bozo')
            
        elif attempt == number:
            await context.send('Finally, it only took you '+str(guesses)+' guesses')
            break
        #await context.send('Try again')

@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.command()
async def drawf(ctx):
    attachment_url = ctx.message.attachments[0].url
    file_request = requests.get(attachment_url)
    #print(file_request.content.decode('ascii'))
    commands = file_request.content.decode('ascii')
    commands = commands.splitlines()
    im = Image.open('draw.png')
    w, h = im.size
    for args in commands:
        p = args.split(',')
        x = int(p[0])
        y = int(p[1])
        color = p[2]

        if x < 0 or x > w or y < 0 or y > h:
            await ctx.send(f'Coordinates out of bounds, Image is {w} x {h}')
            return

        color = getcolor(color)
        im.putpixel((x,y), color)

    im.save('draw.png')
    await ctx.send(file=discord.File('draw.png'))



    

    
@bot.command()
async def draw(ctx, *args):
    im = Image.open('draw.png')
    w, h = im.size
    for req in args:
        p = req.split(',')
        x = int(p[0])
        y = int(p[1])
        color = p[2]

        if x < 0 or x > w or y < 0 or y > h:
            await ctx.send(f'Coordinates out of bounds, Image is {w} x {h}')
            return
        
        color = getcolor(color)
        
        im.putpixel((x,y), color)

    im.save('draw.png')
    await ctx.send(file=discord.File('draw.png'))
    
@bot.command()
async def show(ctx):
    await ctx.send(file=discord.File('draw.png'))

@bot.command()
async def recipe(ctx, *args):
    parameters = {
            'app_id': '6fcb1115',
            'app_key': '82235407371fa7638eb783963660b238',
            'q': args[0],
            'type': 'public',
            'random': True
            
        }

    response = requests.get("https://api.edamam.com/api/recipes/v2", params=parameters)
    
    #jprint(response.json())
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    guess = 0
    
    while guess < len(response.json()['hits']):
        urllib.request.urlretrieve(response.json()['hits'][guess]['recipe']['image'], "pic.jpg")
        ingredients = ""
        for x in response.json()['hits'][guess]['recipe']['ingredientLines']:
            ingredients += x
            ingredients += "\n"
            #await message.channel.send(x)
        if 'dm' in args:
            await ctx.author.send(response.json()['hits'][guess]['recipe']['label'])
            await ctx.author.send(file=discord.File('pic.jpg'))
            await ctx.author.send(ingredients)
            await ctx.author.send(response.json()['hits'][guess]['recipe']['url'])
        else:
            await ctx.send(response.json()['hits'][guess]['recipe']['label'])
            await ctx.send(file=discord.File('pic.jpg'))
            await ctx.send(ingredients)
            await ctx.send(response.json()['hits'][guess]['recipe']['url'])
        await ctx.send('View next?')
        resp = await bot.wait_for('message', check=checkauth(ctx.author), timeout=30)
        if resp is None:
            await ctx.send('Thanks for using me senpai')
        if resp.content.lower() != 'next' and resp.content.lower() != 'yes':
            break
        guess +=1
    
    await ctx.send('Thanks for using me')


@bot.command()
async def ask(ctx):
    responses = ['It is certain', 'WIthout a doubt', 'Yes',
    'Ask again later', 'Better not tell you now', 'Concentrate and ask again',
    'No', 'Outlook not so good', 'Very doubtful']

    await ctx.channel.send(random.choice(responses))






def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def checknum(author): 
    def inner_check(message): 
        if message.author != author:
            return False
        try: 
            int(message.content) 
            return True 
        except ValueError: 
            return False
    return inner_check

def checkauth(author): 
    def inner_check(message): 
        if message.author != author:
            return False
        else:
            return True
    return inner_check

def getcolor(color):
    if color == "red":
        return (255, 0, 0)
    elif color == "green":
        return (0, 255, 0)
    elif color == "blue":
        return (0, 0, 255)
    elif color == "yellow":
        return (255,255,0)
    elif color == "cyan":
        return (0,255,255)   
    elif color == "magenta":
        return (255,0,255) 
    elif color == "black":
        return (0,0,0) 
    elif color == "white":
        return (255,255,255) 
    elif color == "gray":
        return (128,128,128) 
    else:
        print("Error: invalid color string.")
        



#client.run(TOKEN)
bot.run(TOKEN)

