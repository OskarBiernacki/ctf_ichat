import random
import ichat.models
import ichat.utils

class BotMenager:
    def __init__(self, botsDescriptionFile):
        self.bots = []
        self.botCount = 0
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
        for bot in self.bots:
            bot.createAccount()


class Bot:
    #data
    def __init__(self, name):
        self.username = name
        self.messages = []
        self.password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=16))
        self.id = None
    def addMessage(self, message):
        self.messages.append(message)

    #ichat
    def createAccount(self):
        self.id = ichat.utils.create_user(username=self.username, password=self.password)
        print(f'Created account for {self.username}')

    #def
    def __str__(self):
        return f'{self.username}:{self.password} {self.messages}'

if __name__ == '__main__':
    botMenager = BotMenager("BotsCharacters.txt")