from pyrogram import filters
from pyrogram.types import ChatMemberUpdated

from bot import bot, group, LOGGER, _open
from bot.func_helper.utils import judge_admins
from bot.sql_helper.sql_emby import sql_get_emby
from bot.func_helper.emby import emby


@bot.on_chat_member_updated(filters.chat(group))
async def leave_del_emby(_, event: ChatMemberUpdated):
    if event.old_chat_member and not event.new_chat_member:
        if judge_admins(event.from_user.id):
            # admins无视规则 直接跳过
            return
        user_fname = event.old_chat_member.user.first_name
        if not event.old_chat_member.is_member:
            try:
                e = sql_get_emby(tg=event.old_chat_member.user.id)
                if e is None or e.embyid is None:
                    return await bot.send_message(chat_id=event.chat.id,
                                                  text=f'✅ [{user_fname}](tg://user?id={event.old_chat_member.user.id}) 已经离开了群组')

                if await emby.emby_del(id=e.embyid):
                    LOGGER.info(
                        f'【退群删号】- {user_fname}-{event.old_chat_member.user.id} 已经离开了群组，咕噜噜，ta的账户被吃掉啦！')
                    await bot.send_message(chat_id=event.chat.id,
                                           text=f'✅ [{user_fname}](tg://user?id={event.old_chat_member.user.id}) 已经离开了群组，咕噜噜，ta的账户被吃掉啦！')
                else:
                    LOGGER.error(
                        f'【退群删号】- {user_fname}-{event.old_chat_member.user.id} 已经离开了群组，但是没能吃掉ta的账户，请管理员检查！')
                    await bot.send_message(chat_id=event.chat.id,
                                           text=f'❎ [{user_fname}](tg://user?id={event.old_chat_member.user.id}) 已经离开了群组，但是没能吃掉ta的账户，请管理员检查！')
                if _open["leave_ban"]:
                    await bot.ban_chat_member(chat_id=event.chat.id, user_id=event.old_chat_member.user.id)
            except Exception as e:
                LOGGER.error(f"【退群删号】- {event.old_chat_member.user.id}: {e}")
        else:
            pass
    elif event.old_chat_member and event.new_chat_member:
        # if str(event.new_chat_member.status) == 'ChatMemberStatus.BANNED':
        if not event.new_chat_member.is_member:
            user_fname = event.new_chat_member.user.first_name
            try:
                e = sql_get_emby(tg=event.new_chat_member.user.id)
                if e is None or e.embyid is None:
                    return await bot.send_message(chat_id=event.chat.id,
                                                  text=f'✅ [{user_fname}](tg://user?id={event.new_chat_member.user.id}) 已经离开了群组')

                if await emby.emby_del(id=e.embyid):
                    LOGGER.info(
                        f'【退群删号】- {user_fname}-{event.new_chat_member.user.id} 已经离开了群组，咕噜噜，ta的账户被吃掉啦！')
                    await bot.send_message(chat_id=event.chat.id,
                                           text=f'✅ [{user_fname}](tg://user?id={event.new_chat_member.user.id}) 已经离开了群组，咕噜噜，ta的账户被吃掉啦！')
                else:
                    LOGGER.error(
                        f'【退群删号】- {user_fname}-{event.new_chat_member.user.id} 已经离开了群组，但是没能吃掉ta的账户，请管理员检查！')
                    await bot.send_message(chat_id=event.chat.id,
                                           text=f'❎ [{user_fname}](tg://user?id={event.new_chat_member.user.id}) 已经离开了群组，但是没能吃掉ta的账户，请管理员检查！')
                if _open["leave_ban"]:
                    await bot.ban_chat_member(chat_id=event.chat.id, user_id=event.new_chat_member.user.id)
            except Exception as e:
                LOGGER.error(f"【退群删号】- {event.new_chat_member.user.id}: {e}")
    else:
        pass
