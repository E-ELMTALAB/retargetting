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

#                         # Send the message
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


def log_user_info(user):
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO telegram_users (chat_id, first_name, last_name, username)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (chat_id) DO UPDATE
        SET first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            username = EXCLUDED.username
        """,
        (
            user.id,
            getattr(user, 'first_name', None),
            getattr(user, 'last_name', None),
            getattr(user, 'username', None),
        ),
    )
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
EXCLUSION_DATE = datetime(2023, 6, 6, tzinfo=timezone.utc)
MESSAGE_SEND_DELAY = 1  # seconds
MAX_USERS_PER_MINUTE = 20

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Regex pattern for matching tokens of the form "16 digits-UPPER(4)-alphanumeric(10)"
TOKEN_REGEX = re.compile(r"\b\d{16}-[A-Z]{4}-[A-Za-z0-9]{10}\b")

# Raw text containing all pro tokens. Emojis or other characters are ignored
# when extracting the actual token codes.
PRO_TOKEN_TEXT = [
    "0010709693205105-ACAG-bU7bO3rTF4",
    "0040290856203970-HBBS-nbEFnJKscN",
    "0067790337975878-LIVE-jzz06kOwEw",
    "0079582434123596-NGYQ-lp2TxnOOR3",
    "0087635746096400-EWOQ-1PgtnB90IL",
    "0108266119832926-PUVD-oVBBSr4Rhl",
    "0139399494016442-YEZY-N8EBxFljcz",
    "0149516732110798-KLHH-cCtPhUYFtM",
    "0150940641291688-XFKR-L00ynoQwd0",
    "0152695440442975-VFUS-SSMqOXNpd6",
    "0161751519739377-GKGA-ALs5KS26VT",
    "0165629598886300-WGIA-Zmeb7g3k9Y",
    "0174551241352642-IZDU-c2qnwOat2F",
    "0174823131406919-IHCK-fx8RWATiHW",
    "0191487626283477-UFBH-Bux7t35Ymu",
    "0192239428948390-QSLH-78kNu42gGt",
    "0201492697930649-SWWM-o9NaA9fFrL",
    "0226702608748101-OOBS-DvEVbMJpH4",
    "0240297894236711-UJFW-8BZkxwMEDQ",
    "0255203313574157-ZNOB-Ns2PhaaXrq",
    "0261253751499098-INOU-nPd3ogVWC6",
    "0276550826587323-KVCV-s8eUGJSU94",
    "0280590361384422-ERUK-AUE2F50EG3",
    "0285546459730536-SKIF-JsoAMZT41v",
    "0292400388768987-DKNV-ah2tRg0G57",
    "0300081176386327-HEFW-ik8OAe5VJ4",
    "0302230750510295-ZTSW-w5WCq29kG2",
    "0338327988884165-RLRE-x0ZLiBNIhV",
    "0365823790010905-VRAZ-BMzOA94eNp",
    "0371629160970409-EIBK-d33uyCbc1I",
    "0372751840837438-RIYR-LFjP7RNcxq",
    "0380203646257997-QXYE-uUXHAihnj2",
    "0381935671817875-LNYZ-VgcXekZpbE",
    "0384450420146589-QJDJ-23Ho7ICLKc",
    "0389227352685278-CEBG-EzA4B5LDgr",
    "0403498340543349-POMB-jud0mOjKve",
    "0408459980039608-DRMQ-HjBhpHezKA",
    "0409003320477305-LWDP-EChc3XJEg2",
    "0426297543788360-NPEH-yBH1anuS0D",
    "0436043656318346-IIYC-Lc7t3nb8sz",
    "0463956269352735-AKWH-BYw2ZfaLW5",
    "0488243983644687-VWNI-7b86E3xggl",
    "0501714523881479-YKUE-KA0RJPJ3qV",
    "0525598672172919-JVZI-07ULCUe93k",
    "0544897698010133-YDQP-WKBq50G6Dm",
    "0554351758062207-AMEJ-zwDQbWssbU",
    "0572240503886809-AHZQ-0cPHL35K25",
    "0585203753477677-JHYG-WkWyHjdf0F",
    "0596484110064366-OALS-S3iri2x01Z",
    "0614314781078637-SWRE-VTO4aR16PB",
    "0633135784238183-BIHQ-OLJqPcfD3v",
    "0635605652441372-JQWM-YN1cVlRHC9",
    "0636105765919434-EQDF-rWCBrjUQfu",
    "0639421664122196-HQRQ-7K28zPw890",
    "0639487312143282-PWVX-VSZEwXLjFq",
    "0691728883055102-QKFW-EfjjvISiFj",
    "0700623282470637-PNPC-jywTa16E6h",
    "0701063133294323-DYPV-zNjOgHHGFX",
    "0717805502637124-YBQK-RcKmQMSMee",
    "0767061570511015-XQYK-QQjXboOzH5",
    "0784737700715037-DNLP-rHBY6JrlQY",
    "0799506547410792-BTRV-pGYnqA78xG",
    "0823437483413420-RAJV-VH3w66EZmA",
    "0833851224335479-EPJI-mqlICfnUxg",
    "0833976168569975-NQID-hyW53K6rLb",
    "0842699295023855-FHNP-s2IrbBWz7B",
    "0850340913368869-QAQO-O2Cg5OVuwl",
    "0853878813453357-YWNV-K9Gfp5bHiM",
    "0864456066913280-BKIW-ZqJoKISngE",
    "0867442283125520-GIKX-vP4czyiX5Z",
    "0875484497727010-OJOC-BpRFtABW5B",
    "0916182423306291-XMFJ-tanGQQluSN",
    "0917086717883229-VQOD-uymRywCrUz",
    "0921143851842012-MFLS-fC61roKSxX",
    "0950754486250017-LSFO-ftfMCn5b0t",
    "0964442176230657-EXKA-o6oLnEFEWl",
    "0971032340709349-MSYB-cEQdAltBOD",
    "0972428301171491-ALPI-Mbhn9nk1R4",
    "0973394288801321-TIBL-p4S7o44VIn",
    "0973668725130250-USZD-lyvTNTtKXL",
    "0993625464841571-ILXS-7fieHqI6xp",
    "1020072255878260-ARAB-Ir8ngfXKbt",
    "1021373430453858-OJGX-N8gJvkwvZV",
    "1027171823139339-MRXO-uGtaZ8DlPi",
    "1054737035264530-MGGG-XYhextfFum",
    "1059597542893200-JIDD-VN1qEoQDjG",
    "1067823853344324-GMSA-aR6q5Tb0OK",
    "1082593515685400-LOEX-FXvtfBK7WQ",
    "1085496704957232-YRNZ-y3lKqwu0Jt",
    "1089865389114784-XWAR-DEE2BGvryG",
    "1097066604686494-TFOM-6JY2jFhenY",
    "1101380503701888-SQUU-quhQKZSZNI",
    "1103174843221717-IVVS-XuKSiqrpwK",
    "1112830613196573-JXTR-dG74qqZGel",
    "1114415271991009-VMYB-SYomzVJDLF",
    "1116677664048981-COPH-rJX4IfpHG2",
    "1124694552339433-OGTU-p3q7h1DVH9",
    "1126110121053399-TDJK-dkx5e32w3e",
    "1136685973278133-QQMR-CKeDluuMPJ",
    "1141373689319440-EXSR-DjmCaz3IWA",
    "1170008174969427-ZUHS-aXegzhuB2Q",
    "1179137245712671-TUFF-Wqd73XaYWr",
    "1180935646729754-GIWM-bXkbDxE4G7",
    "1194887845308044-OLQS-XAPX1o0vL8",
    "1198983612027591-DQPQ-r9iecU5czz",
    "1240121349241072-CTZP-LgVUoALoM6",
    "1242010645792869-GTJD-JJixeGINqE",
    "1253689901100612-OCUN-WqQIsmAWcL",
    "1254837933454598-JROZ-y2leEuq6lk",
    "1272403160236095-EHKB-R33mJbA73t",
    "1272988859738685-YXQJ-Z3qPidHRTa",
    "1274319135097845-JTVC-ivJXocAB4q",
    "1323728246578017-MCQS-98RbHqLJkK",
    "1326637114836354-VHKX-iv4PtIjI8U",
    "1353431512136014-JRIP-M5OXrEwxho",
    "1358350499769118-KZHD-4VJr4uAKtw",
    "1373643491309856-TKBT-9W9qNo6cxZ",
    "1374164988456348-CHVL-kRU9PdTnNI",
    "1386921938225747-BYHA-lOf5AEfWm1",
    "1400882191519861-EVZB-uT9KCGpqXy",
    "1434934319064770-GUYT-EGWb0m45dP",
    "1440719750334428-JBCM-eTmDAd41s7",
    "1469529848524044-DPCH-vEYkBYfYWU",
    "1482456432045438-CPGA-EtvplHtUzi",
    "1490455067793631-OPWK-CIkUB4r9yN",
    "1490922186911148-GYLB-QD69Zwq5IR",
    "1499450595487299-HBEM-RUtNC4YKRP",
    "1502590478877563-DIOH-U08qMUdGYD",
    "1515363547948115-QELG-AMO7dCt5gp",
    "1518862880539587-RJTP-2hnHm1eSpf",
    "1538509935587074-JGUY-eDJArDir02",
    "1545593955409460-ESKL-EcwqMrqAOS",
    "1580748434782231-IFKM-4QviWNW0JJ",
    "1584349491850150-OJOV-EGCcuhRY6H",
    "1590034857282660-TCNK-ifUaETG59y",
    "1612170451545362-SZIC-QeYjTsugt2",
    "1659313952401149-WROH-UxGzWOL00n",
    "1666094440461424-RNDC-fwIlqi9erE",
    "1687897047404074-OFDW-E9PaczyzrW",
    "1702933814249692-RSTX-i4CDCo9hzC",
    "1703192588101160-NPTV-jgpO2UTVkA",
    "1718764214350415-FDDH-vcAMeFgD3o",
    "1745227415100818-EKQZ-7snEiO9pWn",
    "1766589676418878-SAFF-eYYOHEqDs0",
    "1794487614767004-XQYD-E3edlq9GJB",
    "1799402429580545-QYSB-xrfwtlsEC6",
    "1834946453629609-IVBF-HWahhTUN98",
    "1837496848327293-RIAC-7Z6JfAVVmn",
    "1839005270668346-JUJB-U4qGf09jv1",
    "1858186166052180-OMLP-VkJ8UmyTK3",
    "1876153715775745-HHVW-8lPIhZfcWR",
    "1884253701041638-LJWD-eIkfh2SoLt",
    "1925514427794934-XMCA-lKJ59ouu1e",
    "1926977974488022-XIKY-RayJqMu6z4",
    "1945686363726241-CIGG-RXY7BrpYG1",
    "1947311557565118-ENMB-rkTlV4yWsn",
    "1959809188854366-AUKM-cQDf2d755Q",
    "1961466811021613-NYAC-AOdCkuxtci",
    "1963547993564653-LNET-PFmDOCSGaW",
    "2005116678304923-KYCL-qYt5YhdYLM",
    "2008067750753504-HZWV-SSSerPJFCk",
    "2028335294178503-ZHBN-bS8ve6C1gp",
    "2032498605066887-MTXQ-6yv2PXD0sV",
    "2038719707032609-KKRB-NavZMTJ3Xu",
    "2041718798085636-GRLB-GU9wCv6rZU",
    "2044052692419106-PDIK-O5UIGpnF68",
    "2049036048868982-EUIE-2A2m3BiSYm",
    "2082261912107523-OOAT-nH6dwh1naw",
    "2130197989728618-XMZH-LJOKCNHWrU",
    "2142109316088964-KAIY-mReMA4VCYr",
    "2145671024252293-NAPP-UBmS5ys74P",
    "2150760842954968-ZUIQ-SsN73A5qvK",
    "2158918635327565-FKJH-KkEs7JN8rl",
    "2210738472805768-INYP-BylhFRTSW6",
    "2224371937032869-XMCX-CNzYc0Y3KZ",
    "2259378477566377-WXHP-M2lD9EtZ3F",
    "2279777447393466-SBOU-cSjCevEQ29",
    "2283606794535771-MKIY-FxrWjxUaJu",
    "2290880371280850-SAMR-3wxYhbNFZ7",
    "2291619649315435-KHRL-tR31iUMI2R",
    "2333249495189305-NEAN-CBysJ9QfI0",
    "2348148944215477-KPPH-9Nx0oFjiRU",
    "2361104007466239-DCHE-JEpElXnIsa",
    "2364476142443527-BUNC-xWO4F7ERlu",
    "2382685522168235-QEGN-ImeRnzgEVT",
    "2391670001249247-ZKDQ-aYdjp5iFUA",
    "2393115823737688-BXRB-0qKLQl06DJ",
    "2396905685013447-NWEA-17N9nMGQrU",
    "2418034429826337-STPF-BmLNnMOPJX",
    "2422234958404461-OPKO-iLF1y1awl2",
    "2432077410514250-WSGO-g9U14BhkiX",
    "2455488706815325-OXMV-Vh9ApZSwlz",
    "2460890069622340-LUMH-Vpte9PSUou",
    "2502755185324606-CQAT-VAkzijibDw",
    "2502822682589533-PMEX-QNp5c2nsvE",
    "2536421986958447-GIKV-f7VWpYVNvF",
    "2537242645862147-FVZV-lRAxwyCzl1",
    "2555205697908097-NQOY-4RJ0RLRMVO",
    "2555580849286677-VHNN-zmwZZ0gSvG",
    "2566033006247121-ZVLX-Lu9Lu1LCn3",
    "2580261509925706-IUPX-SG8aRUyuEL",
    "2602273304537505-VSNV-SsEHz8Fyh6",
    "2606845602987120-GKDC-APNSXrFcY4",
    "2616332189558987-TMVI-jsJGSk6tE7",
    "2618789810645109-WNIX-3NlHlePctv",
    "2619673547864490-XHPF-j9PjHBngSK",
    "2625812437984275-OHCN-PeHNkatign",
    "2625938398059919-MMVZ-net0qDUMXE",
    "2629347556185738-TZYI-BJXXW9sMVH",
    "2675321241839511-HZDO-61u1UzhC4p",
    "2680935009529984-WABZ-LYsy0mNaO0",
    "2704422876551182-PZXS-vswEVTtw4K",
    "2713164475583230-CBDD-JwEghUFc7g",
    "2723910795616018-JDHO-qt8ZOsNDHg",
    "2735536453610347-KRYI-GKnhjBjPpf",
    "2737185370620061-JVXE-jb3j8tdXda",
    "2743469592493167-TIOY-Jh6okbeYzg",
    "2746077530243011-IBYP-YC0mxA78kT",
    "2794685898579166-MHRL-ZA1JA5SpmA",
    "2823240764672024-UQVD-imEe27TBxo",
    "2826525799110946-DKMQ-3HVjix9CHw",
    "2835318484894391-ZWGY-oaKwJXOOvB",
    "2843318772393618-GOUT-kocsABgBHu",
    "2848681749704519-RPQI-VVS3TPVWJH",
    "2870939778526447-KKDS-TEwxhPSkEz",
    "2883447306590718-UIMM-pb8ON9TJyS",
    "2898815353939887-KVVB-Paf04odZ1y",
    "2915516659285394-YKNH-qZzleFKD2a",
    "2968637985684351-HVGV-rUJ5rTaUvs",
    "2981237125739558-LPCY-bKm62RaMiR",
    "2991649769532821-CQKE-rN1jYx9mzA",
    "2995939130553625-OPCV-XyVHJkHCaN",
    "2996255014456488-ZMND-MKLrwRSMnr",
    "3004887441708347-DXEB-QVFWdJFdkV",
    "3009926195889634-MOIB-ZxEFkfdCJf",
    "3051606084955721-FMKI-N9SCMrSnY7",
    "3059713694727387-ODNF-XxbFo5oxJH",
    "3073148564802982-CNCN-kO7dkzcJT7",
    "3097199769406843-HFTH-nzBYl4JaOa",
    "3136820101102812-MIJA-B9kTJHn0Ui",
    "3141981839292183-LBRJ-WMIWr0caVc",
    "3145469608413699-LPBY-r8WUsidYR9",
    "3165101340804176-QQTP-jDdUThjAHi",
    "3171446280844454-GVIK-XlOC2myk4t",
    "3179365876685367-THFD-NO0STepgC0",
    "3179627584406059-QMKZ-qCa4fgR4Xs",
    "3210100387568881-WDGY-jnGikn7C7p",
    "3219333963006540-LHRU-aryP7aJXos",
    "3238623216440652-OFYK-zLeM88OhRP",
    "3281369316928634-LSFW-rSXx2mqVGi",
    "3291745291315907-EVRF-w7kgV4vXyP",
    "3309654530799142-IRLI-del8CuE8EV",
    "3333679101548705-PSWT-gswJEYPa2C",
    "3367350635027290-DJUO-NhYMH8YfyL",
    "3424581941471969-BGXF-MeZijGgFB8",
    "3433972423640630-RWZJ-BJEdVsBI5y",
    "3454240483124509-LBRW-fepkkzRcRd",
    "3456984302046843-PJIR-urVG6Wvv6H",
    "3482437993231020-ZYHJ-rg9DGgvtZu",
    "3563214175798801-STPQ-sji5vL6w48",
    "3564237201180100-JPHQ-xc47juSP5q",
    "3567828333571613-PCSW-JoqMqTLrfX",
    "3570569283072157-BVON-0NF9DKRm5g",
    "3571439950363997-FBTE-fRIVPXActR",
    "3578014362846441-WESG-eJid8MUW1A",
    "3578661594099719-YHZZ-xQ3TbBTpp0",
    "3609358893279071-HVIJ-oWqrdTJTJB",
    "3632888586987829-TFXF-ldammHdgyH",
    "3641906151933518-IXZT-j2J16MOo7m",
    "3646295042674593-VDSU-iZ1qDVXffE",
    "3647898069455764-HLCV-ExWd8ITWaV",
    "3648480446303038-XSVE-sqIueKEya1",
    "3685287215871515-WYBP-4V7zbS4CDE",
    "3686196775364193-VSSM-YPg7VOmlnI",
    "3690486756884499-YKPS-d9eRON88ee",
    "3692750848022320-KHFT-khQHRr5GL4",
    "3707663071604477-VYAQ-pbOIbos2Bi",
    "3740827430119705-TSVH-TMn4mi0pnZ",
    "3751655876411820-AIBG-le48q0hEys",
    "3757640944626948-ICKU-aDWjGMQm2p",
    "3761796552160267-YDMY-vuzXkTUdQB",
    "3762201839915574-CJSK-q9b8gqkq4N",
    "3763148597586654-NGIQ-wejLCK1oIC",
    "3795505989325075-YQPJ-18t7eEm8He",
    "3828403152877463-PPJQ-RYyfwdMKHZ",
    "3829273460799670-KPPE-nyh5X7Q6rn",
    "3835143338610104-GYNL-Te9YAChv3g",
    "3839672344314404-CBWV-EYkFY9nylu",
    "3860634578404285-KGBJ-uusJRU3Ins",
    "3881916766694558-MLVA-A3p88uRHaz",
    "3908633086034038-SXTG-fwgxA6WOCE",
    "3995048918325775-FRXO-BHgGR2y5yB",
    "4002417769048938-DTNA-qNezI9jfQr",
    "4014412432924228-FIYE-MqZ4PqSgQn",
    "4014633456945364-HGWB-6ROaBRuDy2",
    "4028910584946750-ITGD-GbownG9Hah",
    "4029523463776684-YHTE-1Z8m2ytxfo",
    "4037029339479866-BGFE-XNmpFcT36Y",
    "4048584590051544-FDOE-BEqcttWCH7",
    "4049179652308707-LEDT-KaPpgeI2xQ",
    "4051818211385841-KDGW-pVMBI2byLE",
    "4053443697949635-DUKT-hA5gB2o7iL",
    "4055168356044959-JKQS-fYYsnXDKDU",
    "4055516517692639-VFYL-a8kQBMJryW",
    "4087404103037533-TAQM-UOHb39ODLB",
    "4113654646259573-NSOF-bxwZzzsXXQ",
    "4115036853931201-RWVA-RBYZekrfcA",
    "4118109167958027-WYBQ-9Cfa0QcTx1",
    "4121407685650160-OIDV-KP0AlY9kP0",
    "4145607819393991-OVDF-V129RNCg47",
    "4160850813813918-JAXK-x3oC0gTHiH",
    "4184411623384867-XNJL-6uWzmW1ciq",
    "4193578111027080-XQTO-JEwF7aknvY",
    "4218961503031924-MUUG-p4BhNIpuNd",
    "4224192673313425-NHVH-KyhGMFKbCS",
    "4239264348275059-BRFQ-lMdlcAD7Ov",
    "4256418704905036-NHOB-2pr0pHPYno",
    "4263159948284139-NJVX-qq4Qbgb35k",
    "4268744414247319-ZBDY-yJCeFf9c4B",
    "4279694879460707-CRAC-LJZIafFju6",
    "4307621243955550-KPAU-on7iIFZb1D",
    "4316358116439762-HOAE-M31LVojhvk",
    "4339250805949127-RRQL-nKvKmRKr5e",
    "4356735872923915-ARWU-SF0qIA3ZSl",
    "4361919541162861-LHIF-fAh7sYwKZT",
    "4362268102033634-HAZW-FN8gFP41X9",
    "4371126266911438-LUHH-uNSfTBehIJ",
    "4383433666115123-WXGM-Oygi4TkkHK",
    "4390564214864734-UKOS-kQy0gyFMB1",
    "4403189620529722-MWHE-6Tq9xAllJV",
    "4408753032497723-KLOU-e3EJA8n5Of",
    "4410435517565992-ZJSA-5wWut3UMnZ",
    "4413939831245347-QOJA-USpgL5kCvZ",
    "4418290815386018-VNYS-iMhIKEOJ2S",
    "4432052660247904-RNDI-P6YxUWILkV",
    "4438236567270669-GEPH-9VE7iFEJld",
    "4458138228497065-BLSA-XQSkLzMQqb",
    "4479865498072315-BXNZ-fTjR0jhLfh",
    "4484891512792596-ZAXP-iM0sCtlXcb",
    "4484998529186612-URDC-iKO9yNf68u",
    "4489869506968821-AKWZ-cK5Qnir5at",
    "4497177863706107-XYDD-RKhOK52wC6",
    "4527483180069769-SKQQ-MSWPvN3Qcz",
    "4531210152552970-KOAU-pxY9UhRkn4",
    "4533022663972978-VKQO-rfVI74eTqD",
    "4550851513604068-DWGK-MC2QZ3K3h6",
    "4557026731760273-MABZ-Ah7TWzD9nz",
    "4561549175128030-DDIR-dNPdOtqr8G",
    "4570548441606227-HKSG-MQdsIXCHji",
    "4575314011785183-KHTC-GquWAkcPe2",
    "4578940227685754-KBMV-mvZJQiXJ3E",
    "4585657781231454-VMQY-VHWiER7AyQ",
    "4610305095463767-IPTY-CJvvo3mFHg",
    "4619294804833121-CKEB-xxzfOqJojI",
    "4636311334347031-AESZ-yebdk1CTVi",
    "4644343804675815-XQHF-mVaENWnu0N",
    "4684874617867095-VWJC-2xoRMBj0zl",
    "4707639649797805-OKNL-KkIICa3hGw",
    "4711271703542058-YRFB-DEzv3IlvuG",
    "4713025510063704-YCEB-KQuG1Ooe2j",
    "4715187030161628-SESD-DiDIOjbCgj",
    "4750158590922469-XCDP-fye5BrLTVA",
    "4757920581646868-OMOX-5kgy8KoRSZ",
    "4761722888942236-ZIRO-l1lPBJLJyH",
    "4782322927766503-NOJF-FW8rCCBqm4",
    "4803808881707674-VOOV-cJhaQ29XR9",
    "4818005817618342-WWEX-ytZoLQqjaK",
    "4822476703620563-TCAU-YJurhRugv5",
    "4822500562619652-DLFD-wMei8gsiLi",
    "4833538399067028-BNYI-KWBZg4ne0o",
    "4833588722890753-BRHC-CFSD6qXnUw",
    "4837605090656276-CSAI-cAyYzOKAZd",
    "4848701388648292-TRAG-J6e2H7ZO90",
    "4871688808338034-TBRB-fbjM84fTPX",
    "4884381569745005-YNXA-LHQ2ADkYbF",
    "4887191929518921-VWPY-mKQ02ZydVO",
    "4901362410112543-RDWK-LkkfGmd01C",
    "4903702579618296-HNEX-sEW3CSS65r",
    "4917333387274743-TYDF-aoTH17OG1z",
    "4918939641013806-PZZJ-UdLbJQzaeE",
    "4919992915399592-EEJU-U6WaMGpmZV",
    "4921471262069964-GGIE-rty9HqUNDa",
    "4945303543313881-KQNV-oYw4hNyAyy",
    "4953671052681942-GMSJ-Oxr5zih1U0",
    "4966154290572040-OPPX-K1X0JXzU4u",
    "4992594491182385-BTPF-6aMfqwSlbV",
    "5004888837573131-NUOF-RrgiWT86Oj",
    "5010693540450406-APFK-6BkHee91Ue",
    "5018779296639222-CIQR-5x19GjLfq8",
    "5025780387590840-CPTI-AVWVOtiKgV",
    "5047212688561244-VUJH-ANvobBRu0X",
    "5052616082278184-GSRR-mGcXQOfdOU",
    "5058509900033708-NRFI-QuYSwG30li",
    "5107321894210113-CPSX-DZVKDEKXgn",
    "5121039807347790-LXIQ-AnBDGYJrAL",
    "5121449859422694-MQPS-ID4utrWQFP",
    "5124515294742416-QFQO-evvQVLqspv",
    "5125824334396573-SVHR-yNnerGKszz",
    "5128253717260697-LGPL-jiSWMJbbL5",
    "5132214972133485-BJYI-XEH1m8I2cT",
    "5143149452193192-CNHK-7FitubAZl2",
    "5165443319952067-FGQN-VaSxCrwFKn",
    "5194596311814809-XDME-DG2ATKA3O6",
    "5195013731567857-DBBY-kI0b3euv4F",
    "5196555073115500-MQKQ-2u2rgBrWS9",
    "5216189126327171-WJSS-VXFHeM7dEy",
    "5219916871362168-JLNS-Z5Ws0QaHpa",
    "5224501697760729-YWDT-O2PqEm8tEZ",
    "5245004808492963-CQBJ-AZm7RBAOpv",
    "5256890488991608-JNUX-rwewjAiCH0",
    "5257543341419928-OBTD-SUm8jyEXms",
    "5258696309073929-MPOT-nFXUrDqRq3",
    "5265075539735019-AKIH-CdaCTG7j8T",
    "5269339266478692-VHRU-dUF03JVvee",
    "5277212522814172-IISX-xlXlVm4g7o",
    "5294656239877221-JLAU-8DKiuiZLeC",
    "5299081103973474-OEFZ-fxDNA7BN1t",
    "5315864833848580-YRMX-xx2IfJdZCL",
    "5331326104930053-YGUU-rSJwq0Xx3z",
    "5333718081206631-TNMK-6Mdb1HRYR2",
    "5334673604434962-OGWF-al3Ws0FR8X",
    "5334686029208066-YKHA-J0BVKCAaSs",
    "5340270709988078-DTCY-S3J0SZStad",
    "5350923632984182-SOKV-33qfeZ37u8",
    "5352395276580121-AEBG-ZyJ5d2DYwW",
    "5359283513175774-DSRM-xeSW4TynNK",
    "5362913128977206-CHNX-7FzO4GYo68",
    "5374168065126809-NHPV-eaOJGRmTNq",
    "5377208000472050-EWYN-qZ8lmrS6FT",
    "5382034326245205-LNCD-tzwewbGMPH",
    "5385519443751173-IQZQ-k7e7UEYQ3L",
    "5385856852286619-DGBZ-nBNW81u9gq",
    "5386574586029836-YTUS-rjZgEVTmtN",
    "5399836776319243-FDBJ-udchZg6CZ7",
    "5403753062841807-QNVD-nzOvXVni5A",
    "5416236274155347-HBIP-ImiSCqt9S7",
    "5430036280644849-OOLZ-VW4KD3Mu1M",
    "5446337520669986-NFPR-E50Vi7hFrc",
    "5448266787599994-GVUW-ghCQMD8Chv",
    "5476499257851591-FTFE-VkquyW9ch8",
    "5479641587761096-ACTV-GVr6lCkOdh",
    "5481699642245108-FYTM-EeZoS2kKu9",
    "5491569672665927-JYWX-kwRCT8vupf",
    "5501931872635725-FJCW-6A9zgGP28s",
    "5530092612459511-KKFA-tNgXNGQLoB",
    "5550565670410543-HQYP-wETleQQi5e",
    "5553901548627668-NWBY-QCzcJuVasP",
    "5573190781343112-BPDV-zXzgpDuCgN",
    "5586089451544243-OKOS-2X745fLD7w",
    "5621654686399717-FIQF-IQN4EP30qw",
    "5627384043360734-FSZQ-7I2gPayi3H",
    "5682758702187381-ATCT-fkmBPoiNhn",
    "5696194508806009-PTGB-3kAtDoa1Hf",
    "5712973324759837-XOCE-fuc4T0Jscb",
    "5743702359977956-PEFO-L5wQFo52tP",
    "5758327843762068-XLRX-Z7WwOPGTTf",
    "5760412185450384-UFFE-pR9cNoNixA",
    "5772129621553190-QETE-sMKYAFwwBt",
    "5780359433604421-BHKU-F9O6kUguVz",
    "5791902362286558-WNIL-OWlLwbmojq",
    "5806270296246174-HIGQ-w4HgQ8xWq5",
    "5813452812155599-MFIL-KaXsWQhiOp",
    "5822068147181071-IWXQ-cN4JETteMl",
    "5843393699495905-ITLU-CWg6rMk10D",
    "5849820284018132-WCNE-ff8iAmlVoU",
    "5852591206273913-IRSD-nNjIv0yy30",
    "5880406585713595-LQUI-d7iYmtRFpZ",
    "5887088801478829-KZJN-PuaUNMh5IL",
    "5887334072167045-KLZG-e9YSnnMujD",
    "5909039576098622-BTTO-VgSSKzp1GE",
    "5937989531334689-UNCK-ruDvh75bj0",
    "5941455706035021-GTSD-D0qP1U8ovi",
    "5942976388114428-QQDL-p30N5lOmxM",
    "5949736967523310-PXZG-9YUcnCNpLp",
    "5964573224861002-GAGY-hsMRvqDsie",
    "5980164981781593-KSUF-vFLkvwboom",
    "5980418863258980-UWSP-r2ENrJvWcg",
    "5980767719181916-EEDG-ZBQWDMihud",
    "5989641314703742-ZHDT-yIZoCNwWbv",
    "6027245388649493-TQVU-LcjkGSBawL",
    "6031828327504319-LSYI-BohoHtvqHa",
    "6040860286187390-MBXH-ILMKN1B9HY",
    "6047596746314220-ETUF-IAPAKkVVN6",
    "6051284848772131-PXRJ-k7Vjny964t",
    "6051929312555320-XLEN-GA6aqpIZv8",
    "6053870356382548-KESY-wCf9jwmNxM",
    "6058432398495559-FKHZ-20oX8LIsQc",
    "6063565790416289-MLBZ-yeRcXpPput",
    "6085877815215262-MLAI-KFjh747Rlk",
    "6115348276247359-RGNH-QCjpo5yoP7",
    "6148448126479319-IMCU-rqtSSbfOnZ",
    "6150182840718069-RVLV-KVotb6IWlO",
    "6158093749377153-RYYQ-bOpjdSSW2N",
    "6162580817030533-FPSL-Rku0jlMQlA",
    "6201556253550510-HIHW-Y0ZqcOvsYH",
    "6202316630165687-WEFZ-Y96CbQMijp",
    "6217644367413709-CCIV-DVEJcCJRed",
    "6262111679774588-MGVF-YO9h2ctLjE",
    "6266105558660583-BCJC-1rGHOlvSKo",
    "6286429485014436-BNMC-hxt8HCPTkR",
    "6290269842387650-PGKZ-X6LHhbfJXE",
    "6325320421424537-WXFO-buATdjATur",
    "6339713750634575-REIR-C0qiVcjTfa",
    "6363164429960190-PSMY-hFMQsmTp6J",
    "6377972276494836-IPZM-uB8e20y4FH",
    "6388152624709504-WQMB-t9kqyCuy7Z",
    "6397912107337934-HYIC-fE6kkVJOWn",
    "6430509924420134-IALH-yu3DCiJRox",
    "6495493712022713-YBJE-E7iqmcGASJ",
    "6532345127993019-VMXU-kpP1iyezmz",
    "6536569504816329-IKLH-rr4Ay08DxT",
    "6541424059170002-STAO-ZtAgOSJZcq",
    "6542945869547551-FAJD-GCoMQLTSgm",
    "6596921674152984-RKVY-6zkEAhELli",
    "6633752388355610-VAGA-uy0QNHAsuE",
    "6635262758116784-LMNT-VM6fI8gF5r",
    "6678543067923258-YLCY-OUWcHGWmnJ",
    "6678958333674321-BVWK-6zlisOIZme",
    "6693186556844157-ZJCZ-3vjWm9Fn81",
    "6712951251051384-PTJZ-73tpd6pNbW",
    "6723191906248528-RGUX-V8zsCsCwni",
    "6731406539991384-HMMY-QV0cvYnCFp",
    "6733276707849310-PTAP-QHSJ6hmspA",
    "6733382711559872-SSGQ-YzUCQDAS9h",
    "6741369176776209-SFIM-QC76362dZs",
    "6742613080834988-DIIM-ljmrhHZjWL",
    "6743988494242780-THEC-J9Oohbxyxp",
    "6761505174170379-LAJX-rDbtz7CwDT",
    "6800785912920735-NVHI-7t1KJB6sRR",
    "6820135244924158-NCUX-rjU7XWVkKi",
    "6821888327757537-CNTO-KqJxfcFsTI",
    "6840299605638794-YNYN-OQoQpl4gNY",
    "6859555224130990-OPTP-gcj9X58YZf",
    "6865481045144229-MNSO-EIsWt1OcJx",
    "6880258086775996-KUTL-Wxbg1kjKsn",
    "6886543764414165-BDVV-n5PVFrhZy8",
    "6899957335187454-PVXK-2lJ74E2kqB",
    "6904055329455877-TOZX-C82n5WAkzP",
    "6904246780459821-UVRU-GfOlYgSLyy",
    "6905021609203438-AFBE-sgwBqqgrpb",
    "6907282864737191-YYLK-mCPIrlgNKL",
    "6908046690054126-OCBK-Pxw3DN9Gkv",
    "6914445675620394-PIJS-E0f938U3co",
    "6950390193688232-GJBV-da3rxbZyY8",
    "6968702072743878-QNVA-pfHdGqSF4D",
    "6998643433406517-GWMM-6ws0VAcID0",
    "7010641226648553-SHHD-Mpxvb2dA4F",
    "7041379799600597-YWOA-zDjZsMYjku",
    "7047471647483988-ZACW-UxOEQRqbJA",
    "7049919590064788-TLKX-RcivZxlDrV",
    "7054821242380110-ZXMO-GgIdcvplyz",
    "7063398437702170-XTHL-WUI9Cuh7Z3",
    "7076005958853214-SIHQ-O5Q3R2TCBJ",
    "7076633330933314-ZWZJ-ZOfVEA3nlD",
    "7080603747554263-KKJX-S4PfUdgkuM",
    "7104709689262113-IUQM-80SqaFzzcQ",
    "7105436976128011-KTVG-wZE4ePeeLn",
    "7109825255398728-NNVR-HmIhseZ2qV",
    "7113852643229924-IDMT-TGckA7VF3g",
    "7116589785906041-HRNL-ZyF0Zm0ink",
    "7132868074237566-OTJC-OTEHRj3rYe",
    "7161393247890119-OZIM-umPKZEZwf7",
    "7199294176093717-SYEJ-jfgcjSfoZA",
    "7223525093398195-JKUK-vTHJ3Mh8H0",
    "7240707708429205-HQHU-qX7gp8xvfr",
    "7246506761764224-HEDH-H2W3inmT5Y",
    "7251921576690668-VFHE-JQzscEsxZC",
    "7253000521799669-EMAE-MQztyi2ww7",
    "7259723523344437-MTLF-qWHjjVphbt",
    "7279348914864715-LBXA-3oFQbK0BR3",
    "7283223053620012-EQXI-MWYTeDzzyU",
    "7301228533870104-LQWU-bMYIj5YuJH",
    "7334094331463055-ACZT-9s5laJkNpB",
    "7354938740860229-RIQK-xdBresQlhj",
    "7386529824142942-AOPJ-uECh3q54UV",
    "7397337703891932-PLRI-hbPoLaPuqu",
    "7402527904541572-JVRW-MKFz2KDUqS",
    "7406739034024743-ZKGQ-1YliZ2s1zW",
    "7412267721881716-VGDQ-M60Q7r2n54",
    "7418223654826601-CTIQ-TJG3ZmICrb",
    "7438816760980859-WTND-EzM06UjXTq",
    "7482613980825907-KRNR-iMwf3Zh1Yd",
    "7483858288280050-TTPM-mT1q8x3APK",
    "7511575882666727-VWJD-mtaEqfEkfH",
    "7519081186965783-TZIF-wSXBdVlrDW",
    "7527940984693392-TMEN-zB3oC1btc4",
    "7532120759877023-PZPH-dGYdGiFGCN",
    "7533289318732007-ZJCV-gAiRUy3Awv",
    "7549610237164452-FDHW-I0Rx5vTiUN",
    "7563759877193490-PHBN-H6LK0x8SYS",
    "7588925511767319-XQQV-Sp2uJn74F0",
    "7598504236091480-UJWC-pEpPEErmAB",
    "7604788881280359-VDFY-siIi8SmItc",
    "7606137899980904-QNNE-l6TAHp6N1L",
    "7608628747435985-NNUZ-nVZ23t1Wwr",
    "7619396441144481-CLSU-flpVVjMXyT",
    "7643819002026050-ZBWJ-QAN7MeL0DJ",
    "7666021748678837-FBQN-NK0jBWT1e3",
    "7679272594552065-WCIP-kq7TliS0GE",
    "7691340830492473-GXPY-Cr8qX2OGqi",
    "7715347345496210-MBQU-kg4NyJPlOZ",
    "7718448123480457-MOTZ-qUZGNEzCxP",
    "7726859770473003-CUFL-m2EA82iPTY",
    "7727026912306123-KSOE-TDLQhn5H2r",
    "7746470899691972-CIMA-4BOzeQ8ByY",
    "7748962657990322-VHDL-FAbvGOgrBb",
    "7759732269883426-LLMS-8bp6r0mIis",
    "7773964390151215-VLXQ-SSbCeYSQjC",
    "7776470226790427-WJQR-cNlxEh166w",
    "7782076709181007-KJAD-9wq1SqtisJ",
    "7818058517092799-DUEQ-nC27kJyzdf",
    "7825272379718332-BMXK-SCIpLzDY4r",
    "7843211437015827-YXJX-O1YHdB56hz",
    "7848550152092340-XAIS-3lha9OJlf8",
    "7897541020137397-SKNT-sXUNlqrNh3",
    "7903166538190533-SGKZ-oEcOVAMjdA",
    "7916343732836893-VEHI-qrUk1HHog0",
    "7921244704760642-IIXL-AWmMlOtFkE",
    "7932011312379188-SIDW-CtpVIADynp",
    "7952679353890284-UWUC-njpM8o1ylt",
    "7964212533590318-FNOP-SylMpZWwZ2",
    "7987181288997858-HYHW-P2nUlShem3",
    "7998255158418892-SNWB-NR4wjnN8ee",
    "8004884896198111-MHAA-TpaemGoLVk",
    "8015993849354758-HZJW-ZEroeGSapK",
    "8017614237927686-UEZV-OGdj6EnKjT",
    "8024873680849777-URLG-JUjC5FUfOs",
    "8066974376358245-JDMC-heNv01TzCj",
    "8072890420782916-YRWR-4z5Jtu3gQK",
    "8074811341923409-CEUL-ClTXVTTPti",
    "8077185664592490-OWJC-rDEobQTeJH",
    "8084638911678969-GYGK-Pm4lMNEPZN",
    "8089182442744303-BFXI-2XSVDXj2wi",
    "8093706435342183-UZAR-YhYetdvFLV",
    "8115509310209974-JKCF-0wjwr55wTK",
    "8115725877435222-YEKW-tFqjIhBpIi",
    "8117240025440566-BEOZ-77ZrOeUcJx",
    "8145744202378062-PXQZ-o7mysnHWdh",
    "8156211687911925-VWCM-KlwcNnsBOk",
    "8161703837767631-OYJE-wP7BDT0nW7",
    "8175273339646752-AKKB-SPvrRAKo6q",
    "8190289596898077-XGIB-MCF380Qppj",
    "8192359719750737-XYZN-FJ3qn1CjNm",
    "8203100550138354-HOQU-I3SXpfFPC6",
    "8203569632610248-QXNA-tN815ETEMm",
    "8211735653789756-LGYT-kygApvbFVM",
    "8221403347861163-MUIC-lCK24Y3wUa",
    "8240623554472267-PHQJ-R5BcYngGz0",
    "8251755089936985-EOHB-qttW4qrj3r",
    "8255164103469005-AGZK-MBDwSKcCx5",
    "8294484343680466-KCCV-6oHsT0u4tB",
    "8304690299239991-DRTR-av7KS1IMKB",
    "8314220499479910-WKOL-jk9VO5w3IB",
    "8319427734835962-LOCW-AV82LLMkMH",
    "8327689282003014-AHCI-Qyz7bZeizx",
    "8327777187290761-PEBC-zfX2sIprDd",
    "8329421496778580-OVFV-zkGRzHyyID",
    "8334114845708079-RHJD-eUflmRBM3c",
    "8370910583250284-RMKE-3wKligFlaZ",
    "8385135790452962-GPCR-2OZxmdwRsc",
    "8411647235852423-RGAW-QN3rSsN4Oa",
    "8413720289681269-QPBZ-sotLBl3Mmm",
    "8426607648299363-UAXN-GuuVxryhml",
    "8428756067778748-OATY-A7DK1ssClO",
    "8435008016182290-RFNA-Eg3qNxLVCe",
    "8440122730572422-DQOR-OyAHt7lxGM",
    "8458695184426676-WFLC-GbyvxEkytr",
    "8472747657914947-GTFF-V5MhcQCu0h",
    "8473995535412943-KVBY-Wg3RB8u3gl",
    "8503353088304882-BRFG-RLWI0EAfSB",
    "8521191900698082-KQGQ-kCaRGnHlsa",
    "8532137212540704-BBBD-YkcHI1p95m",
    "8537794599097208-LXNM-fI7eRdLMZj",
    "8544189149359001-FUQH-faJwUqJjJW",
    "8546675647533553-OMYT-lNaoDo4qfG",
    "8560770071670126-SXXQ-ogc2qNFBdX",
    "8561898902870282-ZCQQ-Kp7bLp7K1I",
    "8565113642605758-MMCU-aVSbnhv66l",
    "8569200747566521-YHCE-aXp2dmmbUZ",
    "8590958079479365-DUGN-g9AQ9ORdh7",
    "8591683741242994-CDJX-NH4UAWbWml",
    "8622880805036913-PZOI-OzYqQLMZkZ",
    "8637810938432691-PYNK-bR2KmoDLUB",
    "8649374902779091-BARS-2HFhvK5wrG",
    "8652368050120945-NBOV-kRKveyzixc",
    "8662212493605294-KHEJ-kRS0r2JjeD",
    "8702235748392825-ZDIJ-CnWMDj7xVR",
    "8738196540280094-TIWV-JJVU1zub3b",
    "8751038053341138-SSSW-IuTepZrmoT",
    "8755624657327465-WQMY-6aCF3tisOf",
    "8755907915147336-MLFY-26HZ6TTxYr",
    "8758006194365733-BYDF-jzIfF3SSP1",
    "8759542835340066-VNBN-6rfsB4nahB",
    "8760126954112525-EFZZ-zvUEvQs2JL",
    "8772933587159619-PTQV-1m0o6macIz",
    "8788126441577384-WEDV-cBdWjL1S5s",
    "8807547601912335-JLHW-McbAZk8Po4",
    "8807762327858967-VWIF-xVLHkZlaCS",
    "8807895338782856-QWWF-raUNqyfsQm",
    "8831483372922538-KOLI-j5WaiaQsw5",
    "8846584310172354-EYBM-nGm8qjb2VU",
    "8887255738635883-CRFR-FxsJrfBZX6",
    "8888326133661115-QVQY-6qZPhU5B94",
    "8899439709898155-WSJX-VvD6kUDaMz",
    "8923071509122152-VHDM-9vCQevlqgj",
    "8927311113431332-XYUK-6OSsAaWRB6",
    "8934261172272085-VGUF-EZx39npcB0",
    "8939821842962727-WGAZ-9IBRm3M5Tk",
    "8951459007434449-OSPJ-l1Bt1WC1Ky",
    "8970137090032632-YIWK-QGgS3LQw2m",
    "8996467830559924-SIMC-DK3IcRlR8u",
    "9004388773448654-WOWE-idFbfa8c2Q",
    "9005604958711874-JGOP-fLPazrVEYp",
    "9006210998046078-YRCS-eaXFU2dDnP",
    "9013729820460933-DFVV-zfkFEvDlaz",
    "9018494479490801-RXNG-OoxjrU1ZWc",
    "9023651124580547-STBC-I38X8ctQwW",
    "9026946847080999-BRQH-kYsTWJBhEH",
    "9055895797090765-BWEZ-YXb4GenPsy",
    "9061084479989630-DPVM-3QVC3h1d1t",
    "9068814661746796-TBFF-BsisHssXlM",
    "9078609418662400-ULSA-DElNcZMMix",
    "9113230803816464-EMUC-wd555MeZG9",
    "9127652526489898-CRBF-MUhSkmfkkE",
    "9128679540901504-KXCN-m4ETIOOMzw",
    "9137701186805579-GASX-ldSG7Jtn6e",
    "9155923575401418-NWLN-nNpVNuhjUB",
    "9164581234140959-IIAZ-kWpTXBVpHx",
    "9168082200459669-YHTE-cWHYNeXEkS",
    "9168726644001811-ZFHX-nHAm4UUNJl",
    "9176740050323529-IPKZ-baBwV8wFRo",
    "9202402353718915-UZCL-u3YfS3lQm0",
    "9207843571854197-VFAR-MixtTIEPHT",
    "9210344173111944-YRMN-BZOYUVzmWJ",
    "9210718441522872-ZFYB-XL1NJwc1Ih",
    "9227091774007239-GTHY-aj4PFfLZQD",
    "9264322201890345-EDHA-3xQlBHZ6Iu",
    "9266456793439821-EFTH-sAyQuaKvx1",
    "9281086584993532-LXLU-Za72nOdQYo",
    "9286544410249326-HUIZ-qBCCl7pEwd",
    "9331485909086387-CEPC-mVJUQUGGdt",
    "9337065389591183-KAHG-bNlYrGxfk1",
    "9339978784517635-ZDYR-krBCKfSoqw",
    "9342127476718865-OZBF-yzx55Wn6vl",
    "9344745633607834-JSJF-HsiHr0aRwJ",
    "9354777454342727-ABML-V75vf3FM8Q",
    "9357938590078624-TTXE-py9IeMJoLZ",
    "9429661863365697-NSVM-rKrMRAXnNP",
    "9443273385375845-EEXH-Z8TJDT5k9R",
    "9454105885521341-USXU-z8pIhgky2j",
    "9457439224121298-QYWI-6TUXoDsgG7",
    "9476076404920234-CSRA-Gt0zYjQxF2",
    "9485487566466203-EBUL-y9hSbs1p7I",
    "9491198367423349-CAMH-yrXDfCvhNe",
    "9511122535051850-XCDE-JDysCzAfL2",
    "9512047544526528-AEUB-LEIwOYeaKN",
    "9522278107319962-AGLI-37AJNDBZXu",
    "9523776023543121-RMMV-9CVoAlYE0P",
    "9525242565414916-LAEQ-YHjmnvo7cS",
    "9543116289353023-GPFX-T3oXzWvzPh",
    "9545285078301934-LQFL-FILSjsMiR3",
    "9547369267588669-QOYT-ffs3hPPbZg",
    "9569080100549467-BGUI-k2tA49d2XP",
    "9570691484974722-VCDQ-60TnJZI8A9",
    "9574779348440193-DTMX-MWiBgs1SDI",
    "9601469864020847-LHHS-mZ5nni1m6F",
    "9624673481859448-QYXP-qgmokJSLdo",
    "9640638239072969-LAIX-VtODjugS9h",
    "9658976912012558-RJGM-OIznF9eCk0",
    "9661690312706065-UEXP-gArwMPcPQ0",
    "9669659008863488-BUMB-POw1q42Ph9",
    "9680352513764133-NBCE-KF1X5L8ez2",
    "9715977660590057-GMWR-gdTbMp4Pav",
    "9721159678827141-GQLP-sLIY81hnsW",
    "9733009683118742-UASS-W2pJCkKfCQ",
    "9742795766876535-WUQK-NbjJeKY4Fe",
    "9753829299164045-UBVJ-d8BxmYaxae",
    "9795722447543343-VIPJ-TIFUoJ9O4Y",
    "9808388212065860-RHVC-3d2e4Td6rU",
    "9816911455090178-ODVM-4edpVR8wXs",
    "9827922562951339-BDTN-raxy2guWCn",
    "9832274735491446-EXSP-5V7EUGt0qP",
    "9895504745338682-EDPU-pootvr7wVF",
    "9904036158925580-NNSU-aYusJrCKqm",
    "9914136662123949-OKHF-L0S5lZHtuM",
    "9931517755132256-YIUC-SJxoA9IPMy",
    "9949254216480364-IORE-OpTLSbSOCM",
    "9962381973246142-VVMT-E4f12Mdz69",
    "9972682051915781-FVZK-ULIRKS6gO6",
    "9974513402642514-PZDD-Nj2uMvXScu",
    "9981262822613142-VCWP-ZxCJItjWsE",
    "9986161144208804-CGCD-SkXY2pYKiA",
    "9987045394988011-YDHJ-EqWJuFPE37",
    "9995517161817000-QTJV-4Gp7FbmVBH",
]

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
                if True:
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
        log_user_info(user)
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
            log_user_info(user)
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
            if message.date > cutoff_date:
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