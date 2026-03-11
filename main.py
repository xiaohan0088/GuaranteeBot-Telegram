import asyncio
import logging
import re
import os
from datetime import datetime
from typing import Union
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramAPIError
import config
from database import Database
from utils import validate_auth, save_video, delete_video, get_video_path, periodic_auth_check, is_auth_valid, set_auth_valid
logging.basicConfig(level=logging.INFO)
OO00OOOOO00O = Bot(token=config.BOT_TOKEN)
OO00O0O00O00 = MemoryStorage()
O0O0OOOOO0OO = Dispatcher(storage=OO00O0O00O00)
O0O0O0O0OOO0 = Database()

class ConfigStates(StatesGroup):
    waiting_guarantee_name = State()
    waiting_yq_video = State()
    waiting_ty_video = State()
    waiting_buttons = State()

async def O00O00O0OO0O(O00OO0O0O000: int, OO000000OOOO: int) -> bool:
    try:
        O000000O00O0 = await OO00OOOOO00O.get_chat_member(O00OO0O0O000, OO000000OOOO)
        return O000000O00O0.status in ['administrator', 'creator']
    except:
        return False

async def OO0000O0000O(O0000OO0OO00: int) -> bool:
    try:
        OO0OOOO000OO = await OO00OOOOO00O.get_chat_member(O0000OO0OO00, OO00OOOOO00O.id)
        return OO0OOOO000OO.status in ['administrator', 'creator']
    except:
        return False

def O00O00OO0OO0(O00OOO0O0O0O: int) -> bool:
    return O00OOO0O0O0O in config.ADMIN_IDS

def OO00OOOO0000(OO000OOO0OOO: int) -> str:
    return '⭐️' * max(1, min(5, OO000OOO0OOO))

async def O0O0000OO0O0(OOO00O00O00O: types.Chat) -> str:
    if OOO00O00O00O.username:
        return f'https://t.me/{OOO00O00O00O.username}'
    try:
        O0OO00OO0O00 = await OO00OOOOO00O.create_chat_invite_link(OOO00O00O00O.id)
        return O0OO00OO0O00.invite_link
    except TelegramAPIError:
        return ''

async def O0OOOO00O0OO(OOO0O0OOOOO0: int, OO0O0OOOOO0O: bool):
    if OO0O0OOOOO0O:
        OOOO00OOO000 = ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True)
    else:
        OOOO00OOO000 = ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_polls=False, can_send_other_messages=False, can_add_web_page_previews=False)
    try:
        await OO00OOOOO00O.set_chat_permissions(OOO0O0OOOOO0, OOOO00OOO000)
    except Exception as e:
        logging.error(f'Failed to set permissions in {OOO0O0OOOOO0}: {e}')

def OOOOOO0OOOOO(O0OO00O000O0: dict, O0OO0OOO000O: str) -> tuple:
    if O0OO00O000O0['remaining_deposit'] >= O0OO00O000O0['deposit']:
        OO00OOOOOO00 = '✅未超押'
    else:
        OO00OOOOOO00 = '❌超押'
    OO00O0OO00OO = OO00OOOO0000(O0OO00O000O0['stars'])
    O0OO0O000OO0 = f"tg://user?id={O0OO00O000O0['owner_id']}"
    OO0000O00O0O = f"tg://user?id={O0OO00O000O0['authorized_by']}"
    O000O0000000 = f"✅正常营业 放心交易 [官方公群]\n\n└公群UID：{O0OO00O000O0['group_id']}\n└公群星级：{OO00O0OO00OO}\n└公群编号：{O0OO00O000O0['number']}\n└公群名称：{O0OO00O000O0['group_name']}\n└押金数额：{O0OO00O000O0['deposit']}\n└剩余额度：{O0OO00O000O0['remaining_deposit']} {OO00OOOOOO00}\n└业务标签：{O0OO00O000O0['business']}\n└公群链接：<a href='{O0OO00O000O0['group_link']}'>点此处进入</a>\n└群负责人：<a href='{O0OO0O000OO0}'>{O0OO00O000O0['owner_name']}</a>\n└授权人员：<a href='{OO0000O00O0O}'>{O0OO00O000O0['authorized_by_name']}</a>"
    OOO00O000OOO = O0O0O0O0OOO0.get_buttons()
    if OOO00O000OOO:
        O0OO00O0O0O0 = InlineKeyboardBuilder()
        for O0OOO00OO00O in OOO00O000OOO:
            if len(O0OOO00OO00O) == 2:
                O0OO00O0O0O0.button(text=O0OOO00OO00O[0], url=O0OOO00OO00O[1])
        O0OO00O0O0O0.adjust(1)
        return (O000O0000000, O0OO00O0O0O0.as_markup())
    else:
        return (O000O0000000, None)

