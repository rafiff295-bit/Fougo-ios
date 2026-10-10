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
import telebot
from telebot import types

# =============================================================================
# ⚙️ কনফিগারেশন
# =============================================================================
DEFAULT_BOT_TOKEN = "8974328420:AAH0vNMnDVbCK05EjQU_hbl6DyaIneFmsGI"
DEFAULT_OWNER_ID = 8245269289

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip() or DEFAULT_BOT_TOKEN
if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
    BOT_TOKEN = DEFAULT_BOT_TOKEN

raw_oid = os.environ.get("OWNER_ID", "").strip()
OWNER_ID = int(raw_oid) if raw_oid.isdigit() else DEFAULT_OWNER_ID

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_db.json")

# =============================================================================
# 💾 ডাটাবেস ফাংশন
# =============================================================================
def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "keys": {},
            "users": {},
            "admins": [OWNER_ID],
            "sellers": [],
            "stats": {"total_generated": 0, "total_users": 0}
        }
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if OWNER_ID not in data.get("admins", []):
                data.setdefault("admins", []).append(OWNER_ID)
            return data
    except Exception as e:
        print(f"Error loading DB: {e}")
        return {"keys": {}, "users": {}, "admins": [OWNER_ID], "sellers": [], "stats": {"total_generated": 0, "total_users": 0}}

def save_db(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving DB: {e}")

# =============================================================================
# 🔑 লাইসেন্স কি জেনারেশন (FOUGO VIP অ্যালগরিদম)
# =============================================================================
TIER_DURATIONS = {
    "24h": timedelta(hours=24),
    "7d": timedelta(days=7),
    "30d": timedelta(days=30),
    "lifetime": timedelta(days=3650),
    "master": timedelta(days=3650)
}

def generate_fougo_key(tier="30d", generated_by=OWNER_ID):
    if tier == "master":
        key = "FOUGO-VIP-2026-ADMIN"
    elif tier == "lifetime":
        hex_rand = "".join([random.choice("0123456789ABCDEF") for _ in range(4)])
        key = f"FOUGO-VIP-LIFETIME-{hex_rand}"
    else:
        hex_chars = "0123456789ABCDEF"
        p1 = "".join([random.choice(hex_chars) for _ in range(4)])
        chk = 0
        for ch in p1:
            chk = ((chk * 31) + ord(ch)) & 0xFFFFFFFF
        hex_chk = hex(chk % 0xFFFF)[2:].upper().zfill(4)[:2]
        p2 = hex_chk + random.choice(hex_chars) + random.choice(hex_chars)
        key = f"FOUGO-VIP-{p1}-{p2}"

    now = datetime.utcnow()
    exp = now + TIER_DURATIONS.get(tier, timedelta(days=30))

    db = load_db()
    db["keys"][key] = {
        "tier": tier,
        "created_at": now.isoformat(),
        "expires_at": exp.isoformat(),
        "generated_by": generated_by,
        "is_used": False,
        "used_by": None,
        "used_at": None
    }
    db["stats"]["total_generated"] = db["stats"].get("total_generated", 0) + 1
    save_db(db)
    return key

# =============================================================================
# 👥 রোল এবং পারমিশন
# =============================================================================
def is_owner(uid):
    return uid == OWNER_ID

def check_account_expired(account_info):
    if not account_info or not account_info.get("expires_at"):
        return False
    try:
        exp = datetime.fromisoformat(account_info["expires_at"])
        return datetime.utcnow() > exp
    except Exception:
        return False

def is_admin(uid):
    if is_owner(uid):
        return True
    db = load_db()
    if uid in db.get("admins", []):
        admin_info = db.get("users", {}).get(str(uid), {}).get("admin_role")
        if admin_info and check_account_expired(admin_info):
            return False
        return True
    return False

def is_seller(uid):
    if is_owner(uid) or is_admin(uid):
        return True
    db = load_db()
    if uid in db.get("sellers", []):
        seller_info = db.get("users", {}).get(str(uid), {}).get("seller_role")
        if seller_info and check_account_expired(seller_info):
            return False
        return True
    return False

def get_user_role(uid):
    if is_owner(uid):
        return "👑 Owner (Root Access)"
    if is_admin(uid):
        return "🛡️ Co-Admin"
    if is_seller(uid):
        return "💼 Authorized Reseller"
    return "👤 General User"

def get_user_credits(uid):
    if is_owner(uid) or is_admin(uid):
        return 999999
    db = load_db()
    return db.get("users", {}).get(str(uid), {}).get("credits", 0)

def consume_credit(uid):
    if is_owner(uid) or is_admin(uid):
        return True
    db = load_db()
    u_str = str(uid)
    cr = db.get("users", {}).get(u_str, {}).get("credits", 0)
    if cr > 0:
        db["users"][u_str]["credits"] = cr - 1
        save_db(db)
        return True
    return False

# =============================================================================
# 🎛️ বাটন কীবোর্ড লেআউট
# =============================================================================
def get_main_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=2)
    role_is_priv = is_owner(uid) or is_admin(uid) or is_seller(uid)
    
    if role_is_priv:
        markup.add(
            types.InlineKeyboardButton("🔑 Generate VIP Key", callback_data="menu_generate"),
            types.InlineKeyboardButton("📜 Key History", callback_data="menu_keys_list")
        )
    else:
        markup.add(
            types.InlineKeyboardButton("🎁 Request 24h Free Trial", callback_data="action_free_trial"),
            types.InlineKeyboardButton("💳 Buy VIP Key", callback_data="menu_pricing")
        )

    markup.add(
        types.InlineKeyboardButton("📱 iOS IPA Download", callback_data="menu_ipa_download"),
        types.InlineKeyboardButton("⚙️ Inject & Install Guide", callback_data="menu_install_guide")
    )
    markup.add(
        types.InlineKeyboardButton("👤 My Account Status", callback_data="menu_my_account"),
        types.InlineKeyboardButton("💬 Support / Contact", callback_data="menu_support")
    )

    if is_owner(uid) or is_admin(uid):
        admin_btns = [
            types.InlineKeyboardButton("👑 Admin Panel", callback_data="menu_admin_panel"),
            types.InlineKeyboardButton("📊 System Stats", callback_data="menu_stats")
        ]
        markup.add(*admin_btns)

    markup.add(types.InlineKeyboardButton("🔄 Refresh Dashboard", callback_data="menu_refresh"))
    return markup

