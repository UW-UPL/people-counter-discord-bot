import discord
import random
import asyncio
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

channel_id = 1069334415425147010  # Replace with the ID of the text channel to update
sleep_interval = 0
is_sleeping = False

with open("DISCORD_BOT_TOKEN", "r") as f:
    token = f.read()


@tasks.loop(minutes=15)
async def update_channel_name():
    global is_sleeping
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    while not client.is_closed():
        if not is_sleeping:
            random_number = random.randint(1, 100)  # Replace with your desired range of random numbers
            new_name = f"Random Number: {random_number}"
            await channel.edit(name=new_name)
        await asyncio.sleep(10)  # 900 seconds = 15 minutes


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    update_channel_name.start()


@client.event
async def on_message(message):
    global sleep_interval, is_sleeping
    if message.author == client.user:
        return
    if message.content.startswith("!sleep"):
        try:
            args = message.content.split()[1:]
            if len(args) == 0:
                is_sleeping = True
                await message.channel.send("Channel updates paused.")
            else:
                duration = int(args[0])
                unit = args[1] if len(args) > 1 else "s"
                if unit == "d":
                    sleep_interval = duration * 86400
                elif unit == "h":
                    sleep_interval = duration * 3600
                elif unit == "m":
                    sleep_interval = duration * 60
                else:
                    sleep_interval = duration
                is_sleeping = True
                if sleep_interval == 0:
                    await message.channel.send("Channel updates paused indefinitely.")
                else:
                    await message.channel.send(f"Channel updates paused for {duration} {unit}.")
        except:
            await message.channel.send("Invalid command.")
    elif message.content.startswith("!resume"):
        sleep_interval = 0
        is_sleeping = False
        await message.channel.send("Channel updates resumed.")

client.run(token)
