class Food:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
    def __repr__(self):
        return f'Food: {self.name} is a {self.kind}'
        
    def describe(self):
        print(f'{self.name} is a {self.kind}')
    #a static version of the describe method
    @staticmethod
    def describe_static(food):
        print(f'{food.name} is a {food.kind}')
    #a class method version of the describe method
    @classmethod
    def describe_class(cls, food):
        print(f'{food.name} is a {food.kind}')

class Meat(Food):
    def __init__(self, name):
        super().__init__(name, 'meat')
    def cook(self):
        print(f'Cooking {self.name}')

class Fruit(Food):
    def __init__(self, name):
        super().__init__(name, 'fruit')
    def clean(self):
        print(f'Cleaning {self.name}')
food = Fruit('apple', 'fruit')
food.clean()
food.describe()