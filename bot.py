from config import TOKEN
from generator import generate
import logging
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = TOKEN
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(text="Привет! Это srganbot!\n"
                        "Я помогу улучшить качество твоей фотографии,\nпросто отправь фото!\n\n"
                        "/info - получить подробную информацию")


@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    await message.reply(text="Этот бот является реализацией итогового проекта Deep Learning School.\n\n"
                        "Работу выполнил Михаил Сергеев,\n"
                        "stepik_id: 31945458.\n\n"
                        "Февраль, 2021.")


@dp.message_handler(content_types=['photo'])
async def handle_photo(message):
    await message.photo[-1].download('data/input.jpg')
    generate('data/input.jpg').save('data/output.jpg')
    with open('data/output.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Готово!')


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler(regexp='(^dog[s]?$|puppy)')
async def dog(message: types.Message):
    with open('data/dog.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Dog is here! Woof!')


@dp.message_handler()
async def exception(message: types.Message):
    await message.answer("Привет, нажмите /start, чтобы начать.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
