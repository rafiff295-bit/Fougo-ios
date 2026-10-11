"""
=============================================================================
🛡️ FOUGO VIP - 100% BUTTON-DRIVEN TELEGRAM BOT (ULTRA RESILIENT EDITION)
=============================================================================
👑 Owner ID: 8245269289
🤖 Bot Token: 8974328420:AAH0vNMnDVbCK05EjQU_hbl6DyaIneFmsGI
📌 নো কমান্ড — ১০০% আকর্ষণীয় ইনলাইন বাটন দ্বারা পরিচালিত!
=============================================================================
"""

import os
import sys
import time
import json
import random
from datetime import datetime, timedelta

try:
    import telebot
    from telebot import types
    TELEBOT_LOADED = True
except ImportError:
    TELEBOT_LOADED = False
    import urllib.request

    class _MockUser:
        def __init__(self, d):
            self.id = d.get('id', 0)
            self.first_name = d.get('first_name', '')
            self.username = d.get('username', '')

    class _MockChat:
        def __init__(self, d):
            self.id = d.get('id', 0)

    class _MockMessage:
        def __init__(self, d):
            self.message_id = d.get('message_id', 0)
            self.text = d.get('text', '')
            self.from_user = _MockUser(d.get('from', {}))
            self.chat = _MockChat(d.get('chat', {}))

    class _MockCallbackQuery:
        def __init__(self, d):
            self.id = str(d.get('id', ''))
            self.data = d.get('data', '')
            self.from_user = _MockUser(d.get('from', {}))
            self.message = _MockMessage(d.get('message', {}))

    class _TypesModule:
        class InlineKeyboardButton:
            def __init__(self, text, callback_data=None, url=None, **kwargs):
                self.text = text
                self.callback_data = callback_data
                self.url = url
            def to_dict(self):
                d = {'text': self.text}
                if self.callback_data is not None:
                    d['callback_data'] = str(self.callback_data)
                if self.url is not None:
                    d['url'] = self.url
                return d

        class InlineKeyboardMarkup:
            def __init__(self, row_width=2):
                self.row_width = row_width
                self.keyboard = []
            def add(self, *buttons):
                row = []
                for btn in buttons:
                    row.append(btn.to_dict() if hasattr(btn, 'to_dict') else btn)
                    if len(row) >= self.row_width:
                        self.keyboard.append(row)
                        row = []
                if row:
                    self.keyboard.append(row)
            def row(self, *buttons):
                self.keyboard.append([b.to_dict() if hasattr(b, 'to_dict') else b for b in buttons])
            def to_dict(self):
                return {'inline_keyboard': self.keyboard}

    types = _TypesModule()

    class _FallbackTeleBot:
        def __init__(self, token, parse_mode='HTML'):
            self.token = token
            self.parse_mode = parse_mode
            self.message_handlers = []
            self.callback_handlers = []
            self._offset = None

        def _api_call(self, method, payload=None):
            url = f"https://api.telegram.org/bot{self.token}/{method}"
            headers = {"Content-Type": "application/json"}
            data = json.dumps(payload).encode('utf-8') if payload else None
            req = urllib.request.Request(url, data=data, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=35) as resp:
                    return json.loads(resp.read().decode('utf-8'))
            except Exception as e:
                return {"ok": False, "description": str(e)}

        def message_handler(self, commands=None, func=None, **kwargs):
            def decorator(handler):
                self.message_handlers.append({'commands': commands, 'func': func, 'handler': handler})
                return handler
            return decorator

        def callback_query_handler(self, func=None, **kwargs):
            def decorator(handler):
                self.callback_handlers.append({'func': func, 'handler': handler})
                return handler
            return decorator

        def send_message(self, chat_id, text, reply_markup=None, parse_mode=None):
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode or self.parse_mode
            }
            if reply_markup:
                payload['reply_markup'] = reply_markup.to_dict() if hasattr(reply_markup, 'to_dict') else reply_markup
            res = self._api_call('sendMessage', payload)
            if res.get('ok'):
                return _MockMessage(res['result'])
            return None

        def reply_to(self, message, text, reply_markup=None, parse_mode=None):
            chat_id = message.chat.id if hasattr(message, 'chat') else message.get('chat', {}).get('id')
            return self.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)

        def edit_message_text(self, text, chat_id=None, message_id=None, reply_markup=None, parse_mode=None, **kwargs):
            payload = {
                'chat_id': chat_id,
                'message_id': message_id,
                'text': text,
                'parse_mode': parse_mode or self.parse_mode
            }
            if reply_markup:
                payload['reply_markup'] = reply_markup.to_dict() if hasattr(reply_markup, 'to_dict') else reply_markup
            return self._api_call('editMessageText', payload)

        def answer_callback_query(self, callback_query_id, text=None, show_alert=False):
            payload = {'callback_query_id': callback_query_id}
            if text:
                payload['text'] = text
                payload['show_alert'] = show_alert
            return self._api_call('answerCallbackQuery', payload)

        def infinity_polling(self, timeout=20, long_polling_timeout=20):
            print("🚀 Zero-Dependency Telegram Polling Engine Active...", flush=True)
            while True:
                try:
                    payload = {'timeout': long_polling_timeout}
                    if self._offset is not None:
                        payload['offset'] = self._offset
                    res = self._api_call('getUpdates', payload)
                    if not res.get('ok'):
                        time.sleep(2)
                        continue
                    updates = res.get('result', [])
                    for u in updates:
                        self._offset = u['update_id'] + 1
                        if 'message' in u:
                            msg = _MockMessage(u['message'])
                            for h in self.message_handlers:
                                match = True
                                if h['commands']:
                                    cmd = (msg.text or '').split()[0].replace('/', '') if (msg.text or '').startswith('/') else ''
                                    if cmd not in h['commands']:
                                        match = False
                                if match and h['func']:
                                    try:
                                        if not h['func'](msg):
                                            match = False
                                    except Exception:
                                        match = False
                                if match:
                                    try:
                                        h['handler'](msg)
                                    except Exception as err:
                                        print(f"Message handler error: {err}")
                                    break
                        elif 'callback_query' in u:
                            cq = _MockCallbackQuery(u['callback_query'])
                            for h in self.callback_handlers:
                                match = True
                                if h['func']:
                                    try:
                                        if not h['func'](cq):
                                            match = False
                                    except Exception:
                                        match = False
                                if match:
                                    try:
                                        h['handler'](cq)
                                    except Exception as err:
                                        print(f"Callback handler error: {err}")
                                    break
                except Exception as e:
                    print(f"Polling loop notice: {e}")
                    time.sleep(2)

    class _TelebotModule:
        TeleBot = _FallbackTeleBot
        types = _TypesModule()

    telebot = _TelebotModule()

