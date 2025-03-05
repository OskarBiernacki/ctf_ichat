from ichat import app, db
from ichat.botMeanger import BotMenager
from ichat.utils import create_user, send_message
import os

if __name__ == '__main__':
    if os.path.exists('instance/users.db'):
        print('Removing old database...')
        os.remove('instance/users.db')
    with app.app_context():
        db.create_all()

        botMenager = BotMenager('BotsCharacters.txt')
        botMenager.createUsersForBots()
        
    #     print('Creating admin user...')
    #     create_user(username='admin', password='admin', is_admin=True)
    #     create_user(username='Bob', password='password123')
    #     create_user(username='Zimbabwe King', password='password123')
    #     send_message(sender_id=2, receiver_id=1, content='Hello Admin! I\'m Bob!')
    #     send_message(sender_id=1, receiver_id=2, content='??')
    #     send_message(sender_id=2, receiver_id=1, content='Nothing')
    #     send_message(sender_id=1, receiver_id=1, content='Testing')
    #     send_message(sender_id=3, receiver_id=1, content='Hello I\'m Zimbabwe King!')
    #     send_message(sender_id=1, receiver_id=2, content='Baka')

    # app.run(debug=False)