import discord
from discord import app_commands
import commands
import keys
import os
import json

def run_discord_bot():
    TOKEN = keys.DISCORD_BOT_TOKEN
    guild_id = keys.TEST_SERVER                      
    intents = discord.Intents.default()                 #sets bot features (everything sans presences, members, message content)
    intents.members = True
    intents.message_content = True                      #additional features - namely responsing to DMs                    
    client = discord.Client(intents=intents)            #class of the bot itself
    tree = discord.app_commands.CommandTree(client)

                                                #Commands
    @tree.command(name='hello', description='say hi!', guild=discord.Object(id=guild_id))
    async def hello(interaction):
        await interaction.response.send_message('hi!')

    @tree.command(name='ping', description='relays the delay time between recieving and responding to commands',guild=discord.Object(id=guild_id))
    async def ping(interaction):
        await interaction.response.send_message(f'Pong!\n`Message took {client.latency} to send`')

    @tree.command(name='roll', description='roll die, DND style',guild=discord.Object(id=995821619039715409))
    async def roll(interaction, roll_data: str):
        try:
            roll_result = commands.roll_calc(roll_data)
        except Exception as e:
            roll_result = e
        await interaction.response.send_message(f'You rolled a {roll_result}')

    @tree.command(name='wordle', description='#buggy as hell/defunct: helps solve the daily wordle',guild=discord.Object(id=guild_id))
    async def ping(interaction, wordle_guesses: str):
        try:
            wordle_solns = commands.wordle(wordle_guesses)
        except Exception as e:
            wordle_solns = e
        await interaction.response.send_message(f'{wordle_solns}')

    @tree.command(name="create_resource", description='Create a new list of resources - for updating, use update resource', guild=discord.Object(id=guild_id))
    async def create_resource_list(interaction, resource_list_name: str, resource_list: str):
        try:
            with open('data/resource_list_list.txt','a') as table_of_contents:
                table_of_contents.write(f'{resource_list_name}')
                table_of_contents.close()
            with open('data/resource_list.txt', 'a') as macro_list:
                macro_list.write(f'\n{resource_list_name}\n')
                macro_list.write(f'{resource_list}')
                macro_list.write(f'\n;')
                macro_list.close()
            commands.resource_sort('data/resource_list.txt')
            await interaction.response.send_message(f'Successfully saved {resource_list_name}!')
        except Exception as e:
            await interaction.response.send_message(f' There was a {e} error, please tell @AlanHol')
            
    @tree.command(name="resource", description='Display list of resources', guild=discord.Object(id=guild_id))
    async def read_resource_list(interaction, resource_list_name: str = 'None'):
        try:
            if resource_list_name == 'None':
                print('done detected')
                with open('data/resource_list_list.txt','r') as table_of_contents:
                    message = ''
                    for line in table_of_contents:
                        message += line
                    table_of_contents.close()
                    print(message)
                await interaction.response.send_message(message)
            else:
                message = ''
                in_list = False
                with open('data/resource_list.txt', 'r') as macro_list:
                    for line in macro_list:
                        if line.strip() == resource_list_name: #break statement? stop checking this once the if statement is true once
                            in_list = True
                        if in_list and line.strip() !=";":
                            message += line
                        if in_list and line.strip() == ";":
                            in_list = False
                    macro_list.close()
                if message == '':
                    await interaction.response.send_message(f'List not found, check your spelling?')
                else:    
                    await interaction.response.send_message(message)
        except Exception as e:
            await interaction.response.send_message(f' There was a {e} error, please tell @AlanHol')

    @tree.command(name="create_bookmark", description='create a new bookmark', guild=discord.Object(id=guild_id))
    async def create_bookmark(interaction, book_name: str, page_number: int, private: bool):
        try:
            bookmark = f' `{private}` user:{interaction.id} {book_name}: page/chapter #:{page_number}'
            with open('data/bookmark.txt','a') as list_of_bookmarks:
                list_of_bookmarks.write(bookmark) #create dictionary
            list_of_bookmarks.close()
            await interaction.response.send_message(f'Created bookmark successfully')           
        except Exception as e:
            await interaction.response.send_message(f' There was a {e} error, please tell @AlanHol')

    @tree.command(name="bookmark", description='checks current bookmark for a book, use * to check all', guild=discord.Object(id=guild_id))
    async def bookmark(interaction):
        with open('data/bookmark.txt', 'r') as list_of_bookmarks:
            bookmarks = ""
            for line in list_of_bookmarks:
                bookmarks += line
            list_of_bookmarks.close()
        await interaction.response.send_message(f'{bookmarks}')           
                    
    @tree.command(name="help", description='Display possible commands with a more comprehensive breakdown of usage', guild=discord.Object(id=guild_id))
    async def help_desk(interaction):
        message = ""
        with open('data/help_desk.txt', 'r') as help_desk:
            for line in help_desk:
                message = message + line
            help_desk.close()
        await interaction.response.send_message(f'{message}')

    @tree.command(name="guildmates", description='Shows current guild members', guild=discord.Object(id=guild_id))
    async def guildmates(interaction):
        message = ""
        for member in interaction.guild.members:
            message += str(member) + "\n"
        await interaction.response.send_message(f'{message}')

    @tree.command(name="at_everyone", description='Shows users @everyone count', guild=discord.Object(id=guild_id))
    async def at_everyone(interaction, member: str):       
        member = int(member[2:-1])
        at_everyone_list = json.load(open(f'data/at_everyone_{interaction.guild.id}.json', 'r'))                 
        for server,server_users in at_everyone_list.items():
            for user,user_data in server_users.items():
                if member == user_data["user_id"]:
                    current_guild = client.get_guild(interaction.guild_id)
                    discord_name = current_guild.get_member(member)
                    message = f'the user {discord_name} has sent out an @ everyone in this server a total of {user_data["counter"]} times before.'
        await interaction.response.send_message(f'{message}')

    @tree.command(name="at_here", description='Shows users @here count', guild=discord.Object(id=guild_id))
    async def at_here(interaction, member: str):       
        member = int(member[2:-1])
        at_here_list = json.load(open(f'data/at_here_{interaction.guild.id}.json', 'r'))                 
        for server,server_users in at_here_list.items():
            for user,user_data in server_users.items():
                if member == user_data["user_id"]:
                    current_guild = client.get_guild(interaction.guild_id)
                    discord_name = current_guild.get_member(member)
                    message = f'the user {discord_name} has sent out an @ here in this server a total of {user_data["counter"]} times before.'
        await interaction.response.send_message(f'{message}')
        
                                                #Start up event
    @client.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=guild_id)) #updates guild commands NOTE: global commands are not implemented
        print(f'Logged in as {client.user} (ID: {client.user.id})')
        print("Command Tree Synced and Ready!")
        print('____________________________________')

        for guild in client.guilds: #creates dictionaries for servers that don't have one yet
            if os.path.isfile(f'data/at_everyone_{guild.id}.json'):
                pass
            else:
                with open(f'data/at_everyone_{guild.id}.json','w') as at_everyone_initialization: 
                    at_everyone_list = '{"server_' + str(guild.id) + '": {'
                    for member in guild.members:
                        at_everyone_list += '"user_' + str(member.id) + '" : {"user_id": ' + str(member.id) + ', "counter": 0 } , \n'
                    at_everyone_list = at_everyone_list[:-3]
                    at_everyone_list += '} }'
                    print(at_everyone_list) #preview of the dictionary in terminal before writing to a .json
                    at_everyone_initialization.write(at_everyone_list)
                    at_everyone_initialization.close()

            if os.path.isfile(f'data/at_here_{guild.id}.json'):
                pass
            else:
                with open(f'data/at_here_{guild.id}.json','w') as at_here_initialization: 
                    at_here_list = '{"server_' + str(guild.id) + '": {'
                    for member in guild.members:
                        at_here_list += '"user_' + str(member.id) + '" : {"user_id": ' + str(member.id) + ', "counter": 0 } , \n'
                    at_here_list = at_here_list[:-3]
                    at_here_list += '} }'
                    print(at_here_list) #preview of the dictionary in terminal before writing to a .json
                    at_here_initialization.write(at_here_list)
                    at_here_initialization.close()

    @client.event
    async def on_message(message):
        if "@everyone" in message.content: #check if a message has @everyone in it
            at_everyone_list = json.load(open(f'data/at_everyone_{message.guild.id}.json', 'r'))                 
            for server,server_users in at_everyone_list.items():
                for user,user_data in server_users.items():
                    if message.author.id == user_data["user_id"]:
                        user_data['counter'] += 1
                        with open(f'data/at_everyone_{message.guild.id}.json','w') as at_everyone_needing_counter_updating:
                            at_everyone_needing_counter_updating.write(str(at_everyone_list).replace("'",'"')) 
                            at_everyone_needing_counter_updating.close
        if "@here" in message.content: #check if a message has @here in it
            at_here_list = json.load(open(f'data/at_here_{message.guild.id}.json', 'r'))                 
            for server,server_users in at_here_list.items():
                for user,user_data in server_users.items():
                    if message.author.id == user_data["user_id"]:
                        user_data['counter'] += 1
                        with open(f'data/at_here_{message.guild.id}.json','w') as at_here_needing_counter_updating:
                            at_here_needing_counter_updating.write(str(at_here_list).replace("'",'"')) 
                            at_here_needing_counter_updating.close

    client.run(TOKEN) #actually runs the thing


run_discord_bot()