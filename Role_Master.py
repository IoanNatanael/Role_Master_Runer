import discord
import os


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    token = os.environ.get("token")

    @client.event
    async def on_ready():
        print(f"Bot is active.")

    bot_channel_id = None

    @client.event
    async def on_message(message):

        if message.content.startswith("^setchannel"):
            # Check if the user is a server admin
            if message.author.guild_permissions.administrator:
                # Get the channel ID from the message content
                if len(message.content.split("!")) > 1:
                    channel_id = message.content.split("!")[1]
                else:
                    # Handle the case where the "!" character is not found
                    await message.channel.send("Invalid command format. Please use the format ^setchannel !channel_id")
                    return

                global bot_channel_id
                bot_channel_id = int(channel_id)

                # Send a confirmation message in the same channel
                await message.channel.send(f"Bot channel set to <#{bot_channel_id}>")
            else:
                # If the user doesn't have the necessary permissions, send an error message
                await message.channel.send("You do not have the necessary permissions to set the bot channel.")

        elif bot_channel_id is not None and message.channel.id == bot_channel_id and message.content.startswith(
                "!add_role"):
            # Check if the user is a server admin
            if message.author.guild_permissions.administrator:
                # Get the role name from the message content
                if len(message.content.split("!")) > 1:
                    role_name = message.content.split("!")[1]
                else:
                    # Handle the case where the "!" character is not found
                    await message.channel.send("Invalid command format. Please use the format `!add_role @user !role`")
                    return
                # Get the role object that you want to add
                role = discord.utils.get(message.guild.roles, name=role_name)

                if role is not None:
                    # Get a list of all the user mentions in the message
                    mentions = message.mentions

                    # Loop through each mentioned user and add the role to them
                    for user in mentions:
                        try:
                            await user.add_roles(role)
                            await message.channel.send(f"Added role '{role.name}' to {user.name}")
                        except discord.Forbidden:
                            await message.channel.send("Missing permissions to add roles to users.")
                        except discord.HTTPException:
                            await message.channel.send("Failed to add the role. Please try again later.")
                else:
                    # If the role was not found, send an error message
                    await message.channel.send(f"Role '{role_name}' not found.")
            else:
                # If the user doesn't have the necessary permissions, send an error message
                await message.channel.send("You do not have the necessary permissions to add roles.")

        elif bot_channel_id is not None and message.channel.id == bot_channel_id and message.content.startswith(
                "!remove_role"):
            # Check if the user is a server admin
            if message.author.guild_permissions.administrator:
                # Get the role name from the message content
                if len(message.content.split("!")) > 1:
                    role_name = message.content.split("!")[1]
                else:
                    # Handle the case where the "!" character is not found
                    await message.channel.send(
                        "Invalid command format. Please use the format `!remove_role @user !role`")
                    return
                # Get the role object that you want to remove
                role = discord.utils.get(message.guild.roles, name=role_name)

                if role is not None:
                    # Get a list of all the user mentions in the message
                    mentions = message.mentions

                    # Loop through each mentioned user and remove the role from them
                    for user in mentions:
                        try:
                            await user.remove_roles(role)
                            await message.channel.send(f"Removed role '{role.name}' from {user.name}")
                        except discord.Forbidden:
                            await message.channel.send("Missing permissions to remove roles from users.")
                        except discord.HTTPException:
                            await message.channel.send("Failed to remove the role. Please try again later.")
                else:
                    # If the role was not found, send an error message
                    await message.channel.send(f"Role '{role_name}' not found or it already exists.")
            else:
                # If the user doesn't have the necessary permissions, send an error message
                await message.channel.send("You do not have the necessary permissions to remove roles.")

        elif message.content.startswith("!info"):
            help_message = """
            **Available Commands:**
            - **^setchannel !channel_id**: Set the bot channel.
            Usage: `^setchannel !channel_id`
            """
            await message.channel.send(help_message)

        elif message.channel.id == bot_channel_id and message.content.startswith("!help"):
            help_message = """
            **Available Commands:**

            - **!add_role @user !role**: Add a role to mentioned users.
            Usage: `!add_role @user !role`

            - **!remove_role @user !role**: Remove a role from mentioned users.
            Usage: `!remove_role @user !role`
            """
            await message.channel.send(help_message)

    client.run(token)


run_discord_bot()