def get_key_generation_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("⚡ 24-Hour Trial", callback_data="gen_key_24h"),
        types.InlineKeyboardButton("🥉 7-Day Pass", callback_data="gen_key_7d")
    )
    markup.add(
        types.InlineKeyboardButton("🥈 30-Day VIP Pass", callback_data="gen_key_30d"),
        types.InlineKeyboardButton("🥇 Lifetime VIP Pass", callback_data="gen_key_lifetime")
    )
    if is_owner(uid):
        markup.add(types.InlineKeyboardButton("👑 Master Admin Key", callback_data="gen_key_master"))
    markup.add(types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_back_main"))
    return markup

def safe_edit_text(chat_id, message_id, text, reply_markup=None):
    try:
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    except Exception as e:
        if "message is not modified" not in str(e).lower():
            bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode="HTML", disable_web_page_preview=True)

def render_welcome_message(uid, first_name):
    role = get_user_role(uid)
    cr = get_user_credits(uid)
    cr_text = "♾️ Unlimited" if (is_owner(uid) or is_admin(uid)) else f"{cr} Keys"
    
    return (
        f"🛡️ <b>Welcome to FOUGO VIP Bot!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 Hello, <b>{first_name}</b>!\n"
        f"🆔 Your Telegram ID: <code>{uid}</code>\n"
        f"🎖️ Status: <b>{role}</b>\n"
        f"💳 Credits: <b>{cr_text}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👉 <i>Choose an option from the buttons below:</i>"
    )

# =============================================================================
# 🚀 বট হ্যান্ডলার ও বোতাম কন্ট্রোল
# =============================================================================
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start', 'help', 'menu'])
def cmd_start(message):
    uid = message.from_user.id
    fname = message.from_user.first_name or "VIP Member"
    db = load_db()
    u_str = str(uid)
    if u_str not in db["users"]:
        db["users"][u_str] = {
            "id": uid,
            "first_name": fname,
            "username": message.from_user.username or "",
            "joined_at": datetime.utcnow().isoformat(),
            "credits": 0,
            "trial_used": False
        }
        db["stats"]["total_users"] = len(db["users"])
        save_db(db)

    text = render_welcome_message(uid, fname)
    bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(uid))

