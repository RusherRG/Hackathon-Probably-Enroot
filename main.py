from flask import Flask
from flask import render_template, flash, redirect, url_for, request, session
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    return render_template('index.html', page='IndexPage')


@app.route('/opt', methods=['GET', 'POST'])
def opt():
    return render_template('optimize.html', page='IndexPage')


@app.route('/make', methods=['GET', 'POST'])
def make():
    return render_template('make.html', page='IndexPage')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
