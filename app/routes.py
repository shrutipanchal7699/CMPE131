from app import app

@app.route('/')
def homePage():
    return 'Hello world'

@app.route('/auth')
def authPage():
    return 'Login and Registration Page'

@app.route('/rooms')
def roomListPage():
    return 'page to filter and search for rooms'

@app.route('/rooms/<id>')
def roomDetailPage(id):
    return 'room detail page'

@app.route('/rooms/<id>/book')
def reserveRoomPage(id):
    return 'Reserve room page'