async def OO0OOO000O00(O000O00OO0OO: int, message: Message=None):
    OOO0OO00OOO0 = O0O0O0O0OOO0.get_config('guarantee_name') or '担保名称'
    OO0OOO00OO0O = f'欢迎光临【{OOO0OO00OOO0}】\n这里是 【{OOO0OO00OOO0}】官方防伪认证中心\n\n本机器人用于：\n验证公群是否为{OOO0OO00OOO0}担保公群\n查询公群上押金额/公群老板/业务员\n谨防碰瓷、冒充、骗子/野鸡担保\n\n请输入公群编号进行查询或发起远程验群选择你已经加入需要验证的群组'
    O000OO00O000 = InlineKeyboardBuilder()
    O000OO00O000.button(text='我要验群', callback_data='verify_by_number')
    if O00O00OO0OO0(O000O00OO0OO):
        O000OO00O000.button(text='配置机器人', callback_data='config_menu')
    O000OO00O000.adjust(1)
    await OO00OOOOO00O.send_message(O000O00OO0OO, OO0OOO00OO0O, reply_markup=O000OO00O000.as_markup())

async def OOOOO0O0OOOO():
    for O0O000OO00O0 in config.ADMIN_IDS:
        try:
            await OO00OOOOO00O.send_message(O0O000OO00O0, '请发送授权码以激活机器人')
        except Exception as e:
            logging.error(f'Failed to send auth request to admin {O0O000OO00O0}: {e}')

@O0O0OOOOO0OO.message.outer_middleware
@O0O0OOOOO0OO.callback_query.outer_middleware
async def OOO0OO00000O(OO0OO000OO00, OOOOO00000OO, O00O0O0O0OO0):
    if is_auth_valid():
        return await OO0OO000OO00(OOOOO00000OO, O00O0O0O0OO0)
    O0O00OOO0O0O = None
    O000000O0000 = None
    OO00000O0OOO = False
    if isinstance(OOOOO00000OO, Message):
        O0O00OOO0O0O = OOOOO00000OO.from_user.id
        O000000O0000 = OOOOO00000OO.chat.type
        OO00000O0OOO = False
    elif isinstance(OOOOO00000OO, CallbackQuery):
        O0O00OOO0O0O = OOOOO00000OO.from_user.id
        O000000O0000 = OOOOO00000OO.message.chat.type
        OO00000O0OOO = True
    if O00O00OO0OO0(O0O00OOO0O0O) and O000000O0000 == 'private':
        if OO00000O0OOO:
            await OOOOO00000OO.answer('⚠️ 请先发送授权码', show_alert=True)
            return
        elif OOOOO00000OO.text:
            return await OO0OO000OO00(OOOOO00000OO, O00O0O0O0OO0)
        else:
            return
    return

@O0O0OOOOO0OO.message(CommandStart())
async def O00000OOO0O0(OO00OOO0O00O: Message):
    if OO00OOO0O00O.chat.type != 'private':
        return
    await OO0OOO000O00(OO00OOO0O00O.chat.id, OO00OOO0O00O)

@O0O0OOOOO0OO.callback_query(F.data == 'verify_by_number')
async def OO000O0O0O00(O00O0OO0O0OO: CallbackQuery, O0O0OO0OOOO0: FSMContext):
    await O00O0OO0O0OO.message.edit_text('请发送群编号')
    await O0O0OO0OOOO0.set_state('waiting_group_number')
    await O00O0OO0O0OO.answer()

