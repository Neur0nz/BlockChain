import random
import datetime
name='Max'
age=27
hobbies=["coding", "fencing", "climbing"]
person1 = {'name': name,'age': age, 'hobbies': hobbies}
person2 = {'name': 'jimmy','age': 22, 'hobbies': ['coding', 'swimming']}
persons= [person1,person2]

names = [per['name'] for per in persons]

larger_than_20 = all(per['age']>20 for per in persons)

new_persons = persons[:]
new_persons[0]['name']='Nadav'

a, b=[per for per in persons]
print(a)
print(b)
random1 = random.randint(1,10)
random2 = random.randint(0,1)
date = datetime.datetime.now()
print(str(date)+"   "+str(random1))

