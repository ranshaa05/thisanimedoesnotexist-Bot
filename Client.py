from pyppeteer import launch
import discord
from discord.ext import commands
import asyncio


client = commands.Bot(command_prefix = "$", Intents = discord.Intents().all(), case_insensitive=True)
secret = "ODA5MDQ2NzY2MzEzOTMwNzYy." + "YCPZhA.L2M2BAH8uB3Qq5iBMlA_KpJKu7Y"


@client.command()
async def waifu(ctx, *, msg):
    browser = await launch(headless=False, autoClose=False)
    page = await browser.newPage()
    await page.setViewport({'width': 1550, 'height': 1000})
    
    await ask_for_seed(ctx)
    await ask_for_creativity_level(ctx)
    

    try:
        creativity_value = int(msg)
        print(msg)
        if creativity_value > 18 or creativity_value < 1:
            await ctx.channel.send("Try Again.")
            return await ask_for_seed(ctx)
    except ValueError:
        ctx.channel.send("try again.")
        return await ask_for_creativity_level(ctx)

    await page.goto('https://thisanimedoesnotexist.ai/slider.html?seed=' + seed)
    pic_to_click = await page.querySelectorAll(".psi-value")
    await pic_to_click[creativity_value -1].click()





async def ask_for_seed(ctx):
    await ctx.channel.send("What Seed?")
    msg = await client.wait_for("message", timeout=120)
    seed = msg.content
    
async def ask_for_creativity_level(ctx):
    await ctx.channel.send("Creativity level? (1-18)")
    msg = await client.wait_for("message", timeout=120)

client.run(secret)