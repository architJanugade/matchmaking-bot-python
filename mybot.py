import discord
import json
import random
import os
from discord.ext import commands

TOKEN = ""
client = commands.Bot(command_prefix = '--')

os.chdir(r'D:\Programming\Projects\Discord bot\jsonFiles')
SoloCounter = 30
SolominCounter = 10
Queueiter = 1
T_Queueiter = 1
TeamCounter = 50
TeamminCounter = 20

extensions = [
    "cogs.Matchmaking",
    "cogs.Moderator"
]

@client.event
async def on_ready():
    botInfo = await client.application_info()
    oauthlink = discord.utils.oauth_url(botInfo.id)

    print('---------')
    print('Username: {}'.format(client.user.name))
    print('ID: {}'.format(client.user.id))
    print('Server count: {}'.format(str(len(client.servers))))
    print('Member count: {}'.format(str(len(set(client.get_all_members())))))
    print('OAuth URL: {}'.format(oauthlink))
    print('Cogs: {}'.format(client.cogs))
    print('---------')


######################### Register Team #################################
@client.command(pass_context = True)
@commands.has_role('Registered')
async def registerTeam( ctx , teamName , player1: discord.Member , player2: discord.Member , player3: discord.Member , player4: discord.Member , player5: discord.Member):
    if ctx.message.channel.id == "549911021511245834":
        with open('Teams.json' , 'r') as f:
            Teams = json.load(f)
        players = [player1 , player2 , player3 , player4 , player5]
        await update_data_Team(ctx , Teams , teamName , players)
        with open('Teams.json' , 'w') as f:
            json.dump(Teams , f , indent = 2)

async def update_data_Team(ctx , Teams , teamName , players):
    if not teamName in Teams:
        Teams[teamName] = {}
        Teams[teamName]["teamElo"] = 0
        Teams[teamName]["Players"] = []
        Role = teamName
        await client.create_role(ctx.message.server , name = Role, hoist = True , mentionable = True )
        TeamRole = discord.utils.get(ctx.message.server.roles , name = Role)
        for player in players:
            print(player)
            Teams[teamName]["Players"].append(player.mention)
            await client.add_roles(player , TeamRole)
        await client.say("{} is Registered as Team Cheers!!!!".format(teamName))

    else:
        await client.say("you are already registered")
############################ Register Solo ###################################
@client.command(pass_context = True)
async def registersolo( ctx , name: discord.Member):
    if ctx.message.channel.id == "549911021511245834":
        with open('Solo.json' , 'r') as f:
            Solo = json.load(f)
        await update_data_solo(Solo ,   name , ctx)
        with open('Solo.json' , 'w') as f:
            json.dump(Solo , f , indent = 2)

async def update_data_solo( Solo , name , player):
    if not player.message.author.mention in Solo:
        author = player.message.author.mention
        member = player.message.author
        Solo[author] = {}
        Solo[author]["name"] = name
        Solo[author]["Elo"] = 0
        nickname = str(Solo[author]["Elo"]) + "~" + Solo[author]["name"]
        Role = discord.utils.get(player.message.server.roles , name = 'Registered')
        member.nick = nickname
        await client.add_roles(member , Role)
        await client.say("{} is Registered as Solo Cheers Guys!!!!".format(author))
    else:
        await client.say("you are already registered")


############################### Win Team ################################
@client.command(pass_context = True)
@commands.has_role('Mod')
async def winT(ctx , T_Queueno , Team , Team2):
    with open('Teams_Queue.json' , 'r') as f:
        Teams_Queue = json.load(f)
    with open('Teams.json' , 'r') as f:
        Teams = json.load(f)
    Teams[Team]["teamElo"] = Teams[Team]["teamElo"] + TeamCounter
    Teams[Team2]["teamElo"] = Teams[Team2]["teamElo"] - TeamminCounter
    await display_win_team(Team , Team2)
    with open('Teams.json' , 'r') as f:
        json.dump(Teams , f , indent = 2)

###############CReate Team Queue Channel###########################
@client.command(pass_context = True)
@commands.has_role('Mod')
async def CreateTQueueChannel(ctx):
    with open('Teams_Queue.json' , 'r') as f:
        Teams_Queue = json.load(f)
    Teams_Queue["1"] = []
    with open('Teams_Queue.json' , 'w') as f:
        json.dump(Teams_Queue , f , indent = 2)

########################## Join Team Queue ###################
@client.command(pass_context = True)
@commands.has_role('Registered')
async def joinQT(ctx , TeamName):
    if ctx.message.channel.id == "549910313995206687":
        with open('Teams.json' , 'r') as f:
            Teams = json.load(f)
        if "{}".format(TeamName) in Teams:
            with open('Teams_Queue.json' , 'r') as f:
                Teams_Queue = json.load(f)
                await update_data_Team_Queue(Teams_Queue , TeamName)
                with open('Teams_Queue.json' , 'w') as f:
                    json.dump(Teams_Queue , f , indent = 2)
        else:
            await client.say("{} is not registerd".format(TeamName))

