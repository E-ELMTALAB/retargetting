# import asyncio
# import nest_asyncio
# from datetime import datetime, timezone, timedelta
# from telethon import TelegramClient, errors, types
# import time
# import psycopg2
# from psycopg2.extras import DictCursor
# import os

# nest_asyncio.apply()

# # --------------------------- Configuration --------------------------- #

# # 1. Telegram API Credentials
# API_ID = 123456  # <-- Replace with your API ID
# API_HASH = '0123456789abcdef0123456789abcdef'  # <-- Replace with your API Hash
# SESSION_NAME = 'retargetting1.session'  # Arbitrary session name without path

# # Database URL
# DATABASE_URL = 'postgresql://posts_owner:jYw1bfDnOHW2@ep-holy-glitter-a287uyrp-pooler.eu-central-1.aws.neon.tech/retargetting?sslmode=require'  # Replace with your database URL

# # Database Helper Functions
# def get_database_settings():
#     conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM settings WHERE id = 1")
#     settings = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return settings

# # Helper function to update operation flag
# def update_operation_flag(flag):
#     conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
#     cursor = conn.cursor()
#     cursor.execute("UPDATE settings SET operation_flag = %s WHERE id = 1", (flag,))
#     conn.commit()
#     cursor.close()
#     conn.close()

# # Fetch settings from the database
# settings = get_database_settings()

# # Get settings values
# START_TIME = settings['start_time']
# INCLUDE_KEYWORD = settings['include_keyword']
# EXCLUDE_KEYWORD = settings['exclude_keyword']
# MAX_USERS_TO_PROCESS = settings['max_users']
# OPERATION_FLAG = settings['operation_flag']

# # 2. Additional settings
# EXCLUSION_DATE = datetime(2025, 5, 5, tzinfo=timezone.utc)
# MESSAGE_SEND_DELAY = 1  # seconds
# MAX_USERS_PER_MINUTE = 20

# client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# def get_sent_user_ids():
#     try:
#         with open("sent_users.txt", "r") as file:
#             return set(int(line.strip()) for line in file if line.strip().isdigit())
#     except FileNotFoundError:
#         return set()

# def log_sent_user(user_id):
#     with open("sent_users.txt", "a") as file:
#         file.write(f"{user_id}\n")

# # async def already_has_keyword(user, keyword, max_messages=100):
# #     try:
# #         async for message in client.iter_messages(user.id, limit=max_messages):
# #             if message.text and keyword in message.text:
# #                 return True
# #     except Exception as e:
# #         print(f"Error while checking for keyword with user {user.username or user.id}: {e}")
# #     return False
# async def already_has_keyword(user, keywords, max_messages=100):
#     try:
#         # If the keywords are "NOTHING", return True
#         if keywords == "NOTHING":
#             return True

#         # Split the keywords string into a list
#         keyword_list = keywords.split(',')

#         async for message in client.iter_messages(user.id, limit=max_messages):
#             if message.text:
#                 # Check if any of the keywords are in the message
#                 if any(keyword in message.text for keyword in keyword_list):
#                     return True
#     except Exception as e:
#         print(f"Error while checking for keywords with user {user.username or user.id}: {e}")
#     return False



# async def get_all_group_messages(group_id):
#     print(f"Fetching messages from group chat ID {group_id}...")
#     all_messages = []
#     try:
#         async for message in client.iter_messages(group_id, reverse=True):
#             all_messages.append(message)
#     except Exception as e:
#         print(f"Error fetching messages from group: {e}")
#     print(f"Fetched {len(all_messages)} messages from the group.")
#     return all_messages

# async def send_message_to_user(user, message):
#     """
#     Send a single message to a user, handling different message types.

