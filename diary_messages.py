import json
import os
from datetime import datetime

DATA_DIR = 'data'


# Load messages for a user
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


# Delete a message
def delete_message(user, entry_id):
    user_file = os.path.join(DATA_DIR, f'diary_{user}.json')
    messages = load_messages(user)

    if 0 <= entry_id < len(messages):
        messages.pop(entry_id)

    with open(user_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4)


# Edit a message
def edit_message(user, entry_id, new_text, new_image=None):
    user_file = os.path.join(DATA_DIR, f'diary_{user}.json')
    messages = load_messages(user)

    if 0 <= entry_id < len(messages):
        messages[entry_id]['text'] = new_text
        if new_image:
            messages[entry_id]['image'] = new_image

    with open(user_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4)


# Get a single message for editing
def get_message(user, entry_id):
    messages = load_messages(user)
    return messages[entry_id] if 0 <= entry_id < len(messages) else None
