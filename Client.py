import discord
from discord.ext import commands
from random import randint

client = commands.Bot(command_prefix = "$", Intents = discord.Intents().all(), case_insensitive=True)
secret = "ODA5MDQ2NzY2MzEzOTMwNzYy." + "YCPZhA.L2M2BAH8uB3Qq5iBMlA_KpJKu7Y"

connected_users = []

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="$waifu"))

@client.command()
async def waifu(ctx):
    if ctx.author.id in connected_users:
        await ctx.channel.send("Whoops! One user cannot start me twice. You can type 'exit or try again.")
        return
    else:
        connected_users.append(ctx.author.id)

    await ctx.channel.send("Hello, my name is ThisAnimeDoesNotExist Bot :slight_smile:\nUsing me, you can get pictures of anime characters that do not exist from https://thisanimedoesnotexist.ai .\nAll you need to do is give me a few details and I'll fetch a picture.\n WARNING: since this bot uses an AI, it may produce lewed pictures.\nLet's start with the picture's seed.")
    
    if await ask_for_seed(ctx) == False:                    #this executes the functions and checks if a user exited.
        await ctx.channel.send("Exiting...")
        connected_users.remove(ctx.author.id)
        return 
    await ctx.channel.send("Great! Now let's move on to the next part.")
    if await ask_for_creativity_level(ctx) == False:
        await ctx.channel.send("Exiting...")
        connected_users.remove(ctx.author.id)
        return 

    await ctx.channel.send("Here's your Anime! Thanks for playing! :slight_smile:")
    await ctx.channel.send('https://thisanimedoesnotexist.ai/results/psi-' + str(round(psi_level, 1)) + "/seed" + seed + '.png')
    connected_users.remove(ctx.author.id)


async def ask_for_seed(ctx):
    await ctx.channel.send("The seed determines the base picture. You can either type a number or type 'random' to get a random seed.\nWhat Seed?")
    global msg, seed
    msg = await client.wait_for("message", timeout=120)
    while not await check(msg, ctx):
        msg = await client.wait_for("message", timeout=120)
    seed = msg.content
    if seed.lower() == "random":
        seed = str(randint(1, 10000))
        await ctx.channel.send("Seed is " + seed)
    
    if seed.lower() == "exit":
        return False

    if not seed.isnumeric():
        await ctx.channel.send("Seeds have to be numbers only! Try again.")
        return await ask_for_seed(ctx)

    if len(seed) <= 5:
        for i in range(4):
            if len(seed) == 5:
                return
            seed = "0" + seed

    else:
        await ctx.channel.send("Seeds can only be between 0 and 99999. Try again.")
        return await ask_for_seed(ctx)
    


async def ask_for_creativity_level(ctx):
    global msg
    await ctx.channel.send("This part will determine how creative the AI will be when creating the picture. 'random' is also an option here :wink:\nAI creativity level? (1-18)")
    msg = await client.wait_for("message", timeout=120)
    while not await check(msg, ctx):
        msg = await client.wait_for("message", timeout=120)

    creativity_value = msg.content

    if creativity_value.lower() == "random":
        creativity_value = str(randint(1, 18))
        await ctx.channel.send("Creativity level is " + creativity_value)

    if creativity_value.lower() == "exit":
        return False

    if not creativity_value.isnumeric():
        await ctx.channel.send("Creativity Values have to be numbers only! Try again.")
        return await ask_for_creativity_level(ctx)
    
    creativity_value = int(creativity_value)
    if creativity_value > 18 or creativity_value < 1:
        await ctx.channel.send("Creativity Values have to be between 1 and 18. Try again")
        return await ask_for_creativity_level(ctx)
    else:
        global psi_level
        psi_level = 0.2
        for i in range(creativity_value):
            psi_level = psi_level + 0.1


async def check(msg, ctx):
    if not (msg.author == ctx.author and msg.channel == ctx.channel):
        return False
    if msg.content == "$waifu":
        return False
    else:
        return True
    

client.run(secret)