# Telegram Todo Bot

A simple Telegram bot that helps you manage your personal todo list. The bot stores tasks in a local JSON file, with each user having their own separate list.

## Features

- **`/start`** - Get a welcome message and learn about available commands
- **`/todo <task>`** - Add a new task to your personal todo list
- **`/list`** - View all your saved tasks

## Prerequisites

- Python 3.7 or higher
- A Telegram account
- A Telegram bot token (free)

## Step-by-Step Setup Instructions

### Step 1: Create a Bot with BotFather

1. Open Telegram and search for **@BotFather** (or go to https://t.me/BotFather)
2. Start a chat with BotFather by clicking **Start**
3. Send the command `/newbot`
4. BotFather will ask you to choose a name for your bot (e.g., `My Todo Bot`)
5. Then choose a username for your bot (must end in `bot`, e.g., `my_todo_helper_bot`)
6. If successful, BotFather will send you a message like:
   ```
   Done! Congratulations on your new bot. You will find it at t.me/my_todo_helper_bot.
   
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
7. **Copy the token** (the long string after "Use this token...") - you'll need it in the next step!

### Step 2: Set the TELEGRAM_BOT_TOKEN Environment Variable

#### On Linux/macOS:

Open a terminal and run:
```bash
export TELEGRAM_BOT_TOKEN='your_bot_token_here'
```

Replace `'your_bot_token_here'` with the actual token you got from BotFather.

> **Note:** This sets the variable only for the current terminal session. To make it permanent, add the export line to your `~/.bashrc`, `~/.zshrc`, or similar shell configuration file.

#### On Windows (Command Prompt):

```cmd
set TELEGRAM_BOT_TOKEN=your_bot_token_here
```

#### On Windows (PowerShell):

```powershell
$env:TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

### Step 3: Install Dependencies

Navigate to the directory containing `requirements.txt` and run:

```bash
pip install -r requirements.txt
```

This will install the `python-telegram-bot` library.

### Step 4: Run the Bot

In the same terminal where you set the environment variable, run:

```bash
python bot.py
```

You should see output like:
```
Bot is starting... Press Ctrl+C to stop.
```

### Step 5: Start Using Your Bot

1. Open Telegram and search for your bot by its username (e.g., `@my_todo_helper_bot`)
2. Start a chat with your bot
3. Send `/start` to see the welcome message
4. Try adding a task: `/todo fix login bug`
5. View your tasks: `/list`

## How It Works

- Tasks are stored in a file called `tasks.json` in the same directory as the bot
- Each user's tasks are stored separately using their Telegram user ID
- The bot runs continuously until you stop it (press `Ctrl+C` in the terminal)

## Stopping the Bot

To stop the bot, press `Ctrl+C` in the terminal where it's running.

## Troubleshooting

### "TELEGRAM_BOT_TOKEN environment variable not set!"

Make sure you've set the environment variable correctly in the same terminal session where you're running the bot.

### "ModuleNotFoundError: No module named 'telegram'"

Run `pip install -r requirements.txt` to install the required library.

### Bot doesn't respond

- Make sure the bot is running (check the terminal for errors)
- Verify you started a chat with your bot in Telegram
- Try sending `/start` again

## Security Note

Never share your bot token publicly or commit it to version control. Always use environment variables to keep it secure.
