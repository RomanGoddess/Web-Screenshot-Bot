# (c) AlenPaulVarghese
# -*- coding: utf-8 -*-

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from pyrogram import (
    Client,
    filters
)
from plugins.logger import logging  # pylint:disable=import-error
import os

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(10)

BLACKLIST = ['drive.google.com', 'tor.checker.in', 'youtube.com', 'youtu.be']
HOME = InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Format - PDF', callback_data='format')],
            [InlineKeyboardButton(text='Page - Full', callback_data="page")],
            # [InlineKeyboardButton(text='Landscape', callback_data="orientation")],
            [InlineKeyboardButton(text='show additional options ˅', callback_data="options")],
            [InlineKeyboardButton(text='▫️ start render ▫️', callback_data="render")],
            [InlineKeyboardButton(text='cancel', callback_data="cancel")]
                            ])


@Client.on_message(filters.command(["start"]))
async def start(_: Client, message: Message) -> None:
    LOGGER.debug(f"USED_CMD --> /start command >> @{message.from_user.username}")
    await message.reply_text(
        f"<b>Hello {message.from_user.first_name} 👋,\n"
        "I Can Render Website Of A Given Link To Either 𝗣𝗗𝗙 or 𝗣𝗡𝗚/𝗝𝗣𝗘𝗚</b>",
        quote=True,
        reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("𝗔𝗕𝗢𝗨𝗧 🤔", callback_data="about_cb")
            ]
        ])
    )


@Client.on_message(filters.command(["about", 'feedback']))
async def feedback(_: Client, message: Message) -> None:
    LOGGER.debug(f"USED_CMD --> /about command >> @{message.from_user.username}")
    await message.reply_text(
        text="**⭕️ My Name : 𝗪𝗘𝗕 𝗠𝗨𝗡𝗖𝗛 𝗕𝗢𝗧**\n\n**⭕️ Language :** `Python3`\n\n**⭕️ Library :** **Pyrogram Asyncio 0.16.1**\n\n**⭕️ Source Code : 👉** [Click Here](https://t.me/NoSourceCode)**",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("𝗖𝗥𝗘𝗔𝗧𝗢𝗥 🧕", url="https://t.me/Iggie"),
                InlineKeyboardButton("𝗚𝗥𝗢𝗨𝗣 👥", url="https://t.me/LeechZone")],
            [InlineKeyboardButton(
                "📳 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗡𝗗𝗥𝗢𝗜𝗗 𝗔𝗣𝗣𝗦 📳",
                url="https://t.me/joinchat/AAAAAE-44AkxSyqIMj1tdQ")]
            ])
    )


@Client.on_message(filters.command(["delete"]) & filters.private)
async def delete(_: Client, message: Message) -> None:
    LOGGER.debug(f"USED_CMD --> /delete command >> @{message.from_user.username}")
    try:
        sudo_user = int(os.environ["SUDO_USER"])
    except Exception:
        LOGGER.debug('DEL__CMD --> status failed >> user not a sudo')
        return
    if message.from_user.id == sudo_user:
        random_message = await message.reply_text('Processing')
        LOGGER.debug('DEL__CMD --> status pending >> sudo user found processing')
        if os.path.isdir('./FILES/'):
            with open('walk.txt', 'w') as writer:
                for root, dirs, files in os.walk('./FILES/', topdown=False):
                    writer.write(str(root)+'\n\n'+str(dirs)+'\n\n'+str(files))
            if os.path.isfile('walk.txt'):
                LOGGER.debug('DEL__CMD --> status pending >> sending file')
                await message.reply_document(
                    document='walk.txt',
                )
                await random_message.delete()
                os.remove('walk.txt')
                LOGGER.debug('DEL__CMD --> status pending >> waiting for user confirmation')
                await message.reply_text(
                    text='Do you want to delete?',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text='Yes', callback_data='deleteyes')],
                        [InlineKeyboardButton(text='No', callback_data='deleteno')],
                    ])
                    )
    else:
        return


@Client.on_message(filters.command(['debug', 'log']) & filters.private)
async def send_log(_: Client, message: Message) -> None:
    LOGGER.debug(f"USED_CMD --> /debug command >> @{message.from_user.username}")
    try:
        sudo_user = int(os.environ["SUDO_USER"])
        if sudo_user != message.chat.id:
            raise Exception
    except Exception:
        LOGGER.debug('LOG__CMD --> status failed >> user not a sudo')
        return
    if os.path.exists('debug.log'):
        await message.reply_document(
            'debug.log'
        )
        LOGGER.debug('LOG__CMD --> status sucess >> log send to the sudo_user')
    else:
        await message.reply_text("file not found")