# =============================================================================
# ⚙️ কনফিগারেশন (User Specified)
# =============================================================================
DEFAULT_BOT_TOKEN = "8974328420:AAH0vNMnDVbCK05EjQU_hbl6DyaIneFmsGI"
DEFAULT_OWNER_ID = 8245269289

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip() or DEFAULT_BOT_TOKEN
if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
    BOT_TOKEN = DEFAULT_BOT_TOKEN

raw_oid = os.environ.get("OWNER_ID", "").strip()
OWNER_ID = int(raw_oid) if raw_oid.isdigit() else DEFAULT_OWNER_ID

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# =============================================================================
# 💾 ডাটাবেজ সিস্টেম (Persistent bot_db.json)
# =============================================================================
DB_FILE = "bot_db.json"

def load_db():
    default_db = {
        "admins": {},   # str(user_id): {"credits": -1, "keys_count": 0, "date": "...", "expires_at": -1}
        "sellers": {},  # str(user_id): {"credits": 50, "keys_count": 0, "added_by": "...", "date": "...", "expires_at": -1}
        "keys": [],     # [{"key": "...", "tier": "...", "by": 123, "time": "..."}]
        "total_generated": 0
    }
    if not os.path.exists(DB_FILE):
        return default_db
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for k in default_db:
                if k not in data:
                    data[k] = default_db[k]
            return data
    except Exception:
        return default_db

def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving database: {e}")

# সেশন স্টেট (বাটনের মাধ্যমে মাল্টি-স্টেপ প্রম্পটের জন্য)
# user_id -> {"action": "add_admin" / "add_seller", "target_id": ..., "step": ...}
user_states = {}

