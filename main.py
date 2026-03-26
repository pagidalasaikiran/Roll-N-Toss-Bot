import secrets
import hashlib
import time
import json
import os
import datetime
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import os
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
FILE_NAME = "results.json"

# Load data
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        results_history = json.load(f)
else:
    results_history = []

# Multiplayer storage
active_games = {}

# Anti-spam (faster)
user_last_play = {}

def can_play(user_id):
    now = time.time()
    if user_id in user_last_play and now - user_last_play[user_id] < 0.5:
        return False
    user_last_play[user_id] = now
    return True

# Keyboard
def get_keyboard():
    return ReplyKeyboardMarkup(
        [["🎲 Roll Dice", "🪙 Flip Coin"]],
        resize_keyboard=True
    )

# Async save (NON-BLOCKING)
async def save_data():
    with open(FILE_NAME, "w") as f:
        json.dump(results_history, f, indent=4)

# Generate game
def generate_game(is_dice=True):
    secret = secrets.token_hex(16)

    if is_dice:
        result = secrets.randbelow(6) + 1
        game_type = "Dice"
    else:
        result = secrets.choice(["Heads", "Tails"])
        game_type = "Coin"

    data = f"{secret}:{result}"
    hash_value = hashlib.sha256(data.encode()).hexdigest()
    game_id = secrets.token_hex(4)

    return game_id, secret, result, hash_value, game_type

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Welcome to Roll N Toss!\n\nChoose an option below:",
        reply_markup=get_keyboard()
    )

# Help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 Roll N Toss Help\n\n"
        "🎮 Game Controls:\n"
        "🎲 Roll Dice → Use button\n"
        "🪙 Flip Coin → Use button\n\n"
        "📜 Commands:\n"
        "/start - Start the bot\n"
        "/result - View your game history\n"
        "/verify <id> - Verify a game\n"
        "/restart - Restart the bot\n\n"
        "👥 Multiplayer:\n"
        "/startgame @user - Start a game\n"
        "/join <id> - Join a game\n"
    )
    await update.message.reply_text(text)

# Gameplay
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name
    text = update.message.text

    if not can_play(user_id):
        return

    if text == "🎲 Roll Dice":
        game_id, secret, result, hash_value, game_type = generate_game(True)
        message = f"🎲 You rolled: {result}"

    elif text == "🪙 Flip Coin":
        game_id, secret, result, hash_value, game_type = generate_game(False)
        message = f"🪙 Result: {result}"

    else:
        return

    await update.message.reply_text(message, reply_markup=get_keyboard())

    timestamp = datetime.datetime.now().strftime("%d %b %I:%M %p")

    results_history.append({
        "user": username,
        "user_id": user_id,
        "game_id": game_id,
        "type": game_type,
        "result": result,
        "time": timestamp,
        "secret": secret,
        "hash": hash_value
    })

    # Save asynchronously
    asyncio.create_task(save_data())

# /result
async def result_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_results = [r for r in results_history if r.get("user_id") == user_id]

    if not user_results:
        await update.message.reply_text("📜 No results yet.")
        return

    text = "📜 Your Game History\n\n"

    for r in user_results[-10:]:
        emoji = "🎲" if r.get("type", "Dice") == "Dice" else "🪙"
        text += f"{emoji} {r.get('result')} • {r.get('time')} • {r.get('game_id')}\n"

    await update.message.reply_text(text)

# /verify
async def verify_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /verify <game_id>")
        return

    gid = context.args[0]

    for r in results_history:
        if r.get("game_id") == gid:
            data = f"{r['secret']}:{r['result']}"
            computed_hash = hashlib.sha256(data.encode()).hexdigest()
            verified = computed_hash == r["hash"]

            status = "✅ Verified" if verified else "❌ Failed"

            await update.message.reply_text(
                f"🔍 Verification\n\n"
                f"🆔 {gid}\n"
                f"🎯 {r['result']}\n\n"
                f"{status}\n\n"
                f"🔐 Hash:\n{r['hash']}\n\n"
                f"🔑 Secret:\n{r['secret']}"
            )
            return

    await update.message.reply_text("❌ Game ID not found.")

# /resetit (admin)
async def reset_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    global results_history
    results_history = []

    asyncio.create_task(save_data())

    await update.message.reply_text("🧹 History reset successfully.")

# /restart (everyone)
async def restart_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_last_play.clear()
    await update.message.reply_text("♻️ Restarted successfully.")
    os._exit(0)

# Multiplayer
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /startgame @username")
        return

    player1 = update.effective_user
    player2_username = context.args[0]

    game_id = secrets.token_hex(3)

    active_games[game_id] = {
        "player1": player1,
        "player2_username": player2_username
    }

    await update.message.reply_text(
        f"🎮 Game created!\nWaiting for {player2_username} to join...\n\nGame ID: {game_id}"
    )

async def join_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return

    game_id = context.args[0]

    if game_id not in active_games:
        await update.message.reply_text("❌ Game not found.")
        return

    game = active_games[game_id]
    player2 = update.effective_user

    if f"@{player2.username}" != game["player2_username"]:
        return

    player1 = game["player1"]

    roll1 = secrets.randbelow(6) + 1
    roll2 = secrets.randbelow(6) + 1

    if roll1 > roll2:
        result_text = f"🏆 {player1.first_name} wins!"
    elif roll2 > roll1:
        result_text = f"🏆 {player2.first_name} wins!"
    else:
        result_text = "🤝 It's a tie!"

    await update.message.reply_text(
        f"🎲 Multiplayer Result\n\n"
        f"{player1.first_name}: {roll1}\n"
        f"{player2.first_name}: {roll2}\n\n"
        f"{result_text}"
    )

    del active_games[game_id]

# Run
app = (
    ApplicationBuilder()
    .token(TOKEN)
    .concurrent_updates(True)
    .build()
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("result", result_cmd))
app.add_handler(CommandHandler("verify", verify_cmd))
app.add_handler(CommandHandler("resetit", reset_history))
app.add_handler(CommandHandler("restart", restart_bot))
app.add_handler(CommandHandler("startgame", start_game))
app.add_handler(CommandHandler("join", join_game))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling(drop_pending_updates=True)
