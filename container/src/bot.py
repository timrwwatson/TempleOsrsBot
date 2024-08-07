import discord
from discord.ext import commands

import asyncio
from datetime import datetime
import logging
import logging.handlers
import random

from time_query import get_time

from temple_osrs import TempleOsrs

version_num = 0.82
version_date = "24/07/07"
changelog="""```- Elidinis - Date Conversion, made simpler, it uses discord built in conversion from epoch time```"""

def read_conf() -> dict:
    rtn_dict = {}
    with open("src/conf/conf", "r") as conf:
        for lines in conf:
            lines = lines.strip()
            split = lines.split("=")
            rtn_dict[split[0]] = split[1]
    return rtn_dict

logger_gen = logging.getLogger()
logger_gen.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='src/logs/discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger_gen.addHandler(handler)

logger = logging.getLogger('discord')

description = '''Iamxerxes helper bot that will check templeosrs for the CC's achievements periodically!'''

intents = discord.Intents.default()
intents.message_content = True
help_command = commands.DefaultHelpCommand(no_category = 'Commands')

bot = commands.Bot(command_prefix='!', description=description, intents=intents, help_command=help_command)
TO = TempleOsrs()
last_check_time = datetime.now()
list_to_send = []
monthly_list_to_send =  []


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command(help="Check for new achievements in the CC TempleOsrs Page")
async def check(ctx):
    now = datetime.now()
    diff = now - last_check_time
    if (diff.total_seconds() / 60) < 10:
        logger.warning(f"User: {ctx.message.author} tried to check the API too quickly. ({(diff.total_seconds() / 60)} minutes since last check)")
        await ctx.message.author.send("The bot checked the API less than 10 minutes ago! We don't want to over work the API :(")
    else:
        await check_achievements(ctx.channel.id, command=True)

@bot.command(help="Get information of when the bot last queried TempleOsrs for achievements.")
async def last_check(ctx):
    now = datetime.now()
    diff = (now - last_check_time).total_seconds() / 60
    diff = float(diff)
    await ctx.send(f"The bot last quered the API at: {last_check_time.strftime('%y/%m/%d %X')} that was {diff:.2f} minutes ago. It recieved {len(list_to_send)} new items.")
    
@bot.command(help="Get bot version and changelog details")
async def version(ctx):
    await ctx.send(f"The bot was updated on {version_date} with version number **{version_num}** the changelog notes are: {changelog}")

@bot.command(help="Get previous monthly CC achievements/top players")
async def monthly(ctx):
    global monthly_list_to_send
    if len(monthly_list_to_send) < 1:
        logger.warning(f"User: {ctx.message.author} tried to check the monthly cc records but it was empty")
        await ctx.message.author.send("Unfortunately there are no stored monthly records, sorry!")
    else:
        for msg in monthly_list_to_send:
            await ctx.message.author.send(msg)

@bot.command(help="Bot rolls a dice between 1-6 (inclusive)")
async def roll(ctx):
    random_number = random.randint(1,6)
    await ctx.send(f"The bot rolled a {random_number}!")

@bot.command(help="Bot converts a time to a few different timezones")
async def time(ctx, date, time, zone="Europe/London"):
    time = date + " " + time
    printStr = await get_time(time=time, zone=zone)
    await ctx.send(printStr)

@bot.event
async def setup_hook() -> None:
    # start the task to run in the background
    bot.bg_task = bot.loop.create_task(bot.my_background_task())
    #global list_to_send
    #list_to_send = ["trial", "by", "fire"]
    #pass
       

@bot.event
async def my_background_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            logger.info("Running background check")
            await check_achievements(conf["channelid"])
            await asyncio.sleep(int(conf["time"]))
        except Exception as e:
            logger.exception(f"Exception hit in my_background_task with exception text: {e}")
        
    
async def check_achievements(channel_num: int, command: bool=False):
    global last_check_time
    global list_to_send
    global monthly_list_to_send
    try:
        channel = bot.get_channel(int(channel_num))  # channel ID goes here
        list_to_send, monthly_check = await TO.get_cc_current_achievements()
        logger.info(f"Finished check of achievements, found: {len(list_to_send)} items")
        last_check_time = datetime.now()
        if len(list_to_send) == 0 and command:
            await channel.send(f"No new achievements found!")
        else:
            for msg in list_to_send:
                if msg and channel:
                    await channel.send(msg)
                else:
                    logger.error(f"Bot fails to find channel: {channel} or message: {msg}")
        
        if monthly_check:
            logger.info(f"Starting Monthly check")
            monthly_list_to_send = await TO.get_cc_monthly_achievements()
            for msg in monthly_list_to_send:
                await channel.send(msg)
        
    except Exception as e:
        logger.exception(f"While running check_achievements an exception was thrown: {e}")

conf = read_conf()
bot.run(conf["token"])