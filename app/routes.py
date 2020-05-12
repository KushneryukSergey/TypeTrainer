from app import app
from module import main


check = True


@app.route('/')
@app.route('/index')
def index():
    return "You are hero"
