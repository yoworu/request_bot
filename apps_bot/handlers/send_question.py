from aiogram import Router, F, Bot, html
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest


from middlewares.check_registration import CheckRegistration
from states.question import QuestionSG
from config import bot_config

question_router = Router()
question_router.message.middleware(CheckRegistration())


@question_router.message(Command('start'))
async def cmd_start_handler(message: Message):
    await message.answer('/question')


@question_router.message(Command('question'))
async def question_command_handler(message: Message, state: FSMContext):
    await message.answer("Send question")
    await state.set_state(QuestionSG.waiting_for_question)
    
    
@question_router.message(QuestionSG.waiting_for_question, F.text.func(len) > 50)
async def uncorrect_question_handler(message: Message):
    await message.answer('Question shouldn\'t be so long')


@question_router.message(QuestionSG.waiting_for_question)
async def correct_question_handler(message: Message, 
                                   state: FSMContext,
                                   bot: Bot):
    try:
        username = message.from_user.username
    except TelegramBadRequest:
        username = message.from_user.id
        
    result_text = (
        html.bold(f'Question from @{username}\n\n') + html.quote(message.text)
    )
    try:
        await bot.send_message(chat_id=bot_config.channel_id,
                               text=result_text,
                               parse_mode='html')    
    except TelegramBadRequest:
        await message.answer('Invalid channel id')
    else:
        await state.clear()