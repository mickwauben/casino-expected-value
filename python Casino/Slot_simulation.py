import random
fruit=[1,2,3,4,5,6,7,8,9]
amount = 1000000
total=0
for i in range (amount):
    spin=[]
    for j in range (3):
        spin.append(random.choice(fruit))
    if spin[0]==spin[1]==spin[2]:
        total=total+25
    elif spin[0]==spin[1] or spin[1]==spin[2] or spin[0]==spin[2]:
        total=total+1
    else:
        total=total-1
print(total/amount)        
        
