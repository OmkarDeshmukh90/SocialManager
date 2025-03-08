import os
import schedule
import time
import threading
import random

from mastodon import Mastodon, StreamListener
from dotenv import load_dotenv
from .config import MASTODON_CLIENT_ID, MASTODON_CLIENT_SECRET, MASTODON_ACCESS_TOKEN, MASTODON_API_BASE_URL
from .ai_generator import generate_text  # new function for free text generation
from .db import create_db, log_conversation

# Initialize Mastodon client
mastodon = Mastodon(
    client_id=MASTODON_CLIENT_ID,
    client_secret=MASTODON_CLIENT_SECRET,
    access_token=MASTODON_ACCESS_TOKEN,
    api_base_url=MASTODON_API_BASE_URL
)

def post_toot(text):
    """Post a toot (status) on Mastodon."""
    try:
        mastodon.status_post(text)
        print("Toot posted successfully!")
    except Exception as e:
        print("Error posting toot:", e)

def reply_to_notification(notification, personality="witty"):
    """Reply to a notification using personality-driven AI."""
    try:
        original_text = notification['status']['content']
        # Here you can either reuse generate_text or generate_personality_reply if you wish to maintain tone.
        reply_text = generate_text(f"Generate a witty reply to the following message: {original_text}")
        log_conversation(notification['status']['id'], reply_text)
        mastodon.status_post(reply_text, in_reply_to_id=notification['status']['id'])
        print(f"Replied to notification {notification['id']} successfully!")
    except Exception as e:
        print("Error posting reply:", e)

# -----------------------
# LLM-based Toot Generation
# -----------------------
def generate_attention_toot():
    """
    Use an LLM to generate a unique toot message.
    The message is crafted to catch attention and is themed around one of:
    tech, finance, or politics.
    """
    domains = ["tech", "finance", "politics"]
    chosen_domain = random.choice(domains)
    prompt = (f"Generate an engaging, witty, and attention-grabbing Mastodon toot "
              f"about {chosen_domain} that is informative and creative.")
    # Call the LLM to generate a message (assuming generate_text returns the generated text).
    toot_message = generate_text(prompt)
    return toot_message.strip()

# -----------------------
# Scheduler for Posting
# -----------------------
def scheduled_post():
    """Function to post a scheduled toot with an LLM-generated message."""
    message = generate_attention_toot()
    print("Posting scheduled toot:", message)
    post_toot(message)

def run_scheduler():
    """Run the scheduler loop to post every 2 hours."""
    # Schedule the post every 2 hours.
    schedule.every(2).hours.do(scheduled_post)
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check pending tasks every minute

# -----------------------
# Stream Listener for Immediate Replies
# -----------------------
class MastodonListener(StreamListener):
    def on_notification(self, notification):
        # Only act on mention notifications (which are often replies)
        if notification.get('type') == 'mention':
            print(f"Received mention notification: {notification['id']}")
            reply_to_notification(notification, personality="witty")

def run_stream_listener():
    """Run the stream listener to handle incoming notifications."""
    try:
        mastodon.stream_user(MastodonListener())
    except Exception as e:
        print("Error in stream listener:", e)

# -----------------------
# Main Execution: Run Scheduler and Stream Listener Concurrently
# -----------------------
if __name__ == "__main__":
    # Create the database if it doesn't exist.
    create_db()

    # Optionally post an initial toot.
    

    # Set up scheduler thread for scheduled posts.
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Set up streaming thread for immediate replies.
    stream_thread = threading.Thread(target=run_stream_listener, daemon=True)
    stream_thread.start()

    # Keep the main thread running.
    while True:
        time.sleep(1)
