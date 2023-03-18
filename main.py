import logging
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN, GROUP_ID

# Enable logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Assign chat ID to the group ID
async def get_group(message: types.Message):
    """
    Assign chat ID to GROUP_ID.
    """
    global GROUP_ID
    GROUP_ID = message.chat.id

    await bot.send_message(chat_id=GROUP_ID, text='Chat ID has been assigned')
# Greet users with a welcome message
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Greet user with welcome message, and admin with another message.
    """
    # Define user_type variable
    user_type = "admin" if message.chat.id == ADMIN_ID else "user"

    # Define welcome message
    welcome_message = f"Welcome, {user_type}. This is your bot."

    # Send welcome message
    await message.reply(welcome_message)
# Get direct links from the user and upload them
@dp.message_handler(content_types=[types.ContentType.TEXT])
async def get_links(message: types.Message):
    """
    Download files from link, send to Telegram chat, and delete file locally.
    """
    # Set parameters for requests to download files
    params = {'url': message.text, 'force': True}
    # Use requests to download a file
    response = requests.get('http://torrentapi.org/pubapi_v2.php',
                            params=params)
    content = response.content.decode('utf-8')

    results = json.loads(content).get('torrent_results')
    if not results:
        msg = ("The link you provided could not be found. Please check the "
               "link and try again.")
        await message.reply(msg)
    for i in results[:5]:
        # Select the first torrent from the results
        href = i['download']
        # Download the torrent file
        response = requests.get(href)

        # Save the torrent file locally
        with open(i['title'] + ".torrent", "wb") as f:
            f.write(response.content)

        # Define the message to send
        msg = (f"Title: {i['title']}\nCategory: {i['category']}\nSize: "
               f"{i['size_human']}\n"
               f"Up: {i['seeders']} | Down: {i['leechers']}\n"
               f"{i['download']}\n{"="*35}")

       
