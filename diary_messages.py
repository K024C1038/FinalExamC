import os
import json
from datetime import datetime

# Directory to store user-specific diaries
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)


# Load messages for a specific user
def load_messages(user):
    user_file = os.path.join(DATA_DIR, f'diary_{user}.json')

    if not os.path.exists(user_file):
        return []

    with open(user_file, 'r', encoding='utf-8') as f:
        return json.load(f)


# Save a new diary entry with optional image
def save_message(user, message, image=None):
    user_file = os.path.join(DATA_DIR, f'diary_{user}.json')
    messages = load_messages(user)

    timestamp = datetime.now().strftime('%Y/%m/%d %H:%M')
    messages.insert(0, {'text': message, 'image': image, 'date': timestamp})

    with open(user_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4)


# Delete a message by its entry ID for a specific user
def delete_message(user, entry_id):
    user_file = os.path.join(DATA_DIR, f'diary_{user}.json')
    messages = load_messages(user)

    if 0 <= entry_id < len(messages):
        messages.pop(entry_id)

    with open(user_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4)


# Retrieve a specific entry by ID for a user
def get_entry(user, entry_id):
    messages = load_messages(user)
    if 0 <= entry_id < len(messages):
        return messages[entry_id]
    return None


# Update an entry with new text and optional new image for a user
def update_entry(user, entry_id, updated_text, new_image_filename=None):
    user_file = os.path.join(DATA_DIR, f'diary_{user}.json')
    messages = load_messages(user)

    if 0 <= entry_id < len(messages):
        # Update text
        messages[entry_id]['text'] = updated_text

        # Update image if provided
        if new_image_filename:
            messages[entry_id]['image'] = new_image_filename

        # Save updated data
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=4)
