from private import TOKEN
from get_day import get_today_events

from discord import Embed, Intents
from discord.ext import commands
from datetime import datetime, time, timedelta
import asyncio
from random import choice

intents = Intents.all()

bot = commands.Bot(command_prefix="$", intents=intents)
WHEN = time(16, 0, 0) 
channel_id = 951945350468481044  # Put your channel id here

emojis = []

with open('emojis') as file:
    emojis = file.read().rstrip().split(' ')

async def called_once_a_day():  # Fired every day
    # Make sure your guild cache is ready so the channel can be found via get_channel
    await bot.wait_until_ready()

    events = get_today_events()
    # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(channel_id) as there's less looping involved, but just get_channel still works fine
    channel = bot.get_channel(channel_id)

    description = ""

    if len(events) > 0:
        description = "\n".join([f"- {e} {choice(emojis)}" for e in events])
    else:
        description = f"Y'a rien à fêter aujourd'hui {choice(emojis)}"

    embed = Embed(
        title=datetime.today().strftime("On est le %d/%m et on fête 🥳"),
        description=description
        )
    await channel.send(embed=embed)


async def background_task():
    now = datetime.now()
    # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        # Seconds until tomorrow (midnight)
        seconds = (tomorrow - now).total_seconds()
        # Sleep until tomorrow and then the loop will start
        await asyncio.sleep(seconds)
    while True:
        # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        now = datetime.now()
        target_time = datetime.combine(now.date(), WHEN)
        seconds_until_target = (target_time - now).total_seconds()
        # Sleep until we hit the target time
        await asyncio.sleep(seconds_until_target)
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        # Seconds until tomorrow (midnight)
        seconds = (tomorrow - now).total_seconds()
        # Sleep until tomorrow and then the loop will start a new iteration
        await asyncio.sleep(seconds)

if __name__ == "__main__":
    bot.loop.create_task(background_task())
    bot.run(TOKEN)
