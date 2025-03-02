import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from colorama import Fore

app = Flask('chat_chat_chat_ctf')
app.config['SECRET_KEY'] = 'random_secret_key_2929271738391'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    send_time = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(150), nullable=False)

    def __str__(self):
            return f'Message from {self.sender_id} to {self.receiver_id} at {self.send_time}: {self.content}'

    

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
        return redirect(url_for(f'logout'))

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
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        send_message(sender_id=1, receiver_id=new_user.id, content='Hello! I\'m the admin!')
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
            content=request.args.get('content')
            send_message(user_id, receiver_user_id, content)
        except Exception as e:
            print(f'Error: {e}')

    return redirect(f'/chat/{receiver_user_id}')

@app.route('/chat/<int:receiver_user_id>')
@login_required
def user_chat(receiver_user_id):
    user_id = current_user.id
    messages_recived = Message.query.filter_by(receiver_id=user_id).filter_by(sender_id=receiver_user_id).all()
    messages_sended = Message.query.filter_by(sender_id=user_id).filter_by(receiver_id=receiver_user_id).all()

    print(get_contacts_users(user_id))
    conversation = messages_sended+messages_recived
    conversation.sort(key=lambda message: message.send_time)
    
    reciver_user = User.query.filter_by(id=receiver_user_id).first()
    try:
        if reciver_user is None:
            return redirect(f'/chat/{get_contacts_users(user_id)[0]}')
    except Exception as e:
        print(f'Error: {e}')
        return redirect(url_for('logout'))

    html_messages_content = ''
    for message in conversation:
        if message.sender_id == user_id:
            print(f'{Fore.BLUE}{message.content}')
            html_messages_content += f'<div class="message sent">'
            html_messages_content +=f'<div class="sender">{current_user.username}</div>'
            html_messages_content +=f'<div class="content">{message.content}</div>'
            html_messages_content += f'</div>'
        else:
            print(f'{Fore.GREEN}{message.content}')
            html_messages_content += f'<div class="message received">'
            html_messages_content +=f'<div class="sender">{reciver_user.username}</div>'
            html_messages_content +=f'<div class="content">{message.content}</div>'
            html_messages_content += f'</div>'

    html_contacts_content = ''
    for contact_user_id in get_contacts_users(user_id):
        contact_user = User.query.filter_by(id=contact_user_id).first()
        if contact_user is None:
            continue
        html_contacts_content += f'<a href="/chat/{contact_user_id}"><div class="user">{contact_user.username}</div></a>'

    return render_template("chat.html", active_user=current_user.username, receiver_user_id=receiver_user_id, messages_content=html_messages_content, html_contacts_content=html_contacts_content)

def send_message(sender_id, receiver_id, content):
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content, send_time=datetime.datetime.now())
    db.session.add(new_message)
    db.session.commit()
def create_user(username, password, is_admin=False):
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
def get_contacts_users(user_id):
    contacts = []
    messages = Message.query.filter_by(receiver_id=user_id).all() + Message.query.filter_by(sender_id=user_id).all()
    messages.sort(key=lambda message: message.send_time)
    messages.reverse()
    for message in messages:
        if message.sender_id not in contacts and message.sender_id != user_id:
            contacts.append(message.sender_id)
        if message.receiver_id not in contacts and message.receiver_id != user_id:
            contacts.append(message.receiver_id)
        if message.sender_id == user_id and message.receiver_id == user_id and user_id not in contacts:
            contacts.append(user_id)
    return contacts


if __name__ == '__main__':
    if os.path.exists('instance/users.db'):
        print('Removing old database...')
        os.remove('instance/users.db')
    with app.app_context():
        db.create_all()
    
        print('Creating admin user...')
        create_user(username='admin', password='admin', is_admin=True)
        create_user(username='Bob', password='password123')
        create_user(username='Zimbabwe King', password='password123')
        send_message(sender_id=2, receiver_id=1, content='Hello Admin! I\'m Bob!')
        send_message(sender_id=1, receiver_id=2, content='??')
        send_message(sender_id=2, receiver_id=1, content='Nothing')
        send_message(sender_id=1, receiver_id=1, content='Testing')
        send_message(sender_id=3, receiver_id=1, content='Hello I\'m Zimbabwe King!')
        send_message(sender_id=1, receiver_id=2, content='Baka')

    app.run(debug=False)