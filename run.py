from threading import Thread
from ichat import app, db
from ichat.botMeanger import BotMenager
from ichat.utils import create_user, send_message
import os
import random
if __name__ == '__main__':
    if os.path.exists('instance/users.db'):
        print('Removing old database...')
        os.remove('instance/users.db')
    with app.app_context():
        db.create_all()

        create_user(username='admin', password='admin', is_admin=True)

        botMenager = BotMenager('BotsCharacters.txt')
        botMenager.createUsersForBots()
        botMaintananceLoop = Thread(target=botMenager.startBotMaintananceLoop)
        botMaintananceLoop.start()



    app.run(debug=False)