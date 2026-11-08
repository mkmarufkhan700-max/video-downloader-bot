import os
import telebot
import yt_dlp
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# আপনার Telegram BotFather থেকে পাওয়া টোকেনটি এখানে বসান
TOKEN = '8901692681:AAGL9sbRRWF_SM1UW6D0g8in6iZaMCLxESE'

# আপনার টেলিগ্রাম ইউজারনেম
ADMIN_USERNAME = '@saikomaruf420'

bot = telebot.TeleBot(TOKEN)

# ডেটা সংরক্ষণ করার ফাইলগুলোর নাম
USERS_FILE = 'users.txt'
STATS_FILE = 'stats.txt'

# ফাইল না থাকলে তৈরি করে নেওয়া
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        f.write('')

if not os.path.exists(STATS_FILE):
    with open(STATS_FILE, 'w') as f:
        f.write('0')

# ইউজার কাউন্ট সেভ করার ফাংশন
def add_user(user_id):
    with open(USERS_FILE, 'r') as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, 'a') as f:
            f.write(str(user_id) + '\n')

# ডাউনলোড কাউন্ট বাড়ানোর ফাংশন
def increment_download():
    try:
        with open(STATS_FILE, 'r') as f:
            count = int(f.read().strip() or 0)
    except:
        count = 0
    with open(STATS_FILE, 'w') as f:
        f.write(str(count + 1))

# মোট ইউজারের সংখ্যা বের করার ফাংশন
def get_total_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return len(f.read().splitlines())
    except:
        return 0

