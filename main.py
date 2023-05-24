import discord
import config
import sqlite3
from discord.ext import commands

TOKEN = config.TOKEN

# Создаем экземпляр бота
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

banned = ["Ё", "ё", "Ъ", "ъ", "Ы", "ы", "Э", "э"]

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('words.db')
cursor = connection.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS banned_words (
        word TEXT PRIMARY KEY
    )
''')
connection.commit()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Проверяем, если сообщение было отправлено в личные сообщения (ЛС)
    if isinstance(message.channel, discord.DMChannel):
        return

    # Получаем список запрещенных слов из базы данных
    cursor.execute('SELECT word FROM banned_words')
    words_banned = [word[0] for word in cursor.fetchall()]

    if any(phrase in message.content for phrase in banned or words_banned):
        user = message.author
        channel = await user.create_dm()

        await channel.send(f'СЛАВА УКРАЇНІ!!! Видалене повідомлення `{message.content}`')
        await message.delete()

    await bot.process_commands(message)


@bot.command()
@commands.has_permissions(administrator=True)
async def add_banned_word(ctx, word):
    # Добавляем новое запрещенное слово в базу данных
    cursor.execute('INSERT INTO banned_words (word) VALUES (?)', (word,))
    connection.commit()
    await ctx.send(f'Слово "{word}" добавлено в список запрещенных.')

# Запускаем бота
bot.run(TOKEN)
