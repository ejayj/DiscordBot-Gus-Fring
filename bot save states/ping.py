# #how to ping a user
# #  If you have the ctx object (inside a command)
# await ctx.send(ctx.message.author.mention)
# # If you have a message object (such as the on_message event)
# await message.channel.send(message.author.mention)
# # If you know their ID
# await ctx.send("<@" + str(user_id) + ">")

# #how to ping a role
# @client.command() #v1
#        @commands.has_permissions(administrator=True)
#        async def ping(ctx, *, msg):
#             for guild in client.guilds:
#                 role = get(guild.roles, name = 'Wafaduck Alerts')
#                 for channel in guild.channels:
#                     if(channel.name == 'wafaduck-alerts'):   
#                         await channel.send(f"{role.mention}")