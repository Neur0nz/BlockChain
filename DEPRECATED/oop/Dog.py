from Animal import Animal
class Dog(Animal):
    def __init__(self, name: str, age: int, weight: float, breed: str):
        super().__init__(name, age, weight)
        self.breed = breed
    def bark(self):
        print(f'{self.name} is barking')