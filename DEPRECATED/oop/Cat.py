from Animal import Animal
from Dog import Dog
class Cat(Animal):
    def __init__(self, name: str, age: int, weight: float, color: str):
        super().__init__(name, age, weight)
        self.color = color
    def purr(self):
        print(f'{self.name} is purring')
    def eat(self):
        print(f'{self.name} is eating')
    def sleep(self):
        print(f'{self.name} is sleeping')

dog1 = Dog('Fido', 5, 10, 'Lab')
cat1 = Cat('Fluffy', 2, 3, 'White')
dog1.bark()
cat1.sleep()