#     :param user: Telethon User entity
#     :param message: Telethon Message object
#     """
#     try:
#         if message.text:
#             # Send text message
#             await client.send_message(entity=user, message=message.text)
#             print(f"Sent text message to {user.username or user.id}")
#         elif message.media:
#             # Handle different media types
#             if isinstance(message.media, types.MessageMediaPhoto):
#                 # Send photo
#                 # await client.send_file(entity=user, file=message.media)
#                 print(f"Sent photo to {user.username or user.id}")
#             elif isinstance(message.media, types.MessageMediaDocument):
#                 # Check the document type
#                 doc = message.media.document
#                 if doc.mime_type.startswith('audio'):
#                     # Send voice message
#                     # await client.send_file(entity=user, file=message.media, voice_note=True)
#                     print(f"Sent voice message to {user.username or user.id}")
#                 else:
#                     # Send other documents
#                     # await client.send_file(entity=user, file=message.media)
#                     print(f"Sent document to {user.username or user.id}")
#             elif isinstance(message.media, types.MessageMediaUnsupported):
#                 print(f"Unsupported media type for message ID {message.id}. Skipping.")
#             else:
#                 # Handle other media types like videos, etc.
#                 # await client.send_file(entity=user, file=message.media)
#                 print(f"Sent media to {user.username or user.id}")
#         else:
#             print(f"No content to send for message ID {message.id}. Skipping.")

#         # Delay between sending each message to reduce flood risk
#         await asyncio.sleep(MESSAGE_SEND_DELAY)

#     except errors.FloodWaitError as e:
#         # If Telegram tells us to wait, we obey
#         print(f"[FloodWait] Sleeping for {e.seconds} seconds before retrying...")
#         await asyncio.sleep(e.seconds + 5)
#         await send_message_to_user(user, message)  # Retry
#     except Exception as e:
#         print(f"Failed to send message ID {message.id} to {user.username or user.id}. Error: {e}")

# import uuid

# # async def send_messages_to_user(user, messages):
# #     try:
# #         for message in messages:
# #             if "[ID]" in message:
# #               messsage.replace("[ID]" , str(uuid.uuid4()))
# #             await send_message_to_user(user, message)
# #         log_sent_user(user.id)
# #     except Exception as e:
# #         print(f"Failed to send messages to {user.username or user.id}. Error: {e}")
# async def send_messages_to_user(user, messages):
#     try:
#         for message in messages:
#             # Check if the message is a service message and skip it
#             if isinstance(message, types.MessageService):
#                 print(f"Skipping MessageService for {user.username or user.id}.")
#                 continue  # Skip service messages

#             # Replace [ID] with a new UUID if the message is a regular message and contains [ID]
#             if "[ID]" in message.text:
#                 message.text = message.text.replace("[ID]", str(uuid.uuid4()))
#             print(message.text)

#             # Send the message
#             await send_message_to_user(user, message)

#         # Log the user as successfully sent
#         log_sent_user(user.id)
#     except Exception as e:
#         print(f"Failed to send messages to {user.username or user.id}. Error: {e}")


# async def user_started_chat_before_date(user_id, cutoff_date):
#     try:
#         async for message in client.iter_messages(user_id, reverse=True, limit=1):
#             if message.date < cutoff_date:
#                 return True
#         return False
#     except Exception as e:
#         print(f"Error while checking chat start date for user {user_id}: {e}")
#     return False



# async def main():
#     global OPERATION_FLAG

#     await client.start()
#     print("Client started.")

#     while True:
#         settings = get_database_settings()
#         OPERATION_FLAG = settings['operation_flag']

#         if not OPERATION_FLAG:
#             print("Operation flag is not set. Waiting...")
#             await asyncio.sleep(30)
#             continue

#         group_messages = await get_all_group_messages(-4795827651)  # Replace with GROUP_CHAT_ID
#         if not group_messages:
#             print("No messages to send. Exiting.")
#             break

#         sent_user_ids = get_sent_user_ids()
#         processed_users = 0
#         users_processed_this_minute = 0
#         batch_start_time = time.time()

#         async for dialog in client.iter_dialogs():

#             if processed_users >= settings['max_users']:
#                 break

#             if not dialog.is_user:
#                 continue

#             user = dialog.entity
#             if user.bot or user.id in sent_user_ids:
#                 continue

#             if not await user_started_chat_before_date(user.id, EXCLUSION_DATE):
#                 print(f"The user {user.username or user.id} started chat after {EXCLUSION_DATE}. Skipping...")
#                 continue

