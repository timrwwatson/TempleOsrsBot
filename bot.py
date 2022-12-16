from discord.ext import tasks, commands

import discord
import asyncio

from datetime import datetime
import logging
import logging.handlers

from temple_osrs import TempleOsrs, Achievement

description = '''Iamxerxes helper bot that will check templeosrs for the CC's achievements periodically!'''

intents = discord.Intents.default()
intents.message_content = True

def read_conf() -> dict:
    rtn_dict = {}
    with open("conf", "r") as conf:
        for lines in conf:
            lines.strip()
            split = lines.split("=")
            rtn_dict[split[0]] = split[1]
    return rtn_dict

logger_gen = logging.getLogger()
logger_gen.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='logs/discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger_gen.addHandler(handler)

logger = logging.getLogger('discord')

class MyClient(discord.Client):
    def __init__(self, channel_id:int, time_to_check:int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id
        self.time_to_check = int(time_to_check)
        self.TO = TempleOsrs()
        self.last_check = self.last_check = datetime.now()
        logger.info(f"Bot constructed with channelid: {self.channel_id} and time to check: {self.time_to_check} seconds")

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.bg_task = self.loop.create_task(self.my_background_task())
       
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    
    async def my_background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            logger.info("Running background check")
            await self.check_achievements(self.channel_id)
            await asyncio.sleep(self.time_to_check)
            
        
    async def check_achievements(self, channel_num: int):
        channel = self.get_channel(channel_num)  # channel ID goes here
        list_to_send = self.TO.get_cc_current_achievements()
        logger.info(f"Finished check of achievements, found: {len(list_to_send)} items")
        self.last_check = datetime.now()
        for msg in list_to_send:
            await channel.send(msg)

    async def on_message(self, message):

        if message.content.startswith("!check"):
            now = datetime.now()
            diff = now - self.last_check
            if (diff.total_seconds() / 60) < 10:
                logger.warning(f"User: {message.author} tried to check the API too quickly. ({(diff.total_seconds() / 60)} minutes since last check)")
                await message.author.send("The bot checked the API less than 10 minutes ago! We don't want to over work the API :(")
            else:
                await self.check_achievements(self.channel_id)


conf = read_conf()

client = MyClient(conf["channelid"], conf["time"], intents=intents, description=description)
client.run(conf["token"])

