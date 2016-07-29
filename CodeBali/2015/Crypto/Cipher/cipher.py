#!/usr/bin/python3

with open('cipher.txt','r') as f:
    numbers = f.read().split(' ')[:-1]

flag = ''

for number in numbers:
    if len(number) >= 6:
        flag += chr(int(number, 2))
    elif number[0] == '0':
        flag += chr(int(number, 8))
    else:
        try:
            flag += chr(int(number))
        except:
            flag += chr(int(number, 16))

print (flag)
