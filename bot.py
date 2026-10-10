"""
=============================================================================
🛡️ FOUGO VIP - 100% BUTTON-DRIVEN TELEGRAM BOT (ULTRA RESILIENT EDITION)
=============================================================================
👑 Owner ID: 8245269289
🤖 Bot Token: 8939358271:AAE6nCsj62GGY_8lKoW1fQoXGKhNRNGd-NA
📌 নো কমান্ড — ১০০% আকর্ষণীয় ইনলাইন বাটন দ্বারা পরিচালিত!
=============================================================================
"""

import os
import sys
import time
import json
import random
from datetime import datetime, timedelta
import telebot
from telebot import types

# =============================================================================
# ⚙️ কনফিগারেশন (User Specified)
# =============================================================================
DEFAULT_BOT_TOKEN = "8939358271:AAE6nCsj62GGY_8lKoW1fQoXGKhNRNGd-NA"
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
    if not os.path.exists(DB_FILE):
        return {
            "admins": [OWNER_ID],
            "resellers": {},
            "keys": {},
            "settings": {
                "bot_status": True,
                "allow_free_key": True,
                "server_version": "v3.8.2-PRO"
            }
        }
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if OWNER_ID not in data.get("admins", []):
                data.setdefault("admins", []).append(OWNER_ID)
            return data
    except Exception:
        return {
            "admins": [OWNER_ID],
            "resellers": {},
            "keys": {},
            "settings": {
                "bot_status": True,
                "allow_free_key": True,
                "server_version": "v3.8.2-PRO"
            }
        }

def save_db(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving db: {e}")

# =============================================================================
# 🔑 কী (Key) জেনারেটর ইঞ্জিন
# =============================================================================
def generate_key_string(prefix="FOUGO"):
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    part1 = "".join(random.choices(chars, k=4))
    part2 = "".join(random.choices(chars, k=4))
    part3 = "".join(random.choices(chars, k=4))
    return f"{prefix}-{part1}-{part2}-{part3}"

def is_admin(user_id):
    db = load_db()
    return user_id in db.get("admins", []) or user_id == OWNER_ID

# =============================================================================
# 🎨 ইনলাইন কীবোর্ড বিল্ডার
# =============================================================================
def main_menu_keyboard(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    b_free = types.InlineKeyboardButton("🎁 ফ্রি ২ ঘণ্টা ট্রায়াল কী", callback_data="btn_free_trial")
    b_verify = types.InlineKeyboardButton("🔍 কী স্ট্যাটাস যাচাই", callback_data="btn_check_key_prompt")
    b_buy = types.InlineKeyboardButton("💎 VIP কী ক্রয় করুন", callback_data="btn_buy_vip")
    b_help = types.InlineKeyboardButton("📖 ব্যবহার সহায়িকা", callback_data="btn_guide")

    markup.add(b_free)
    markup.add(b_verify, b_buy)
    markup.add(b_help)

    if is_admin(user_id):
        b_admin = types.InlineKeyboardButton("👑 এডমিন ড্যাশবোর্ড", callback_data="admin_dashboard")
        markup.add(b_admin)

    return markup

def admin_dashboard_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("⚡ সিঙ্গেল কী তৈরি", callback_data="adm_gen_single")
    b2 = types.InlineKeyboardButton("📦 বাল্ক (Bulk) কী তৈরি", callback_data="adm_gen_bulk")
    b3 = types.InlineKeyboardButton("📊 কী পরিসংখ্যান", callback_data="adm_stats")
    b4 = types.InlineKeyboardButton("🗑️ মেয়াদোত্তীর্ণ কী মুছুন", callback_data="adm_cleanup")
    b5 = types.InlineKeyboardButton("🔙 মূল মেনু", callback_data="btn_main_menu")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b5)
    return markup

def single_key_duration_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("⏱️ ২ ঘণ্টা", callback_data="gen_key_2h"),
        types.InlineKeyboardButton("🗓️ ১ দিন", callback_data="gen_key_1d")
    )
    markup.add(
        types.InlineKeyboardButton("📅 ৭ দিন", callback_data="gen_key_7d"),
        types.InlineKeyboardButton("🌟 ৩০ দিন", callback_data="gen_key_30d")
    )
    markup.add(
        types.InlineKeyboardButton("♾️ লাইফটাইম", callback_data="gen_key_999d")
    )
    markup.add(
        types.InlineKeyboardButton("🔙 এডমিন প্যানেল", callback_data="admin_dashboard")
    )
    return markup

# =============================================================================
# 📩 মেসেজ হ্যান্ডলার (Start & Text)
# =============================================================================
user_waiting_state = {}

