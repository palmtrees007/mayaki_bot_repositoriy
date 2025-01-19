from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from keyboards.keyboards import PaginationKeyboard, PaginationKbForHis, StartKb
from states.states import *
from LEXICON import btns_clbks, texts, lamps
from utils.methods import change_mayak, prepare_book
from db_for_lamps.db import *

import os


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def command_start_pressed(message: Message, state: FSMContext):
    await message.answer(text=texts['greetings'],
                         reply_markup=StartKb())
    


@router.callback_query(F.data == btns_clbks['mayaki_btn'])
async def mayaki_btn_process(callback: CallbackQuery, state: FSMContext, all_media_dir, link_dir):
    mayak: Mayak = data_for_mayaks[1]
    new_photo = FSInputFile(path=os.path.join(all_media_dir, mayak.img))
    with open(os.path.join(link_dir, mayak.map), 'r', encoding='utf-8') as link_file:
        link = link_file.read()
    
    await callback.message.answer_photo(photo=new_photo,
                               caption=mayak.caption, 
                         reply_markup=PaginationKeyboard(url=link))  
    await callback.message.delete()  
    await state.set_state(FSMPagination.page)
    await state.update_data(page=1)
    
    data = await state.get_data()
    print(data['page'])



@router.message(CommandStart(), ~StateFilter(default_state))
async def not_start(message: Message):
    await message.delete()


@router.callback_query(F.data == btns_clbks['rht_btn'], StateFilter(FSMPagination.page))
async def right_btn_pressed(callback: CallbackQuery, pages, state: FSMContext, all_media_dir, link_dir):
    data = await state.get_data()
    
    if data['page'] == pages:
        await state.update_data(page=1)
    else:
        await state.update_data(page=data['page']+1)
    
    data = await state.get_data()
    mayak: Mayak = data_for_mayaks[data['page']]
    new_photo = FSInputFile(path=os.path.join(all_media_dir, mayak.img))
    with open(os.path.join(link_dir, mayak.map), 'r', encoding='utf-8') as link_file:
        link = link_file.read()
    
    await change_mayak(name=mayak.caption, 
                       url=link, 
                       file=mayak.img, 
                       all_media_dir=all_media_dir, 
                       callback=callback)
    
    print(data['page'])


@router.callback_query(F.data == btns_clbks['lft_btn'], StateFilter(FSMPagination.page))
async def left_btn_pressed(callback: CallbackQuery, pages, state: FSMContext, all_media_dir, link_dir):
    data = await state.get_data()
    
    if data['page'] == 1:
        await state.update_data(page=pages)
    else:
        await state.update_data(page=data['page']-1)
    
    data = await state.get_data()
    mayak: Mayak = data_for_mayaks[data['page']]
    new_photo = FSInputFile(path=os.path.join(all_media_dir, mayak.img))
    with open(os.path.join(link_dir, mayak.map), 'r', encoding='utf-8') as link_file:
        link = link_file.read()
    
    await change_mayak(name=mayak.caption, 
                       url=link, 
                       file=mayak.img, 
                       all_media_dir=all_media_dir, 
                       callback=callback)
    
    print(data['page'])


