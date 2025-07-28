# 🎧 Discord Voice Channel Watcher

A simple Discord bot that sends a text alert when **two specific users** are in a voice channel at the same time.

---

## 🚀 Features

- Monitors two target users on your server
- Sends an alert to a designated text channel when both are in the same or any voice channel
- Lightweight and easy to deploy

---

## 🛠️ Setup (Local)

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/discord-voice-alerts.git
   cd discord-voice-alerts
   ````

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**

   In the project root, create a `.env` file with the following variables:

   ```
   DISCORD_TOKEN=your_discord_bot_token
   GUILD_ID=your_server_id
   TEXT_CHANNEL_ID=text_channel_id_for_alerts
   USER1_ID=first_user_id
   USER2_ID=second_user_id
   ```

5. **Run the bot**

   ```bash
   python3 bot.py
   ```

---

## ☁️ Deployment (Railway)

1. **Push the code to GitHub**

2. **Create a new Railway project**

   * Choose “Deploy from GitHub Repo”
   * Select this repo

3. **Add a `Procfile`**

   Create a file called `Procfile` (no extension) with this content:

   ```
   worker: python3 bot.py
   ```

4. **Add environment variables in Railway UI**

   Add the same variables from `.env` into Railway under **Settings → Variables**:

   * `DISCORD_TOKEN`
   * `GUILD_ID`
   * `TEXT_CHANNEL_ID`
   * `USER1_ID`
   * `USER2_ID`

5. **(Optional) Set Start Command manually**

   If Railway complains about no start command, go to your service’s **Settings → Start Command** and set:

   ```
   python3 bot.py
   ```

6. **Deploy**

   Trigger a deploy or commit to GitHub — Railway will run your bot in the cloud.

---

## 🧪 Example Behavior

If both user A and user B join any voice channel at the same time, the bot will send:

```
🔔 Alert: <@user1> and <@user2> are now in a voice channel together!
```

---

## 📦 Requirements

All dependencies are in `requirements.txt`. Key packages:

* `discord.py`
* `python-dotenv`

---

## 🧾 License

MIT License — use it freely.

---

## 🤔 Troubleshooting

* Make sure your bot has **privileged gateway intents** enabled (especially for voice state tracking).
* Ensure the bot has permission to read and send messages in the text channel.
* Check IDs are correct and not swapped.
* Use `print()` or `logging` to debug user detection issues.

---

## 💬 Questions?

Open an issue or fork the repo. Contributions welcome!