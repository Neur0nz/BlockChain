import time
class Clock:
    def __init__(self, seconds_elapsed):
        self.__seconds_elapsed = seconds_elapsed

    def print_time(self):
        minute = self.seconds_elapsed // 60
        hour = minute // 60
        minute = minute % 60
        print(f'{hour}:{minute}:{self.seconds_elapsed % 60}')

    def tick(self):
        self.__seconds_elapsed += 1
clocke = Clock(0)
while True:
    clocke.tick()
    clocke.print_time()
    print(clocke.__dict__)
    time.sleep(1)
# double underscore is a private variable or method (not accessible outside the class) (isnt enforced by python, just a convention, buy youll be yelled at!) 