import nextcord
import random
import os
import logging
import coloredlogs

from nextcord.ext import commands
from typing import Optional


#logging config
coloredlogs.install()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logging.getLogger("nextcord").setLevel(logging.WARNING)

#bot config
client = commands.Bot(intents = nextcord.Intents().all(), case_insensitive=True)

@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="/anime"))
    logging.info("Bot is ready!")


TOKEN_FILE = "token.txt"
if not os.path.exists(TOKEN_FILE):
    logging.error(f"Error: {TOKEN_FILE} not found in program directory.")
    exit()
with open(TOKEN_FILE, "r") as file:
    TOKEN = file.read().strip()


@client.slash_command()
async def anime(interaction: nextcord.Interaction,
                seed: nextcord.Range[1, 100000] = nextcord.SlashOption(description="Seed to base the picture off of.", required=True, default=1),
                creativity: nextcord.Range[1, 18] = nextcord.SlashOption(description="Creativity level for the picture.", required=True, default=1),
                random_seed: Optional[bool] = nextcord.SlashOption(description="Randomizes the seed (seed value doesn't matter).", required=False),
                random_creativity: Optional[bool] = nextcord.SlashOption(description="Randomizes the creativity level (creativity value doen't matter).", required=False)):
    "Fetches a picture from an anime that does not exist yet from https://thisanimedoesnotexist.ai."

    #this is in order to include 0 as a valid seed, as nextxord allows negative numbers if min is 0
    seed = seed - 1
    creativity = creativity - 1

    if random_seed:
        seed = random.choice(range(0, 100000))
    seed = await make_seed_valid(seed)

    if random_creativity:
        creativity = random.choice(range(0, 18))
    psi_value = await make_creativity_valid(creativity)

    await interaction.response.send_message(f"""Here's your Anime! I hope you like it! :slight_smile:
*_Seed: {seed}_* || *_Creativity Level: {psi_value}_*
https://thisanimedoesnotexist.ai/results/psi-{psi_value}/seed{seed}.png""")



async def make_seed_valid(seed):
    seed = f"{seed:05}"
    return seed
    
async def make_creativity_valid(creativity_value):
    creativity_value = round(0.1 * creativity_value + 0.3, 1)
    return creativity_value


if __name__ == '__main__':
    client.run(TOKEN)