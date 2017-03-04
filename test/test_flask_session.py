#! /usr/bin/env python
# coding:utf-8


from flask import Flask, session, redirect, url_for, escape, request, make_response
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    # print 'index',request.cookies.get('userid')
    # print 'index',session.get('username')
    # print 'index',session.get('userid')
    if session.get('userid') == request.cookies.get('userid') and request.cookies.get('userid') != None:
        return 'Logged in as %s' % session.get('username')
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    print '/login',request.cookies.get('userid')
    print '/login',session.get('userid')
    if request.method == 'POST':
        # print 'POST',request.cookies.get('userid')
        # print 'POST',session.get('username')
        resp = make_response(redirect(url_for('index')))
        session['username'] = request.form['username']
        session['userid'] = str(uuid.uuid1())
        resp.set_cookie('userid', session['userid'])
        return resp
        # return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # print '/logout',request.cookies.get('userid')
    # print '/logout',session.get('username')
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('userid', None)
    return redirect(url_for('login'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
    app.run(debug=True)

