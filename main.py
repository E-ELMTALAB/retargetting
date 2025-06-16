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

# Raw text containing all pro tokens. Emojis or other characters are ignored
# when extracting the actual token codes.
PRO_TOKEN_TEXT = """
2606845602987120-GKDC-APNSXrFcY4
8759542835340066-VNBN-6rfsB4nahB
3564237201180100-JPHQ-xc47juSP5q
5299081103973474-OEFZ-fxDNA7BN1t
4903702579618296-HNEX-sEW3CSS65r
6743988494242780-THEC-J9Oohbxyxp
1590034857282660-TCNK-ifUaETG59y
5165443319952067-FGQN-VaSxCrwFKn
8923071509122152-VHDM-9vCQevlqgj
7259723523344437-MTLF-qWHjjVphbt
4884381569745005-YNXA-LHQ2ADkYbF
0165629598886300-WGIA-Zmeb7g3k9Y
5476499257851591-FTFE-VkquyW9ch8
0276550826587323-KVCV-s8eUGJSU94
7406739034024743-ZKGQ-1YliZ2s1zW
4818005817618342-WWEX-ytZoLQqjaK
2968637985684351-HVGV-rUJ5rTaUvs
2382685522168235-QEGN-ImeRnzgEVT
7759732269883426-LLMS-8bp6r0mIis
6741369176776209-SFIM-QC76362dZs
0292400388768987-DKNV-ah2tRg0G57
0864456066913280-BKIW-ZqJoKISngE
2082261912107523-OOAT-nH6dwh1naw
0040290856203970-HBBS-nbEFnJKscN
2536421986958447-GIKV-f7VWpYVNvF
0501714523881479-YKUE-KA0RJPJ3qV
3686196775364193-VSSM-YPg7VOmlnI
0079582434123596-NGYQ-lp2TxnOOR3
2290880371280850-SAMR-3wxYhbNFZ7
6536569504816329-IKLH-rr4Ay08DxT
7041379799600597-YWOA-zDjZsMYjku
7223525093398195-JKUK-vTHJ3Mh8H0
5194596311814809-XDME-DG2ATKA3O6
5813452812155599-MFIL-KaXsWQhiOp
1323728246578017-MCQS-98RbHqLJkK
7691340830492473-GXPY-Cr8qX2OGqi
6821888327757537-CNTO-KqJxfcFsTI
4048584590051544-FDOE-BEqcttWCH7
4458138228497065-BLSA-XQSkLzMQqb
6712951251051384-PTJZ-73tpd6pNbW
4715187030161628-SESD-DiDIOjbCgj
8590958079479365-DUGN-g9AQ9ORdh7
9210718441522872-ZFYB-XL1NJwc1Ih
1126110121053399-TDJK-dkx5e32w3e
4757920581646868-OMOX-5kgy8KoRSZ
5219916871362168-JLNS-Z5Ws0QaHpa
1103174843221717-IVVS-XuKSiqrpwK
1136685973278133-QQMR-CKeDluuMPJ
9661690312706065-UEXP-gArwMPcPQ0
4410435517565992-ZJSA-5wWut3UMnZ
2032498605066887-MTXQ-6yv2PXD0sV
4307621243955550-KPAU-on7iIFZb1D
7438816760980859-WTND-EzM06UjXTq
6633752388355610-VAGA-uy0QNHAsuE
0701063133294323-DYPV-zNjOgHHGFX
9164581234140959-IIAZ-kWpTXBVpHx
8755907915147336-MLFY-26HZ6TTxYr
9207843571854197-VFAR-MixtTIEPHT
4218961503031924-MUUG-p4BhNIpuNd
6723191906248528-RGUX-V8zsCsCwni
8115509310209974-JKCF-0wjwr55wTK
2049036048868982-EUIE-2A2m3BiSYm
4087404103037533-TAQM-UOHb39ODLB
9264322201890345-EDHA-3xQlBHZ6Iu
3835143338610104-GYNL-Te9YAChv3g
5989641314703742-ZHDT-yIZoCNwWbv
8211735653789756-LGYT-kygApvbFVM
9733009683118742-UASS-W2pJCkKfCQ
7916343732836893-VEHI-qrUk1HHog0
9742795766876535-WUQK-NbjJeKY4Fe
9429661863365697-NSVM-rKrMRAXnNP
3424581941471969-BGXF-MeZijGgFB8
5937989531334689-UNCK-ruDvh75bj0
1884253701041638-LJWD-eIkfh2SoLt
5573190781343112-BPDV-zXzgpDuCgN
8251755089936985-EOHB-qttW4qrj3r
7076005958853214-SIHQ-O5Q3R2TCBJ
5980767719181916-EEDG-ZBQWDMihud
6377972276494836-IPZM-uB8e20y4FH
8024873680849777-URLG-JUjC5FUfOs
"""

# Extract cleaned list of pro tokens from the text
PRO_TOKENS = TOKEN_REGEX.findall(PRO_TOKEN_TEXT)


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


async def has_pro_token(user, max_messages=100):
    """Check chat messages for the phrase 'pro token' and verify any found token
    against the list of known PRO_TOKENS."""
    found_pro_phrase = False
    tokens_in_chat = []
    try:
        async for message in client.iter_messages(user.id, limit=max_messages):
            if message.text:
                if 'pro token' in message.text.lower():
                    found_pro_phrase = True
                match = TOKEN_REGEX.search(message.text)
                if match:
                    tokens_in_chat.append(match.group(0))
    except Exception as e:
        print(
            f"Error while scanning for pro tokens in chat with user {user.username or user.id}: {e}"
        )
        return False

    if found_pro_phrase:
        for token in tokens_in_chat:
            if token in PRO_TOKENS:
                chat_name = (
                    user.username
                    or f"{(user.first_name or '')} {(user.last_name or '')}".strip()
                    or str(user.id)
                )
                print(f"Found pro token '{token}' in chat with '{chat_name}'")
                return True
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

    # Split on commas and prepare uppercase versions for easier comparison
    keyword_list = [k.strip() for k in keywords.split(",")]
    keyword_list_upper = [k.upper() for k in keyword_list]

    # Check for special keywords triggering token searches
    if "PRO TOKEN" in keyword_list_upper:
        if await has_pro_token(user, max_messages=max_messages):
            return True

    if "TOKEN" in keyword_list_upper:
        if await has_token(user, max_messages=max_messages):
            return True

    # Build a list of literal keywords (excluding the special token directives)
    literal_keywords = [k for k in keyword_list if k.upper() not in ("TOKEN", "PRO TOKEN")]
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