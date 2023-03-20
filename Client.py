import nextcord
import os
import logging
import coloredlogs

from nextcord.ext import commands
from random import randint
from asyncio import TimeoutError

from delete_messages import *

#logging config
coloredlogs.install()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logging.getLogger("nextcord").setLevel(logging.WARNING)

#bot config
client = commands.Bot(intents = nextcord.Intents().all(), case_insensitive=True)
secret = "MTAxMDI1NzMyMjczNzY3NjM0OQ.G1joLg.DAD2m9bn-9nF6iqcncyvCDZWnAGk0AipvXP-1s"

@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="$waifu"))
    logging.info("Bot is ready!")


TOKEN_FILE = "token.txt"
if not os.path.exists(TOKEN_FILE):
    logging.error(f"Error: {TOKEN_FILE} not found in program directory.")
    exit()

with open(TOKEN_FILE, "r") as file:
    TOKEN = file.read().strip()


connected_users = []
string_commands = ["random", "exit"]


@client.slash_command()
async def anime(interaction: nextcord.Interaction, seed: str = None, creativity: str =  None):
    "Generates a picture from an anime that does not exist yet."
    if interaction.user.id in connected_users:
        await interaction.send("Whoops! One user cannot start me twice. You can type 'exit or try again.")
        await list_last_msg_id(interaction, client)
        return

    else:
        connected_users.append(interaction.user.id)
        logging.info(f"Began bot for user '{interaction.user}'.")

    await interaction.send("Hello! my name is ThisAnimeDoesNotExist Bot :slight_smile:\nUsing me, you can get pictures of anime characters that do not exist from <https://thisanimedoesnotexist.ai> .\nAll you need to do is give me a few details and I'll fetch a picture.")
    await list_last_msg_id(interaction, client)

    if seed == None or not (await check(seed, interaction)):
        seed_value = await get_message(interaction)
        seed_value = await string_command(interaction, seed_value, "seed")
        seed = await make_seed_valid(interaction, seed_value)

    
    if creativity == None or not (await check(creativity, interaction)):
        creativity_value = await get_message(interaction)
        creativity_value = await string_command(interaction, creativity_value, "creativity")
        creativity = await make_creativity_valid(interaction, creativity_value)
    psi_value = convert_creativity_to_psi(creativity)

        
    await interaction.channel.send(f"""Here's your Anime! Thanks for playing! :slight_smile:
    *_Seed: {seed} || Creativity Level: {str(psi_value)}_*
https://thisanimedoesnotexist.ai/results/psi-{str(psi_value)}/seed{seed}.png""")

    connected_users.remove(interaction.user.id)
    logging.info(f"Browser closed for user '{interaction.user}'.")
    

    

async def make_seed_valid(interaction, seed):
    # await interaction.channel.send("Let's start with the picture's seed.\nThe seed determines the base picture. You can either type a number or type 'random' to get a random seed.\nWhat Seed?")
    # await list_last_msg_id(interaction, client)

    while not int(seed) in range(0, 1000000):
        await interaction.channel.send("Seeds can only be between 0 and 99999. Try again.")
        await list_last_msg_id(interaction, client)
        seed = await get_message(interaction)
        

    while len(seed) < 5:
        seed = "0" + seed

    await delete_messages(interaction.user.id, client)
    return seed
    


async def make_creativity_valid(interaction, creativity_value):
    # await interaction.channel.send("Great! Now let's move on to the next part.\nThis part will determine how creative the AI will be when creating the picture. 'random' is also an option here :wink:\nAI creativity level? (1-18)")
    # await list_last_msg_id(interaction, client)
    creativity_value = await string_command(interaction, creativity_value, "creativity")

    creativity_value = int(creativity_value)
    while not creativity_value in range(1, 19):
        await interaction.channel.send("Creativity Values have to be between 1 and 18. Try again")
        await list_last_msg_id(interaction, client)
        creativity_value = int(await get_message(interaction))
    await delete_messages(interaction.user.id, client)
    return creativity_value


async def check(text, interaction):
    if isinstance(text, nextcord.Message):
        if not (text.author.id == interaction.user.id and text.channel.id == interaction.channel.id):
            return False

        text = text.content.lower()
    
    if not text.isnumeric() and text not in string_commands:       #makes sure that the user only types numbers or 'random' or 'exit'
        await interaction.channel.send("Values have to be numbers only! You can type 'exit' to exit or try again.")
        await list_last_msg_id(interaction, client)
        return False

    else:
        return True

def convert_creativity_to_psi(creativity):
    psi_level = 0.2
    for i in range(int(creativity)):
        psi_level = psi_level + 0.1
    return round(psi_level, 1)
        
    
async def random(interaction, max_range):
    message = str(randint(1, max_range))
    await interaction.channel.send(f"Selected {message}", delete_after=3)
    await list_last_msg_id(interaction, client)
    return message


async def exit(interaction):
    await interaction.channel.send("Exiting...", delete_after=3)
    await delete_messages(interaction.user.id, client)
    connected_users.remove(interaction.user.id)
    logging.info(f"Brower closed for user '{interaction.user}'.")
    return


async def get_message(interaction):
    try:
        msg = await client.wait_for("message", timeout=120)
        while not await check(msg, interaction):
            msg = await client.wait_for("message", timeout=120)
        return msg.content.lower()
    except TimeoutError:
        return False

async def string_command(interaction, text, type): #TODO: random will not return
    if text == "random" and type == "seed":
        return await random(interaction, 99999)
    elif text == "random" and type == "creativity":
        return await random(interaction, 18)
    elif text == "exit":
        return await exit(interaction)
    else:
        return text






client.run(TOKEN)