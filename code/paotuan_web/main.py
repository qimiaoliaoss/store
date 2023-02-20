# -*- coding: utf-8 -*-
# @Time : 2023/2/15 16:44
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html', name='world')


if __name__ == "__main__":
    app.run(debug=True, port=8080)