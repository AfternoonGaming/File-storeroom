import telebot
import base64
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = '8028485830:AAFL0Zbt2h_WPlYkMKm9hzPSC44dOsnhTyk'
# Replace with your private ID (must start with -100)
CHANNEL_ID = -100351909661 
# The private invite link to your channel
CHANNEL_LINK = 'https://t.me/+G9R7JhWDN28zYzQ1' 
# ---------------------

bot = telebot.TeleBot(API_TOKEN)

def is_subscribed(user_id):
    try:
        # Works for private channels as long as the bot is an Admin
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

def send_join_request(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Join Private Channel", url=CHANNEL_LINK))
    markup.add(types.InlineKeyboardButton("🔄 I have joined", callback_data="check_join"))
    
    bot.send_message(chat_id, "⚠️ **Access Restricted**\n\nThis bot is for channel members only. Please join the channel below to continue.", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_callback(call):
    if is_subscribed(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "✅ **Access Granted!** You can now use /store or access links.")
    else:
        bot.answer_callback_query(call.id, "❌ You still haven't joined!", show_alert=True)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    if not is_subscribed(message.from_user.id):
        return send_join_request(message.chat.id)

    text = message.text.split()
    if len(text) > 1:
        try:
            encoded_id = text[1]
            file_id = base64.b64decode(encoded_id.encode()).decode()
            # This sends the file back to the user
            bot.send_document(message.chat.id, file_id, caption="File retrieved successfully! ✅")
        except:
            bot.reply_to(message, "Invalid or broken link.")
    else:
        bot.reply_to(message, "Welcome! Send /store to generate a storage link.")

@bot.message_handler(commands=['store'])
def store_cmd(message):
    if not is_subscribed(message.from_user.id):
        return send_join_request(message.chat.id)
        
    msg = bot.reply_to(message, "📤 **Ready!** Send me the photo, video, or file you want to store.")
    bot.register_next_step_handler(msg, process_storage)

def process_storage(message):
    if not is_subscribed(message.from_user.id):
        return send_join_request(message.chat.id)

    file_id = None
    if message.content_type == 'video': file_id = message.video.file_id
    elif message.content_type == 'photo': file_id = message.photo[-1].file_id
    elif message.content_type == 'document': file_id = message.document.file_id
    
    if file_id:
        encoded_id = base64.b64encode(file_id.encode()).decode()
        bot_username = bot.get_me().username
        share_link = f"https://t.me/{bot_username}?start={encoded_id}"
        bot.reply_to(message, f"🔗 **Your Link is Ready:**\n\n`{share_link}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Error: Please send a media file.")

bot.infinity_polling()