#             if settings['include_keyword'] and not await already_has_keyword(user, settings['include_keyword'], max_messages=100):
#                 INCLUDE_KEYWORD = settings['include_keyword']
#                 print(f"The user {user.username or user.id} does not have the keyword '{INCLUDE_KEYWORD}' in chat. Skipping...")
#                 continue

#             if settings['exclude_keyword'] and await already_has_keyword(user, settings['exclude_keyword'], max_messages=100):
#                 EXCLUDE_KEYWORD = settings['exclude_keyword']
#                 print(f"The user {user.username or user.id} has the excluded keyword '{EXCLUDE_KEYWORD}' in chat. Skipping...")
#                 continue

#             if users_processed_this_minute >= MAX_USERS_PER_MINUTE:
#                 elapsed = time.time() - batch_start_time
#                 if elapsed < 60:
#                     sleep_time = 60 - elapsed
#                     print(f"Reached {MAX_USERS_PER_MINUTE} users in under a minute. Sleeping {sleep_time:.1f}s...")
#                     await asyncio.sleep(sleep_time)
#                 users_processed_this_minute = 0
#                 batch_start_time = time.time()

#             print(f"\nSending messages to {user.username or user.id}...")
#             group_messages = await get_all_group_messages(-4795827651)  # Replace with GROUP_CHAT_ID
#             await send_messages_to_user(user, group_messages)

#             users_processed_this_minute += 1
#             processed_users += 1
#             await asyncio.sleep(20)

#         print(f"\nAll messages sent successfully. Processed {processed_users} users this run.")
#         break

# if __name__ == "__main__":
#     try:
#         asyncio.get_event_loop().run_until_complete(main())
#     except KeyboardInterrupt:
#         print("\nScript interrupted by user. Exiting...")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")


import asyncio
import nest_asyncio
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient, errors, types
import time
import psycopg2
from psycopg2.extras import DictCursor
import os
import re

nest_asyncio.apply()

# --------------------------- Configuration --------------------------- #

# 1. Telegram API Credentials
API_ID = 123456  # <-- Replace with your API ID
API_HASH = '0123456789abcdef0123456789abcdef'  # <-- Replace with your API Hash
SESSION_NAME = 'retargetting1.session'  # Arbitrary session name without path

# Database URL
DATABASE_URL = 'postgresql://posts_owner:jYw1bfDnOHW2@ep-holy-glitter-a287uyrp-pooler.eu-central-1.aws.neon.tech/retargetting?sslmode=require'  # Replace with your database URL

# Database Helper Functions
def get_database_settings():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings WHERE id = 1")
    settings = cursor.fetchone()
    cursor.close()
    conn.close()
    return settings

# Helper function to update operation flag
def update_operation_flag(flag):
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    cursor = conn.cursor()
    cursor.execute("UPDATE settings SET operation_flag = %s WHERE id = 1", (flag,))
    conn.commit()
    cursor.close()
    conn.close()

# Fetch settings from the database
settings = get_database_settings()

# Get settings values
START_TIME = settings['start_time']
INCLUDE_KEYWORD = settings['include_keyword']
EXCLUDE_KEYWORD = settings['exclude_keyword']
MAX_USERS_TO_PROCESS = settings['max_users']
OPERATION_FLAG = settings['operation_flag']

# 2. Additional settings
EXCLUSION_DATE = datetime(2025, 6, 6, tzinfo=timezone.utc)
MESSAGE_SEND_DELAY = 1  # seconds
MAX_USERS_PER_MINUTE = 20

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Regex pattern for matching tokens of the form "16 digits-UPPER(4)-alphanumeric(10)"
TOKEN_REGEX = re.compile(r"\b\d{16}-[A-Z]{4}-[A-Za-z0-9]{10}\b")


def get_sent_user_ids():
    try:
        with open("sent_users.txt", "r") as file:
            return set(int(line.strip()) for line in file if line.strip().isdigit())
    except FileNotFoundError:
        return set()


def log_sent_user(user_id):
    with open("sent_users.txt", "a") as file:
        file.write(f"{user_id}\n")


