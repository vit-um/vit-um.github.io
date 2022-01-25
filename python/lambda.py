# list of dictionary
people = [
    {"name":"Harry", "house":"Gryffindor"},
    {"name":"Cho", "house":"Ravenclaw"},
    {"name":"Draco","house":"Slytherin"}
]

def f(person):
    return person["name"]

people.sort(key = f)

print(people)

# А тепер те саме за допомогою функції lambda

people.sort(key = lambda person: person["house"])

print(people)
