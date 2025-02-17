from datetime import datetime, timezone, timedelta

from pyrogram import filters

from bot import bot, bot_photo, group, sakura_b, LOGGER, prefixes, ranks
from bot.func_helper.emby import emby
from bot.func_helper.filters import admins_on_filter
from bot.func_helper.utils import convert_to_beijing_time
from bot.sql_helper.sql_emby import sql_get_emby, sql_update_embys, Emby, sql_update_emby
from bot.func_helper.msg_utils import deleteMessage


async def user_plays_rank(days=7):
    results = await emby.emby_cust_commit(user_id=None, days=days, method='sp')
    if results is None:
        return await bot.send_photo(chat_id=group[0], photo=bot_photo,
                                    caption=f'🍥 获取过去{days}天UserPlays失败了嘤嘤嘤 ~ 手动重试 ')
    else:
        txt = f'**▎{ranks["logo"]}过去{days}天看片榜**\n\n'
        xu = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩']
        n = 0
        ls = []
        for r in results:
            em = sql_get_emby(r[0])
            if em is None:
                emby_name = '已删除用户'
                minutes = '0'
                tg = None
            else:
                tg = em.tg
                minutes = int(r[1]) // 60
                emby_name = f'{r[0]}'
                if em.lv == 'a':
                    emby_name = f'{r[0][:1]}░{r[0][-1:]}'  # ||  隐藏效果与链接不可同时存在
                ls.append([tg, em.iv + minutes])
            txt += f'**{xu[n]} - **[{emby_name}](tg://user?id={tg}) : **{minutes}** min\n'
            n += 1
        txt += f'\n#UPlaysRank {datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")}'
        send = await bot.send_photo(chat_id=group[0], photo=bot_photo, caption=txt)
        if sql_update_embys(some_list=ls, method='iv'):
            await send.reply(f'**自动将观看时长转换为{sakura_b}\n请已上榜用户检查是否到账**')
            LOGGER.info(f'【userplayrank】： ->成功 数据库执行批量操作{ls}')
        else:
            await send.reply(f'**🎂！！！为上榜用户增加{sakura_b}出错啦** @工程师看看吧~ ')
            LOGGER.error(f'【userplayrank】：-？失败 数据库执行批量操作{ls}')


async def user_day_plays():
    await user_plays_rank(1)


async def user_week_plays():
    await user_plays_rank(7)


@bot.on_message(filters.command('user_ranks', prefixes) & admins_on_filter)
async def shou_dong_uplayrank(_, msg):
    await deleteMessage(msg)
    try:
        days = int(msg.command[1])
        await user_plays_rank(days=days)
    except (IndexError, ValueError):
        await msg.reply(
            f"🔔 请手动加参数 user_ranks+天数，已加入定时任务管理面板，**手动运行user_ranks注意使用**，以免影响{sakura_b}的结算")


async def check_low_activity():
    now = datetime.now(timezone(timedelta(hours=8)))
    success, users = await emby.users()
    if success is False:
        return await bot.send_message(chat_id=group[0], text='⭕ 调用emby api失败')

    # print(users)
    for user in users:
        # 数据库先找
        e = sql_get_emby(tg=user["Name"])
        if e is None:
            continue

        elif e.lv == 'c':
            # print(e.tg)
            try:
                ac_date = convert_to_beijing_time(user["LastActivityDate"])
            except KeyError:
                ac_date = "None"
            finally:
                if ac_date == "None" or ac_date + timedelta(days=15) < now:
                    if await emby.emby_del(id=e.embyid):
                        await bot.send_message(chat_id=group[0],
                                               text=f'**🔋#活跃检测** - [{e.name}](tg://user?id={e.tg})\n#id{e.tg} 禁用后未解禁，已执行删除。')
                        LOGGER.info(f"【活跃检测】- 删除账户 {user['Name']} #id{e.tg}")
                    else:
                        await bot.send_message(chat_id=group[0],
                                               text=f'**🔋#活跃检测** - [{e.name}](tg://user?id={e.tg})\n#id{e.tg} 禁用后未解禁，执行删除失败。')
                        LOGGER.info(f"【活跃检测】- 删除账户失败 {user['Name']} #id{e.tg}")

        elif e.lv == 'b':
            try:
                ac_date = convert_to_beijing_time(user["LastActivityDate"])
                # print(e.name, ac_date, now)
                if ac_date + timedelta(days=21) < now:
                    if await emby.emby_change_policy(id=user["Id"], method=True):
                        sql_update_emby(Emby.embyid == user["Id"], lv='c')
                        await bot.send_message(chat_id=group[0],
                                               text=f"**🔋#活跃检测** - [{user['Name']}](tg://user?id={e.tg})\n#id{e.tg} 21天未活跃，禁用")
                        LOGGER.info(f"【活跃检测】- 禁用账户 {user['Name']} #id{e.tg}：21天未活跃")
                    else:
                        await bot.send_message(chat_id=group[0],
                                               text=f"**🎂#活跃检测** - [{user['Name']}](tg://user?id={e.tg})\n21天未活跃，禁用失败啦！检查emby连通性")
                        LOGGER.info(f"【活跃检测】- 禁用账户 {user['Name']} #id{e.tg}：禁用失败啦！检查emby连通性")
            except KeyError:
                if await emby.emby_change_policy(id=user["Id"], method=True):
                    sql_update_emby(Emby.embyid == user["Id"], lv='c')
                    await bot.send_message(chat_id=group[0],
                                           text=f"**🔋#活跃检测** - [{user['Name']}](tg://user?id={e.tg})\n#id{e.tg} 注册后未活跃，禁用")
                    LOGGER.info(f"【活跃检测】- 禁用账户 {user['Name']} #id{e.tg}：注册后未活跃禁用")
                else:
                    await bot.send_message(chat_id=group[0],
                                           text=f"**🎂#活跃检测** - [{user['Name']}](tg://user?id={e.tg})\n#id{e.tg} 注册后未活跃，禁用失败啦！检查emby连通性")
                    LOGGER.info(f"【活跃检测】- 禁用账户 {user['Name']} #id{e.tg}：禁用失败啦！检查emby连通性")


@bot.on_message(filters.command('low_activity', prefixes) & admins_on_filter)
async def run_low_ac(_, msg):
    await deleteMessage(msg)
    send = await msg.reply(f"⭕ 不活跃检测运行ing···")
    await check_low_activity()
    await send.delete()
