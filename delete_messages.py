user_msg_channel_binder = {}

async def list_last_msg_id(ctx, client): #bind the id's of the message to the channel it was sent in to the user that activated the bot
    last_msg = await ctx.channel.history().get(author=client.user)
    if ctx.author.id in user_msg_channel_binder.keys():
        user_msg_channel_binder[ctx.author.id].append((last_msg.id, last_msg.channel.id))
    else:
        user_msg_channel_binder[ctx.author.id] = [(last_msg.id, last_msg.channel.id)]


async def delete_messages(ctx, client): #delete messages in reverse order
    for message_id, channel_id in user_msg_channel_binder[ctx.author.id][::-1]:
        await client.http.delete_message(channel_id, message_id)
    user_msg_channel_binder[ctx.author.id] = [] #reset user's msg list

