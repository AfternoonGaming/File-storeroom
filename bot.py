import telebot
import base64
import os
from telebot import types
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv() 
API_TOKEN = os.getenv('BOT_TOKEN')

# Apne channel ki ID yahan likhein
CHANNEL_ID = -100123456789 

# Apne channel ka invite link yahan paste karein
CHANNEL_LINK = 'https://t.me/+G9R7JhWDN28zYzQ1' 
# ---------------------

if not API_TOKEN:
    print("Error: BOT_TOKEN nahi mila!")
    exit()

bot = telebot.TeleBot(API_TOKEN)

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception:
        return False

def send_join_request(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Join Channel", url=CHANNEL_LINK))
    markup.add(types.InlineKeyboardButton("🔄 I have joined", callback_data="check_join"))
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
        bot_username = bot.get_me().username
        share_link = f"https://t.me/{bot_username}?start={encoded_id}"
        bot.reply_to(message, f"🔗 **Link Ready:**\n`{share_link}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Please send media only.")

print("Bot is starting...")
bot.infinity_polling()
    markup.add(types.InlineKeyboardButton("🔄 I have joined", callback_data="check_join"))
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
    if message.content_type == 'video': file_id = message.video.file_id
    elif message.content_type == 'photo': file_id = message.photo[-1].file_id
    elif message.content_type == 'document': file_id = message.document.file_id
    
    if file_id:
        encoded_id = base64.b64encode(file_id.encode()).decode()
        bot_username = bot.get_me().username
        share_link = f"https://t.me/{bot_username}?start={encoded_id}"
        bot.reply_to(message, f"🔗 **Link Ready:**\n`{share_link}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Please send media only.")

print("Bot is starting...")
bot.infinity_polling()
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
    if message.content_type == 'video': file_id = message.video.file_id
    elif message.content_type == 'photo': file_id = message.photo[-1].file_id
    elif message.content_type == 'document': file_id = message.document.file_id
    
    if file_id:
        encoded_id = base64.b64encode(file_id.encode()).decode()
        bot_username = bot.get_me().username
        share_link = f"https://t.me/{bot_username}?start={encoded_id}"
        bot.reply_to(message, f"🔗 **Link Ready:**\n`{share_link}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Please send media only.")

print("Bot is starting...")
bot.infinity_polling()
