import sqlite3
import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, make_response, \
    send_file
from werkzeug.utils import secure_filename

UPLOADER_FOLDER = '/Users/eberechukwukathomas/Desktop/back_up/static'
app = Flask(__name__)
app.config['UPLOADER_FOLDER'] = UPLOADER_FOLDER
conn = sqlite3.connect('user.db', check_same_thread=False)
name = 'Ajala'
cursor = conn.cursor()


@app.route('/game')
def account():
    cursor.execute("SELECT image_tag from Users where email=?", ('g@gmail.com',))
    file = cursor.fetchone()
    for i in file:
        new_life = send_from_directory(app.config['UPLOADER_FOLDER'], i)


if __name__ == '__main__':
    app.run(port=2900, debug=True)