# মোট ডাউনলোডের সংখ্যা বের করার ফাংশন
def get_total_downloads():
    try:
        with open(STATS_FILE, 'r') as f:
            return int(f.read().strip() or 0)
    except:
        return 0


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # ইউজারকে ডেটাবেসে যোগ করা
    add_user(message.chat.id)
    
    welcome_text = (
        "📥 **𝐀ʟʟ-ɪɴ- 𝐕ɪᴅᴇᴏ & 𝐀ᴜᴅɪᴏ 𝐃ᴏᴡɴʟᴏᴀᴅᴇʀ 𝐁ᴏᴛ**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "আসসালামু আলাইকুম! 👋\n"
        "আমাকে তৈরি করেছে: —͟͞͞𝐗𝐀፝֟͢𝐈𝐊𝐎❀𝐌𝐀፝֟͢𝐑𝐔𝐅⤸\n\n"
        "আমাকে যেকোনো প্ল্যাটফর্মের লিংক পাঠান:\n"
        "• 🎵 𝗧𝗜𝗞 𝗧𝗢𝗞\n"
        "• 📘 𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞\n"
        "• 🎬 𝗬𝗢𝗨𝗧𝗨𝗕𝗘\n"
        "• 📸 𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠\n\n"
        "লিংক পাঠালেই আমি আপনাকে **ভিডিও** অথবা **অডিও (MP3)** নামানোর অপশন দেবো!\n\n"
        f"⚠️ কোনো রকম প্রবলেম বা সাহায্য লাগলে অ্যাডমিনের সাথে যোগাযোগ করো: {ADMIN_USERNAME}"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")


# অ্যাডমিনের জন্য স্ট্যাটস চেক করার কমান্ড (/stats)
@bot.message_handler(commands=['stats'])
def show_stats(message):
    # চাইলে এখানে নিজের ইউজার আইডি দিয়ে সিকিউরিটি দিতে পারেন, যাতে শুধু আপনিই দেখতে পারেন
    total_users = get_total_users()
    total_downloads = get_total_downloads()
    
    stats_text = (
        "📊 **Bot Statistics / স্ট্যাটিস্টিক্স**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"👥 **মোট ইউজার (User):** {total_users} জন\n"
        f"📥 **মোট ডাউনলোড (Download):** {total_downloads} টি ফাইল\n\n"
        f"👑 Developed By: {ADMIN_USERNAME}"
    )
    bot.reply_to(message, stats_text, parse_mode="Markdown")


user_links = {}

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()
    
    if url.startswith("http://") or url.startswith("https://"):
        platform = "🌍 Unknown Platform"
        if "tiktok.com" in url or "vm.tiktok.com" in url or "vt.tiktok.com" in url:
            platform = "🎵 TikTok"
        elif "facebook.com" in url or "fb.watch" in url or "m.facebook.com" in url:
            platform = "📘 Facebook"
        elif "youtube.com" in url or "youtu.be" in url:
            platform = "🎬 YouTube"
        elif "instagram.com" in url:
            platform = "📸 Instagram"
            
        user_links[message.chat.id] = url
        
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(
            InlineKeyboardButton("📥 ভিডিও ডাউনলোড (Video)", callback_data="dl_video"),
            InlineKeyboardButton("🎵 শুধু অডিও (MP3)", callback_data="dl_audio")
        )
        
        bot.reply_to(
            message, 
            f"🔗 **প্ল্যাটফর্ম:** {platform}\n\nদয়া করে নিচের যেকোনো একটি বাটন সিলেক্ট করুন:", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )
    else:
        bot.reply_to(message, f"⚠️ দয়া করে একটি সঠিক লিংক (URL) পাঠান।\nকোনো সমস্যা হলে যোগাযোগ করুন: {ADMIN_USERNAME}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if chat_id not in user_links:
        bot.answer_callback_query(call.id, "❌ লিংকটি মেয়াদোত্তীর্ণ হয়ে গেছে। দয়া করে আবার নতুন করে লিংক পাঠান।")
        return
        
    url = user_links[chat_id]
    
    if call.data == "dl_video":
        bot.answer_callback_query(call.id, "ভিডিও ডাউনলোড শুরু হচ্ছে...")
        sent_msg = bot.send_message(chat_id, "⏳ ভিডিও প্রসেস ও ডাউনলোড হচ্ছে, একটু অপেক্ষা করুন...")
        output_filename = "downloaded_video.mp4"
        
        if os.path.exists(output_filename):
            os.remove(output_filename)
            
        ydl_opts = {
            'outtmpl': output_filename,
            'format': 'best',
            'noplaylist': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            if os.path.exists(output_filename):
                with open(output_filename, 'rb') as f:
                    bot.send_video(
                        chat_id, 
                        f, 
                        caption=(
                            "✅ **ভিডিও সফলভাবে ডাউনলোড হয়েছে!**\n\n"
                            "👑 𝗗ᴇᴠᴇʟᴏᴘᴇᴅ 𝐁ʏ: 🝐꯭𝄀꯭𝗫͠𝗔͟𝗜͟𝗞͟𝗢 ⃪͢𐏓𝗠͠𝗔͟𝗥͟𝗨͟𝗙🍷\n"
                            f"💬 সাহায্য বা প্রবলেমের জন্য: {ADMIN_USERNAME}"
                        ),
                        parse_mode="Markdown"
                    )
                bot.delete_message(chat_id, sent_msg.message_id)
                os.remove(output_filename)
                
                # সফল ডাউনলোডের পর কাউন্ট বাড়বে
                increment_download()
                
                if chat_id in user_links:
                    del user_links[chat_id]
            else:
                bot.edit_message_text(f"❌ ভিডিও ডাউনলোড করা সম্ভব হয়নি। যোগাযোগ করুন: {ADMIN_USERNAME}", chat_id, sent_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ ডাউনলোড করতে সমস্যা হয়েছে। লিংকটি সঠিক কি না চেক করুন বা যোগাযোগ করুন: {ADMIN_USERNAME}", chat_id, sent_msg.message_id)

    elif call.data == "dl_audio":
        bot.answer_callback_query(call.id, "অডিও কনভার্ট শুরু হচ্ছে...")
        sent_msg = bot.send_message(chat_id, "🎵 অডিও (MP3) কনভার্ট হচ্ছে, একটু অপেক্ষা করুন...")
        output_filename = "downloaded_audio.mp3"
        
        if os.path.exists(output_filename):
            os.remove(output_filename)
            
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            actual_file = "downloaded_audio.mp3"
            if os.path.exists(actual_file):
                with open(actual_file, 'rb') as audio_file:
                    bot.send_audio(
                        chat_id, 
                        audio_file, 
                        caption=(
                            "🎵 **অডিও সফলভাবে ডাউনলোড হয়েছে!**\n\n"
                            "👑 তৈরি করেছে: 🝐꯭𝄀꯭𝗫͠𝗔͟𝗜͟𝗞͟𝗢 ⃪͢𐏓𝗠͠𝗔͟𝗥͟𝗨͟𝗙Ξ ꯭꯭𝅥ͦ🗿🍷\n"
                            f"💬 সাহায্য বা প্রবলেমের জন্য: {ADMIN_USERNAME}"
                        ),
                        parse_mode="Markdown"
                    )
                bot.delete_message(chat_id, sent_msg.message_id)
                os.remove(actual_file)
                
                # সফল ডাউনলোডের পর কাউন্ট বাড়বে
                increment_download()
                
                if chat_id in user_links:
                    del user_links[chat_id]
            else:
                bot.edit_message_text(f"❌ অডিও ফাইল তৈরি করা সম্ভব হয়নি। যোগাযোগ করুন: {ADMIN_USERNAME}", chat_id, sent_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ অডিও ডাউনলোড বা কনভার্ট করতে সমস্যা হয়েছে। যোগাযোগ করুন: {ADMIN_USERNAME}", chat_id, sent_msg.message_id)

print("Ultimate Video Downloader Bot with Stats is running...")
bot.infinity_polling()
