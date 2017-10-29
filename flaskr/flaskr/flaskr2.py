from flask import Flask, render_template, redirect, session, url_for
from database import init_db, db_session


app = Flask(__name__)  # create the application instance :)


from views import users
app.register_blueprint(users.mod)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    return render_template('show_entries.html')


@app.route('/add', methods=['POST'])
def add_entry():
    return render_template('show_entries.html')


if __name__ == '__main__':
    init_db()
    app.debug = True
    app.secret_key = 'bjtu-sql'
    app.run()
