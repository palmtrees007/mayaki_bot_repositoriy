from aiogram import Bot
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile, InputFile
from aiogram.enums.input_media_type import InputMediaType

from keyboards.keyboards import PaginationKeyboard

import sqlite3
import os


PAGE_SIZE = 800


async def get_data(m_id):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = '''
SELECT *
FROM mayaki
WHERE id = ?;
'''
        cursor.execute(query, (m_id,))
        res = cursor.fetchall()
        print('Данные получены')
        cursor.close()
        
    except sqlite3.Error as err:
        res = None
        print(err)
    finally:
        if connection:
            connection.close()
        return res


async def change_mayak(name: str, url: str, file: str, all_media_dir: str, callback: CallbackQuery) -> None:
    new_photo = FSInputFile(path=os.path.join(all_media_dir, file))
    media = InputMediaPhoto(media=new_photo, caption=name)
    await callback.message.edit_media(media=media,
                                      reply_markup=PaginationKeyboard(url=url))
    

def _get_part_text(text, start, size):
    smbs = (',', '.', '!', ':', ';', '?')
    ln = len(text)
    end = 1
    for i in range(ln-1, start, -1):
        if text[i] in smbs:
            if i < ln-1:
                if i+1 < ln:
                    if text[i+1] not in smbs and len(text[start:i+1]) <= size:
                        end = i
                        break
            else:
                if len(text[start:i+1]) <= size:
                    end = i
                    break
    res = text[start:end+1]
    return res, len(res)


def prepare_book(path: str) -> dict[int, str]:
    book: dict[int, str] = {}
    with open(path, mode='r', encoding='utf-8') as file:
        text = file.read().replace('\n', '').replace('  ', '\n  ')
        ln = len(text)
        start = 0
        if ln//PAGE_SIZE == ln/PAGE_SIZE:
            st = ln//PAGE_SIZE
        else:
            st = ln//PAGE_SIZE+1
        for i in range(st+1):
            r = _get_part_text(text, start, PAGE_SIZE)
            book[i+1] = r[0].lstrip()
            start += r[1]
    return book