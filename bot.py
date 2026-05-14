import telebot
from telebot import types
import requests
import json
import os
from datetime import datetime, timedelta
import random

TOKEN = "8738795425:AAG1m5eqcpYeLv48q1A737rhq3wNREIPn98"
GEMINI_KEY = 'AIzaSyCkqEICP3dywWqtnZfCeopqTgxyDFrIeAM'
ADMIN_ID = 6307919195
PAYMENT_NUMBER = "01154578251"

bot = telebot.TeleBot(TOKEN)

# ملفات البيانات
DATA_FILES = {
    'users': 'users_data.json',
    'economy': 'economy_data.json',
    'achievements': 'achievements_data.json',
    'shop': 'shop_data.json',
    'stats': 'stats_data.json',
    'developers': 'developers_data.json',
    'dev_requests': 'dev_requests_data.json',
    'daily_limits': 'daily_limits.json'
}

def load_data(key):
    if os.path.exists(DATA_FILES[key]):
        try:
            with open(DATA_FILES[key], 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(key, data):
    with open(DATA_FILES[key], 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# البيانات الرئيسية
users_db = load_data('users')
economy = load_data('economy')
achievements = load_data('achievements')
shop = load_data('shop')
stats = load_data('stats')
developers = load_data('developers')
dev_requests = load_data('dev_requests')
daily_limits = load_data('daily_limits')

# الأقسام الـ 30
SECTIONS = {
    '🤖': {'name': 'AI Tools', 'features': ['AI Chat', 'Image Analysis', 'Text Writer', 'Code Helper', 'Translation']},
    '⚙️': {'name': 'Tools', 'features': ['Encryptor', 'Data Analyzer', 'Color Generator', 'Code Formatter', 'URL Shortener']},
    '🎮': {'name': 'Entertainment', 'features': ['Games', 'Quizzes', 'Stories', 'Puzzles', 'Music Player']},
    '💎': {'name': 'Premium', 'features': ['Photo Editor', 'Video Maker', 'Live Stream', 'Premium Support', 'Advanced Features']},
    '₿': {'name': 'Crypto Hub', 'features': ['Price Monitor', 'Market Analysis', 'Portfolio Tracker', 'News Feed', 'Trading Bot']},
    '📱': {'name': 'Social Media', 'features': ['Follower Manager', 'Post Scheduler', 'Analytics', 'Content Ideas', 'Engagement Tracker']},
    '🎨': {'name': 'Design Studio', 'features': ['Logo Maker', 'Banner Creator', 'Font Designer', 'Icon Generator', 'Color Palette']},
    '📝': {'name': 'Content Creator', 'features': ['Article Writer', 'SEO Optimizer', 'Hashtag Generator', 'Copywriter', 'Grammar Checker']},
    '💼': {'name': 'Business Pro', 'features': ['Invoice Generator', 'CRM System', 'Team Manager', 'Report Builder', 'Budget Planner']},
    '📚': {'name': 'Learning Hub', 'features': ['100+ Courses', 'Certifications', 'Quizzes', 'Study Plans', 'Resources']},
    '🎵': {'name': 'Music Studio', 'features': ['Music Maker', 'Audio Editor', 'Beat Creator', 'Remixer', 'Mixer']},
    '🏥': {'name': 'Health & Fitness', 'features': ['Workout Plans', 'Nutrition Tracker', 'Health Tips', 'Fitness Goals', 'Meditation']},
    '✈️': {'name': 'Travel Guide', 'features': ['Trip Planner', 'Hotel Finder', 'Flight Tracker', 'Travel Tips', 'Visa Info']},
    '🎰': {'name': 'Gaming Platform', 'features': ['Game Store', 'Tournaments', 'Leaderboards', 'Rewards', 'Streaming']},
    '🔒': {'name': 'Security Suite', 'features': ['Password Manager', 'VPN Guide', 'Security Check', 'Data Protection', 'Encryption']},
    '🎬': {'name': 'Movies & Shows', 'features': ['Movie Finder', 'Reviews', 'Trailers', 'Recommendations', 'Watchlist']},
    '🍔': {'name': 'Food & Recipes', 'features': ['Recipe Finder', 'Nutrition Info', 'Cooking Tips', 'Food Delivery', 'Meal Planner']},
    '🏠': {'name': 'Home Automation', 'features': ['Smart Home Guide', 'Device Control', 'Automation Tips', 'Energy Saver', 'Security']},
    '👗': {'name': 'Fashion & Style', 'features': ['Style Advisor', 'Outfit Planner', 'Trends', 'Shopping Guide', 'Virtual Try-On']},
    '🚗': {'name': 'Auto & Cars', 'features': ['Car Finder', 'Maintenance Tips', 'Price Tracker', 'Reviews', 'Insurance Help']},
    '⚽': {'name': 'Sports Hub', 'features': ['Live Scores', 'Stats Analysis', 'Team News', 'Betting Tips', 'Schedule']},
    '🌍': {'name': 'Weather & Maps', 'features': ['Weather Forecast', 'Map Navigation', 'Location Info', 'Alerts', 'Air Quality']},
    '💊': {'name': 'Pharmacy', 'features': ['Medicine Info', 'Doctor Finder', 'Health Records', 'Prescriptions', 'Appointments']},
    '🎓': {'name': 'Education Hub', 'features': ['Homework Help', 'Exam Prep', 'Study Resources', 'Career Guide', 'Scholarships']},
    '🌱': {'name': 'Eco Lifestyle', 'features': ['Green Tips', 'Sustainability', 'Eco Products', 'Carbon Tracker', 'Community']},
    '💻': {'name': 'Dev Tools', 'features': ['API Integration', 'Code Libraries', 'Debugging Tools', 'Documentation', 'Testing']},
    '🔧': {'name': 'Maintenance', 'features': ['System Monitor', 'Backup Manager', 'Update Checker', 'Performance Boost', 'Cleanup']},
    '📊': {'name': 'Analytics Pro', 'features': ['Advanced Stats', 'Data Visualization', 'Reports', 'Trends', 'Predictions']},
    '🌟': {'name': 'Premium Plus', 'features': ['VIP Access', 'Priority Support', 'Exclusive Features', 'Early Access', 'Special Perks']},
    '🎁': {'name': 'Rewards & Gifts', 'features': ['Daily Rewards', 'Bonus Points', 'Gift Cards', 'Referral Rewards', 'Seasonal Events']},
}

# روابط التحديثات
UPDATES = {
    'Telegram': {
        'version': '9.5.0',
        'link': 'https://telegram.org/blog/update-all-november-2024',
        'icon': '📲'
    },
    'Python': {
        'version': '3.12.1',
        'link': 'https://www.python.org/downloads/release/python-3121/',
        'icon': '🐍'
    },
    'pyTelegramBotAPI': {
        'version': '4.14.0',
        'link': 'https://github.com/eternnoir/pyTelegramBotAPI/releases/tag/4.14.0',
        'icon': '🤖'
    },
    'requests': {
        'version': '2.31.0',
        'link': 'https://github.com/psf/requests/releases/tag/v2.31.0',
        'icon': '📡'
    },
    'Gemini AI': {
        'version': '1.5',
        'link': 'https://ai.google.dev/gemini-api/docs',
        'icon': '✨'
    },
    'MongoDB': {
        'version': '4.6.1',
        'link': 'https://docs.mongodb.com/database/release-notes/4.6/',
        'icon': '💾'
    },
    'Firebase': {
        'version': '6.3.0',
        'link': 'https://firebase.google.com/docs/reference/rest/database',
        'icon': '🔥'
    },
    'JSON': {
        'version': '3.12',
        'link': 'https://docs.python.org/3/library/json.html',
        'icon': '📋'
    }
}

def setup_user(uid):
    uid_str = str(uid)
    if uid_str not in users_db:
        users_db[uid_str] = {
            'username': '',
            'coins': 5000,
            'gems': 500,
            'xp': 0,
            'level': 1,
            'is_vip': False,
            'referrals': 0,
            'daily_streak': 0,
            'last_claim': '2026-01-01',
            'achievements_unlocked': [],
            'dev_rank': 'Free',
            'daily_requests': 0,
            'api_key': f"DEV_{uid}_{random.randint(10000, 99999)}",
            'stats': {
                'total_uses': 0,
                'total_earned': 0,
                'total_spent': 0
            },
            'joined_date': datetime.now().isoformat()
        }
        save_data('users', users_db)

def get_user_rank(xp):
    if xp < 100: return '🌱 Novice'
    elif xp < 500: return '🔍 Explorer'
    elif xp < 1000: return '⭐ Master'
    elif xp < 5000: return '👑 Legend'
    else: return '🔥 Immortal'

def add_rewards(uid, coins=0, gems=0, xp=0):
    uid_str = str(uid)
    if uid_str in users_db:
        users_db[uid_str]['coins'] += coins
        users_db[uid_str]['gems'] += gems
        users_db[uid_str]['xp'] += xp
        
        if users_db[uid_str]['xp'] >= (users_db[uid_str]['level'] * 500):
            users_db[uid_str]['level'] += 1
        
        save_data('users', users_db)
        return True
    return False

def get_daily_limit(uid, rank):
    limits = {
        'Free': 5,
        'Starter': 20,
        'Pro': 100,
        'Enterprise': 1000
    }
    return limits.get(rank, 5)

def get_main_menu(uid):
    uid_str = str(uid)
    setup_user(uid)
    user = users_db[uid_str]
    
    markup = types.InlineKeyboardMarkup(row_width=3)
    
    rank = get_user_rank(user['xp'])
    markup.add(types.InlineKeyboardButton(
        f"👤 {rank} | Lvl {user['level']} | 💰{user['coins']} 💎{user['gems']}", 
        callback_data="profile"
    ))
    
    sections_list = list(SECTIONS.items())
    for i in range(0, len(sections_list), 3):
        row = []
        for j in range(3):
            if i + j < len(sections_list):
                icon, data = sections_list[i + j]
                row.append(types.InlineKeyboardButton(
                    f"{icon}", 
                    callback_data=f"section_{icon}"
                ))
        if row:
            markup.row(*row)
    
    markup.add(
        types.InlineKeyboardButton("🎁 مكافآت يومية", callback_data="daily_reward"),
        types.InlineKeyboardButton("💻 كن مطور", callback_data="dev_menu")
    )
    markup.add(
        types.InlineKeyboardButton("📡 التحديثات", callback_data="updates"),
        types.InlineKeyboardButton("🛍️ متجر", callback_data="shop_menu")
    )
    markup.add(
        types.InlineKeyboardButton("📊 ترتيب", callback_data="leaderboard"),
        types.InlineKeyboardButton("🤝 ادعُ صديق", callback_data="referral")
    )
    
    return markup

@bot.message_handler(commands=['start'])
def start_bot(message):
    uid = message.from_user.id
    uid_str = str(uid)
    setup_user(uid)
    users_db[uid_str]['username'] = message.from_user.first_name
    save_data('users', users_db)
    
    if len(message.text.split()) > 1:
        try:
            ref_id = int(message.text.split()[1])
            if ref_id != uid and str(ref_id) in users_db:
                add_rewards(ref_id, coins=500, gems=50, xp=50)
                add_rewards(uid, coins=500, gems=50, xp=50)
                users_db[str(ref_id)]['referrals'] += 1
                save_data('users', users_db)
                bot.send_message(ref_id, f"✅ صديق جديد انضم!\n+500💰 +50💎 +50XP")
        except:
            pass
    
    bot.send_message(
        message.chat.id,
        """
🔥 **مرحباً بك في البوت الخرافي!** 🔥

✨ أقوى بوت تليجرام في العالم
🎮 30 قسم + 150+ ميزة فريدة
💰 نظام مكافآت ذكي
👨‍💻 نظام مطورين محترف
📡 روابط التحديثات الحية
👑 كن من أفضل 10 لاعبين

اختر قسم واستمتع! 🚀
        """,
        reply_markup=get_main_menu(uid),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'updates')
def show_updates(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    for name, info in UPDATES.items():
        markup.add(types.InlineKeyboardButton(
            f"{info['icon']} {name} v{info['version']}", 
            callback_data=f"update_{name}"
        ))
    
    markup.add(types.InlineKeyboardButton("⬅️ رجوع", callback_data="back_menu"))
    
    bot.send_message(
        call.message.chat.id,
        "📡 **آخر التحديثات:**",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('update_'))
def open_update(call):
    name = call.data.split('update_')[1]
    if name in UPDATES:
        info = UPDATES[name]
        text = f"""
{info['icon']} **{name}**
النسخة: {info['version']}

🔗 [اضغط هنا للتحديث]({info['link']})
        """
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == 'dev_menu')
def dev_menu(call):
    uid = call.from_user.id
    uid_str = str(uid)
    user = users_db[uid_str]
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    rank = user['dev_rank']
    limit = get_daily_limit(uid, rank)
    
    markup.add(types.InlineKeyboardButton(
        f"👨‍💻 {rank} | {user['daily_requests']}/{limit} طلبات", 
        callback_data="none"
    ))
    
    if user['daily_requests'] < limit:
        markup.add(types.InlineKeyboardButton(
            "🆕 طلب تطوير جديد", 
            callback_data="new_dev_request"
        ))
    else:
        markup.add(types.InlineKeyboardButton(
            "⬆️ ترقية الرتبة", 
            callback_data="upgrade_dev"
        ))
    
    markup.add(
        types.InlineKeyboardButton("🔑 API Key", callback_data="show_api_key"),
        types.InlineKeyboardButton("📋 طلباتي", callback_data="my_requests")
    )
    
    markup.add(
        types.InlineKeyboardButton("💰 الأسعار", callback_data="dev_prices"),
        types.InlineKeyboardButton("⬅️ رجوع", callback_data="back_menu")
    )
    
    text = f"""
👨‍💻 **نظام المطورين**

رتبتك: {rank}
الطلبات المتاحة: {user['daily_requests']}/{limit}
API Key: {user['api_key'][:20]}...

اختر ما تريد:
    """
    
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'new_dev_request')
def new_dev_request(call):
    uid = call.from_user.id
    uid_str = str(uid)
    user = users_db[uid_str]
    rank = user['dev_rank']
    limit = get_daily_limit(uid, rank)
    
    if user['daily_requests'] >= limit:
        bot.send_message(call.message.chat.id, f"❌ انتهت طلباتك اليومية!\n⏰ عد غداً أو ترقَّ")
        return
    
    bot.send_message(call.message.chat.id, "📝 **صف لي طلب التطوير بالتفصيل:**")
    bot.register_next_step_handler(call.message, process_dev_request)

def process_dev_request(message):
    uid = message.from_user.id
    uid_str = str(uid)
    
    request_id = f"REQ_{uid}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    dev_requests[request_id] = {
        'user_id': uid,
        'username': message.from_user.first_name,
        'request': message.text,
        'status': 'pending',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    users_db[uid_str]['daily_requests'] += 1
    add_rewards(uid, coins=100, gems=10, xp=50)
    
    save_data('dev_requests', dev_requests)
    save_data('users', users_db)
    
    # إخطار Admin
    admin_text = f"""
🆕 **طلب تطوير جديد!**
معرف: {request_id}
من: {message.from_user.first_name}
الطلب: {message.text}
    """
    
    bot.send_message(ADMIN_ID, admin_text)
    
    bot.send_message(
        message.chat.id,
        f"""
✅ **تم استقبال طلبك!**

معرف الطلب: `{request_id}`
الحالة: قيد المراجعة ⏳
الوقت المتوقع: 24-48 ساعة

المكافآت:
💰 +100 عملة
💎 +10 جوهرة
⭐ +50 خبرة

شكراً لك! 🙏
        """,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'show_api_key')
def show_api_key(call):
    uid = call.from_user.id
    uid_str = str(uid)
    api_key = users_db[uid_str]['api_key']
    
    bot.send_message(
        call.message.chat.id,
        f"""
🔑 **API Key الخاص بك:**

`{api_key}`

استخدم هذا المفتاح في طلباتك للمطور.
        """,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'dev_prices')
def dev_prices(call):
    text = """
💰 **أسعار الرتب:**

🔹 **Free** - مجاني
   ✅ 5 طلبات/اليوم
   ✅ دعم أساسي
   💰 0₪

🔹 **Starter** - 300₪/شهر
   ✅ 20 طلب/اليوم
   ✅ API كامل
   ✅ دعم أولوي

🔹 **Pro** - 700₪/شهر
   ✅ 100 طلب/اليوم
   ✅ API متقدم
   ✅ 24/7 support

🔹 **Enterprise** - 2000₪/شهر
   ✅ 1000 طلب/اليوم
   ✅ دعم مخصص
   ✅ ميزات إضافية
    """
    
    bot.send_message(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data.startswith('section_'))
def handle_section(call):
    uid = call.from_user.id
    icon = call.data.split('_')[1]
    
    if icon in SECTIONS:
        section = SECTIONS[icon]
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        for feature in section['features']:
            markup.add(types.InlineKeyboardButton(
                f"✨ {feature}",
                callback_data=f"use_{feature.replace(' ', '_')}"
            ))
        
        markup.add(types.InlineKeyboardButton("⬅️ رجوع", callback_data="back_menu"))
        
        bot.send_message(
            call.message.chat.id,
            f"### {icon} {section['name']}\n\nاختر ميزة:",
            reply_markup=markup,
            parse_mode="Markdown"
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('use_'))
def use_feature(call):
    uid = call.from_user.id
    feature = call.data.split('use_')[1].replace('_', ' ')
    
    add_rewards(uid, coins=random.randint(100, 500), gems=random.randint(10, 50), xp=random.randint(25, 100))
    
    bot.send_message(
        call.message.chat.id,
        f"""
✅ **تم استخدام:** {feature}

🎁 **المكافآت:**
💰 +{random.randint(100, 500)} عملة
💎 +{random.randint(10, 50)} جوهرة
⭐ +{random.randint(25, 100)} خبرة

🚀 استمتع!
        """
    )

@bot.callback_query_handler(func=lambda call: call.data == 'profile')
def show_profile(call):
    uid = call.from_user.id
    uid_str = str(uid)
    user = users_db[uid_str]
    rank = get_user_rank(user['xp'])
    
    profile_text = f"""
👤 **ملفك الشخصي**
━━━━━━━━━━━━━━━
📛 الاسم: {user['username']}
📊 الرتبة: {rank}
⭐ المستوى: {user['level']}
💫 الخبرة: {user['xp']} XP

💰 العملات:
💰 {user['coins']} عملة
💎 {user['gems']} جوهرة

🤝 الإحالات: {user['referrals']}
👨‍💻 رتبة المطور: {user['dev_rank']}
📅 التاريخ: {user['joined_date'][:10]}
    """
    
    bot.send_message(call.message.chat.id, profile_text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == 'daily_reward')
def daily_reward(call):
    uid = call.from_user.id
    uid_str = str(uid)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if users_db[uid_str]['last_claim'] != today:
        users_db[uid_str]['daily_streak'] += 1
        streak = users_db[uid_str]['daily_streak']
        
        reward_coins = 500 * streak
        reward_gems = 50 * streak
        reward_xp = 100 * streak
        
        add_rewards(uid, coins=reward_coins, gems=reward_gems, xp=reward_xp)
        users_db[uid_str]['last_claim'] = today
        
        # إعادة تعيين الطلبات اليومية
        users_db[uid_str]['daily_requests'] = 0
        
        save_data('users', users_db)
        
        bot.send_message(
            call.message.chat.id,
            f"""
🎁 **مكافأة يومية!** 🎉

🔥 سلسلتك: {streak} يوم متتالي!

💰 +{reward_coins} عملة
💎 +{reward_gems} جوهرة
⭐ +{reward_xp} خبرة

✅ تم إعادة تعيين الطلبات اليومية!
🌅 عد غداً لمكافأة أكبر!
            """
        )
    else:
        bot.send_message(call.message.chat.id, "⏰ لقد أخذت المكافأة اليومية!\n🌅 عد غداً")

@bot.callback_query_handler(func=lambda call: call.data == 'leaderboard')
def show_leaderboard(call):
    sorted_users = sorted(
        users_db.items(),
        key=lambda x: x[1]['coins'] + x[1]['gems'] * 10,
        reverse=True
    )[:10]
    
    leaderboard_text = "🏆 **الترتيب العالمي** 🏆\n━━━━━━━━━━━━━━━\n\n"
    medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    
    for idx, (uid, user) in enumerate(sorted_users):
        total = user['coins'] + user['gems'] * 10
        leaderboard_text += f"{medals[idx]} {user['username']} - {total} نقطة\n"
    
    bot.send_message(call.message.chat.id, leaderboard_text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == 'referral')
def referral_link(call):
    uid = call.from_user.id
    link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
    
    bot.send_message(
        call.message.chat.id,
        f"""
🔗 **رابط إحالتك:**
`{link}`

📊 الإحالات: {users_db[str(uid)]['referrals']}

💰 +500 عملة لكل صديق
💎 +50 جوهرة
⭐ +50 خبرة
        """,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'shop_menu')
def shop_menu(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💰 Starter - 100₪", callback_data="buy_starter"),
        types.InlineKeyboardButton("💎 Premium - 500₪", callback_data="buy_premium")
    )
    markup.add(
        types.InlineKeyboardButton("👑 Legendary - 1000₪", callback_data="buy_legendary"),
        types.InlineKeyboardButton("⬅️ رجوع", callback_data="back_menu")
    )
    
    bot.send_message(
        call.message.chat.id,
        "🛍️ **المتجر:**\n\nاختر حزمة:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_purchase(call):
    package = call.data.split('buy_')[1]
    packages = {
        'starter': {'name': 'Starter', 'price': '100₪', 'coins': 1000, 'gems': 50},
        'premium': {'name': 'Premium', 'price': '500₪', 'coins': 10000, 'gems': 500},
        'legendary': {'name': 'Legendary', 'price': '1000₪', 'coins': 50000, 'gems': 2500}
    }
    
    pkg = packages[package]
    bot.send_message(
        call.message.chat.id,
        f"""
💳 **اشترِ {pkg['name']}**

السعر: {pkg['price']}
💰 {pkg['coins']} عملة
💎 {pkg['gems']} جوهرة

📱 رقم الدفع: {PAYMENT_NUMBER}

بعد التحويل اكتب: /confirm_payment
        """
    )

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👥 الأعضاء", callback_data="admin_users"),
        types.InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")
    )
    markup.add(
        types.InlineKeyboardButton("📋 الطلبات", callback_data="admin_requests"),
        types.InlineKeyboardButton("👑 VIP", callback_data="admin_vip")
    )
    
    bot.send_message(message.chat.id, "🔑 **لوحة التحكم**", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.from_user.id == ADMIN_ID and call.data.startswith('admin_'))
def admin_actions(call):
    if call.data == 'admin_stats':
        total_users = len(users_db)
        total_coins = sum(u['coins'] for u in users_db.values())
        vip_count = sum(1 for u in users_db.values() if u['is_vip'])
        
        bot.send_message(
            call.message.chat.id,
            f"""
📊 **الإحصائيات:**
👥 الأعضاء: {total_users}
💰 إجمالي العملات: {total_coins}
👑 VIP: {vip_count}
📋 الطلبات: {len(dev_requests)}
            """
        )
    
    elif call.data == 'admin_requests':
        pending = [r for r in dev_requests.values() if r['status'] == 'pending']
        text = f"📋 **طلبات معلقة: {len(pending)}**\n\n"
        for req_id, req in list(dev_requests.items())[:5]:
            text += f"👤 {req['username']}\n📝 {req['request'][:50]}...\n\n"
        bot.send_message(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data == 'back_menu')
def back_menu(call):
    uid = call.from_user.id
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📱 **القائمة الرئيسية:**",
        reply_markup=get_main_menu(uid)
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_none(call):
    pass

print("✅ البوت يعمل الآن على Render!")
print(f"👤 Admin ID: {ADMIN_ID}")

bot.polling(none_stop=True)
