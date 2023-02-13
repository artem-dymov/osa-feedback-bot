from aiogram import Bot, Dispatcher, executor, types
import json

with open('settings.json', 'r') as file:
    py_data = json.load(file)
    BOT_TOKEN = py_data['BOT_TOKEN']
    SUPPORT_CHAT_ID = py_data['SUPPORT_CHAT_ID']


ban_list = []

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привіт! Напиши своє запитання і модератори його отримають")


@dp.message_handler(commands=['chat_id'])
async def chat_id_handler(message: types.Message):
    await message.answer(message.chat.id)


@dp.message_handler()
async def question_handler(message: types.Message):
    if message.chat.id == SUPPORT_CHAT_ID:

        if message.reply_to_message is not None:
            try:
                user_id = int(message.reply_to_message.text.split('=')[-1].strip())
            except Exception:
                await message.reply('Немає такого користувача!')
                return -1

            if message.text == '/ban':
                ban_list.append(user_id)
                await message.reply(f'Банхаммер покарав цього злодія!\nid злодія - {user_id}')
            else:
                try:
                    await bot.send_message(chat_id=message.reply_to_message.text.split('=')[-1].strip(),
                                           text=message.text)
                    await message.reply('Відповідь надіслана!')
                except Exception as e:
                    await message.reply(f'Повідомлення не надіслано!\n\n{e}')

    elif message.chat.id in ban_list:
        pass

    else:
        if message.from_user.id not in ban_list:
            await bot.send_message(chat_id=SUPPORT_CHAT_ID, text=f'{message.text}\n\nUser id = {message.from_user.id}')

            await message.answer('Ваше повідомлення відправлено! Будь ласка, чекайте на відповідь')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
