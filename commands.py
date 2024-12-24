from telegram import Chat, ChatMember, Message, MessageEntity, Update, User
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus, MessageEntityType

from settings import *

__all__ = [
    'check',
    'check_edited',
]

async def try_to_ban(message: Message, chat: Chat, user: User, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await message.delete()
        await context.bot.ban_chat_member(chat.id, user.id, revoke_messages=True)
    except Exception as e:
        await message.reply_text("Failed to ban the user.")
        print(f"Error: {e}")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message: Message | None = update.message

    if message is None:
        return
    
    content: str = ""
    if message.text:
        content = message.text
    if message.quote:
        content += message.quote.text

    msg_entities: list[MessageEntity] = [*message.entities]
    if (message.quote) and (message.quote.entities):
        msg_entities += [*message.quote.entities]

    if content == "" and len(msg_entities) == 0:
        return

    user: User | None = message.from_user
    if user is None:
        return
    
    chat: Chat = message.chat

    if chat.id not in ALLOWED_GROUPS:
        await context.bot.leave_chat(chat.id)
        return 

    # ignore admins or not
    if not SKIP_CHECKING_ADMINS:
        user_as_chat_member: ChatMember = await context.bot.get_chat_member(chat.id, user.id)
        if user_as_chat_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return

    # [BAN/DELETE] if includes custom emojis or other entity types
    for entity in msg_entities:
        # [BAN]
        if entity.type in (MessageEntityType.CODE, MessageEntityType.CUSTOM_EMOJI):
            await try_to_ban(message, chat, user, context)
            return
        # [DELETE]
        elif entity.type in (MessageEntityType.BOT_COMMAND, 
                             MessageEntityType.MENTION, 
                             MessageEntityType.EMAIL, 
                             MessageEntityType.URL, 
                             MessageEntityType.HASHTAG, 
                             MessageEntityType.TEXT_LINK, 
                             MessageEntityType.PHONE_NUMBER, 
                             MessageEntityType.TEXT_MENTION,
                             MessageEntityType.CASHTAG):
            await message.delete()
            return

    # [DELETE] if includes ban words
    for ban_word in BAN_WORDS:
        if ban_word.lower() in content.lower():
            try:
                await message.delete()
                return
            except Exception as e:
                print(f'Error: {e}')

async def check_edited(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message: Message | None = update.edited_message

    if message is None:
        return
    
    content: str = ""
    if message.text:
        content = message.text
    if message.quote:
        content += message.quote.text

    msg_entities: list[MessageEntity] = [*message.entities]
    if (message.quote) and (message.quote.entities):
        msg_entities += [*message.quote.entities]

    if content == "" and len(msg_entities) == 0:
        return

    user: User | None = message.from_user
    if user is None:
        return
    
    chat: Chat = message.chat

    # ignore admins or not
    if not SKIP_CHECKING_ADMINS:
        user_as_chat_member: ChatMember = await context.bot.get_chat_member(chat.id, user.id)
        if user_as_chat_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return

    # [BAN/DELETE] if includes custom emojis or other entity types
    for entity in msg_entities:
        # [BAN]
        if entity.type in (MessageEntityType.CODE, MessageEntityType.CUSTOM_EMOJI):
            await try_to_ban(message, chat, user, context)
            return
        # [DELETE]
        elif entity.type in (MessageEntityType.BOT_COMMAND, 
                             MessageEntityType.MENTION, 
                             MessageEntityType.EMAIL, 
                             MessageEntityType.URL, 
                             MessageEntityType.HASHTAG, 
                             MessageEntityType.TEXT_LINK, 
                             MessageEntityType.PHONE_NUMBER, 
                             MessageEntityType.TEXT_MENTION,
                             MessageEntityType.CASHTAG):
            await message.delete()
            return

    # [DELETE] if includes ban words
    for ban_word in BAN_WORDS:
        if ban_word.lower() in content.lower():
            try:
                await message.delete()
                return
            except Exception as e:
                print(f'Error: {e}')

