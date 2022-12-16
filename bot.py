from discord.ext import tasks

import discord

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

        # an attribute we can access from our task
        self.counter = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=60)  # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(460122271131107350)  # channel ID goes here
        self.counter += 1
        await channel.send(self.counter)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


conf = read_conf()

client = MyClient(intents=discord.Intents.default())
client.run(conf["token"])