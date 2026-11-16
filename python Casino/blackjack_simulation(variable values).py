import random, csv
kaarten=[]
amount=1000000
total=0
EVlist=[]
with open("kaarten.csv", mode="r", encoding="utf-8") as bestand:
    reader = csv.reader(bestand, delimiter=";")
    for row in reader:
        kaarten.append(row)
for j in range(12,21):
    total=0
    for i in range(amount):
        player_hand=[]
        dealer_hand=[]
        player_hand.append(random.choice(kaarten))
        player_hand.append(random.choice(kaarten))
        dealer_hand.append(random.choice(kaarten))
        dealer_hand.append(random.choice(kaarten))
        player_value=0
        player_Ase=0
        dealer_value=0
        dealer_Ase=0
        for kaart in player_hand:
            player_value= player_value+ int(kaart[2])
            if kaart[1]== 'aas':
                player_Ase= player_Ase+1
        while player_value > 21 and player_Ase > 0:
                player_value = player_value - 10
                player_Ase = player_Ase - 1    
        while player_value<j:
            player_hand.append(random.choice(kaarten))
            player_value = 0
            player_Ase = 0
            for kaart in player_hand:
                player_value = player_value + int(kaart[2])
                if kaart[1] == "aas":
                    player_Ase = player_Ase + 1
            while player_value > 21 and player_Ase > 0:
                player_value = player_value - 10
                player_Ase = player_Ase - 1
        
        for kaart in dealer_hand:
            dealer_value= dealer_value+ int(kaart[2])
            if kaart[1]== 'aas':
                dealer_Ase= dealer_Ase+1
        while dealer_value > 21 and dealer_Ase > 0:
                dealer_value = dealer_value - 10
                dealer_Ase = dealer_Ase - 1    
        while dealer_value<17:
            dealer_hand.append(random.choice(kaarten))
            dealer_value = 0
            dealer_Ase = 0
            for kaart in dealer_hand:
                dealer_value = dealer_value + int(kaart[2])
                if kaart[1] == "aas":
                    dealer_Ase = dealer_Ase + 1
            while dealer_value > 21 and dealer_Ase > 0:
                dealer_value = dealer_value - 10
                dealer_Ase = dealer_Ase - 1
        if player_value > 21:
            total = total - 1
        elif dealer_value > 21:
            total = total + 1
        elif dealer_value > player_value:
            total = total - 1
        elif player_value > dealer_value:
            total = total + 1
    EV=total/amount
    EVlist.append(EV)
    print(j, EV)

        