@bot.callback_query_handler(func=lambda call: True)
def on_callback(call):
    uid = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    fname = call.from_user.first_name or "VIP Member"

    # ব্যাক টু মেইন মেনু
    if data in ["menu_back_main", "menu_refresh"]:
        text = render_welcome_message(uid, fname)
        safe_edit_text(cid, mid, text, get_main_keyboard(uid))
        bot.answer_callback_query(call.id, "Dashboard updated!")
        return

    # কি জেনারেশন মেনু
    if data == "menu_generate":
        if not (is_owner(uid) or is_admin(uid) or is_seller(uid)):
            bot.answer_callback_query(call.id, "⚠️ Only Admins & Sellers can generate keys!", show_alert=True)
            return
        text = (
            "🔑 <b>Select VIP Key Tier to Generate:</b>\n\n"
            "• <b>24h Trial</b> — For quick testing\n"
            "• <b>7-Day</b> — 1 Week VIP Access\n"
            "• <b>30-Day</b> — 1 Month Full Access\n"
            "• <b>Lifetime</b> — Permanent VIP Access\n\n"
            "👇 <i>Tap a button to generate instantly:</i>"
        )
        safe_edit_text(cid, mid, text, get_key_generation_keyboard(uid))
        return

    # বিভিন্ন টিয়ারের কি তৈরি করা
    if data.startswith("gen_key_"):
        tier = data.replace("gen_key_", "")
        if tier == "master" and not is_owner(uid):
            bot.answer_callback_query(call.id, "❌ Only Owner can generate Master Key!", show_alert=True)
            return

        if not consume_credit(uid):
            bot.answer_callback_query(call.id, "❌ Insufficient credits! Contact Owner.", show_alert=True)
            return

        key = generate_fougo_key(tier=tier, generated_by=uid)
        tier_names = {
            "24h": "24-Hour Trial Key",
            "7d": "7-Day VIP Pass",
            "30d": "30-Day VIP Pass",
            "lifetime": "Lifetime VIP Pass",
            "master": "👑 Master Admin Key"
        }

        resp_text = (
            f"✅ <b>FOUGO VIP Key Generated!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ Tier: <b>{tier_names.get(tier, tier)}</b>\n"
            f"🔑 License Key:\n<code>{key}</code>\n\n"
            f"💡 <i>Tap to copy the key and enter it in FOUGO app!</i>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🔑 Generate Another Key", callback_data="menu_generate"),
            types.InlineKeyboardButton("🔙 Main Menu", callback_data="menu_back_main")
        )
        safe_edit_text(cid, mid, resp_text, markup)
        bot.answer_callback_query(call.id, "Key Generated Successfully! 🎉")
        return

    # ফ্রি ট্রায়াল রিকোয়েস্ট
    if data == "action_free_trial":
        db = load_db()
        u_str = str(uid)
        user_data = db.get("users", {}).get(u_str, {})
        if user_data.get("trial_used", False):
            bot.answer_callback_query(call.id, "⚠️ You have already claimed your 24h trial!", show_alert=True)
            return

        trial_key = generate_fougo_key("24h", generated_by=uid)
        if u_str in db["users"]:
            db["users"][u_str]["trial_used"] = True
            save_db(db)

        resp_text = (
            f"🎉 <b>Your 24-Hour Free Trial Key!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔑 <code>{trial_key}</code>\n\n"
            f"Enjoy full VIP features for 24 hours!\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Main Menu", callback_data="menu_back_main"))
        safe_edit_text(cid, mid, resp_text, markup)
        return

    # আইপিএ ডাউনলোড ও গাইড
    if data == "menu_ipa_download":
        text = (
            "📱 <b>FOUGO iOS IPA Download</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "iOS 14 - 18+ এর জন্য ফুল বাইপাস এবং অ্যান্টি-ব্যান বিল্ড।\n\n"
            "📥 <b>Download Sources:</b>\n"
            "• GitHub Actions Artifacts\n"
            "• Direct Signed IPA Links\n\n"
            "💡 <i>Sideloadly, Scarlet, TrollStore অথবা Esign দিয়ে সাইন করে ইনস্টল করুন।</i>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_back_main"))
        safe_edit_text(cid, mid, text, markup)
        return

    # মাই একাউন্ট
    if data == "menu_my_account":
        role = get_user_role(uid)
        cr = get_user_credits(uid)
        text = (
            f"👤 <b>Your Account Details</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• Name: {fname}\n"
            f"• Telegram ID: <code>{uid}</code>\n"
            f"• Access Level: <b>{role}</b>\n"
            f"• Available Credits: <b>{cr}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="menu_back_main"))
        safe_edit_text(cid, mid, text, markup)
        return

    # ডিফল্ট ফলব্যাক
    bot.answer_callback_query(call.id, "Updated!")

# =============================================================================
# 🏁 রানার
# =============================================================================
if __name__ == "__main__":
    print(f"🤖 Starting FOUGO VIP Telegram Bot...")
    print(f"👑 Owner ID: {OWNER_ID}")
    
    # পুরানো কোনো পেণ্ডিং রিকোয়েস্ট ক্লিয়ার করা
    try:
        bot.remove_webhook()
        print("✅ Webhook removed, using Long Polling.")
    except Exception as e:
        print(f"Webhook note: {e}")

    print("🚀 Bot is LIVE! Waiting for user messages...")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=20)
        except Exception as err:
            print(f"⚠️ Polling loop reconnecting: {err}")
            time.sleep(3)
