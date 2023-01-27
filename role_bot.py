from decouple import config
import discord
from datetime import datetime

token = config("TOKEN")
my_guild = config("DISCORD_GUILD")
okuda = config("OKUDA_ID")
role_id = config("ROLE_ID")
clown_id = config("CLOWN_ID")
admin_id = config("ADMIN_ID")

intents = discord.Intents.default()
intents.message_content=True
intents.members=True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == my_guild:
            break
    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id}\n)",
    )
    botactivity = discord.Game(name="Escape From Tarkov", start=datetime(year=2022, month=1, day=1, minute=1, hour=2))
    await client.change_presence(activity=botactivity, status=discord.Status.dnd)


@client.event
async def on_member_join(member):
    guild = member.guild
    try:
        if guild is None:
            print("GUILD NOT FOUND")
            return "GUILD NOT FOUND"

        role = guild.get_role(int(role_id))
        clown = guild.get_role(int(clown_id))
        admin = guild.get_role(int(admin_id))

        if role is None:
            print("ERROR ROLE WAS NOT FOUND")
            return "ERROR ROLE WAS NOT FOUND"

        if clown is None:
            return "ERROR CLOWN WAS NOT FOUND"


        if member.id == int(okuda):
            to_send = f'OKUDA ОБНАРУЖЕН!'
            await guild.system_channel.send(to_send)
            await member.add_roles(clown)
            await member.add_roles(admin)
        else:
            await member.add_roles(role)


    except discord.HTTPException:
                return "DISCORD ROLE ERROR"


client.run(token)