# =============================================================================
# 🔐 পারমিশন ও রোল চেকার
# =============================================================================
def get_user_role(uid: int):
    """
    রিটার্ন করে: 'owner' | 'admin' | 'seller' | 'user'
    এবং মেয়াদ উত্তীর্ণ হলে সেলার/অ্যাডমিন পদ বাতিল করে সাধারণ ইউজার করে দেয়।
    """
    if uid == OWNER_ID:
        return "owner"
    
    db = load_db()
    s_uid = str(uid)
    now = time.time()

    # অ্যাডমিন চেক
    if s_uid in db.get("admins", {}):
        adm = db["admins"][s_uid]
        exp = adm.get("expires_at", -1)
        if exp != -1 and now > exp:
            del db["admins"][s_uid]
            save_db(db)
            return "user"
        return "admin"

    # সেলার চেক
    if s_uid in db.get("sellers", {}):
        sel = db["sellers"][s_uid]
        exp = sel.get("expires_at", -1)
        if exp != -1 and now > exp:
            del db["sellers"][s_uid]
            save_db(db)
            return "user"
        return "seller"

    return "user"

def get_user_credits(uid: int):
    """
    ওনার = -1 (Unlimited)
    অ্যাডমিন = -1 অথবা নির্ধারিত সংখ্যা
    সেলার = নির্ধারিত সংখ্যা
    সাধারণ ইউজার = 0
    """
    if uid == OWNER_ID:
        return -1
    db = load_db()
    s_uid = str(uid)
    if s_uid in db.get("admins", {}):
        return db["admins"][s_uid].get("credits", -1)
    if s_uid in db.get("sellers", {}):
        return db["sellers"][s_uid].get("credits", 0)
    return 0

def deduct_credit(uid: int) -> bool:
    """কী জেনারেট করার সময় ক্রেডিট বিয়োগ করা"""
    if uid == OWNER_ID:
        return True
    db = load_db()
    s_uid = str(uid)
    if s_uid in db.get("admins", {}):
        c = db["admins"][s_uid].get("credits", -1)
        if c == -1:
            return True
        if c > 0:
            db["admins"][s_uid]["credits"] = c - 1
            save_db(db)
            return True
        return False
    if s_uid in db.get("sellers", {}):
        c = db["sellers"][s_uid].get("credits", 0)
        if c > 0:
            db["sellers"][s_uid]["credits"] = c - 1
            save_db(db)
            return True
        return False
    return False

