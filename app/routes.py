from app import app

@app.route('/')
def homePage():
    return 'Hello world'

@app.route('/auth'):
def authPage():
    return 'Login and Registration Page'

@app.route('/rooms'):
def roomListPage():
    return 'page to filter and search for rooms'