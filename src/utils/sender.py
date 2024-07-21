import asyncio
from typing import Dict, Union, List

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession


def generate_keyboard(
        btn_text: str = None,
        btn_url: str = None
) -> Union[InlineKeyboardMarkup, None]:
    btn_build = InlineKeyboardBuilder()
    btn_build.row(
        InlineKeyboardButton(
            text=btn_text,
            url=btn_url
        )
    )
    return btn_build.as_markup()


async def send_preview_with_keyboard(
        msg: Message,
        photo: str = None,
        text: str = "",
        btn_text: str = None,
        btn_url: str = None
) -> int:
    keyboard = generate_keyboard(btn_text, btn_url)
    send_message = await msg.answer_photo(caption=text, photo=photo, reply_markup=keyboard)
    return send_message.message_id


async def send_preview(
        message: Message,
        data: Dict
) -> int:
    message_id = await send_preview_with_keyboard(
        message,
        data['msg_photo'],
        data["msg_text"],
        data["btn_text"],
        data["btn_url"]
    )
    return message_id


async def send_mail(session : AsyncSession,
                    bot: Bot,
                    user_id: int,
                    from_chat_id: int,
                    message_id: int,
                    keyboard:InlineKeyboardMarkup = None
) -> bool:
    try:
        await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=message_id, reply_markup=keyboard)
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return await send_mail(session, bot, user_id, from_chat_id,message_id, keyboard)
    except Exception as e:
        print(e)
        return False
    return True

async def start_sender(
        session : AsyncSession,
        bot : Bot,
        data : Dict,
        user_ids : List[int],
        from_chat_id : int,
        message_id
) -> int:
    keyboard = generate_keyboard(data['btn_text'], data['btn_url'])
    count = 0
    for u_id in user_ids:
        if await send_mail(session, bot, u_id, from_chat_id,message_id, keyboard):
            count += 1
        await asyncio.sleep(0.05)
    return count