# =============================================================================
# 🔑 ক্রিপ্টোগ্রাফিক FOUGO VIP কী জেনারেটর (Algorithmic Signature Valid)
# =============================================================================
def generate_vip_key(tier: str, creator_id: int) -> str:
    chars = "0123456789ABCDEF"
    p3 = "".join(random.choice(chars) for _ in range(4))
    checksum = 0
    for b in p3.encode("utf-8"):
        checksum = ((checksum * 31) + b) & 0xFFFFFFFF
    hex_check = f"{(checksum % 0xFFFF):04X}"
    p4 = hex_check[:2] + "".join(random.choice(chars) for _ in range(2))
    key_str = f"FOUGO-VIP-{p3}-{p4}"

    # ডাটাবেজে সংরক্ষণ
    db = load_db()
    db["total_generated"] = db.get("total_generated", 0) + 1
    db["keys"].append({
        "key": key_str,
        "tier": tier,
        "by": creator_id,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    # ইউজার কাউন্ট বাড়ানো
    s_uid = str(creator_id)
    if s_uid in db.get("admins", {}):
        db["admins"][s_uid]["keys_count"] = db["admins"][s_uid].get("keys_count", 0) + 1
    elif s_uid in db.get("sellers", {}):
        db["sellers"][s_uid]["keys_count"] = db["sellers"][s_uid].get("keys_count", 0) + 1
    save_db(db)

    return key_str

# =============================================================================
# 🔘 ইনলাইন কিবোর্ড জেনারেটর (১০০% বাটন ড্রাইভেন)
# =============================================================================
def get_main_keyboard(uid: int):
    role = get_user_role(uid)
    markup = types.InlineKeyboardMarkup(row_width=2)
    b_gen = types.InlineKeyboardButton("🔑 ভিআইপি কী তৈরি করুন", callback_data="menu_generate")

    if role == "owner":
        b_admin_mgr = types.InlineKeyboardButton("👑 অ্যাডমিন কন্ট্রোল", callback_data="panel_admin_mgr")
        b_seller_mgr = types.InlineKeyboardButton("💼 সেলার কন্ট্রোল", callback_data="panel_seller_mgr")
        b_stats = types.InlineKeyboardButton("📊 সম্পূর্ণ ডাটা ও হিস্ট্রি", callback_data="menu_stats")
        b_master = types.InlineKeyboardButton("🔑 মাস্টার কী দেখুন", callback_data="gen_master")
        b_refresh = types.InlineKeyboardButton("🔄 পেজ রিফ্রেশ করুন", callback_data="menu_main")
        markup.add(b_gen)
        markup.add(b_admin_mgr, b_seller_mgr)
        markup.add(b_stats, b_master)
        markup.add(b_refresh)
    elif role == "admin":
        b_seller_mgr = types.InlineKeyboardButton("💼 সেলার কন্ট্রোল", callback_data="panel_seller_mgr")
        b_stats = types.InlineKeyboardButton("📊 আমার তৈরি কী সমূহ", callback_data="menu_stats")
        b_refresh = types.InlineKeyboardButton("🔄 রিফ্রেশ", callback_data="menu_main")
        markup.add(b_gen)
        markup.add(b_seller_mgr)
        markup.add(b_stats, b_refresh)
    elif role == "seller":
        b_stats = types.InlineKeyboardButton("📊 আমার তৈরি কী", callback_data="menu_stats")
        b_refresh = types.InlineKeyboardButton("🔄 রিফ্রেশ", callback_data="menu_main")
        markup.add(b_gen)
        markup.add(b_stats, b_refresh)
    else:
        b_buy = types.InlineKeyboardButton("🛒 কী বা ক্রেডিট কিনুন", url=f"tg://user?id={OWNER_ID}")
        b_refresh = types.InlineKeyboardButton("🔄 রিফ্রেশ করুন", callback_data="menu_main")
        markup.add(b_gen)
        markup.add(b_buy, b_refresh)
    return markup

def get_tier_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("⚡ ১ দিন ট্রায়াল (1 Day)", callback_data="gen_tier_1d")
    b2 = types.InlineKeyboardButton("📅 ৭ দিন ভিআইপি (7 Days)", callback_data="gen_tier_7d")
    b3 = types.InlineKeyboardButton("💎 ৩০ দিন ভিআইপি (30 Days)", callback_data="gen_tier_30d")
    b4 = types.InlineKeyboardButton("♾️ আজীবন ভিআইপি (Lifetime)", callback_data="gen_tier_lifetime")
    b_back = types.InlineKeyboardButton("🔙 প্রধান মেনুতে ফিরুন", callback_data="menu_main")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b_back)
    return markup

def safe_edit_text(chat_id, message_id, text, reply_markup=None):
    try:
        bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
    except Exception as e:
        if "message is not modified" not in str(e).lower():
            try:
                bot.send_message(chat_id, text, reply_markup=reply_markup)
            except Exception:
                pass

def render_welcome_message(uid: int, first_name: str = "VIP Member") -> str:
    role = get_user_role(uid)
    credits = get_user_credits(uid)
    
    role_titles = {
        "owner": "👑 ওনার (Owner)",
        "admin": "🛡️ অ্যাডমিন (Admin)",
        "seller": "💼 সেলার (Reseller)",
        "user": "👤 সাধারণ ইউজার (Customer)"
    }
    role_str = role_titles.get(role, "👤 ইউজার")
    credit_str = "♾️ আনলিমিটেড (Unlimited)" if credits == -1 else f"{credits} টি"
    
    return (
        f"<b>🛡️ FOUGO VIP LICENSE MANAGEMENT BOT</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 স্বাগতম, <b>{first_name}</b>!\n"
        f"🏷️ আপনার পদবি: <b>{role_str}</b>\n"
        f"💳 অবশিষ্ট ক্রেডিট: <b>{credit_str}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>নিচের বাটনগুলো চেপে আপনার প্রয়োজনীয় কাজ সম্পন্ন করুন:</i>"
    )

@bot.message_handler(commands=['start', 'help', 'menu'])
def cmd_start(message):
    uid = message.from_user.id
    welcome_text = render_welcome_message(uid, message.from_user.first_name)
    bot.reply_to(message, welcome_text, reply_markup=get_main_keyboard(uid))

@bot.callback_query_handler(func=lambda call: True)
def on_callback(call):
    uid = call.from_user.id
    data = call.data

    if data == "menu_main":
        welcome_text = render_welcome_message(uid, call.from_user.first_name)
        safe_edit_text(call.message.chat.id, call.message.message_id, welcome_text, reply_markup=get_main_keyboard(uid))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        return

    if data == "menu_generate":
        role = get_user_role(uid)
        credits = get_user_credits(uid)
        if role == "user" and credits <= 0:
            text = (
                "⚠️ <b>দুঃখিত! আপনার কোনো ক্রেডিট নেই।</b>\n\n"
                "FOUGO VIP লাইসেন্স কী তৈরি করার জন্য অ্যাডমিন বা ওনারের কাছ থেকে ক্রেডিট রিচার্জ করুন।"
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🛒 ওনারের সাথে যোগাযোগ করুন", url=f"tg://user?id={OWNER_ID}"))
            markup.add(types.InlineKeyboardButton("🔙 প্রধান মেনুতে ফিরুন", callback_data="menu_main"))
            safe_edit_text(call.message.chat.id, call.message.message_id, text, reply_markup=markup)
            bot.answer_callback_query(call.id)
            return

        text = (
            "🔑 <b>লাইসেন্স মেয়াদের ধরণ নির্বাচন করুন:</b>\n\n"
            "আপনি কতদিনের জন্য কী তৈরি করতে চান? নিচের যেকোনো একটি বাটনে চাপ দিন:"
        )
        safe_edit_text(call.message.chat.id, call.message.message_id, text, reply_markup=get_tier_keyboard())
        bot.answer_callback_query(call.id)
        return

    if data.startswith("gen_tier_"):
        tier_code = data.replace("gen_tier_", "")
        tier_names = {
            "1d": "১ দিন ট্রায়াল (1 Day)",
            "7d": "৭ দিন ভিআইপি (7 Days)",
            "30d": "৩০ দিন ভিআইপি (30 Days)",
            "lifetime": "♾️ আজীবন ভিআইপি (Lifetime)"
        }
        tier_title = tier_names.get(tier_code, "ভিআইপি অ্যাক্সেস")

        if not deduct_credit(uid):
            safe_edit_text(
                call.message.chat.id,
                call.message.message_id,
                "❌ <b>ক্রেডিট শেষ!</b> আপনার অ্যাকাউন্টে পর্যাপ্ত ক্রেডিট নেই।",
                reply_markup=get_main_keyboard(uid)
            )
            bot.answer_callback_query(call.id, text="ক্রেডিট শেষ!", show_alert=True)
            return

        key = generate_vip_key(tier_title, uid)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        remaining_credits = get_user_credits(uid)
        rem_str = "♾️ আনলিমিটেড" if remaining_credits == -1 else f"{remaining_credits} টি"

        text = (
            "🎉 <b>FOUGO VIP লাইসেন্স কী সফলভাবে তৈরি হয়েছে!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔑 <b>লাইসেন্স কী:</b>\n<code>{key}</code>\n\n"
            f"⏳ <b>মেয়াদ:</b> <b>{tier_title}</b>\n"
            f"💳 <b>অবশিষ্ট ক্রেডিট:</b> <b>{rem_str}</b>\n"
            f"🕒 <b>তৈরির সময়:</b> {now_str}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📋 <i>কী-টির ওপর আলতো চাপ দিয়ে কপি করুন এবং FOUGO VIP অ্যাপের লগইন বক্সে পেস্ট করুন।</i>"
        )
        markup = types.InlineKeyboardMarkup(row_width=2)
        b_another = types.InlineKeyboardButton("⚡ আরেকটি কী তৈরি করুন", callback_data="menu_generate")
        b_home = types.InlineKeyboardButton("🔙 প্রধান মেনু", callback_data="menu_main")
        markup.add(b_another, b_home)
        safe_edit_text(call.message.chat.id, call.message.message_id, text, reply_markup=markup)
        bot.answer_callback_query(call.id, text="কী তৈরি সম্পন্ন!", show_alert=False)
        return

    if data == "gen_master":
        if get_user_role(uid) != "owner":
            bot.answer_callback_query(call.id, text="অনুমতি নেই!", show_alert=True)
            return
        master_keys = [
            "FOUGO-VIP-2026-ADMIN",
            "FOUGO-VIP-LIFETIME",
            "FOUGO-VIP-PREMIUM-ACCESS",
            "FOUGO-BYPASS-ACTIVE-2026",
            "FOUGO-VIP-SECURITY-PASS"
        ]
        mk_text = "\n".join([f"• <code>{k}</code>" for k in master_keys])
        text = (
            "👑 <b>মাস্টার অ্যাডমিন কী তালিকা:</b>\n\n"
            "এই কী-গুলো সুইফট কোডের কোর ইঞ্জিনে চিরস্থায়ীভাবে অনুমোদিত:\n\n"
            f"{mk_text}\n\n"
            "⚠️ <i>এই কী-গুলো শুধুমাত্র আপনি বা বিশ্বস্ত অ্যাডমিনরা ব্যবহার করবেন।</i>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 প্রধান মেনু", callback_data="menu_main"))
        safe_edit_text(call.message.chat.id, call.message.message_id, text, reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    if data == "menu_stats":
        db = load_db()
        role = get_user_role(uid)
        if role == "owner":
            total_k = len(db.get("keys", []))
            total_adm = len(db.get("admins", {}))
            total_sel = len(db.get("sellers", {}))
            recent = db.get("keys", [])[-5:]
            recent_str = ""
            for item in reversed(recent):
                recent_str += f"• <code>{item['key']}</code> ({item['tier']}) - বাই {item['by']}\n"
            if not recent_str:
                recent_str = "<i>এখনও কোনো কী তৈরি করা হয়নি।</i>"

            text = (
                "📊 <b>FOUGO VIP সিস্টেম পরিসংখ্যান</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔑 সর্বমোট তৈরি কী: <b>{total_k} টি</b>\n"
                f"👑 অ্যাক্টিভ অ্যাডমিন: <b>{total_adm} জন</b>\n"
                f"💼 অ্যাক্টিভ সেলার: <b>{total_sel} জন</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🕒 <b>সর্বশেষ তৈরি ৫টি কী:</b>\n"
                f"{recent_str}"
            )
        else:
            my_keys = [k for k in db.get("keys", []) if k.get("by") == uid]
            recent = my_keys[-5:]
            recent_str = ""
            for item in reversed(recent):
                recent_str += f"• <code>{item['key']}</code> ({item['tier']})\n"
            if not recent_str:
                recent_str = "<i>আপনি এখনও কোনো কী তৈরি করেননি।</i>"
            text = (
                "📊 <b>আপনার ব্যক্তিগত পরিসংখ্যান</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔑 আপনার মোট তৈরি কী: <b>{len(my_keys)} টি</b>\n"
                f"💳 অবশিষ্ট ক্রেডিট: <b>{get_user_credits(uid)} টি</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🕒 <b>আপনার তৈরি সর্বশেষ ৫টি কী:</b>\n"
                f"{recent_str}"
            )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 প্রধান মেনু", callback_data="menu_main"))
        safe_edit_text(call.message.chat.id, call.message.message_id, text, reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

@bot.message_handler(func=lambda msg: True)
def on_general_message(message):
    uid = message.from_user.id
    welcome_text = render_welcome_message(uid, message.from_user.first_name)
    bot.reply_to(message, welcome_text, reply_markup=get_main_keyboard(uid))

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🟢 FOUGO VIP Telegram Bot (100% Button Edition) চালু হয়েছে!")
    print(f"👑 Owner ID: {OWNER_ID}")
    print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-5:]}")
    print("🔘 বাটন-ড্রাইভেন মোডে মেসেজ নেওয়া হচ্ছে...")
    print("="*60 + "\n")
    while True:
        try:
            bot.infinity_polling(timeout=30, long_polling_timeout=30)
        except Exception as e:
            time.sleep(5)