@bot.message_handler(commands=["start", "menu"])
def cmd_start(message):
    first_name = message.from_user.first_name or "User"
    welcome_text = (
        f"<b>👋 স্বাগতম, {first_name}!</b>\n\n"
        f"🛡️ <b>FOUGO VIP iOS Security Key Portal</b>-এ আপনাকে স্বাগতম।\n"
        f"এখান থেকে আপনি কোনো কমান্ড টাইপ না করেই শুধু নিচের বাটন চাপ দিয়ে "
        f"তাত্ক্ষণিক অ্যাক্টিভেশন কী পেতে ও ভেরিফাই করতে পারবেন।\n\n"
        f"📌 <b>নিচের যে কোনো একটি অপশন বেছে নিন:</b>"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_keyboard(message.from_user.id))

@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    uid = message.from_user.id
    if uid in user_waiting_state:
        state = user_waiting_state.pop(uid)
        if state == "WAITING_VERIFY_KEY":
            verify_key_input(message)
            return

    cmd_start(message)

# =============================================================================
# 🔘 বাটন ক্লিক হ্যান্ডলার (Callbacks)
# =============================================================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    uid = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data

    if data == "btn_main_menu":
        bot.edit_message_text(
            "<b>🛡️ FOUGO VIP - মূল মেনু</b>\n\nনিচের বাটন থেকে নির্বাচন করুন:",
            chat_id=chat_id,
            message_id=call.message.message_id,
            reply_markup=main_menu_keyboard(uid)
        )
        return

    if data == "btn_free_trial":
        db = load_db()
        user_free_key = None
        for k, info in db.get("keys", {}).items():
            if info.get("claimed_by") == uid and info.get("is_trial"):
                user_free_key = (k, info)
                break

        if user_free_key:
            k_name, k_info = user_free_key
            exp = k_info.get("expires_at", "অজানা")
            text = (
                "⚠️ <b>আপনি ইতিমধ্যে একটি ফ্রি ট্রায়াল কী নিয়েছেন!</b>\n\n"
                f"🔑 আপনার কী: <code>{k_name}</code>\n"
                f"⏳ মেয়াদ শেষ: <code>{exp}</code>\n\n"
                "💡 আরও বেশি মেয়াদের কী পেতে '💎 VIP কী ক্রয় করুন' চাপুন।"
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔙 মূল মেনু", callback_data="btn_main_menu"))
            bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup)
            return

        new_key = generate_key_string(prefix="TRIAL")
        exp_time = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
        db["keys"][new_key] = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "expires_at": exp_time,
            "duration": "2 Hours",
            "is_trial": True,
            "claimed_by": uid,
            "claimed_by_name": call.from_user.first_name,
            "used": False,
            "device_id": None
        }
        save_db(db)

        text = (
            "🎉 <b>আপনার ২ ঘণ্টার ফ্রি ট্রায়াল কী প্রস্তুত!</b>\n\n"
            f"🔑 কী: <code>{new_key}</code>\n"
            f"⏱️ মেয়াদ: ২ ঘণ্টা\n"
            f"⏳ ভ্যালিডিটি: <code>{exp_time}</code> পর্যন্ত\n\n"
            "📋 <i>কী-টির উপর ট্যাপ করে কপি করে FOUGO VIP অ্যাপে লগইন করুন।</i>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 মূল মেনু", callback_data="btn_main_menu"))
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup)
        return

    if data == "btn_check_key_prompt":
        user_waiting_state[uid] = "WAITING_VERIFY_KEY"
        text = (
            "🔍 <b>কী যাচাইকরণ:</b>\n\n"
            "আপনার কী-টি চ্যাটে লিখে সেন্ড করুন (যেমন: <code>FOUGO-XXXX-XXXX-XXXX</code>)"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("❌ বাতিল করুন", callback_data="btn_main_menu"))
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup)
        return

    if data == "btn_buy_vip":
        text = (
            "💎 <b>FOUGO VIP পেইড অ্যাক্সেস:</b>\n\n"
            "১ দিন: ৫০ টাকা\n"
            "৭ দিন: ২৫০ টাকা\n"
            "৩০ দিন: ৮০০ টাকা\n"
            "লাইফটাইম: ২০০০ টাকা\n\n"
            "👑 ক্রয় করতে যোগাযোগ করুন: <a href='tg://user?id=8245269289'>@FOUGO_OWNER</a>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 মূল মেনু", callback_data="btn_main_menu"))
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup)
        return

    if data == "btn_guide":
        text = (
            "📖 <b>ব্যবহার সহায়িকা:</b>\n\n"
            "১. 'ফ্রি ট্রায়াল' বাটন চাপ দিয়ে ২ ঘণ্টার কী নিন।\n"
            "২. কী কপি করে FOUGO IPA অ্যাপ ওপেন করে পেস্ট করুন।\n"
            "৩. লগইন বাটনে চাপলেই সরাসরি অ্যাক্সেস পেয়ে যাবেন!\n\n"
            "যেকোনো সমস্যায় এডমিনের সাথে যোগাযোগ করুন।"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 মূল মেনু", callback_data="btn_main_menu"))
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup)
        return

    # Admin actions
    if data == "admin_dashboard":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "⛔ আপনার এই প্যানেলে প্রবেশাধিকার নেই!", show_alert=True)
            return
        bot.edit_message_text(
            "👑 <b>FOUGO VIP এডমিন কন্ট্রোল প্যানেল:</b>\n\nনিচের অপশনগুলো পরিচালনা করুন:",
            chat_id,
            call.message.message_id,
            reply_markup=admin_dashboard_keyboard()
        )
        return

    if data == "adm_gen_single":
        if not is_admin(uid):
            return
        bot.edit_message_text(
            "⚡ <b>সিঙ্গেল কী তৈরি করুন:</b>\nমেয়াদ নির্ধারণ করুন:",
            chat_id,
            call.message.message_id,
            reply_markup=single_key_duration_keyboard()
        )
        return

    if data.startswith("gen_key_"):
        if not is_admin(uid):
            return
        dur_code = data.replace("gen_key_", "")
        dur_map = {
            "2h": ("২ ঘণ্টা", timedelta(hours=2)),
            "1d": ("১ দিন", timedelta(days=1)),
            "7d": ("৭ দিন", timedelta(days=7)),
            "30d": ("৩০ দিন", timedelta(days=30)),
            "999d": ("লাইফটাইম", timedelta(days=9999))
        }
        title, delta = dur_map.get(dur_code, ("১ দিন", timedelta(days=1)))
        new_k = generate_key_string(prefix="FOUGO")
        exp_t = (datetime.now() + delta).strftime("%Y-%m-%d %H:%M:%S")

        db = load_db()
        db["keys"][new_k] = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "expires_at": exp_t,
            "duration": title,
            "is_trial": False,
            "claimed_by": None,
            "used": False,
            "device_id": None
        }
        save_db(db)

        text = (
            f"✅ <b>নতুন VIP কী সফলভাবে তৈরি হয়েছে!</b>\n\n"
            f"🔑 কী: <code>{new_k}</code>\n"
            f"⏱️ মেয়াদ: {title}\n"
            f"⏳ ভ্যালিডিটি: <code>{exp_t}</code>\n"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("➕ আরও একটি তৈরি করুন", callback_data="adm_gen_single"))
        markup.add(types.InlineKeyboardButton("🔙 এডমিন প্যানেল", callback_data="admin_dashboard"))
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup)
        return

    if data == "adm_stats":
        if not is_admin(uid):
            return
        db = load_db()
        total_keys = len(db.get("keys", {}))
        trial_keys = sum(1 for k in db["keys"].values() if k.get("is_trial"))
        vip_keys = total_keys - trial_keys
        text = (
            "📊 <b>ডাটাবেজ পরিসংখ্যান:</b>\n\n"
            f"🔑 সর্বমোট কী: {total_keys} টি\n"
            f"💎 VIP কী: {vip_keys} টি\n"
            f"🎁 ট্রায়াল কী: {trial_keys} টি\n"
            f"👑 বটের স্থিতি: সক্রিয় (Online 24/7)\n"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 এডমিন প্যানেল", callback_data="admin_dashboard"))
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup)
        return

    if data == "adm_cleanup":
        if not is_admin(uid):
            return
        db = load_db()
        now = datetime.now()
        deleted = 0
        rem = {}
        for k, val in db.get("keys", {}).items():
            exp_str = val.get("expires_at", "")
            try:
                exp_dt = datetime.strptime(exp_str, "%Y-%m-%d %H:%M:%S")
                if exp_dt < now:
                    deleted += 1
                    continue
            except Exception:
                pass
            rem[k] = val
        db["keys"] = rem
        save_db(db)
        bot.answer_callback_query(call.id, f"🧹 {deleted} টি মেয়াদোত্তীর্ণ কী মুছে ফেলা হয়েছে!", show_alert=True)
        return

