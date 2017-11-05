from flask import Flask, render_template, redirect, session, url_for
from database import conn, cursor


app = Flask(__name__)  # create the application instance :)


from views import users, message, comment, like_msg
app.register_blueprint(users.mod)
app.register_blueprint(message.mod)
app.register_blueprint(comment.mod)
app.register_blueprint(like_msg.mod)


#@app.teardown_appcontext
#def shutdown_session(exception=None):
    #cursor.close()
    #conn.close()


@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    user_id = session['logged_id']
    sql = 'SELECT * FROM message where user_id = %d ORDER BY c_time DESC' \
        % (user_id)
    cursor.execute(sql)
    m = cursor.fetchall()
    #messages = list(m)
    #for i,message in messages:
        #user_id = message[1]
        #sql = 'SELECT nickname FROM users where user_id = %d' % user_id
        #cursor.execute(sql)
        #u = cursor.fetchone()
        #message[4] = 'u[0]'
    return render_template('show_entries.html', entries=m)


@app.route('/add', methods=['POST'])
def add_entry():
    return render_template('show_entries.html')


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'bjtu-sql'
    app.run()
