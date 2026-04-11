# 🏠 Telegram Wohnung-Suche Bot

The ultimate tool for rapid real estate research in Germany's major cities.

This bot automates the tedious process of monitoring housing listings, delivering real-time updates directly to your Telegram. No more manual refreshing—let the bot handle the search while you focus on the application.

---

---

## 🚀 Key Features
- Instant Research: Aggregates the latest rental listings (Currently focused on Hamburg, with more cities coming soon).
- User-Friendly Interface: Interaction via custom Reply Buttons—no need to memorize slash commands.
- Dockerized: Fully containerized for 1-click deployment on any server or local machine.
- Persistence: Integrated SQLite database to track seen listings and avoid duplicates.

---

## 🛠 Tech Stack
- Language: [Python 3.14+](https://www.python.org/)
- Framework: [Aiogram 3.x](https://docs.aiogram.dev/) (Asynchronous)
- Scraping: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) & [Requests](https://requests.readthedocs.io/)
- Database: [SQLite](https://www.sqlite.org/) (Migration to PostgreSQL planned)
- Infrastructure: [Docker](https://www.docker.com/)

---

## ⚙️ Environment Setup
Create a .env file in the root directory and provide your credentials:
```env
BOT_TOKEN=your_telegram_bot_token_here
URL=target_real_estate_search_url

## 🛠 Installation & Deployment Guide

This guide covers two ways to get the Wohnung-Suche Bot up and running. 

### 📋 Prerequisites
Before you start, ensure you have:
1. Telegram Bot Token: Obtain one from [@BotFather](https://t.me/BotFather).
2. Python 3.14+ (for local setup) or Docker installed.
3. Target URL: The specific search results URL from the real estate portal you are monitoring.
    in my case it is Local Estate Agrigator
---

### 🐳 Deployment via Docker (Recommended)
Docker ensures the bot runs in an isolated environment with all dependencies pre-installed.

#### 1. Build the Image
Navigate to the root directory Immo/ (where the Dockerfile is located) and run:

docker build -t immo-bot .
```

---

## 🧊 Launch the Container 

To ensure your database (data.db) is not lost when the container stops, we use a Volume Mapping. Run the following command:

For Linux/macOS:
```env 
docker run -d \
  --name immo-app \
  --restart always \
  -v "$(pwd)/app/data.db:/app/app/data.db" \
  immo-bot
```

For Windows (PowerShell):
```env
docker run -d `
  --name immo-app `
  --restart always `
  -v "${PWD}/app/data.db:/app/app/data.db" `
  immo-bot
```
Note: The --restart always flag ensures the bot starts automatically if your server reboots.

---
## 🐍 Local Deployment (Development)
Use this method if you want to modify the code and see changes immediately.
1. Environment Setup
Create a virtual environment and install the required packages:
```env 
 python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate
# Activate on Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```
2. Configuration
Create a .env file in the root folder:
```env
BOT_TOKEN=123456789:ABCDEF...
URL=[https://www.example.com/hamburg/apartments](https://www.example.com/hamburg/apartments)
```

3. Run the Bot
```env
python app/bot.py
```

---

## ⚠️⚠️⚠️ Disclaimer & Legal Notice ⚠️⚠️⚠️

### **_Educational Purposes Only!!!:_** 

This project is developed strictly for educational and personal research purposes. 
- The target website used in the examples is for demonstration only. 
- I do not recommend or support using this tool for commercial purposes.
- Users are responsible for complying with the robots.txt files and Terms of Service (ToS) of any website they interact with.

### 🛠 Technical Customization
Please note that this is a template framework. If you intend to use this bot for other platforms:
1. Find your target site: You must provide your own URL in the .env file.
2. Identify HTML Tags: You will need to inspect the target website's source code to find the correct CSS selectors/HTML tags.
3. Modify `parser.py`: You must update the scraping logic in parser.py to match the structure of your chosen site.
4. Testing: It is the user's responsibility to verify that the parser works correctly and respects the site's rate limits.
