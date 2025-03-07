from flask import render_template, redirect, url_for, request, flash, abort, session
from flask_login import login_user, login_required, logout_user, current_user
from ichat import app, db, login_manager
from ichat.models import User, Message
from ichat.utils import send_message, get_contacts_users
import jwt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    try:
        return redirect(f'/chat/{get_contacts_users(current_user.id)[0]}')
    except Exception as e:
        print(f'Error: {e}')
        return redirect(url_for('logout'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', bad_login=True)
    return render_template('login.html', bad_login=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first() is not None:
            return render_template('register.html', bad_register='Username already exists!')

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        id_admin=User.query.filter_by(username='admin').first().id
        if id_admin != new_user.id:
            send_message(sender_id=id_admin, receiver_id=new_user.id, content='Hello! I\'m the admin!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat/<int:receiver_user_id>/send', methods=['GET'])
@login_required
def user_chat_send_message(receiver_user_id):
    if request.method == 'GET':
        try:
            user_id = current_user.id
            content = request.args.get('content')
            send_message(user_id, receiver_user_id, content)
        except Exception as e:
            print(f'Error: {e}')

    return redirect(f'/chat/{receiver_user_id}')

@app.route('/chat/<int:receiver_user_id>')
@login_required
def user_chat(receiver_user_id):
    user_id = current_user.id
    messages_received = Message.query.filter_by(receiver_id=user_id).filter_by(sender_id=receiver_user_id).all()
    messages_sent = Message.query.filter_by(sender_id=user_id).filter_by(receiver_id=receiver_user_id).all()

    conversation = messages_received + messages_sent
    conversation.sort(key=lambda message: message.send_time)

    receiver_user = User.query.get(receiver_user_id)
    if receiver_user is None:
        abort(404)

    html_messages_content = ''
    for message in conversation:
        if message.sender_id == user_id:
            html_messages_content += f'<div class="message sent">'
            html_messages_content += f'<div class="sender">{current_user.username}</div>'
            html_messages_content += f'<div class="content">{message.content}</div>'
            html_messages_content += f'</div>'
        else:
            html_messages_content += f'<div class="message received">'
            html_messages_content += f'<div class="sender">{receiver_user.username}</div>'
            html_messages_content += f'<div class="content">{message.content}</div>'
            html_messages_content += f'</div>'

    html_contacts_content = ''
    for contact_user_id in get_contacts_users(user_id):
        contact_user = User.query.get(contact_user_id)
        if contact_user is None:
            continue
        html_contacts_content += f'<a href="/chat/{contact_user_id}"><div class="user">{contact_user.username}</div></a>'

    admin_button = ''
    if current_user.is_admin:
        admin_button = f'<a href="{ url_for('admin_panel') }" class="logout-button" style="margin-right: 100px">admin-panel</a>'

    return render_template("chat.html", active_user=current_user.username, receiver_user_id=receiver_user_id, messages_content=html_messages_content, html_contacts_content=html_contacts_content, admin_button=admin_button)

@app.route('/admin-panel', methods=['GET'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        abort(404)

    token = request.cookies.get('priv_token')
    SECRET_JWT_KEY='butterfly3'
    print(f'JWT token: {token}')
    if not token:
        token = jwt.encode({
            'admin_panel_priv': True,
            'secret_view_priv': False
        }, SECRET_JWT_KEY, algorithm='HS256')
        session['jwt_token'] = token
        response = app.make_response(redirect(url_for('admin_panel')))
        response.set_cookie('priv_token', token)
        return response

    if request.args.get('revil_sicret') == 'True':
        try:
            decoded_token = jwt.decode(token, SECRET_JWT_KEY, algorithms=['HS256'])
            admin_panel_priv = decoded_token.get('admin_panel_priv')
            secret_view_priv = decoded_token.get('secret_view_priv')
            print( f'panel_priv: {admin_panel_priv}, secret_priv: {secret_view_priv}')
            if not secret_view_priv:
                return render_template('admin_panel.html', secret_message='no privilage for secret view')
            else:
                return render_template('admin_panel.html', secret_message='pjatk{1chat_w45_h4ck3d}')
        except Exception as e:
            print('Error: invalid token')
            return render_template('admin_panel.html', secret_message ='Invalid token, try harder!')
    return render_template('admin_panel.html')