import os
import discord
import json
from discord.ext import commands
os.chdir(r'D:\Programming\Projects\Discord bot\jsonFiles')



class MatchMaking:
    def __init__(self , client):
        self.client = client

    @commands.command(pass_context = True)
    async def addelo(self , ctx , Elo , author):
        print("hey")
        with open('Solo.json' , 'r') as f:
            Solo = json.load(f)
        elo = Solo[author]["Elo"] + int("{}".format(Elo))
        Solo[author]["Elo"] = elo
        with open('Solo.json' , 'w') as f:
            json.dump(Solo , f , indent = 2)




def setup(client):
    client.add_cog(MatchMaking(client))
