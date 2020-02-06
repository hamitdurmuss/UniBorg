"""Log PMs
Check https://t.me/tgbeta/3505"""
import asyncio
import logging
import os
import sys
import re
from telethon import events
from telethon.tl import functions, types
from telethon.tl.types import Channel, Chat, User

from sample_config import Config
from uniborg.util import admin_cmd

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARN)

global NO_PM_LOG_USERS
NO_PM_LOG_USERS = []

@borg.on(events.NewMessage(incoming=True, func=lambda e: e.is_group ))
async def monito_p_m_s(event):
    # me = await borg.get_me()
    # print(me.id)
    # if  event.text == ".loggroups":
    
    link_detect = re.findall(r'([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])',event.message.message)
    # print(link_detect)
    # print("logging success")
    # await event.edit("loggin success")
    sender = await event.get_sender()
    if Config.NC_LOG_P_M_S and not sender.bot:
        chat = await event.get_chat()
        if chat.id not in NO_PM_LOG_USERS and chat.id != borg.uid:
            try:
                if link_detect:
                    e = await client.get_input_entity(Config.PM_LOGGR_BOT_API_ID)
                    # print(event.message.media)
                    fwd_message = await borg.forward_messages(
                        e,
                        event.message,
                        silent=True
                    )
            except Exception as e:
                # logger.warn(str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e) 


@borg.on(events.NewMessage(pattern="nolog ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if Config.NC_LOG_P_M_S:
        if event.is_group:
            if chat.id not in NO_PM_LOG_USERS:
                NO_PM_LOG_USERS.append(chat.id)
                await event.edit("Won't Log Messages from this chat")
                await asyncio.sleep(3)
                await event.delete()
