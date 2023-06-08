from aiogram import types
from loader import dp

@dp.callback_query_handler(lambda call: call.data == "send_document_KZ" or call.data == 'send_document_RU')
async def send_info_document(callback_query: types.CallbackQuery):
    if callback_query.data == "send_document_RU":
        await callback_query.message.edit_text("Пару секунд, загружаю информацию...")

        with open("data/info_files/Что такое ДКП ВИЧ.pdf", "rb") as ru_document:
            await callback_query.message.answer_document(ru_document)

    elif callback_query.data == "send_document_KZ":
        await callback_query.message.edit_text("Бірнеше секунд, ақпаратты жүктеп салу...")

        with open("data/info_files/КДП дегеніміз не.pdf", "rb") as kz_document:
            await callback_query.message.answer_document(kz_document)

    await callback_query.message.delete()
