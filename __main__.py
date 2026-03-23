import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!lookup"):
        target = message.content.split(" ")[1:]
        if len(target) < 1:
            await message.channel.send("Usage: !lookup <PERSON_NAME>")
            return
        target = " ".join(target)
        await message.channel.send(f"Looking up information on **{target}**...")
        api_url = "https://tabber.cicis.info/api/lookup"
        response = requests.post(
            api_url,
            json={"name": target},
            headers={"Content-Type": "application/json", "Host": "tabber.cicis.info"},
            verify=False,
        )
        if response.status_code == 200:
            data = response.json()
            result = data["result"]
            if result:
                await message.channel.send(
                    f"**Query:** {target}\n**Name:** {data['canon_name']}\n**Location (Best Guess):** {result['location']}\n**Reasoning:** {result['reasoning']}"
                )
            else:
                await message.channel.send("No results found.")
        else:
            await message.channel.send("Lookup failed. Please try again later.")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token is None:
        print("Error: DISCORD_TOKEN environment variable not set.")
    else:
        client.run(token)
