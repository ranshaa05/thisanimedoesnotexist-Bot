import nextcord
from nextcord.ext import commands
from random import randint
from asyncio import TimeoutError
from delete_messages import *
from time import sleep

client = commands.Bot(command_prefix = "$", intents = nextcord.Intents().all(), case_insensitive=True)
secret = "OTAwMDQ2MDU2Nzk5MjE5NzYy.YW7n" + "NQ.hKw0jtjSXoKFI4sL1CP715mZuUE"

msg_user_binder = {}
connected_users = []

@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="$waifu"))
    print("\033[1;32;40mBot is ready!\033[0;37;40m")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, nextcord.ext.commands.errors.CommandNotFound):
        return
    raise error

@client.command()
async def waifu(ctx):
    if ctx.message.content.lower() == "$waifu start":
        return

    if ctx.message.content.lower() != "$waifu":
        await ctx.channel.send("Whoops, the correct command is '$waifu'!")
        await list_last_msg_id(ctx, msg_user_binder, client)
        return


    if ctx.author.id in connected_users:
        await ctx.channel.send("Whoops! One user cannot start me twice. You can type 'exit or try again.")
        return

    else:
        connected_users.append(ctx.author.id)
        print("\033[1;37;40mEvent: \033[1;32;40mBot started for user: '" + ctx.author.name + "'.\033[0;37;40m")

    await ctx.channel.send("Hello, my name is ThisAnimeDoesNotExist Bot :slight_smile:\nUsing me, you can get pictures of anime characters that do not exist from <https://thisanimedoesnotexist.ai> .\nAll you need to do is give me a few details and I'll fetch a picture.\nLet's start with the picture's seed.")
    await list_last_msg_id(ctx, msg_user_binder, client)

    if not await ask_for_seed(ctx) or not await ask_for_creativity_level(ctx):
        await ctx.channel.send("Exiting...")
        await list_last_msg_id(ctx, msg_user_binder, client)
        connected_users.remove(ctx.author.id)
        await delete_messages(ctx, msg_user_binder, client)
        print("\033[1;37;40mEvent: \033[93mBot closed for user '" + str(ctx.author.name) + "'.\033[0;37;40m")
        return
    

    await ctx.channel.send("Here's your Anime! Thanks for playing! :slight_smile:")
    await ctx.channel.send(f"https://thisanimedoesnotexist.ai/results/psi-{str(round(psi_level, 1))}/seed{seed}.png")
    await ctx.channel.send(f"*_Seed: {seed} || Creativity Level: {str(round(psi_level, 1))}_*")
    connected_users.remove(ctx.author.id)
    print("\033[1;37;40mEvent: \033[93mBot closed for user '" + str(ctx.author.name) + "'.\033[0;37;40m")
    

async def ask_for_seed(ctx):
    global seed
    await ctx.channel.send("The seed determines the base picture. You can either type a number or type 'random' to get a random seed.\nWhat Seed?")
    await list_last_msg_id(ctx, msg_user_binder, client)
    seed = await get_message(ctx)
    
    while not seed == "random" and not seed == "exit" and not int(seed) in range(0, 1000000):
        await ctx.channel.send("Seeds can only be between 0 and 99999. Try again.")
        await list_last_msg_id(ctx, msg_user_binder, client)
        seed = await get_message(ctx)
        

    seed = await random(ctx, 99999, seed)
    if await stop(seed):
        return False

    while len(seed) < 5:
        seed = "0" + seed

    await delete_messages(ctx, msg_user_binder, client)
    await ctx.channel.send("Great! Now let's move on to the next part.")
    await list_last_msg_id(ctx, msg_user_binder, client)
    return seed
    


async def ask_for_creativity_level(ctx):
    await ctx.channel.send("This part will determine how creative the AI will be when creating the picture. 'random' is also an option here :wink:\nAI creativity level? (1-18)")
    await list_last_msg_id(ctx, msg_user_binder, client)
    creativity_value = await get_message(ctx)
    creativity_value = await random(ctx, 18, creativity_value)

    if await stop(creativity_value):
        return False

    creativity_value = int(creativity_value)
    while not creativity_value in range(1, 19):
        await ctx.channel.send("Creativity Values have to be between 1 and 18. Try again")
        await list_last_msg_id(ctx, msg_user_binder, client)
        creativity_value = int(await get_message(ctx))


    global psi_level
    psi_level = 0.2
    for i in range(creativity_value):
        psi_level = psi_level + 0.1
    await delete_messages(ctx, msg_user_binder, client)
    return psi_level
        
    


async def random(ctx, max_range, value):
    if str(value).lower() == "random":
        value = str(randint(1, max_range))
        await ctx.channel.send(f"Selected {value}")
        await list_last_msg_id(ctx, msg_user_binder, client)
        sleep(2)
        return value
    else:
        return value

async def stop(value):
    if value.lower() == "exit":
        return True
    else:
        return False





async def check(msg, ctx):
    if not (msg.author == ctx.author and msg.channel == ctx.channel):
        return False
    
    msg = msg.content.lower()
    if msg == "$waifu":
        return False

    if not msg.isnumeric() and msg != "random" and msg != "exit":                   #makes sure that the user only types numbers or 'random' or 'exit'
        await ctx.channel.send("Values have to be numbers only! You can type 'exit' to exit or try again.")
        await list_last_msg_id(ctx, msg_user_binder, client)
        return False
    else:
        return True

async def get_message(ctx):
    global msg
    try:
        msg = await client.wait_for("message", timeout=120)
        while not await check(msg, ctx):
            msg = await client.wait_for("message", timeout=120)
        return msg.content.lower()
    except TimeoutError:
        return False



client.run(secret)