@O0O0OOOOO0OO.message(StateFilter('waiting_group_number'), F.text)
async def O0O0000OOO0O(OOO00O0OO000: Message, O0OO0OOOOOOO: FSMContext):
    OO0O0O0000O0 = OOO00O0OO000.text.strip()
    OOO0000O000O = O0O0O0O0OOO0.get_group_by_number(OO0O0O0000O0)
    if not OOO0000O000O:
        await OOO00O0OO000.reply('❌ 公群不存在 请谨慎交易')
        await O0OO0OOOOOOO.clear()
        return
    O0O0000OOO00 = O0O0O0O0OOO0.get_config('guarantee_name') or '担保名称'
    OOO00O0O00OO, O0OO0OO00OO0 = OOOOOO0OOOOO(OOO0000O000O, O0O0000OOO00)
    OO00OO000O0O = O0O0O0O0OOO0.get_config('yq_video')
    if OO00OO000O0O and os.path.exists(OO00OO000O0O):
        O0OOO0O00000 = FSInputFile(OO00OO000O0O)
        await OOO00O0OO000.answer_video(O0OOO0O00000, caption=OOO00O0O00OO, parse_mode='HTML', reply_markup=O0OO0OO00OO0)
    else:
        await OOO00O0OO000.answer(OOO00O0O00OO, parse_mode='HTML', reply_markup=O0OO0OO00OO0)
    await O0OO0OOOOOOO.clear()

@O0O0OOOOO0OO.callback_query(F.data == 'config_menu')
async def OO0OOOO00OOO(O00O0O00O0O0: CallbackQuery):
    if not O00O00OO0OO0(O00O0O00O0O0.from_user.id):
        await O00O0O00O0O0.answer('无权限')
        return
    O0O000OOO00O = InlineKeyboardBuilder()
    O0O000OOO00O.button(text='配置担保名称', callback_data='config_name')
    O0O000OOO00O.button(text='配置验群视频', callback_data='config_yq_video')
    O0O000OOO00O.button(text='配置退押视频', callback_data='config_ty_video')
    O0O000OOO00O.button(text='配置验群消息底部按钮', callback_data='config_buttons')
    O0O000OOO00O.adjust(1)
    await O00O0O00O0O0.message.edit_text('请选择配置项：', reply_markup=O0O000OOO00O.as_markup())
    await O00O0O00O0O0.answer()

@O0O0OOOOO0OO.callback_query(F.data == 'config_name')
async def OOO0OOO00O00(OOO000OOO0OO: CallbackQuery, O0O0OOO0OOO0: FSMContext):
    await OOO000OOO0OO.message.edit_text('请发送担保名称')
    await O0O0OOO0OOO0.set_state(ConfigStates.waiting_guarantee_name)
    await OOO000OOO0OO.answer()

@O0O0OOOOO0OO.message(ConfigStates.waiting_guarantee_name, F.text)
async def O0O00OO0OO0O(OOOOOOO0O000: Message, O0OO0O00OOOO: FSMContext):
    OO000O0O00O0 = OOOOOOO0O000.text.strip()
    O0O0O0O0OOO0.set_config('guarantee_name', OO000O0O00O0)
    await OOOOOOO0O000.reply('担保名称已更新')
    await O0OO0O00OOOO.clear()

@O0O0OOOOO0OO.callback_query(F.data == 'config_yq_video')
async def O00O0OO0000O(O0O0O0O0OO00: CallbackQuery, O00O00O000OO: FSMContext):
    await O0O0O0O0OO00.message.edit_text('请发送一段视频作为验群视频，或使用 /scyq 指令删除当前验群视频')
    await O00O00O000OO.set_state(ConfigStates.waiting_yq_video)
    await O0O0O0O0OO00.answer()

@O0O0OOOOO0OO.message(ConfigStates.waiting_yq_video, F.video)
async def O00O0OOO0OO0(O0OO000O0O0O: Message, O0OO00OO0000: FSMContext):
    O0OOO0OO0OOO = O0OO000O0O0O.video.file_id
    OOO00O0OO0O0 = await OO00OOOOO00O.get_file(O0OOO0OO0OOO)
    O0OOO000O00O = OOO00O0OO0O0.file_path
    OO0O0OOO0O00 = os.path.join(config.SP_DIR, 'yq_video.mp4')
    await OO00OOOOO00O.download_file(O0OOO000O00O, OO0O0OOO0O00)
    O0O0O0O0OOO0.set_config('yq_video', OO0O0OOO0O00)
    await O0OO000O0O0O.reply('验群视频已保存')
    await O0OO00OO0000.clear()