@router.callback_query(F.data == btns_clbks['to_know_btn'], StateFilter(FSMPagination.page))
async def to_know_btn_pressed(callback: CallbackQuery, state: FSMContext, text_dir):
    data = await state.get_data()
    m_id = int(data['page'])
    mayak: Mayak = data_for_mayaks[m_id]
    
    await state.set_state(HisStage.book)
    await state.update_data(page=1, book=prepare_book(path=os.path.join(text_dir, mayak.text)), m_id=m_id)

    data_for_ans = await state.get_data()
    
    await callback.message.answer(text=data_for_ans['book'][data_for_ans['page']], 
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
async def left_his_btn_pressed(callback: CallbackQuery, state: FSMContext):
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
async def back_btn_pressed(callback: CallbackQuery, state: FSMContext, all_media_dir, link_dir):
    data = await state.get_data()
    mayak: Mayak = data_for_mayaks[data['m_id']]
    new_photo = FSInputFile(path=os.path.join(all_media_dir, mayak.img))
    with open(os.path.join(link_dir, mayak.map), 'r', encoding='utf-8') as link_file:
        link = link_file.read()
    
    await callback.message.answer_photo(photo=new_photo,
                               caption=mayak.caption, 
                         reply_markup=PaginationKeyboard(url=link))
    await callback.message.delete()   
    await state.set_state(FSMPagination.page)
    await state.update_data(page=data['m_id'])
    
    data = await state.get_data()
    print(data['page'])


@router.callback_query(F.data == btns_clbks['menu_btn'])
async def menu_btn_pressed(callback: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    await callback.message.answer(text=texts['greetings'],
                         reply_markup=StartKb())
    await callback.message.delete()


@router.callback_query(F.data == btns_clbks['argnt_btn'])
async def argnt_btn_pressed(callback: CallbackQuery, state: FSMContext, all_media_dir):
    await state.set_state(LampsPag.page)
    await state.update_data(page=1)
    lamp: Lamp = data_for_lamps[1]
    new_photo = FSInputFile(path=os.path.join(all_media_dir, lamp.img))

    await callback.message.answer_photo(photo=new_photo,
                               caption=lamps[1], 
                         reply_markup=PaginationKeyboard(url=None))  
    await callback.message.delete()  

    data = await state.get_data()
    print(data['page'])


@router.callback_query(F.data == btns_clbks['rht_btn'], StateFilter(LampsPag.page))
async def rht_lamp_btn_pressed(callback: CallbackQuery, state: FSMContext, all_media_dir):
    data_for_ans = await state.get_data()
    
    if data_for_ans['page'] == len(lamps):
        page = 1
        await state.update_data(page=1)
    else:
        page = data_for_ans['page']+1
        await state.update_data(page=page)

    
    new_data = data_for_lamps[page]
    await change_mayak(name=lamps[page],
                       url=None,
                       file=new_data.img,
                       all_media_dir=all_media_dir,
                       callback=callback)


@router.callback_query(F.data == btns_clbks['lft_btn'], StateFilter(LampsPag.page))
async def lft_lamp_btn_pressed(callback: CallbackQuery, state: FSMContext, all_media_dir):
    data_for_ans = await state.get_data()

    if data_for_ans['page'] == 1:
        page = len(lamps)
        await state.update_data(page=page)
    else:
        page = data_for_ans['page']-1
        await state.update_data(page=page)

    new_data = data_for_lamps[page]
    await change_mayak(name=lamps[page],
                       url=None,
                       file=new_data.img,
                       all_media_dir=all_media_dir,
                       callback=callback)


@router.callback_query(F.data == btns_clbks['to_know_btn'], StateFilter(LampsPag.page))
async def to_know_lamp_pressed(callback: CallbackQuery, state: FSMContext, text_dir, all_media_dir):
    data = await state.get_data()
    lamp_id = int(data['page'])
    lamp: Lamp = data_for_lamps[lamp_id]
    
    await state.set_state(LampUstPag.ustr)
    await state.update_data(page=1, book=prepare_book(path=os.path.join(text_dir, lamp.text)), lamp_id=lamp_id)

    data_for_ans = await state.get_data()
    
    await callback.message.answer(text=data_for_ans['book'][data_for_ans['page']], 
                                  reply_markup=PaginationKbForHis(page=data_for_ans['page']))
    await callback.message.delete()

    
@router.callback_query(F.data == btns_clbks['rht_btn'], StateFilter(LampUstPag.ustr))
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


@router.callback_query(F.data == btns_clbks['lft_btn'], StateFilter(LampUstPag.ustr))
async def left_his_btn_pressed(callback: CallbackQuery, state: FSMContext):
    data_for_ans = await state.get_data()
    
    if data_for_ans['page'] == 1:
        await state.update_data(page=len(data_for_ans['book']), book=data_for_ans['book'])
        page = len(data_for_ans['book'])
    else:
        await state.update_data(page=data_for_ans['page']-1, book=data_for_ans['book'])
        page = data_for_ans['page']-1
    book = data_for_ans['book']
    
    await callback.message.edit_text(text=book[page], reply_markup=PaginationKbForHis(page=page))


@router.callback_query(F.data == btns_clbks['back_btn'], StateFilter(LampUstPag.ustr))
async def back_btn_ustr_pressed(callback: CallbackQuery, state: FSMContext, all_media_dir):
    data = await state.get_data()
    lamp: Lamp = data_for_lamps[data['lamp_id']]

    new_photo = FSInputFile(path=os.path.join(all_media_dir, lamp.img))
    await callback.message.answer_photo(photo=new_photo,
                               caption=lamps[data['lamp_id']], 
                         reply_markup=PaginationKeyboard(url=None))
    await callback.message.delete()   
    await state.set_state(LampsPag.page)
    await state.update_data(page=data['lamp_id'])
    
    data = await state.get_data()
    print(data['page'])


@router.message()
async def else_text(message: Message):
    await message.delete()