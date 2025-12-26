import telebot
import base64
import os
from telebot import types
from dotenv import load_dotenv

load_dotenv() 
API_TOKEN = os.getenv('BOT_TOKEN')

if not API_TOKEN:
    print("Error: BOT_TOKEN nahi mila!")
    exit()

bot = telebot.TeleBot(API_TOKEN)

# Menu Buttons set karne ka code
bot.set_my_commands([
    types.BotCommand("start", "Bot ko shuru karein"),
    types.BotCommand("store", "File link generate karein")
])

@bot.message_handler(commands=['start'])
def start_cmd(message):
    text = message.text.split()
    if len(text) > 1:
        try:
            encoded_id = text[1]
            file_id = base64.b64decode(encoded_id.encode()).decode()
            bot.send_document(message.chat.id, file_id, caption="File retrieved! ✅")
        except Exception:
            bot.reply_to(message, "Invalid link.")
    else:
        bot.reply_to(message, "Welcome! Send /store to generate a file link.")

@bot.message_handler(commands=['store'])
def store_cmd(message):
    msg = bot.reply_to(message, "📤 Send me the Video, Photo, or File.")
    bot.register_next_step_handler(msg, process_storage)

def process_storage(message):
    file_id = None
    if message.content_type == 'video':
        file_id = message.video.file_id
    elif message.content_type == 'photo':
        file_id = message.photo[-1].file_id
    elif message.content_type == 'document':
        file_id = message.document.file_id
    
    if file_id:
        encoded_id = base64.b64encode(file_id.encode()).decode()
        bot_info = bot.get_me()
        share_link = f"https://t.me/{bot_info.username}?start={encoded_id}"
        bot.reply_to(message, f"🔗 **Link Ready:**\n`{share_link}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Please send media only.")

print("Bot is starting with Menu...")
bot.infinity_polling(skip_pending=True)
    markup.add(btn2)
    bot.send_message(chat_id, "⚠️ **Access Restricted**\n\nYou must join our channel to use this bot.", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_callback(call):
    if is_subscribed(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "✅ Access Granted! Use /store.")
    else:
        bot.answer_callback_query(call.id, "❌ Join first!", show_alert=True)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    if not is_subscribed(message.from_user.id):
        return send_join_request(message.chat.id)
    
    text = message.text.split()
    if len(text) > 1:
        try:
            encoded_id = text[1]
            file_id = base64.b64decode(encoded_id.encode()).decode()
            bot.send_document(message.chat.id, file_id, caption="File retrieved! ✅")
        except:
            bot.reply_to(message, "Invalid link.")
    else:
        bot.reply_to(message, "Welcome! Send /store to generate a file link.")

@bot.message_handler(commands=['store'])
def store_cmd(message):
    if not is_subscribed(message.from_user.id):
        return send_join_request(message.chat.id)
    msg = bot.reply_to(message, "📤 Send me the Video, Photo, or File.")
    bot.register_next_step_handler(msg, process_storage)

def process_storage(message):
    file_id = None
    if message.content_type == 'video':
        file_id = message.video.file_id
    elif message.content_type == 'photo':
        file_id = message.photo[-1].file_id
    elif message.content_type == 'document':
        file_id = message.document.file_id
    
    if file_id:
        encoded_id = base64.b64encode(file_id.encode()).decode()
        bot_info = bot.get_me()
        share_link = f"https://t.me/{bot_info.username}?start={encoded_id}"
        bot.reply_to(message, f"🔗 **Link Ready:**\n`{share_link}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Please send media only.")

print("Bot is starting...")
bot.infinity_polling()
