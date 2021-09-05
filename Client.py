import discord
from discord.ext import commands
import os

screenshot_path = os.path.dirname(__file__) + "\\screenshots\\"
client = commands.Bot(command_prefix = "$", Intents = discord.Intents().all(), case_insensitive=True)
secret = "ODA5MDQ2NzY2MzEzOTMwNzYy." + "YCPZhA.L2M2BAH8uB3Qq5iBMlA_KpJKu7Y"


@client.command()
async def waifu(ctx):
    await ctx.channel.send("Hello, my name is ThisAnimeDoesNotExist Bot :slight_smile:\nUsing me, you can get pictures of anime characters that do not exist from https://thisanimedoesnotexist.ai .\nAll you need to do is give me a few details and I'll fetch a picture.\nLet's start with the picture's seed.")
    await ask_for_seed(ctx)
    await ctx.channel.send("Great! Now let's move on to the next part.")
    await ask_for_creativity_level(ctx)

    await ctx.channel.send("Here's your Anime! Thanks for playing! :slight_smile:")
    await ctx.channel.send('https://thisanimedoesnotexist.ai/results/psi-' + str(round(psi_level, 1)) + "/seed" + seed + '.png')



async def ask_for_seed(ctx):
    await ctx.channel.send("The seed determines the base picture.\nWhat Seed?")
    global msg, seed
    msg = await client.wait_for("message", timeout=120)
    while not await check(msg, ctx):
        msg = await client.wait_for("message", timeout=120)
    seed = msg.content

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
    await ctx.channel.send("This part will determine how creative the AI will be when creating the picture.\nAI creativity level? (1-18)")
    msg = await client.wait_for("message", timeout=120)
    while not await check(msg, ctx):
        msg = await client.wait_for("message", timeout=120)

    creativity_value = msg.content

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
    else:
        return True
    

client.run(secret)