@O0O0OOOOO0OO.message(Command('scyq'))
async def OOOO0000O0OO(OOO0OOOOOOO0: Message):
    if not O00O00OO0OO0(OOO0OOOOOOO0.from_user.id):
        return
    OOO0O0OOOO0O = O0O0O0O0OOO0.get_config('yq_video')
    if OOO0O0OOOO0O and os.path.exists(OOO0O0OOOO0O):
        os.remove(OOO0O0OOOO0O)
    O0O0O0O0OOO0.delete_config('yq_video')
    await OOO0OOOOOOO0.reply('验群视频已删除')

@O0O0OOOOO0OO.callback_query(F.data == 'config_ty_video')
async def OO0O0OOOO000(OOOO000OOOOO: CallbackQuery, OOOO0OO000O0: FSMContext):
    await OOOO000OOOOO.message.edit_text('请发送一段视频作为退押视频，或使用 /scty 指令删除当前退押视频')
    await OOOO0OO000O0.set_state(ConfigStates.waiting_ty_video)
    await OOOO000OOOOO.answer()

@O0O0OOOOO0OO.message(ConfigStates.waiting_ty_video, F.video)
async def O000O0OO000O(OOOO00OOOO00: Message, OOOOOOOO00OO: FSMContext):
    O0OOO0000OO0 = OOOO00OOOO00.video.file_id
    OO0O0OO00O0O = await OO00OOOOO00O.get_file(O0OOO0000OO0)
    OOO0OO000000 = OO0O0OO00O0O.file_path
    OO0OO0000OOO = os.path.join(config.SP_DIR, 'ty_video.mp4')
    await OO00OOOOO00O.download_file(OOO0OO000000, OO0OO0000OOO)
    O0O0O0O0OOO0.set_config('ty_video', OO0OO0000OOO)
    await OOOO00OOOO00.reply('退押视频已保存')
    await OOOOOOOO00OO.clear()

@O0O0OOOOO0OO.message(Command('scty'))
async def OOOO0OO0O0O0(O000OO0OO00O: Message):
    if not O00O00OO0OO0(O000OO0OO00O.from_user.id):
        return
    O00000000O00 = O0O0O0O0OOO0.get_config('ty_video')
    if O00000000O00 and os.path.exists(O00000000O00):
        os.remove(O00000000O00)
    O0O0O0O0OOO0.delete_config('ty_video')
    await O000OO0OO00O.reply('退押视频已删除')

@O0O0OOOOO0OO.callback_query(F.data == 'config_buttons')
async def O0OOOO0OO0OO(OOOO0000OOO0: CallbackQuery, OOOO0000OO0O: FSMContext):
    await OOOO0000OOO0.message.edit_text('请按照以下格式发送按钮（每行一个，最多六个）：\n按钮1|链接\n按钮2|链接\n或发送 /scan 删除所有按钮')
    await OOOO0000OO0O.set_state(ConfigStates.waiting_buttons)
    await OOOO0000OOO0.answer()