async def update_data_Team_Queue(Teams_Queue , TeamName):
    global T_Queueiter
    T_Queueno = T_Queueiter
    if len(Teams_Queue["{}".format(T_Queueno)]) >= 1:
        Teams_Queue[str(T_Queueno)].append(TeamName)
        await display_Team_Queue(T_Queueno , Teams_Queue , TeamName)
        await display_match(T_Queueno , Teams_Queue)
        T_Queueiter += 1
        T_Queueno = T_Queueiter
        Teams_Queue[str(T_Queueno)] = []

    else:
        if not TeamName in Teams_Queue[str(T_Queueno)]:
            Teams_Queue[str(T_Queueno)].append(TeamName)
            await display_Team_Queue(T_Queueno , Teams_Queue , TeamName)
        else:
            await client.say("{} is already in queue" .format(TeamName))

async def display_Team_Queue(T_Queueno , Teams_Queue , TeamName):
    embed = discord.Embed(
     title = "Team Queue : {}".format(T_Queueno),
     description = "5 v 5 Custom Games"
    )
    embed.add_field(name = 'Team:' , value = "\n".join("<@{}>".format(Teams_Queue[T_Queueno])) , inline = False)
    await client.say(embed = embed)

async def display_match(T_Queueno , Teams_Queue):
    embed = discord.Embed(
        title= "Team Matchup Queue : {}".format(T_Queueno),
        description = "5 v 5 Custom Games"
    )
    embed.add_field(name = 'Teams:' , value = "\n".join(Teams_Queue[str(T_Queueno)]) , inline = False)
    with open('Maps.json' , 'r') as f:
        Maps = json.load(f)
    embed.add_field(name = 'Map:' , value = random.choice(Maps["Maps"]))
    await client.say(embed = embed)
################Show Queue#################
@client.command(pass_context = True)
@commands.has_role('Registered')
async def showQ(ctx , Queueno):
    if ctx.message.channel.id == "549910313995206687":
        with open('Queue.json' , 'r') as f:
            Queue = json.load(f)
        if len(Queue[str(Queueno)]) < 0 :
            await client.say("Queue is empty")
        else:
            await DisplayQueue(Queue , Queueno)

###############Show Team Points##########
@client.command(pass_context = True)
@commadns.has_role('Registered')
async def pointsT(ctx , TeamName):
    if ctx.message.channel.id == "551095980251021323":
        with open('Teams.json' , 'r') as f:
            Teams = json.load(f)
        if TeamName in Teams:
            await client.say("{}".format(Teams[TeamName][teamElo]))


####################Show Points ###############
@client.command(pass_context = True)
@commands.has_role('Registered')
async def points(ctx):
    if ctx.message.channel.id == "551095980251021323":
        with open('Solo.json' , 'r') as f:
            Solo = json.load(f)
        if ctx.message.author.mention in Solo:
            await client.say("{}".format(Solo[ctx.message.author.mention]["Elo"]) + " points{}".format(ctx.message.author.mention))



######################### Win Solo ##############################
@client.command(pass_context = True)
@commands.has_role('Mod' )
async def winS(ctx , Queueno , Teamno , Teamno2):
    with open('Solo_Teams.json' , 'r') as f:
        Solo_Teams = json.load(f)
    with open('Solo.json' , 'r') as f:
        Solo = json.load(f)
    await update_winS(Solo_Teams , Solo , Queueno , Teamno , Teamno2)
    with open('Solo.json' , 'w') as f:
        json.dump(Solo , f , indent = 2)

async def update_winS(Solo_Teams , Solo  , Queueno , Teamno , Teamno2):
    for player in Solo_Teams[str(Queueno)][str(Teamno)]:
        Solo[player]["Elo"] = Solo[player]["Elo"] + SoloCounter
        await update_nick(player)
    for players in Solo_Teams[str(Queueno)][str(Teamno2)]:
        Solo[players]["Elo"] = Solo[players]["Elo"] - SolominCounter
        await update_nick(player)
    await display_updates(Solo_Teams , Teamno , Teamno2 , Queueno)

async def update_nick(name):
    with open('Solo.json' , 'r') as f:
        Solo = json.load(f)
    nickname = str(Solo[name]["Elo"]) + "~" + str(Solo[name]["name"])
    server = client.get_server("549553345044545536")
    member = server.get_member(name[2:len(name)-1])
    member.nick = nickname

async def display_updates(Solo_Teams , Teamno , Teamno2 , Queueno):
    embed = discord.Embed(
        title = "Updates:"
    )
    embed.add_field(name = 'Winning Team + {}'.format(SoloCounter) , value = '\n'.join(Solo_Teams[str(Queueno)][str(Teamno)]))
    embed.add_field(name = 'Losing Team - {}'.format(SolominCounter) , value = '\n'.join(Solo_Teams[str(Queueno)][str(Teamno2)]))
    await client.say(embed = embed)

