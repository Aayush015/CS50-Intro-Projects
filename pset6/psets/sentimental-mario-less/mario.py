from cs50 import get_int
# get the height from the user and prompt the user for wrong input
height = get_int("Height: ")
while (height <= 0 or height >= 9):
    height = get_int("Height: ")

# looing including the height starting from 1 to remove space
for i in range(1, height+1):
    print(" "*(height - i) + "#"*i)