@O0O0OOOOO0OO.message(ConfigStates.waiting_buttons, F.text)
async def OOOO0000O000(OOO0OOO0OOOO: Message, OOO00OOO00O0: FSMContext):
    if OOO0OOO0OOOO.text == '/scan':
        O0O0O0O0OOO0.delete_config('buttons')
        await OOO0OOO0OOOO.reply('所有按钮已删除')
        await OOO00OOO00O0.clear()
        return
    OO000000000O = OOO0OOO0OOOO.text.strip().split('\n')
    OOOOOO00OO00 = []
    for O0O0OO0000OO in OO000000000O:
        if '|' in O0O0OO0000OO:
            O00OO00O0OO0 = O0O0OO0000OO.split('|', 1)
            if len(O00OO00O0OO0) == 2:
                OOOOOO00OO00.append([O00OO00O0OO0[0].strip(), O00OO00O0OO0[1].strip()])
    if len(OOOOOO00OO00) > 6:
        await OOO0OOO0OOOO.reply('最多只能设置六个按钮，请重新发送')
        return
    O0O0O0O0OOO0.set_buttons(OOOOOO00OO00)
    await OOO0OOO0OOOO.reply('按钮已保存')
    await OOO00OOO00O0.clear()

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text.startswith('授权群组 '))
async def O0OOO0OO0O0O(OOO00O0O0000: Message):
    if not O00O00OO0OO0(OOO00O0O0000.from_user.id):
        return
    if not OOO00O0O0000.reply_to_message:
        await OOO00O0O0000.reply('请回复要设置为本群负责人的用户。')
        return
    O0OO0O0O0OOO = OOO00O0O0000.text.split()
    if len(O0OO0O0O0OOO) < 5:
        await OOO00O0O0000.reply('格式错误：授权群组 编号 押金 时长 业务 星级')
        return
    OO000OOOO0O0 = O0OO0O0O0OOO[1]
    try:
        O0O000O0O00O = int(O0OO0O0O0OOO[2])
        OOO0O00O0O00 = int(O0OO0O0O0OOO[3])
    except:
        await OOO00O0O0000.reply('押金和时长必须是数字')
        return
    OO00O0O0O0OO = ' '.join(O0OO0O0O0OOO[4:-1])
    try:
        O0OO000OOOO0 = int(O0OO0O0O0OOO[-1])
        if O0OO000OOOO0 < 1 or O0OO000OOOO0 > 5:
            await OOO00O0O0000.reply('星级必须在1-5之间')
            return
    except:
        await OOO00O0O0000.reply('星级必须是数字')
        return
    O0OO0O0OOO0O = OOO00O0O0000.reply_to_message.from_user
    OO00O00OO000 = O0OO0O0OOO0O.id
    O0O0O0OOOOOO = O0OO0O0OOO0O.full_name
    O00OO00000O0 = OOO00O0O0000.chat.id
    O0OO0O0O000O = OOO00O0O0000.chat.title
    OO000O0OOO00 = await O0O0000OO0O0(OOO00O0O0000.chat)
    O00OO00O00OO = O0O0O0O0OOO0.add_group(group_id=O00OO00000O0, group_name=O0OO0O0O000O, group_link=OO000O0OOO00, number=OO000OOOO0O0, deposit=O0O000O0O00O, business=OO00O0O0O0OO, stars=O0OO000OOOO0, owner_id=OO00O00OO000, owner_name=O0O0O0OOOOOO, authorized_by=OOO00O0O0000.from_user.id, authorized_by_name=OOO00O0O0000.from_user.full_name, duration=OOO0O00O0O00)
    if O00OO00O00OO:
        if await OO0000O0000O(O00OO00000O0):
            await O0OOOO00O0OO(O00OO00000O0, OO0O0OOOOO0O=True)
        await OOO00O0O0000.reply('本群授权成功 开始营业')
    else:
        await OOO00O0O0000.reply('授权失败，请检查数据库')

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text == '撤销授权')
async def O0OOO0O00OO0(OOO000000O0O: Message):
    if not O00O00OO0OO0(OOO000000O0O.from_user.id):
        return
    O00OOOO00000 = OOO000000O0O.chat.id
    O0O0O0O0OOO0.delete_group(O00OOOO00000)
    if await OO0000O0000O(O00OOOO00000):
        await O0OOOO00O0OO(O00OOOO00000, OO0O0OOOOO0O=False)
    await OOO000000O0O.reply('本群已被撤销授权 停止交易')

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text == '本群退押')
async def OO0O00O00OOO(OO0OO000O0O0: Message):
    if not O00O00OO0OO0(OO0OO000O0O0.from_user.id):
        return
    OOOO0OOOO00O = OO0OO000O0O0.chat.id
    if await OO0000O0000O(OOOO0OOOO00O):
        await O0OOOO00O0OO(OOOO0OOOO00O, OO0O0OOOOO0O=False)
    O00O00O00O00 = '本群开启退押流程 请还未完成交易的在24小时内联系担保负责人或业务员处理'
    O00O0OOOO0OO = O0O0O0O0OOO0.get_config('ty_video')
    if O00O0OOOO0OO and os.path.exists(O00O0OOOO0OO):
        O0OO00O0OOO0 = FSInputFile(O00O0OOOO0OO)
        await OO0OO000O0O0.reply_video(O0OO00O0OOO0, caption=O00O00O00O00)
    else:
        await OO0OO000O0O0.reply(O00O00O00O00)

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text.regexp('^群加押\\s+\\d+$'))
async def O0OOO0O0OO0O(OOO000O0O000: Message):
    if not O00O00OO0OO0(OOO000O0O000.from_user.id):
        return
    O0O0O000OOOO = re.match('^群加押\\s+(\\d+)$', OOO000O0O000.text)
    O000O00O00O0 = int(O0O0O000OOOO.group(1))
    OOO0O0O0000O = OOO000O0O000.chat.id
    OO00OOO0OO00 = O0O0O0O0OOO0.get_group(OOO0O0O0000O)
    if not OO00OOO0OO00:
        await OOO000O0O000.reply('本群尚未授权')
        return
    OO000OO000OO = OO00OOO0OO00['deposit']
    O00OO0OO0OO0 = OO00OOO0OO00['remaining_deposit']
    OO000O0O0O0O = OO000OO000OO + O000O00O00O0
    O00O0OOO0000 = O00OO0OO0OO0 + O000O00O00O0
    O0O0O0O0OOO0.update_group(OOO0O0O0000O, deposit=OO000O0O0O0O, remaining_deposit=O00O0OOO0000)
    await OOO000O0O000.reply(f'本群加押成功 原押金：{OO000OO000OO} 现押金：{OO000O0O0O0O}')

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text.regexp('^本群减押\\s+\\d+$'))
async def O0O0OOOO0OOO(O0O0O00OO0O0: Message):
    if not O00O00OO0OO0(O0O0O00OO0O0.from_user.id):
        return
    O000OO00O00O = re.match('^本群减押\\s+(\\d+)$', O0O0O00OO0O0.text)
    OOOOO0OO0O00 = int(O000OO00O00O.group(1))
    O0O00O00O0OO = O0O0O00OO0O0.chat.id
    OOOO00OOOOO0 = O0O0O0O0OOO0.get_group(O0O00O00O0OO)
    if not OOOO00OOOOO0:
        await O0O0O00OO0O0.reply('本群尚未授权')
        return
    OOOOOOOOOO0O = OOOO00OOOOO0['deposit']
    O0OOO0OOO000 = OOOO00OOOOO0['remaining_deposit']
    OOO00O0OOOOO = OOOOOOOOOO0O - OOOOO0OO0O00
    O0OOO0O000O0 = O0OOO0OOO000 - OOOOO0OO0O00
    if OOO00O0OOOOO < 0 or O0OOO0O000O0 < 0:
        await O0O0O00OO0O0.reply('押金不能减为负数')
        return
    O0O0O0O0OOO0.update_group(O0O00O00O0OO, deposit=OOO00O0OOOOO, remaining_deposit=O0OOO0O000O0)
    await O0O0O00OO0O0.reply(f'本群减押成功 原押金：{OOOOOOOOOO0O} 现押金：{OOO00O0OOOOO}')

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text.regexp('^群加款\\s+\\d+$'))
async def OO0OOOOO000O(O00O0OOOOO00: Message):
    if not O00O00OO0OO0(O00O0OOOOO00.from_user.id):
        return
    O0OO00OO00OO = re.match('^群加款\\s+(\\d+)$', O00O0OOOOO00.text)
    O0OOOO000OO0 = int(O0OO00OO00OO.group(1))
    OOO0O0O00O0O = O00O0OOOOO00.chat.id
    OO0O00000000 = O0O0O0O0OOO0.get_group(OOO0O0O00O0O)
    if not OO0O00000000:
        await O00O0OOOOO00.reply('本群尚未授权')
        return
    OO00OO000OOO = OO0O00000000['remaining_deposit']
    O0OOO0O0O0O0 = OO00OO000OOO + O0OOOO000OO0
    O0O0O0O0OOO0.update_group(OOO0O0O00O0O, remaining_deposit=O0OOO0O0O0O0)
    await O00O0OOOOO00.reply(f'本群加款成功 原剩余额度：{OO00OO000OOO} 现剩余额度：{O0OOO0O0O0O0}')

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text.regexp('^群扣款\\s+\\d+$'))
async def OOO0000OO00O(O0O00O000O00: Message):
    if not O00O00OO0OO0(O0O00O000O00.from_user.id):
        return
    OOOO000OO0OO = re.match('^群扣款\\s+(\\d+)$', O0O00O000O00.text)
    OOOO0O00OOO0 = int(OOOO000OO0OO.group(1))
    O0000O00OO0O = O0O00O000O00.chat.id
    OO0O0O00O000 = O0O0O0O0OOO0.get_group(O0000O00OO0O)
    if not OO0O0O00O000:
        await O0O00O000O00.reply('本群尚未授权')
        return
    OOO000O0OOOO = OO0O0O00O000['remaining_deposit']
    O0O0O0OO00O0 = OOO000O0OOOO - OOOO0O00OOO0
    if O0O0O0OO00O0 < 0:
        await O0O00O000O00.reply('扣款后剩余额度不能为负数')
        return
    O0O0O0O0OOO0.update_group(O0000O00OO0O, remaining_deposit=O0O0O0OO00O0)
    await O0O00O000O00.reply(f'本群扣款成功 原剩余额度：{OOO000O0OOOO} 现剩余额度：{O0O0O0OO00O0}')

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text.startswith('群星级 '))
async def O00O0O00000O(O0O00000OO00: Message):
    if not O00O00OO0OO0(O0O00000OO00.from_user.id):
        return
    OOO0000000OO = O0O00000OO00.text.strip()
    O00OOO0O0OO0 = OOO0000000OO[4:].strip()
    OO00OOOO0O0O = O0O00000OO00.chat.id
    OO00O00O0000 = O0O0O0O0OOO0.get_group(OO00OOOO0O0O)
    if not OO00O00O0000:
        await O0O00000OO00.reply('本群尚未授权')
        return
    O0O0O00O0OOO = OO00O00O0000['stars']
    if O00OOO0O0OO0.startswith('+'):
        try:
            O000O0OOO0O0 = int(O00OOO0O0OO0[1:])
            OOOO0OO0O00O = O0O0O00O0OOO + O000O0OOO0O0
        except:
            await O0O00000OO00.reply('格式错误，例如：群星级 +2')
            return
    elif O00OOO0O0OO0.startswith('-'):
        try:
            O000O0OOO0O0 = int(O00OOO0O0OO0[1:])
            OOOO0OO0O00O = O0O0O00O0OOO - O000O0OOO0O0
        except:
            await O0O00000OO00.reply('格式错误，例如：群星级 -1')
            return
    else:
        try:
            OOOO0OO0O00O = int(O00OOO0O0OO0)
        except:
            await O0O00000OO00.reply('格式错误，请使用 +N、-N 或直接输入数字')
            return
    OOOO0OO0O00O = max(1, min(5, OOOO0OO0O00O))
    O0O0O0O0OOO0.update_group(OO00OOOO0O0O, stars=OOOO0OO0O00O)
    await O0O00000OO00.reply(f'群星级变更 原星级：{OO00OOOO0000(O0O0O00O0OOO)} 现星级：{OO00OOOO0000(OOOO0OO0O00O)}')

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text == '上课')
async def O000OO0O0O00(OOOOOOO0O0OO: Message):
    if not (await O00O00O0OO0O(OOOOOOO0O0OO.chat.id, OOOOOOO0O0OO.from_user.id) or O00O00OO0OO0(OOOOOOO0O0OO.from_user.id)):
        return
    O0OO0O0OOOO0 = OOOOOOO0O0OO.chat.id
    OO00O00OOO0O = O0O0O0O0OOO0.get_group(O0OO0O0OOOO0)
    if not OO00O00OOO0O:
        await OOOOOOO0O0OO.reply('本群未授权，无法上课')
        return
    if await OO0000O0000O(O0OO0O0OOOO0):
        await O0OOOO00O0OO(O0OO0O0OOOO0, OO0O0OOOOO0O=True)
    await OOOOOOO0O0OO.reply('本群开始营业 正常交易')

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text == '下课')
async def O0O0OO0OO000(O00OOOOOOOOO: Message):
    if not (await O00O00O0OO0O(O00OOOOOOOOO.chat.id, O00OOOOOOOOO.from_user.id) or O00O00OO0OO0(O00OOOOOOOOO.from_user.id)):
        return
    OO0OOO0000O0 = O00OOOOOOOOO.chat.id
    O000O00O000O = O0O0O0O0OOO0.get_group(OO0OOO0000O0)
    if not O000O00O000O:
        await O00OOOOOOOOO.reply('本群未授权，无法下课')
        return
    OOO0O00OOO00 = '本群已打样 暂停交易'
    OO00OO0O00OO = O0O0O0O0OOO0.get_config('yq_video')
    if await OO0000O0000O(OO0OOO0000O0):
        await O0OOOO00O0OO(OO0OOO0000O0, OO0O0OOOOO0O=False)
    if OO00OO0O00OO and os.path.exists(OO00OO0O00OO):
        O0OOOOO00OO0 = FSInputFile(OO00OO0O00OO)
        await O00OOOOOOOOO.reply_video(O0OOOOO00OO0, caption=OOO0O00OOO00)
    else:
        await O00OOOOOOOOO.reply(OOO0O00OOO00)

