import logging
import os
import uuid

from aiogram import Bot, F, Router, types, flags
from aiogram.enums import ParseMode
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hcode
from aiogram.utils.chat_action import ChatActionMiddleware

from conf import api_key, user_list
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=api_key)


"""
States
"""


class States(StatesGroup):
    login = State()
    foreign = State()


"""
aiogram router
"""
router = Router()
router.message.middleware(ChatActionMiddleware())


@router.message(Command("start"))
async def greeting(
    message: Message,
    state: FSMContext,
    bot: Bot,
) -> None:
    print(user_list)
    print(message.from_user.username)
    if message.from_user.username in user_list:
        await state.set_state(States.login)
        await message.reply(f"Welcome!\nYour ID is {hcode(message.from_user.id)}")
    else:
        await state.set_state(States.foreign)
        await message.reply("You are not allowed to use this bot")


@flags.chat_action(initial_sleep=0, action=ChatAction.TYPING, interval=2)
@router.message(States.login)
async def main_loop(
    message: Message,
    state: FSMContext,
    bot: Bot,
) -> None:
    gpt_query = await simple_query(message.text)
    await message.reply(gpt_query)


"""
AI
"""


async def simple_query(user_query):
    logging.info(f"AI query received: {user_query}")
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # {
            #     "role": "system",
            #     "content": "You are a personal assistant, skilled in life planning, calendar management and personal "
            #     "improvements. Today is {dt}. You write in same language as user prompts.".format(
            #         dt=datetime.now()
            #     ),
            # },
            # {
            #     "role": "system",
            #     "content": "Format your answer as json with field user_context ()",
            # },
            {
                "role": "user",
                "content": user_query,
            },
        ],
    )
    reply_text = completion.choices[0].message.content
    return reply_text
