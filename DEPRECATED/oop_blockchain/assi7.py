import json
import pickle
#first and second assignment
running = True
while running:
    choice = input("enter choice: ")
    if choice == "1":
        with open('assignment.txt', 'w') as f:
            f.write(input('enter a new line: ')+'\n')
    elif choice == "2":
        with open('assignment.txt', 'r') as f:
            print(f.readlines())
    elif choice == "3":
        running = False
#third assignment
listed = []
while running:
    choice = input("enter choice: ")
    if choice == "1":
        listed.append(input('enter a new line: '))
    elif choice == "2":
        print(listed)
    elif choice == "3":
        running = False
with open('assignment.txt', 'w') as f:
    f.write(json.dumps(listed))
with open('assignment.p', 'wb') as f:
    f.write(pickle.dumps(listed))
#fourth assignment
with open('assignment.txt', 'r') as f:
    listed = json.loads(f.read())
with open('assignment.p', 'rb') as f:
    listed = pickle.loads(f.read())