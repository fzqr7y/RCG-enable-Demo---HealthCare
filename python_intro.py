

if 3<2:
    print('Hello, Django girls! 3>2')
else:
    print('5 is not greater than 2')
        
name = 'Sonja'
if name == 'Ola':
    print('Hey Ola!')
elif name == 'Sonja':
    print('Hey Sonja!')
else:
    print('Hey anonymous!')        

volume = 85
if volume < 20:
    print("It's kinda quiet.")
elif 20 <= volume < 40:
    print("It's nice for background music")
elif 40 <= volume < 60:
    print("Perfect, I can hear all the details")
elif 60 <= volume < 80:
    print("Nice for parties")
elif 80 <= volume < 100:
    print("A bit loud!")
else:
    print("My ears are hurting! :(")

def hi():
    print('Hi there!')
    print('How are you?')

hi()

# Okay, our first function is ready

def hito(name):
    if name == 'Ola':
        print('Hi to Ola!')
    elif name == 'Sonja':
        print('Hi to Sonja!')
    else:
        print('Hi there ' + name + '!')

hito('Ola')
hito('Jim')

girls = ['Rachel', 'Sonja', 'Monica', 'Phoebe', 'Ola', 'You']
for name in girls:
    hito(name)
    print('Next girl')

# Change the volume if it's too loud or too quiet
if volume < 20 or volume > 80:
    volume = 50
    print("That's better!")

for i in range(1, 6):
    print(i)


