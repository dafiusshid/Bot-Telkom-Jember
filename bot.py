from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, filters, MessageHandler
import mysql.connector
from mysql.connector import Error

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'odc_keys_witel_jember'
}

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        print("Database connection successful")
    except Error as e:
        print(f"Error: {e}")
    return connection

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Database connection closed")

def get_user_by_id(user_id):
    connection = create_connection()
    if connection is None:
        print("Failed to create database connection.")
        return None
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        return user
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection)

def is_keys_odc_available(odc_name):
    connection = create_connection()
    if connection is None:
        print("Failed to create database connection.")
        return None
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM odc_info WHERE odc_name = %s", (odc_name,))
        odc_info = cursor.fetchone()
        return odc_info
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection)

def register_user(user_id, username):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, username, is_registered) VALUES (%s, %s, %s)",
                       (user_id, username, False))
        connection.commit()
        print(f"User {username} registered successfully")
    except Error as e:
        print(f"Error: {e}")
    finally:
        close_connection(connection)

def update_registration_status(user_id, status):
    print(f"status : {status}\nUser id : {user_id}")
    connection = create_connection()
    if connection is None:
        print("Failed to create database connection.")
        return
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET is_registered = %s WHERE user_id = %s", (status, user_id))
        connection.commit()
        print(f"User {user_id} registration status updated to {status}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        close_connection(connection) 
    
    # Implementasikan logika untuk memeriksa layout ODC
def check_odc_layout(odc_name):
    connection = create_connection()
    if connection is None :
        print*("failed to create database connection.")
        return None
    cursor = connection.cursor(dictionary=True)
    try :
        cursor.execute("SELECT * FROM odc_info WHERE odc_name = %s", (odc_name,))
        layout = cursor.fetchone()
        return layout
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection)

    #implementasi logika untuk memvalidasi kode ODC
def validate_odc_code(odc_code):
    connection = create_connection()
    if connection is None :
        print("Failed to create database connection.")
        return False
    cursor = connection.cursor(dictionary=True)
    try :
        cursor.execute("SELECT * FROM odc_info WHERE odc_code = %s", (odc_code,))
        odc_info = cursor.fetchone()
        return odc_info is not None
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        close_connection(connection)

async def upload_photo_before_job(update: Update, context: CallbackContext):
    await update.message.reply_text("Unggah foto sebelum pekerjaan:")

async def upload_photo_after_job(update: Update, context: CallbackContext):
    await update.message.reply_text("Unggah foto setelah pekerjaan:")

async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    data = get_user_by_id(user_id)
    print(f"id {user_id} melakukan start")
    print(data)

    if data is not None and data['is_registered']:
        keyboard = [
            [InlineKeyboardButton("Ketersedian Kunci", callback_data='show_keys')],
            [InlineKeyboardButton("Peminjaman Kunci", callback_data='keys_borrowed')],
        ]
    elif data is not None and not data['is_registered']:
        keyboard = [
            [InlineKeyboardButton("Notify Team Lead", callback_data='notify')],
        ]
    else:
        register_user(user_id, username)
        keyboard = [
            [InlineKeyboardButton("Register", callback_data='register')],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Selamat datang di layanan manajemen kunci! Silakan pilih menu di bawah ini untuk melanjutkan:", 
        reply_markup=reply_markup
    )

async def register_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    keyboard = [
        [InlineKeyboardButton("Approve", callback_data=f"regist_approve_{user_id}")],
        [InlineKeyboardButton("Reject", callback_data=f"regist_reject_{user_id}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id='6305589030', text=f"New user has requested registration:\nUser: @{query.from_user.username}\nPlease approve or reject this request.", reply_markup=reply_markup)

async def handle_registration(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    action, user_id = query.data.split("_")[1:]

    if action == "approve":
        update_registration_status(user_id, True)
        await context.bot.send_message(chat_id=user_id, text=f"Anda telah berhasil menjadi user")
    else:
        await context.bot.send_message(chat_id=user_id, text=f"Permintaan anda ditolak")

async def notify_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    keyboard = [
        [InlineKeyboardButton("Approve", callback_data=f"alert_notify_approve_{user_id}")],
        [InlineKeyboardButton("Reject", callback_data=f"alert_notify_reject_{user_id}")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id='6305589030', text=f"New user needs approval for access:\nUser: @{query.from_user.username}\nPlease approve or reject this request.", reply_markup=reply_markup)

async def handle_notify(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    action, user_id = query.data.split("_")[2:]
    
    if action == "approve":
        update_registration_status(user_id, True)
        await context.bot.send_message(chat_id=user_id, text=f"Anda telah berhasil menjadi user")
    else:
        await context.bot.send_message(chat_id=user_id, text=f"Permintaan anda ditolak")

async def request_key_name(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text("Masukkan nama kunci yang ingin Anda pinjam:")

async def forward_key_request(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    key_name = update.message.text

    keyboard = [
        [InlineKeyboardButton("Approve", callback_data=f"borrow_approve_{user_id}_{key_name}")],
        [InlineKeyboardButton("Reject", callback_data=f"borrow_reject_{user_id}_{key_name}")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id='6305589030', text=f"Request peminjaman kunci:\nUser: @{username}\nKunci: {key_name}\nPlease approve or reject this request.", reply_markup=reply_markup)



async def handle_borrow_approval(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    action, user_id, key_name = query.data.split("_")[1:]

    if action == "approve":
        await context.bot.send_message(chat_id=user_id, text=f"Permintaan peminjaman kunci '{key_name}' Anda telah disetujui.")
    else:
        await context.bot.send_message(chat_id=user_id, text=f"Permintaan peminjaman kunci '{key_name}' Anda telah ditolak.")

async def return_keys_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    keyboard = [
        [InlineKeyboardButton("Pengembalian Kunci", callback_data="keys_returning")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Silakan pilih opsi di bawah ini untuk mengembalikan kunci:", reply_markup=reply_markup)

async def handle_return_keys(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    print(query)

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.message.edit_reply_markup(reply_markup=None)
    print(f"sesi approval: {query.data}")

    if query.data == 'register':
        await register_callback(update, context)
    elif query.data.startswith('regist'):
        await handle_registration(update, context)
    elif query.data == 'notify':
        await notify_callback(update, context)
    elif query.data.startswith('alert'):
        await handle_notify(update, context)
    elif query.data == 'keys_borrowed':
        await request_key_name(update, context)
    elif query.data.startswith('borrow'):
        await handle_borrow_approval(update, context)
    elif query.data == 'keys_returning':
        await handle_return_keys(update, context)

def main():
    application = Application.builder().token("7335623016:AAHMeVUUNjMLCAtr8uTnNGA0HTJF3dEsnvs").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_key_request))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
