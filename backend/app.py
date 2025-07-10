import os
from flask import Flask, request
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("7715422536:AAGcVy9-ojM_2BSqDlScbr7URI9YJF9WBkM")

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

@app.route('/send-pdf', methods=['POST'])
def send_pdf():
    data = request.json or {}
    chat_id = data.get('chat_id')
    file_name = data.get('file_name', "")

    if not chat_id or not file_name:
        return 'Missing chat_id or file_name', 400

    safe_name = os.path.basename(file_name)
    path = os.path.join('pdfs', safe_name)
    if not os.path.isfile(path):
        return 'File not found', 404

    with open(path, 'rb') as f:
        bot.send_document(chat_id=chat_id, document=f, filename=safe_name)

    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8000)))
