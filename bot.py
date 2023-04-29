from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pathlib import Path
import os
from gtts import gTTS
import soundfile
from converter import Converter

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

async def handle_file(file: types.File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")


@dp.message_handler(content_types=[types.ContentType.TEXT])
async def echo_message(msg: types.Message):
    audio = gTTS(text=msg.text, lang ="ru", slow=False)
    audio.save("audio.ogg")
    filename="audio.ogg"
    await bot.send_voice(msg.from_user.id, open(filename, "rb"))
    os.remove(filename)

@dp.message_handler(content_types=[types.ContentType.VOICE])
async def echo_message(msg: types.Message):
    voice = await msg.voice.get_file()
    path = "/home/ubuntu/test/IS20-Gnevanov/"
    await handle_file(file=voice, file_name=f"{voice.file_id}.ogg", path=path)

    full_path = f"{path}/{voice.file_id}.ogg"
    data, samplerate = soundfile.read(full_path)
    soundfile.write(f"{full_path}.wav", data, samplerate)

    converter = Converter(f"{full_path}.wav")
    message_text = converter.audio_to_text()
    os.remove(full_path)
    del converter

    await bot.send_message(msg.from_user.id, message_text)


if __name__ == '__main__':
    executor.start_polling(dp)