async def has_token(user, max_messages=100):
    """
    Scan the user's recent messages for any token matching TOKEN_REGEX.
    If a token is found, print the token and chat name, then return True.
    Otherwise, return False.
    """
    try:
        async for message in client.iter_messages(user.id, limit=max_messages):
            if message.text:
                match = TOKEN_REGEX.search(message.text)
                if match:
                    token = match.group(0)
                    # Determine a human-readable chat name
                    chat_name = user.username or f"{(user.first_name or '')} {(user.last_name or '')}".strip() or str(user.id)
                    print(f"Found token '{token}' in chat with '{chat_name}'")
                    return True
    except Exception as e:
        print(f"Error while scanning for tokens in chat with user {user.username or user.id}: {e}")
    return False


async def already_has_keyword(user, keywords, max_messages=100):
    """
    Check whether the chat with 'user' contains any of the specified 'keywords'.
    - If keywords == "NOTHING", always return True.
    - If "TOKEN" appears anywhere in the comma-separated keywords list, invoke has_token().
    - Otherwise, split the comma-separated keywords string and search for any of them in recent messages.
    """
    # If the keywords are "NOTHING", skip all checks and return True
    if keywords == "NOTHING":
        return True

    # Split on commas and strip whitespace
    keyword_list = [k.strip() for k in keywords.split(",")]

    # If "TOKEN" is one of the requested checks, run the token‐search routine first
    if "TOKEN" in keyword_list:
        if await has_token(user, max_messages=max_messages):
            return True

    # Build a list of literal keywords (exclude the special "TOKEN" token)
    literal_keywords = [k for k in keyword_list if k != "TOKEN"]
    if not literal_keywords:
        # No other keywords to check—if "TOKEN" wasn't found, return False
        return False

    # Otherwise, iterate through recent messages looking for any literal keyword
    try:
        async for message in client.iter_messages(user.id, limit=max_messages):
            if message.text:
                if any(kw in message.text for kw in literal_keywords):
                    return True
    except Exception as e:
        print(f"Error while checking for keywords with user {user.username or user.id}: {e}")

    return False


async def get_all_group_messages(group_id):
    print(f"Fetching messages from group chat ID {group_id}...")
    all_messages = []
    try:
        async for message in client.iter_messages(group_id, reverse=True):
            all_messages.append(message)
    except Exception as e:
        print(f"Error fetching messages from group: {e}")
    print(f"Fetched {len(all_messages)} messages from the group.")
    return all_messages


async def send_message_to_user(user, message):
    """
    Send a single message to a user, handling different message types.

    :param user: Telethon User entity
    :param message: Telethon Message object
    """
    try:
        if message.text:
            # Send text message
            await client.send_message(entity=user, message=message.text)
            print(f"Sent text message to {user.username or user.id}")
        elif message.media:
            # Handle different media types
            if isinstance(message.media, types.MessageMediaPhoto):
                # Send photo
                # await client.send_file(entity=user, file=message.media)
                print(f"Sent photo to {user.username or user.id}")
            elif isinstance(message.media, types.MessageMediaDocument):
                # Check the document type
                doc = message.media.document
                if doc.mime_type.startswith('audio'):
                    # Send voice message
                    # await client.send_file(entity=user, file=message.media, voice_note=True)
                    print(f"Sent voice message to {user.username or user.id}")
                else:
                    # Send other documents
                    # await client.send_file(entity=user, file=message.media)
                    print(f"Sent document to {user.username or user.id}")
            elif isinstance(message.media, types.MessageMediaUnsupported):
                print(f"Unsupported media type for message ID {message.id}. Skipping.")
            else:
                # Handle other media types like videos, etc.
                # await client.send_file(entity=user, file=message.media)
                print(f"Sent media to {user.username or user.id}")
        else:
            print(f"No content to send for message ID {message.id}. Skipping.")

        # Delay between sending each message to reduce flood risk
        await asyncio.sleep(MESSAGE_SEND_DELAY)

    except errors.FloodWaitError as e:
        # If Telegram tells us to wait, we obey
        print(f"[FloodWait] Sleeping for {e.seconds} seconds before retrying...")
        await asyncio.sleep(e.seconds + 5)
        await send_message_to_user(user, message)  # Retry
    except Exception as e:
        print(f"Failed to send message ID {message.id} to {user.username or user.id}. Error: {e}")