def verify_key_input(message):
    key_input = message.text.strip().upper()
    db = load_db()
    if key_input in db.get("keys", {}):
        info = db["keys"][key_input]
        exp = info.get("expires_at", "অজানা")
        dur = info.get("duration", "N/A")
        text = (
            "✅ <b>বৈধ FOUGO VIP কী!</b>\n\n"
            f"🔑 কী: <code>{key_input}</code>\n"
            f"⏱️ মেয়াদ: {dur}\n"
            f"⏳ শেষ হওয়ার তারিখ: <code>{exp}</code>\n"
            f"📱 ব্যবহৃত: {'হ্যাঁ' if info.get('used') else 'না (অব্যবহৃত)'}"
        )
    else:
        text = (
            "❌ <b>অবৈধ বা নকল কী!</b>\n\n"
            "ডাটাবেজে এই কী-টি পাওয়া যায়নি। সঠিক কী দিয়ে পুনরায় চেষ্টা করুন।"
        )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 মূল মেনু", callback_data="btn_main_menu"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

# =============================================================================
# 🚀 বট চালু করার রুটিন (Auto Retry Loop)
# =============================================================================
if __name__ == "__main__":
    print(f"[*] Starting FOUGO VIP Telegram Bot...")
    print(f"[*] Owner ID: {OWNER_ID}")
    
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"[!] Bot Polling Exception: {e}")
            time.sleep(5)
