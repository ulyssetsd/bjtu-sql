from flask import Flask, render_template, redirect, session, url_for
from helpers import conn, cursor
from requete import relationByFollowerId, messageGetAllFromManyUserIdOrder, likeMsgGetOne, userByUserId, likeMsgCountLike, CommentCountCmt


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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html')

@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    ms = relationByFollowerId(session['logged_id'])
    list_user_id = [d['following_id'] for d in ms if 'following_id' in d]
    list_user_id.append(session['logged_id'])
    ms = messageGetAllFromManyUserIdOrder(tuple(list_user_id))
    entries = []
    for m in ms:
        m = dict(m.items())
        m['nickname'] = userByUserId(m['user_id'])['nickname']
        m['like_flag'] = likeMsgGetOne(m['msg_id'], session['logged_id']) is not None
        m['is_mine'] = m['user_id'] == session['logged_id']
        m['like_num'] = likeMsgCountLike(m['msg_id'])
        m['cmt_num'] = CommentCountCmt(m['msg_id'])
        entries.append(m)
    ms=entries

    return render_template('show_entries.html', ms=ms)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'bjtu-sql'
    app.run()