import uuid

async def send_messages_to_user(user, messages):
    """
    Send a batch of messages (from a group) to a single user.
    Skips service messages and injects a new UUID if the text contains “[ID]”.
    """
    try:
        for message in messages:
            # Skip service messages
            if isinstance(message, types.MessageService):
                print(f"Skipping MessageService for {user.username or user.id}.")
                continue

            # Replace [ID] with a new UUID if present
            if message.text and "[ID]" in message.text:
                message.text = message.text.replace("[ID]", str(uuid.uuid4()))
            if message.text:
                print(message.text)

            # Send the message
            await send_message_to_user(user, message)

        # Log the user as successfully sent
        log_sent_user(user.id)
    except Exception as e:
        print(f"Failed to send messages to {user.username or user.id}. Error: {e}")


async def user_started_chat_before_date(user_id, cutoff_date):
    """
    Return True if the last message from the user was before 'cutoff_date'. Otherwise, False.
    """
    try:
        async for message in client.iter_messages(user_id, reverse=False, limit=1):
            if message.date < cutoff_date:
                return True
        return False
    except Exception as e:
        print(f"Error while checking chat start date for user {user_id}: {e}")
    return False


async def main():
    global OPERATION_FLAG

    await client.start()
    print("Client started.")

    while True:
        settings = get_database_settings()
        OPERATION_FLAG = settings['operation_flag']

        if not OPERATION_FLAG:
            print("Operation flag is not set. Waiting...")
            await asyncio.sleep(30)
            continue

        group_messages = await get_all_group_messages(-4795827651)  # Replace with GROUP_CHAT_ID
        if not group_messages:
            print("No messages to send. Exiting.")
            break

        sent_user_ids = get_sent_user_ids()
        processed_users = 0
        users_processed_this_minute = 0
        batch_start_time = time.time()

        async for dialog in client.iter_dialogs():

            if processed_users >= settings['max_users']:
                break

            if not dialog.is_user:
                continue

            user = dialog.entity
            if user.bot or user.id in sent_user_ids:
                continue

            if not await user_started_chat_before_date(user.id, EXCLUSION_DATE):
                print(f"The user {user.username or user.id} started chat after {EXCLUSION_DATE}. Skipping...")
                continue

            # If include_keyword is set, check if the chat already contains it
            if settings['include_keyword'] and not await already_has_keyword(user, settings['include_keyword'], max_messages=100):
                INCLUDE_KEYWORD = settings['include_keyword']
                print(f"The user {user.username or user.id} does not have the keyword '{INCLUDE_KEYWORD}' in chat. Skipping...")
                continue

            # If exclude_keyword is set, check if the chat contains it (or a token if exclude_keyword=="TOKEN")
            if settings['exclude_keyword'] and await already_has_keyword(user, settings['exclude_keyword'], max_messages=100):
                EXCLUDE_KEYWORD = settings['exclude_keyword']
                print(f"The user {user.username or user.id} has the excluded keyword or token '{EXCLUDE_KEYWORD}' in chat. Skipping...")
                continue

            if users_processed_this_minute >= MAX_USERS_PER_MINUTE:
                elapsed = time.time() - batch_start_time
                if elapsed < 60:
                    sleep_time = 60 - elapsed
                    print(f"Reached {MAX_USERS_PER_MINUTE} users in under a minute. Sleeping {sleep_time:.1f}s...")
                    await asyncio.sleep(sleep_time)
                users_processed_this_minute = 0
                batch_start_time = time.time()

            print(f"\nSending messages to {user.username or user.id}...")
            group_messages = await get_all_group_messages(-4795827651)  # Replace with GROUP_CHAT_ID
            await send_messages_to_user(user, group_messages)

            users_processed_this_minute += 1
            processed_users += 1
            await asyncio.sleep(20)

        print(f"\nAll messages sent successfully. Processed {processed_users} users this run.")
        break


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")