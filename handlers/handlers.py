from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from keyboards.keyboards import PaginationKeyboard, PaginationKbForHis, StartKb
from states.states import FSMPagination, HisStage
from LEXICON import btns_clbks, lighthouses, texts
from utils.methods import change_mayak, get_data, prepare_book

import sqlite3
import os


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def command_start_pressed(message: Message, state: FSMContext):
    await message.answer(text=texts['greetings'],
                         reply_markup=StartKb())
    


@router.callback_query(F.data == btns_clbks['mayaki_btn'])
async def mayaki_btn_process(callback: CallbackQuery, state: FSMContext, all_media_dir):
    data_for_ch = await get_data(1)
    data_for_ch = data_for_ch[0]
    new_photo = FSInputFile(path=os.path.join(all_media_dir, data_for_ch[2]))
    
    await callback.message.answer_photo(photo=new_photo,
                               caption=data_for_ch[1], 
                         reply_markup=PaginationKeyboard(url=data_for_ch[3]))  
    await callback.message.delete()  
    await state.set_state(FSMPagination.page)
    await state.update_data(page=1)
    
    data = await state.get_data()
    print(data['page'])



@router.message(CommandStart(), ~StateFilter(default_state))
async def not_start(message: Message):
    await message.delete()


@router.callback_query(F.data == btns_clbks['rht_btn'], StateFilter(FSMPagination.page))
async def right_btn_pressed(callback: CallbackQuery, pages, state: FSMContext, bot: Bot, all_media_dir):
    data = await state.get_data()
    
    if data['page'] == pages:
        await state.update_data(page=1)
    else:
        await state.update_data(page=data['page']+1)
    
    data = await state.get_data()
    data_for_ch = await get_data(m_id=int(data['page']))
    data_for_ch = data_for_ch[0]
    
    await change_mayak(name=data_for_ch[1], 
                       url=data_for_ch[3], 
                       file=data_for_ch[2], 
                       all_media_dir=all_media_dir, 
                       callback=callback)
    
    print(data['page'])


@router.callback_query(F.data == btns_clbks['lft_btn'], StateFilter(FSMPagination.page))
async def left_btn_pressed(callback: CallbackQuery, pages, state: FSMContext, all_media_dir):
    data = await state.get_data()
    
    if data['page'] == 1:
        await state.update_data(page=pages)
    else:
        await state.update_data(page=data['page']-1)
    
    data = await state.get_data()
    data_for_ch = await get_data(m_id=int(data['page']))
    data_for_ch = data_for_ch[0]
    
    await change_mayak(name=data_for_ch[1], 
                       url=data_for_ch[3], 
                       file=data_for_ch[2], 
                       all_media_dir=all_media_dir, 
                       callback=callback)
    
    print(data['page'])


@router.callback_query(F.data == btns_clbks['to_know_btn'])
async def to_know_btn_pressed(callback: CallbackQuery, state: FSMContext, text_dir):
    data = await state.get_data()
    m_id = int(data['page'])
    data_for_his = await get_data(m_id=m_id)
    
    await state.set_state(HisStage.book)
    await state.update_data(page=1, book=prepare_book(path=os.path.join(text_dir, data_for_his[0][4])), m_id=m_id)

    data_for_ans = await state.get_data()
    
    await callback.message.answer(text=data_for_ans['book'][data_for_ans['page']].replace('\n', ''), 
                                  reply_markup=PaginationKbForHis(page=data_for_ans['page']))
    await callback.message.delete()


@router.callback_query(F.data == btns_clbks['rht_btn'], StateFilter(HisStage.book))
async def right_his_btn_pressed(callback: CallbackQuery, state: FSMContext):
    data_for_ans = await state.get_data()
    
    if data_for_ans['page'] == len(data_for_ans['book']):
        await state.update_data(page=1, book=data_for_ans['book'])
        page = 1
    else:
        await state.update_data(page=data_for_ans['page']+1, book=data_for_ans['book'])
        page = data_for_ans['page']+1
    book = data_for_ans['book']
    
    await callback.message.edit_text(text=book[page], reply_markup=PaginationKbForHis(page=page))


@router.callback_query(F.data == btns_clbks['lft_btn'], StateFilter(HisStage.book))
async def right_his_btn_pressed(callback: CallbackQuery, state: FSMContext):
    data_for_ans = await state.get_data()
    
    if data_for_ans['page'] == 1:
        await state.update_data(page=len(data_for_ans['book']), book=data_for_ans['book'])
        page = len(data_for_ans['book'])
    else:
        await state.update_data(page=data_for_ans['page']-1, book=data_for_ans['book'])
        page = data_for_ans['page']-1
    book = data_for_ans['book']
    
    await callback.message.edit_text(text=book[page], reply_markup=PaginationKbForHis(page=page))


@router.callback_query(F.data == btns_clbks['back_btn'], StateFilter(HisStage.book, FSMPagination.page))
async def back_btn_pressed(callback: CallbackQuery, state: FSMContext, all_media_dir):
    data = await state.get_data()
    data_for_ch = await get_data(data['m_id'])
    data_for_ch = data_for_ch[0]
    new_photo = FSInputFile(path=os.path.join(all_media_dir, data_for_ch[2]))
    
    await callback.message.answer_photo(photo=new_photo,
                               caption=data_for_ch[1], 
                         reply_markup=PaginationKeyboard(url=data_for_ch[3]))
    await callback.message.delete()   
    await state.set_state(FSMPagination.page)
    await state.update_data(page=data['m_id'])
    
    data = await state.get_data()
    print(data['page'])


@router.message()
async def else_text(message: Message):
    await message.delete()