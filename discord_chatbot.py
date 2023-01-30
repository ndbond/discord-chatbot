import discord

# retrieve authentication token from token.txt
f = open("token.txt", "r");
token = f.read();

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'{message.channel} by {message.author}')

        # only respond to other people whom post in chatbot channel
        if (message.author != self.user and message.channel.name == "chatbot"):
            await message.reply("hi there!", mention_author=False);

# set intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# run client
client = MyClient(intents=intents)
client.run(token)
