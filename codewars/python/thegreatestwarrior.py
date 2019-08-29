GLOBAL_RANKS = ["Pushover", "Novice", "Fighter",
                "Warrior", "Veteran", "Sage",
                "Elite", "Conqueror", "Champion",
                "Master", "Greatest"]


class Warrior():
    def __init__(self):
        self.level = 1
        self.experience = 100
        self.rank = "Pushover"
        self.achievements = []

    def add_exp(self, amount):
        if self.level is not 100:
            if self.experience + amount > 10000:
                self.experience = 10000
            else:
                self.experience += abs(amount)
        self.level = int(self.experience / 100)
        self.check_rank()

    def check_rank(self):
        self.rank = GLOBAL_RANKS[int(self.level / 10)]

    def training(self, arg):
        if self.level < arg[2]:
            return "Not strong enough"
        else:
            self.achievements.append(arg[0])
            self.add_exp(arg[1])
            return arg[0]

    def battle(self, level):
        # Not sure if level is the actual thing we use????
        if not 100 >= level >= 1:
            return "Invalid level"
        elif self.level - level >= 2:
            return "Easy fight"
        elif self.level == level or level == self.level - 1:
            if self.level == level:
                self.add_exp(10)
            else:
                self.add_exp(5)
            return "A good fight"
        elif GLOBAL_RANKS[int(level / 10) - 1] == GLOBAL_RANKS[int(self.level / 10)] and level - self.level >= 5:
            return "You've been defeated"
        else:
            self.add_exp(20 * (level - self.level) * (level - self.level))
            return "An intense fight"
