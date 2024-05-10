from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
import openpyxl
from selenium import webdriver

import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, filename))

            # Xử lý file ở đây (crawl comments và tạo file comments.xlsx)
            process = subprocess.Popen(["python", "crawl.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            return send_file('./comments.xlsx', as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
