import discord
from revChatGPT.ChatGPT import Chatbot
import threading

# retrieve authentication token from token.txt
f = open("discord.txt", "r");
discordToken = f.read();
f.close();

f = open("chatgpt.txt", "r");
gptToken = f.read();
f.close();


chatbot = Chatbot({
  "session_token": gptToken
}, conversation_id=None, parent_id=None)

class MyClient(discord.Client):
    msgBuffer = ""

    async def tryToRespond(self, message):
    # only respond to other people whom post in chatbot channel
        try:
            response = chatbot.ask(MyClient.msgBuffer)
        except:
            print("Rate limit hit. Retry later.")
        else:
            MyClient.msgBuffer = ""
            await message.reply(response['message'], mention_author=False)
                
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'{message.channel} by {message.author}')
        if (message.author != self.user and message.channel.name == "chatbot"):
            MyClient.msgBuffer = MyClient.msgBuffer + message.content
            await self.tryToRespond(message)
        
        


# set intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# run client
client = MyClient(intents=intents)
client.run(discordToken)
