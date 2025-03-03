from ichat import models,utils
import random

class BotMenager:
    def __init__(self, botsDescriptionFile):
        self.bots = []
        self.botCount = 0
