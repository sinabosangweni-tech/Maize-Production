import pandas as pd
from datetime import datetime

# In-memory storage for messages (in a real app, this would be a database)
messages = []

def save_message(message_data):
    """Save a farmer message"""
    message_data['id'] = len(messages) + 1
    message_data['timestamp'] = datetime.now()
    messages.append(message_data)
    return True

def get_messages(priority=None, msg_type=None):
    """Retrieve messages with optional filtering"""
    filtered_messages = messages.copy()
    
    if priority and priority != "All":
        filtered_messages = [m for m in filtered_messages if m['priority'] == priority]
    
    if msg_type and msg_type != "All":
        filtered_messages = [m for m in filtered_messages if m['type'] == msg_type]
    
    # Sort by timestamp, most recent first
    filtered_messages.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return filtered_messages