@O0O0OOOOO0OO.message(F.chat.type.in_({'group', 'supergroup'}), F.text == '验群')
async def OOOO0O000O0O(O00000O00000: Message):
    OO000OO00OOO = O00000O00000.chat.id
    O00OOO00O0O0 = O0O0O0O0OOO0.get_group(OO000OO00OOO)
    OO00O0OOO00O = O0O0O0O0OOO0.get_config('guarantee_name') or '担保名称'
    if not O00OOO00O0O0:
        await O00000O00000.reply(f'❌本群不是【{OO00O0OOO00O}】担保公群 谨慎交易')
        return
    O0OO0OO00O00, OO00O0OOO0OO = OOOOOO0OOOOO(O00OOO00O0O0, OO00O0OOO00O)
    O0OO0OO0OOO0 = O0O0O0O0OOO0.get_config('yq_video')
    if O0OO0OO0OOO0 and os.path.exists(O0OO0OO0OOO0):
        OO00OOO0OO0O = FSInputFile(O0OO0OO0OOO0)
        await O00000O00000.reply_video(OO00OOO0OO0O, caption=O0OO0OO00O00, parse_mode='HTML', reply_markup=OO00O0OOO0OO)
    else:
        await O00000O00000.reply(O0OO0OO00O00, parse_mode='HTML', reply_markup=OO00O0OOO0OO)

