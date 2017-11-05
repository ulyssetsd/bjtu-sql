from flask import Flask, render_template, redirect, session, url_for
from database import conn, cursor


app = Flask(__name__)  # create the application instance :)


from views import users, message, comment, like_msg, like_cmt
app.register_blueprint(users.mod)
app.register_blueprint(message.mod)
app.register_blueprint(comment.mod)
app.register_blueprint(like_msg.mod)
app.register_blueprint(like_cmt.mod)


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
    messages = list(m)
    for i, message in enumerate(messages):
        message = list(message)
        user_id = message[1]
        sql = 'SELECT nickname FROM users where user_id = %d' % user_id
        cursor.execute(sql)
        u = cursor.fetchone()
        message.append(u[0])
        sql = "SELECT * FROM like_msg where msg_id = %d AND user_id = %d" \
            % (message[0], user_id)
        cursor.execute(sql)
        like = cursor.fetchone()
        if like is not None:
            like_flag = 1
        else:
            like_flag = 0
        message.append(like_flag)
        messages[i] = message

    return render_template('show_entries.html', entries=messages)


@app.route('/add', methods=['POST'])
def add_entry():
    return render_template('show_entries.html')


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'bjtu-sql'
    app.run()
