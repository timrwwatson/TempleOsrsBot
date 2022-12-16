from discord.ext import tasks

import discord

from temple_osrs import TempleOsrs, Achievement

def read_conf() -> dict:
    rtn_dict = {}
    with open("conf", "r") as conf:
        for lines in conf:
            lines.strip()
            split = lines.split("=")
            rtn_dict[split[0]] = split[1]
    return rtn_dict



class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.TO = TempleOsrs()


    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=60)  # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(460122271131107350)  # channel ID goes here
        list_to_send = self.TO.get_cc_current_achievements()
        for msg in list_to_send:
            await channel.send(msg)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


conf = read_conf()

client = MyClient(intents=discord.Intents.default())
client.run(conf["token"])