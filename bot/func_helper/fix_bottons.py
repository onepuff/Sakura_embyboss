from cacheout import Cache
from pykeyboard import InlineKeyboard, InlineButton
from pyrogram.types import InlineKeyboardMarkup
from pyromod.helpers import ikb, array_chunk
from bot import chanel, main_group, bot_name, tz_id, tz_ad, tz_api, _open, user_buy, sakura_b, schedall
from bot.func_helper import nezha_res
from bot.func_helper.emby import emby
from bot.func_helper.utils import judge_admins, members_info

cache = Cache()

"""start面板 ↓"""


def judge_start_ikb(uid: int) -> InlineKeyboardMarkup:
    """
    start面板按钮
    :param uid:
    :return:
    """
    d = [['️👥 用户功能', 'members'], ['🌐 服务器', 'server'], ['🎟️ 使用注册码', 'exchange']]  # ['🏪 商店', 'store_all']
    if _open["checkin"]:
        d.append([f'🎯 签到', 'checkin'])
    if user_buy["stat"] == "y":
        d.append(user_buy["button"])
    lines = array_chunk(d, 2)
    if judge_admins(uid):
        lines.append([['👮🏻‍♂️ admin', 'manage']])
    keyword = ikb(lines)
    return keyword


@cache.memoize(ttl=600)
def buy_sth_ikb() -> InlineKeyboardMarkup:
    """
    购买按钮
    :return:
    """
    d = [[user_buy["button"]], [["💫 回到首页", "back_start"]]]
    return ikb(d)


# un_group_answer
group_f = ikb([[('点击我(●ˇ∀ˇ●)', f't.me/{bot_name}', 'url')]])
# un in group
judge_group_ikb = ikb([[('🌟 频道入口 ', f't.me/{chanel}', 'url'),
                        ('💫 群组入口', f't.me/{main_group}', 'url')],
                       [('❌ 关闭消息', 'closeit')]])

"""members ↓"""


def members_ikb(emby=False) -> InlineKeyboardMarkup:
    """
    判断用户面板
    :param emby:
    :return:
    """
    if emby is True:
        return ikb([[('🏪 兑换商店', 'storeall'), ('🗑️ 删除账号', 'delme')],
                    [('🎬 显示/隐藏', 'embyblock'), ('⭕ 重置密码', 'reset')],
                    [('♻️ 主界面', 'back_start')]])
    else:
        return ikb(
            [[('👑 创建账户', 'create'), ('⭕ 改/绑账户', 'changetg')], [('🎟️ 使用注册码', 'exchange')],
             [('♻️ 主界面', 'back_start')]])


back_start_ikb = ikb([[('💫 回到首页', 'back_start')]])
back_members_ikb = ikb([[('💨 返回', 'members')]])
re_create_ikb = ikb([[('🍥 重新输入', 'create'), ('💫 用户主页', 'members')]])
re_changetg_ikb = ikb([[('✨ 重新输入', 'changetg'), ('💫 用户主页', 'members')]])
re_delme_ikb = ikb([[('♻️ 重试', 'delme')], [('🔙 返回', 'members')]])
re_reset_ikb = ikb([[('♻️ 重试', 'reset')], [('🔙 返回', 'members')]])
re_exchange_b_ikb = ikb([[('♻️ 重试', 'exchange')], [('🔙 返回', 'members')]])


def store_ikb():
    return ikb([[(f'⚖️ {sakura_b}续期', 'store-renew'), (f'♾️ 兑换白名单', 'store-whitelist')],
                [(f'🎟️ 兑换注册码', 'store-invite'), (f'🔍 查询注册码', 'store-query')], [(f'❌ 取消', 'members')]])


re_store_renew = ikb([[('✨ 重新输入', 'changetg'), ('💫 取消输入', 'storeall')]])


def del_me_ikb(embyid) -> InlineKeyboardMarkup:
    return ikb([[('🎯 确定', f'delemby-{embyid}')], [('🔙 取消', 'members')]])


def emby_block_ikb(embyid) -> InlineKeyboardMarkup:
    return ikb(
        [[("✔️️ - 显示", f"emby_unblock-{embyid}"), ("✖️ - 隐藏", f"emby_block-{embyid}")], [("🔙 返回", "members")]])


user_emby_block_ikb = ikb([[('✅ 已隐藏', 'members')]])
user_emby_unblock_ikb = ikb([[('❎ 已显示', 'members')]])

"""server ↓"""


