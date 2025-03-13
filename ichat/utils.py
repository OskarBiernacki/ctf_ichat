from datetime import datetime
from ichat import db
from ichat.models import User, Message

def send_message(sender_id, receiver_id, content, sender_is_bot=False) -> None:
    #blocking messages betwen normal users
    sender_user = User.query.filter_by(id=sender_id).first()
    reciver_user = User.query.filter_by(id=receiver_id).first()

    if sender_user.is_admin and not sender_is_bot:
        print('not allowing users to write as admin to avoid PvP')
        return
    if not (sender_user.is_admin and sender_is_bot): #Admin Bot skip filters
        if sender_id == receiver_id:
            print('self sending not allowed')
            return
        if sender_user is None or reciver_user is None:
            print('unexisting users comunication')
            return
        if not sender_user.is_bot and not reciver_user.is_bot:
            print('Unallowed comunication blocked')
            return

    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content, send_time=datetime.now())
    db.session.add(new_message)
    db.session.commit()

def create_user(username, password, is_admin=False, is_bot=False):
    new_user = User(username=username, password=password, is_admin=is_admin, is_bot=is_bot)
    db.session.add(new_user)
    db.session.commit()
    return new_user.id

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