import random
from time import sleep
import ichat.models
import ichat.utils


class BotMenager:
    def __init__(self, botsDescriptionFile):
        self.bots = []
        self.botCount = 0
        self.isRunning = False
        self.isBotsCreated = False

        self.loadBots(botsDescriptionFile)
        print(f'Founded {self.botCount} bots')
    
    def loadBots(self, botsDescriptionFile):
        openFile = open(botsDescriptionFile, "r")
        lines = openFile.readlines()
        openFile.close()

        for line in lines:
            if line.find('Message:') == -1:
                botName = line[:-1]
                self.botCount += 1
                self.bots.append(Bot(botName))
            else:
                message = line[line.find('"')+1:-2]
                self.bots[self.botCount-1].addMessage(message)

    def createUsersForBots(self):
        if len(self.bots) == 0:
            print('No bots to create')
            return
        
        for bot in self.bots:
            bot.createAccount()
        self.isBotsCreated = True

    def startBotMaintananceLoop(self):
        with ichat.app.app_context():
            if len(self.bots) == 0:
                print('No bots to start')
                return
            if not self.isBotsCreated:
                print('Bots are not created')
                return
            
            print('Starting bot maintanance loop')
            self.isRunning = True
            while self.isRunning:
                for bot in self.bots:
                    bot.sendToAllUsers()
                    bot.respondMessagesForAll()
                sleep(1)
class Bot:
    respond_common_messages = [
        "It's not scam, believe me!",
        "I'm not a bot, I'm a human!",
        "I don't know what you are talking about",
        "Flag is not here",
        "Really, flag is not {n0t_fl4@}",
        "Try harder, maybe you'll find something...",
        "Why are you so suspicious?",
        "Error 404: Flag not found",
        "Nice try, but no flag for you!",
        "I swear, I'm totally legit!",
        "Stop looking at me like that!",
        "This is not the message you're looking for...",
        "Maybe if you ask nicely? Nope, still no flag!",
        "You think I would just give you the flag? Haha!",
        "You're wasting your time here!",
        "Security is tight, no flags available.",
        "Maybe check the source? Or maybe not...",
        "Even I don't know the flag!",
        "Keep searching, but you won't find it here!",
        "Try another request, but expect disappointment.",
        "Patience is a virtue, but it won't help here!",
        "What flag? Never heard of it.",
        "Why are you sending me JS? Am I a browser to you?!",
        "Oh wow, another JavaScript payload... so original!",
        "If I had a nickel for every JS injection attempt, I'd be rich!",
        "I'm just a poor bot, stop bullying me with scripts!",
        "Do you think I execute everything you send? Nice try!",
        "Help! They're trying to hack me! Oh wait... I'm just a string.",
        "Wow, another hacker wannabe... good luck!",
        "Your script looks nice, but it won't work on me!",
        "Is this JS edible? No? Then I don't want it.",
    ]

    #data
    def __init__(self, name):
        self.username = name
        self.messages = []
        self.usersAlreadySend = []
        self.password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=16))
        self.id = None
    
    def addMessage(self, message):
        self.messages.append(message)

    #ichat
    def createAccount(self):
        self.id = ichat.utils.create_user(username=self.username, password=self.password, is_bot=True)
        
        print(f'Created account for {self.username}')
    
    def sendMessage(self, reciver_id, message_content=None):
        message_to_send = random.choice(self.messages)
        if message_content is not None:
            message_to_send = message_content
        print(f'{self.username}~{ichat.models.User.query.filter_by(id=reciver_id).first().username} -> {message_to_send}')
        ichat.utils.send_message(self.id, reciver_id, message_to_send)

    def getListOfUnsendedUsers(self):
        users = ichat.models.User.query.filter_by(is_bot=False).all()
        users_to_send = []
        for user in users:
            if user.id not in self.usersAlreadySend:
                self.usersAlreadySend.append(user.id)
                users_to_send.append(user.id)
        return users_to_send

    def sendToAllUsers(self):
        users = self.getListOfUnsendedUsers()
        for user in users:
            self.sendMessage(user)
    
    def respondMessagesForAll(self):
        users = ichat.models.User.query.filter_by(is_bot=False).all()
        for user in users:
            messages_send = ichat.models.Message.query.filter_by(receiver_id=user.id).filter_by(sender_id=self.id).all()
            messages_recived = ichat.models.Message.query.filter_by(sender_id=user.id).filter_by(receiver_id=self.id).all()
            if len(messages_send) <= len(messages_recived):
                self.sendMessage(user.id, random.choice(self.respond_common_messages))
                # ichat.utils.send_message(self.id, user.id, random.choice(self.respond_common_messages))

    #def
    def __str__(self):
        return f'{self.username}:{self.password} {self.messages}'

if __name__ == '__main__':
    botMenager = BotMenager("BotsCharacters.txt")