import discord
import asyncio
import random
import os
import json
from discord.ext import commands

os.chdir(r'D:\Programming\Projects\Discord bot\jsonFiles')

class MatchMaking:
    global T_Queueiter
    global Queueiter
    def __init__(self , client):
        self.client = client

    @commands.command(pass_context = True)
    async def clear(self , ctx,amount=100):
        channel = ctx.message.channel
        messages = []
        async for message in self.client.logs_from(channel , limit=int(amount)+1):
            messages.append(message)
        await self.client.delete_messages(messages)

def setup(client):
    client.add_cog(MatchMaking(client))
