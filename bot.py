import discord

# ==========================================
# НАСТРОЙКИ (ЗАМЕНИ ДАННЫЕ НА СВОИ)
# ==========================================
import os

TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = 1565085385082536088             # ID канала #warframe-news из Шага 2
PING_ID = 1565087101970677900                # ID роли ИЛИ твоего ID из Шага 2

# Тип пинга: оставь <@&ID> если пингуем РОЛЬ, или замени на <@ID> если пингуем ЛИЧНО ТЕБЯ
PING_MENTION = f"<@&{PING_ID}>" 

# Ключевые слова для поиска (пиши в нижнем регистре)
KEYWORDS = ['stream', 'live', 'devstream', 'prime time', 'twitch', 'стрим']
# ==========================================

# Наключаем намерения (intents), чтобы бот видел текст сообщений
intents = discord.Intents.default()
intents.message_content = True

# Инициализируем бота
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Бот {bot.user} успешно запущен и следит за каналом!')

@bot.event
async def on_message(message):
    # 1. Игнорируем сообщения самого бота, чтобы избежать спама
    if message.author == bot.user:
        return

    # 2. Проверяем, что сообщение пришло именно из нужного канала
    if message.channel.id != CHANNEL_ID:
        return

    # 3. Ищем ключевые слова в тексте сообщения (без учета регистра)
    message_text_lower = message.content.lower()
    
    # Также проверяем заголовки embed-сообщений (на случай, если текст внутри картинки/ссылки)
    embed_text = ""
    if message.embeds:
        embed = message.embeds[0]
        if embed.title:
            embed_text += embed.title.lower()
        if embed.description:
            embed_text += embed.description.lower()

    combined_text = message_text_lower + embed_text

    # Если нашли совпадение
    if any(keyword in combined_text for keyword in KEYWORDS):
        
        # Формируем красивый ответ
        response = (
            f"{PING_MENTION}\n\n"
            f"🔴 **Обнаружен анонс стрима Warframe!**\n\n"
            f"{message.content}\n\n"
            f"🔗 [Перейти к оригинальному сообщению]({message.jump_url})"
        )
        
        # Отправляем пинг в тот же канал
        await message.channel.send(response)

# Запускаем бота
bot.run(TOKEN)