@O0O0OOOOO0OO.message(F.chat.type == 'private', F.text)
async def OO000OO0O000(O00OOO00OOOO: Message):
    if not O00O00OO0OO0(O00OOO00OOOO.from_user.id):
        return
    if not is_auth_valid():
        OO00OO0O00O0 = O00OOO00OOOO.text.strip()
        O0OOOOO0000O, OOOO00O0OO00 = await validate_auth(OO00OO0O00O0)
        if O0OOOOO0000O:
            OOOOO0O000OO = OOOO00O0OO00.get('expiry_time', '')
            O0O0O0O0OOO0.set_auth_code(OO00OO0O00O0, OOOOO0O000OO)
            set_auth_valid(True)
            await O00OOO00OOOO.reply('✅ 授权成功，机器人已启动。')
            await OO0OOO000O00(O00OOO00OOOO.chat.id, O00OOO00OOOO)
        else:
            await O00OOO00OOOO.reply('❌ 授权码无效，请重试。')
        return

async def O00OOOOO0OO0():
    OO0OO00O0O0O = O0O0O0O0OOO0.get_auth_code()
    if OO0OO00O0O0O:
        OOOOO0OO0000, O0O000OO0OOO = await validate_auth(OO0OO00O0O0O)
        set_auth_valid(OOOOO0OO0000)
        if OOOOO0OO0000:
            OOO0OO0OO0O0 = O0O000OO0OOO.get('expiry_time', '')
            O0O0O0O0OOO0.update_auth_check(OOO0OO0OO0O0)
            logging.info('授权有效，机器人启动')
        else:
            logging.warning('授权无效，机器人将限制服务')
            await OOOOO0O0OOOO()
    else:
        set_auth_valid(False)
        logging.info('未设置授权码，等待管理员输入')
        await OOOOO0O0OOOO()
    asyncio.create_task(periodic_auth_check(OO00OOOOO00O, O0O0O0O0OOO0, config.ADMIN_IDS))

async def OOO00000O00O():
    O0O0O0O0OOO0.close()

async def O00OOOOO0O00():
    O0O0OOOOO0OO.startup.register(O00OOOOO0OO0)
    O0O0OOOOO0OO.shutdown.register(OOO00000O00O)
    await O0O0OOOOO0OO.start_polling(OO00OOOOO00O)
if __name__ == '__main__':
    asyncio.run(O00OOOOO0O00())