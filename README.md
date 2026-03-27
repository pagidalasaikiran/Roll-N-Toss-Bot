# 🎲 Roll N Toss Telegram Bot 🤖

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?size=25&duration=3000&color=00F7FF&center=true&vCenter=true&width=600&lines=Roll+Dice+🎲;Flip+Coin+🪙;Multiplayer+Games+🎮;Provably+Fair+System+🔐;Cloud+Deployed+Bot+☁️" />
</p>

---

## 🚀 Live Bot
👉 https://t.me/Roll-N-Toss-Bot

---

## 📌 Overview

**Roll N Toss Bot** is a feature-rich Telegram bot that allows users to:

- 🎲 Roll Dice  
- 🪙 Flip Coins  
- 📜 Track Game History  
- 🔐 Verify Game Fairness  
- 👥 Play Multiplayer Matches  

It is built using Python and deployed on cloud with persistent storage.

---

## ✨ Features

### 🎮 Gameplay
- 🎲 Random Dice Roll (1–6)
- 🪙 Coin Toss (Heads / Tails)

### 📜 History System
- Stores all games permanently  
- Displays recent history  
- No data loss (cloud database)

### 🔐 Provably Fair System
Each game generates:
- Secret  
- Hash  

Verify using:
```
/verify <game_id>
```

### 👥 Multiplayer Mode
```
/startgame @username
/join <game_id>
```

- Two players compete  
- Winner decided automatically  

### ⚡ Anti-Spam Protection
- Prevents rapid spam usage  
- Improves performance stability  

### 🧹 Admin Controls
```
/resetit   → Reset history  
/restart   → Soft restart  
```

---

## 🏗️ Tech Stack

- Python 🐍  
- python-telegram-bot  
- Flask  
- Supabase (Database)  
- Render (Hosting)  
- UptimeRobot (Keep Alive)  

---

## 🌐 Architecture

```
User → Telegram → Bot (Render) → Supabase DB
                ↑
           UptimeRobot
```

---

## ⚙️ Setup & Installation

### 1. Clone Repository
```
git clone https://github.com/pagidalasaikiran/Roll-N-Toss-Bot.git
cd Roll-N-Toss-Bot
```

### 2. Install Requirements
```
pip install -r requirements.txt
```

### 3. Environment Variables
```
BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 4. Run Bot
```
python main.py
```

---

## ☁️ Deployment (Render)

- Connect GitHub repo  
- Add environment variables  
- Deploy as Web Service  

---

## 🔄 Keep Bot Alive

Use UptimeRobot:

- Monitor Type: HTTP  
- Interval: 5 minutes  
- URL: Your Render URL  

---

## 📊 Commands

| Command | Description |
|--------|------------|
| /start | Start bot |
| /result | View history |
| /verify <id> | Verify game |
| /startgame @user | Start multiplayer |
| /join <id> | Join game |
| /resetit | Reset history (admin) |
| /restart | Restart bot |

---

## 🔒 Security

- Tokens stored securely in environment variables  
- No sensitive data exposed  
- Safe API usage  

---

## 🏆 Highlights

- ✅ 24/7 Cloud Deployment  
- ✅ Persistent Database  
- ✅ Multiplayer System  
- ✅ Fairness Verification  
- ✅ Production-ready  

---

## 👨‍💻 Author

**Pagidala Sai Kiran**  
GitHub: https://github.com/pagidalasaikiran  

---

⭐ If you like this project, give it a star!
