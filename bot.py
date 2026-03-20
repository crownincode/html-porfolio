#!/usr/bin/env python3
"""
Simple Telegram Todo Bot

This bot allows users to:
- /start - Get a welcome message and list of commands
- /todo <task> - Add a task to their personal todo list
- /list - View all their saved tasks

Tasks are stored in a local JSON file (tasks.json) keyed by user ID.
The bot token must be provided via the TELEGRAM_BOT_TOKEN environment variable.
"""

import os
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure logging to see what's happening in the console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Path to the JSON file where we store all users' tasks
TASKS_FILE = 'tasks.json'


def load_tasks() -> dict:
    """
    Load all tasks from the JSON file.
    
    Returns:
        dict: A dictionary with user IDs as keys and lists of tasks as values.
              Returns an empty dict if the file doesn't exist or is invalid.
    """
    if not os.path.exists(TASKS_FILE):
        return {}
    
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure data is a dictionary
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error loading tasks file: {e}")
        return {}


def save_tasks(tasks: dict) -> None:
    """
    Save all tasks to the JSON file.
    
    Args:
        tasks: Dictionary with user IDs as keys and lists of tasks as values.
    """
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            # Write with indentation for readability
            json.dump(tasks, f, indent=2, ensure_ascii=False)
    except IOError as e:
        logger.error(f"Error saving tasks file: {e}")


def get_user_tasks(user_id: int) -> list:
    """
    Get the list of tasks for a specific user.
    
    Args:
        user_id: The Telegram user ID.
        
    Returns:
        list: List of task strings for this user.
    """
    tasks = load_tasks()
    # Return the user's tasks or an empty list if none exist
    return tasks.get(str(user_id), [])


def add_user_task(user_id: int, task: str) -> None:
    """
    Add a new task for a specific user.
    
    Args:
        user_id: The Telegram user ID.
        task: The task string to add.
    """
    tasks = load_tasks()
    user_key = str(user_id)
    
    # Initialize empty list if user has no tasks yet
    if user_key not in tasks:
        tasks[user_key] = []
    
    # Add the new task
    tasks[user_key].append(task)
    
    # Save updated tasks back to file
    save_tasks(tasks)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.
    
    Sends a welcome message explaining available commands.
    """
    welcome_message = (
        "👋 Welcome to the Todo Bot!\n\n"
        "I can help you manage your personal todo list.\n\n"
        "Available commands:\n"
        "/todo <task> - Add a new task (e.g., /todo fix login bug)\n"
        "/list - View all your saved tasks\n"
        "/start - Show this welcome message again\n\n"
        "Let's get productive! 🚀"
    )
    await update.message.reply_text(welcome_message)


async def todo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /todo command.
    
    Expects a task description after the command.
    Example: /todo fix login bug
    """
    user_id = update.effective_user.id
    
    # Check if a task was provided
    # context.args contains the text after the command, split by spaces
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide a task!\n"
            "Usage: /todo <your task>\n"
            "Example: /todo fix login bug"
        )
        return
    
    # Join all arguments to form the complete task
    # This handles tasks with multiple words
    task = ' '.join(context.args)
    
    # Add the task to the user's list
    add_user_task(user_id, task)
    
    await update.message.reply_text(f"✅ Task added: \"{task}\"")


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /list command.
    
    Displays all saved tasks for the current user.
    """
    user_id = update.effective_user.id
    tasks = get_user_tasks(user_id)
    
    if not tasks:
        await update.message.reply_text(
            "📝 You have no saved tasks.\n"
            "Add one with: /todo <your task>"
        )
        return
    
    # Format tasks as a numbered list
    tasks_text = "📋 Your tasks:\n\n" + "\n".join(
        f"{i+1}. {task}" for i, task in enumerate(tasks)
    )
    
    await update.message.reply_text(tasks_text)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Log errors caused by updates.
    """
    logger.error(f"Update {update} caused error: {context.error}")


def main() -> None:
    """
    Main function to set up and run the bot.
    """
    # Get the bot token from environment variable
    # This is more secure than hardcoding it in the script
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error(
            "TELEGRAM_BOT_TOKEN environment variable not set!\n"
            "Please set it before running the bot:\n"
            "  export TELEGRAM_BOT_TOKEN='your_bot_token_here'"
        )
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Please set it before running the bot.")
        print("Example: export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
        return
    
    # Create the Application instance with the bot token
    application = Application.builder().token(token).build()
    
    # Register command handlers
    # These connect commands to their handler functions
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("todo", todo_command))
    application.add_handler(CommandHandler("list", list_command))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot is starting...")
    print("Bot is starting... Press Ctrl+C to stop.")
    
    # Run the bot until stopped
    # poll_allowed_updates makes sure we only get updates we care about
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
