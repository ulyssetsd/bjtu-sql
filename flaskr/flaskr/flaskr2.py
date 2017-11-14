from flask import Flask, render_template, redirect, session, url_for
from helpers import conn, cursor


app = Flask(__name__)  # create the application instance :)


from views import users, message, comment, like_msg, like_cmt, relation, search
app.register_blueprint(users.mod)
app.register_blueprint(message.mod)
app.register_blueprint(comment.mod)
app.register_blueprint(like_msg.mod)
app.register_blueprint(like_cmt.mod)
app.register_blueprint(relation.mod)
app.register_blueprint(search.mod)


#@app.teardown_appcontext
#def shutdown_session(exception=None):
    #cursor.close()
    #conn.close()


@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    user_id = session['logged_id']
    cursor.execute("SELECT following_id FROM relation where follower_id = %s", (user_id,))
    ms = cursor.fetchall()
    list_user_id = [d['following_id'] for d in ms if 'following_id' in d]
    list_user_id.append(user_id)
    cursor.execute("SELECT * FROM message where user_id IN %s ORDER BY c_time DESC", (tuple(list_user_id),))
    ms = cursor.fetchall()
    entries = []
    for m in ms:
        m = dict(m.items())
        cursor.execute("SELECT nickname FROM users where user_id = %s", (m['user_id'],))
        u = cursor.fetchone()
        m['nickname'] = u['nickname']
        cursor.execute("SELECT * FROM like_msg where msg_id = %s AND user_id = %s", (m['msg_id'], user_id))
        like = cursor.fetchone()
        if like is not None:
            like_flag = True
        else:
            like_flag = False
        m['like_flag'] = like_flag
        entries.append(m)

    return render_template('show_entries.html', entries=entries, user_id=user_id)


@app.route('/add', methods=['POST'])
def add_entry():
    return render_template('show_entries.html')


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'bjtu-sql'
    app.run()
