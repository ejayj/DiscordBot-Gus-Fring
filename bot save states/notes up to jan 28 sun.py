#official discord reaction setup
# @client.event
# async def on_message(message):
#     if message.content.startswith('$thumb'):
#         channel = message.channel
#         await channel.send('Send me that 👍 reaction, mate')

#         def check(reaction, user):
#             return user == message.author and str(reaction.emoji) == '👍'

#         try:
#             reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
#         except asyncio.TimeoutError:
#             await channel.send('👎')
#         else:
#             await channel.send('👍')


#Giving roles through reactions, and command.has_role?
# from discord.ext import commands
# from discord.utils import get

# bot = commands.Bot(command_prefix='!')

# @bot.command(pass_context=True)
# @commands.has_role("Admin") # This must be exactly the name of the appropriate role
# async def addrole(ctx):
#     member = ctx.message.author
#     role = get(member.server.roles, name="Test")
#     await bot.add_roles(member, role)
    
#MENU COMMAND THAT WORKS:
# @client.tree.command()
#     async def helpi(interaction: discord.Integration):
#         embed = discord.Embed(title="Help panel!", description="Your Desc")
#         select = Select(
#             placeholder="Select something",
#             options=[
#                 SelectOption(label="😆 - Fun", value="1", description="Get all commands according to \"Fun\""),
#                 SelectOption(label="🪛 - Utility", value="2", description="Get all commands according to \"Utility\""),
#                 SelectOption(label="❓ - Info", value="3", description="Get all commands according to \"Info\""),
#                 SelectOption(label="🎭 - Roleplay", value="4", description="Get all commands according to \"Roleplay\""),
#                 SelectOption(label="🪙 - Economy", value="5", description="Get all commands according to \"Economy\""),
#                 SelectOption(label="🛑 - Cancel", value="Cancel", description="Cancel this interaction.")
#             ]
#         )
#         async def callback(interaction):
#             if select.values[0] == "1":
#                 await interaction.response.send_message("Test")
#             elif select.values[0] == "2":
#                 await interaction.response.send_message("Test")
#             elif select.values[0] == "3":
#                 await interaction.response.send_message("Test")
#             elif select.values[0] == "4":
#                 await interaction.response.send_message("Test")
#             elif select.values[0] == "5":
#                 await interaction.response.send_message("Test")
#         select.callback = callback
#         view = View()
#         view.add_item(select)
#         await interaction.response.send_message("ABC", embed=embed, view=view)



# ORIGINAL MENU COMMAND
    # @client.tree.command()
    # async def helpi(ctx):
    #     embed = discord.Embed(title="Help panel!", description="Your Desc")
    #     select = Select(
    #         placeholder="Select something",
    #         options=[
    #             SelectOption(label="😆 - Fun", value="1", description="Get all commands according to \"Fun\""),
    #             SelectOption(label="🪛 - Utility", value="2", description="Get all commands according to \"Utility\""),
    #             SelectOption(label="❓ - Info", value="3", description="Get all commands according to \"Info\""),
    #             SelectOption(label="🎭 - Roleplay", value="4", description="Get all commands according to \"Roleplay\""),
    #             SelectOption(label="🪙 - Economy", value="5", description="Get all commands according to \"Economy\""),
    #             SelectOption(label="🛑 - Cancel", value="Cancel", description="Cancel this interaction.")
    #         ]
    #     )
    #     async def callback(interaction):
    #         if select.values[0] == "1":
    #             await interaction.response.send_message("Test")
    #     select.callback = callback
    #     view = View()
    #     view.add_item(select)
    #     await ctx.send("ABC", embed=embed, view=view)