import discord
from discord.ext import commands

# Создаем экземпляр бота
bot = commands.Bot(command_prefix='!')

# Список символов для удаления
symbols = ['Ё', 'ё', 'Ъ', 'ъ', 'Ы', 'ы', 'Э', 'э']

# Событие запуска бота
@bot.event
async def on_ready():
    print('Бот готов')

# Событие при получении сообщения
@bot.event
async def on_message(message):
    content = message.content
    if any(symbol in content for symbol in symbols):
        await message.delete()  # Удаляем сообщение
        await message.channel.send(f'{message.author.mention}, ваше сообщение было удалено, так как содержало запрещенные символы.')
    await bot.process_commands(message)

# Команда для проверки работоспособности бота
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Запускаем бота
bot.run('YOUR_BOT_TOKEN')