@cache.memoize(ttl=120)
async def cr_page_server():
    """
    翻页服务器面板
    :return:
    """
    a = {}
    b = []
    for x in tz_id:
        # l = a.get(x, {})  获取或创建一个空字典
        name, sever = nezha_res.sever_info(tz_ad, tz_api, x)
        b.append([f'{name}', f'server:{x}'])
        a[x] = f"{sever}"
    if len(tz_id) == 0:
        return ikb([[('🔙 - 用户', 'members'), ('❌ - 关闭', 'closeit')]]), ''
    elif len(tz_id) == 1:
        return ikb([[('🔙 - 用户', 'members'), ('❌ - 关闭', 'closeit')]]), a[tz_id[0]]
    else:
        lines = array_chunk(b, 3)
        lines.append([['🔙 - 用户', 'members'], ['❌ - 关闭', 'closeit']])
        b = ikb(lines)
        # b是键盘，a是sever
        return b, a


"""admins ↓"""

gm_ikb_content = ikb([[('⭕ 注册状态', 'open-menu'), ('🎟️ 生成注册', 'cr_link')],
                      [('💊 查询注册', 'ch_link'), ('🏬 兑换设置', 'set_renew')],
                      [('🌏 定时', 'schedall'), ('🕹️ 主界面', 'back_start'), ('其他 🪟', 'back_config')]])


def open_menu_ikb(openstats, timingstats) -> InlineKeyboardMarkup:
    return ikb([[(f'{openstats} 自由注册', 'open_stat'), (f'{timingstats} 定时注册', 'open_timing')],
                [('⭕ 注册限制', 'all_user_limit')], [('🌟 返回上一级', 'manage')]])


gog_rester_ikb = ikb([[('( •̀ ω •́ )y 点击注册', f't.me/{bot_name}', 'url')]])
back_free_ikb = ikb([[('🔙 返回上一级', 'open-menu')]])
back_open_menu_ikb = ikb([[('🪪 重新定时', 'open_timing'), ('🔙 注册状态', 'open-menu')]])
re_cr_link_ikb = ikb([[('♻️ 继续创建', 'cr_link'), ('🎗️ 返回主页', 'manage')]])
close_it_ikb = ikb([[('❌ - Close', 'closeit')]])


def ch_link_ikb(ls: list) -> InlineKeyboardMarkup:
    lines = array_chunk(ls, 2)
    lines.append([["💫 回到首页", "manage"]])
    return ikb(lines)


def date_ikb(i) -> InlineKeyboardMarkup:
    return ikb([[('🌘 - 月', f'register_mon-{i}'), ('🌗 - 季', f'register_sea-{i}'),
                 ('🌖 - 半年', f'register_half-{i}')],
                [('🌕 - 年', f'register_year-{i}'), ('🎟️ - 已用', f'register_used-{i}')], [('🔙 - 返回', 'ch_link')]])


# 翻页按钮
async def cr_paginate(i, j, n) -> InlineKeyboardMarkup:
    # i 总数，j是当前页数，n是传入的检索类型num，如30天
    keyboard = InlineKeyboard()
    keyboard.paginate(i, j, f'pagination_keyboard:{{number}}-{i}-{n}')
    keyboard.row(
        InlineButton('❌ - Close', 'closeit')
    )
    return keyboard


def cr_renew_ikb():
    checkin = '✔️' if _open["checkin"] else '❌'
    exchange = '✔️' if _open["exchange"] else '❌'
    whitelist = '✔️' if _open["whitelist"] else '❌'
    invite = '✔️' if _open["invite"] else '❌'
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(InlineButton(f'{checkin} 签到', f'set_renew-checkin'),
                 InlineButton(f'{exchange} 续期', f'set_renew-exchange'),
                 InlineButton(f'{whitelist} 白名单', f'set_renew-whitelist'),
                 InlineButton(f'{invite} 邀请码', f'set_renew-invite'))
    keyboard.row(InlineButton(f'◀ 返回', 'manage'))
    return keyboard


""" config_panel ↓"""


def config_preparation() -> InlineKeyboardMarkup:
    code = '✅' if _open["allow_code"] == 'y' else '❎'
    buy_stat = '✅' if user_buy["stat"] == 'y' else '❎'
    leave_ban = '✅' if _open["leave_ban"] else '❎'
    keyboard = ikb(
        [[('📄 导出日志', 'log_out'), ('📌 设置探针', 'set_tz')],
         [('💠 emby线路', 'set_line'), ('🎬 显/隐指定库', 'set_block')],
         [(f'{code} 注册码续期', 'open_allow_code'), (f'{buy_stat} 开关购买', 'set_buy'),
          (f'{leave_ban} 退群封禁', 'leave_ban')],
         [('🔙 返回', 'manage')]])
    return keyboard