####Leave Queue #####
@client.command(pass_context = True)
@commands.has_role('Registered')
async def leaveQ(ctx):
    with open('Queue.json' , 'r') as f:
        Queue = json.load(f)
        await update_data_lQueue(Queue , ctx.message.author)
        with open('Queue.json' , 'w') as f:
            json.dump(Queue , f , indent = 2)

async def update_data_lQueue( Queue , author):
    print(Queueiter)
    if author.mention in Queue[str(Queueiter)]:
        Queue[str(Queueiter)].remove(author.mention)
        await client.say("{} has left the queue".format(author.mention))
    else:
        await client.say("{} is not in the queue".format(author.mention))

###Create Queue Channel ####
@client.command(pass_context = True)
@commands.has_role('Mod')
async def CreateQueueChannel(ctx):
    with open('Queue.json' , 'r') as f:
        Queue = json.load(f)
    Queue[Queueiter] = []
    await client.say("Queue Channel is Created")
    with open('Queue.json' , 'w') as f:
        json.dump(Queue , f , indent = 2)


#############Join Queue#########
@client.command(pass_context = True)
@commands.has_role('Registered')
async def joinQ(ctx):
    with open('Solo.json' , 'r') as f:
        Solo = json.load(f)
    if ctx.message.author.mention in Solo:
        with open('Queue.json' , 'r') as f:
            Queue = json.load(f)
            await update_data_Queue( Queue , ctx.message.author)
        with open('Queue.json' , 'w') as f:
            json.dump(Queue , f , indent = 2)
    else:
        await client.say("{} is not registered".format(ctx.message.author))

async def update_data_Queue(Queue , author):
    global Queueiter
    Queueno = Queueiter
    if len(Queue["{}".format(Queueno)]) >= 9:
        Queue[str(Queueno)].append(author.mention)
        await DisplayQueue(Queue , Queueno)
        await Create_solo_teams(Queue , Queueno)
        Queueiter = Queueiter + 1
        Queueno = Queueiter
        Queue[str(Queueno)] = []

    else:
        if not author.mention in Queue[str(Queueno)]:
            Queue[str(Queueno)].append(author.mention)
            await client.say("{} joined".format(author.mention))
            await DisplayQueue( Queue , Queueno)
        else:
            await client.say("{} already in queue" .format(author.mention))

async def DisplayQueue(  Queue , Queueno):
    embed = discord.Embed(
        title = 'Queue:{}'.format(Queueno),
        description = "5 v 5 Custom Games:"
    )
    embed.add_field(name = "Lobby" , value = '\n'.join(Queue[str(Queueno)]), inline = True)
    await client.say(embed = embed)

async def Create_solo_teams(Queue , Queueno):
    with open('Solo_Teams.json' , 'r') as f:
        Solo_Teams = json.load(f)
    await update_Solo_teams(Solo_Teams , Queueno , Queue)
    with open('Solo_Teams.json' , 'w') as f:
        json.dump(Solo_Teams , f , indent = 2)

async def update_Solo_teams( Solo_Teams , Queueno , Queue):
    if not Queueno in Solo_Teams:
        Solo_Teams[str(Queueno)] = {}
        Solo_Teams[str(Queueno)]["Team1"] = []
        Solo_Teams[str(Queueno)]["Team2"] = []
        for x in range(0 , 5):
            Queuerand = random.choice(Queue[str(Queueno)])
            Queue[str(Queueno)].remove(Queuerand)
            Solo_Teams[str(Queueno)]["Team1"].append(Queuerand)
        for x in range(0 , 5):
            Queuerand = random.choice(Queue[str(Queueno)])
            Queue[str(Queueno)].remove(Queuerand)
            Solo_Teams[str(Queueno)]["Team2"].append(Queuerand)
    await Display_solo_teams(Solo_Teams , Queueno)

async def Display_solo_teams( Solo_Teams , Queueno):
    embed = discord.Embed(
        title = 'Queueno.:{}'.format(Queueno),
        description = '5 v 5 Custom Games'
    )
    embed.add_field(name = "Team1:", value = '\n'.join(Solo_Teams[str(Queueno)]["Team1"]) , inline = True)
    embed.add_field(name = "Team2:", value = '\n'.join(Solo_Teams[str(Queueno)]["Team2"]) , inline = False)
    with open('Maps.json' , 'r') as f:
        Maps = json.load(f)
    embed.add_field(name = "Map:", value = random.choice(Maps["Maps"]) , inline = False)
    embed.add_field(name = "Host of The Match" , value = random.choice(Solo_Teams[str(Queueno)]["Team1"]) , inline = False)
    await client.say(embed = embed)

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

client.run(TOKEN)
