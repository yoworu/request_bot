from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


from states.registration import RegSG
from filters.name_validation import IsValidName
from db.operations import add_user

reg_router = Router(name='registration')



@reg_router.message(Command('registration'))
async def registration_command_handler(message: Message, state: FSMContext):
    await message.answer('Send first name')
    await state.set_state(RegSG.first_name)
    
    
@reg_router.message(IsValidName(), RegSG.first_name)
async def first_name_handler(message: Message, state: FSMContext):
    await message.answer('Send last name')
    await state.update_data(first_name=message.text)
    await state.set_state(RegSG.last_name)
    
    
@reg_router.message(IsValidName(), RegSG.last_name)
async def last_name_handler(message: Message, state: FSMContext):
    await message.answer('Send surname')
    await state.update_data(last_name=message.text)
    await state.set_state(RegSG.middle_name)
    

@reg_router.message(IsValidName(), RegSG.middle_name)
async def middle_name_handler(message: Message,
                              state: FSMContext,
                              async_session: async_sessionmaker[AsyncSession]):
    await message.answer('Done')
    state_data = await state.get_data()
    
    first_name = state_data['first_name']
    last_name = state_data['last_name']
    middle_name = message.text
    
    await add_user(async_session,
                   message.from_user.id,
                   first_name,
                   last_name,
                   middle_name)
    
    
    
    
    