back_config_p_ikb = ikb([[("🎮  ️返回主控", "back_config")]])


def back_set_ikb(method) -> InlineKeyboardMarkup:
    return ikb([[("♻️ 重新设置", f"{method}"), ("🔙 返回主页", "back_config")]])


def try_set_buy(ls: list) -> InlineKeyboardMarkup:
    d = [[ls], [["✅ 体验结束返回", "back_config"]]]
    return ikb(d)


""" other """
register_code_ikb = ikb([[('🎟️ 注册', 'create'), ('⭕ 取消', 'closeit')]])
dp_g_ikb = ikb([[("🈺 ╰(￣ω￣ｏ)", "t.me/Aaaaa_su", "url")]])


async def cr_kk_ikb(uid, first):
    text = ''
    text1 = ''
    keyboard = InlineKeyboard(row_width=2)
    data = await members_info(uid)
    if data is None:
        text += f'**· 🆔 TG** ：[{first}](tg://user?id={uid})\n数据库中没有此ID。ta 还没有私聊过我'
    else:
        name, lv, ex, us, embyid, pwd2 = data
        if name != '无账户信息':
            ban = "🌟 解除禁用" if lv == "已禁用" else '💢 禁用账户'
            keyboard.add(InlineButton(ban, f'user_ban-{uid}'), InlineButton('⚠️ 删除账户', f'closeemby-{uid}'))
            try:
                rst = await emby.emby_cust_commit(user_id=embyid, days=30)
                last_time = rst[0][0]
                toltime = rst[0][1]
                text1 = f"**· 🔋 上次活动** | {last_time.split('.')[0]}\n" \
                        f"**· 📅 过去30天** | {toltime} min"
            except (TypeError, IndexError, ValueError):
                text1 = f"**· 📅 过去30天未有记录**"
        else:
            keyboard.add(InlineButton('✨ 赠送资格', f'gift-{uid}'))
        # if ex != '无账户信息' and ex != '+ ∞': ex = (ex - Now).days + '天'
        text += f"**· 🍉 TG名称** | [{first}](tg://user?id={uid})\n" \
                f"**· 🍒 TG-ID** | `{uid}`\n" \
                f"**· 🍓 当前状态** | {lv}\n" \
                f"**· 🍥 积分{sakura_b}** | {us[0]} · {us[1]}\n" \
                f"**· 💠 账号名称** | {name}\n" \
                f"**· 🚨 到期时间** | **{ex}**\n"
        text += text1
    keyboard.row(InlineButton('🚫 踢出并封禁', f'fuckoff-{uid}'), InlineButton('❌ 删除消息', f'closeit'))
    return text, keyboard


""" sched_panel ↓"""


def sched_buttons():
    dayrank = '✅' if schedall["dayrank"] else '❎'
    weekrank = '✅' if schedall["weekrank"] else '❎'
    dayplayrank = '✅' if schedall["dayplayrank"] else '❎'
    weekplayrank = '✅' if schedall["weekplayrank"] else '❎'
    check_ex = '✅' if schedall["check_ex"] else '❎'
    low_activity = '✅' if schedall["low_activity"] else '❎'
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(InlineButton(f'{dayrank} 播放日榜', f'sched-dayrank'),
                 InlineButton(f'{weekrank} 播放周榜', f'sched-weekrank'),
                 InlineButton(f'{dayplayrank} 看片日榜', f'sched-dayplayrank'),
                 InlineButton(f'{weekplayrank} 看片周榜', f'sched-weekplayrank'),
                 InlineButton(f'{check_ex} 到期保号', f'sched-check_ex'),
                 InlineButton(f'{low_activity} 活跃保号', f'sched-low_activity')
                 )
    keyboard.row(InlineButton(f'🫧 返回', 'manage'))
    return keyboard


""" checkin 按钮↓"""


def shici_button(ls: list):
    shici = []
    for l in ls:
        l = [l, f'checkin-{l}']
        shici.append(l)
    # print(shici)
    lines = array_chunk(shici, 4)
    return ikb(lines)


checkin_button = ikb([[('🔋 重新签到', 'checkin'), ('🎮 返回主页', 'back_start')]])
