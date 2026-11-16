#importeren nodige functies
import tkinter as tk
from tkinter import messagebox
import random, csv, time
#lijsten aanmaken om uit csv toe te voegen
kaarten = []
roulette = []
#lijst vr slotmachine, codes van emojis die zorgen voor fruit
fruit = ["\U0001F352", "\U0001F34B", "\U0001F34A", "\U0001F347", "\U0001F349", "7", "\U00002764", '\U0001F4B0', '\U0001F48E']
#csv bestanden uitlezen en toevoegen aan lijsten
with open("kaarten.csv", mode="r", encoding="utf-8") as bestand:
    #delimiter= aparte cellen bekijken
    reader = csv.reader(bestand, delimiter=";")
    #elementen uit csv toevoegen aan lijsten
    for row in reader:
        kaarten.append(row)
with open("roulette.csv", mode="r", encoding="utf-8") as bestand:
    reader = csv.reader(bestand, delimiter=";")
    for row in reader:
        roulette.append(row)

gebruiker = ""
saldo = 0
startTijd = time.time()

#lobby aanmaken
venster_lobby = tk.Tk()
venster_lobby.title("Casino - start")
venster_lobby.geometry("800x500")

titelLabel = tk.Label(venster_lobby, text="Welkom in het casino", font=("Arial", 24))
titelLabel.place(x=220, y=40, width=380, height=50)
#return variabele vragen/invoervak aanmaken
gebruikerLabel = tk.Label(venster_lobby, text="Voer een gebruikersnaam in:")
gebruikerLabel.place(x=230, y=140, width=250, height=30)
gebruikerInvoer = tk.Entry(venster_lobby)
gebruikerInvoer.place(x=480, y=140, width=180, height=30)

saldoLabel = tk.Label(venster_lobby, text="Geef je saldo in:")
saldoLabel.place(x=230, y=200, width=250, height=30)
saldoInvoer = tk.Entry(venster_lobby)
saldoInvoer.place(x=480, y=200, width=180, height=30)
#spelkeuze
def start_casino():
    #importeren buiten def
    global gebruiker, saldo, venster_menu, saldoLabelMenu
#naam en saldo uit invoervak halen
    gebruiker = gebruikerInvoer.get()
    saldoTekst = saldoInvoer.get()
#kijken of naam is ingevored
    if gebruiker == "":
        messagebox.showerror("Fout", "Geef eerst een naam in.")
        return
#saldo vragen en omzetten in int
    saldo = int(saldoTekst)

    if saldo <= 0:
        messagebox.showerror("Fout", "Je saldo moet groter zijn dan 0.")
        return
#beginscherm verwijderen -> keuze menu aanmaken met knoppen
    venster_lobby.destroy()

    venster_menu = tk.Tk()
    venster_menu.title("Casino - menu")
    venster_menu.geometry("800x500")

    titelLabel = tk.Label(venster_menu, text="Casino", font=("Arial", 26))
    titelLabel.place(x=330, y=30, width=160, height=50)

    saldoLabelMenu = tk.Label(venster_menu, text="Speler: " + gebruiker + "    Saldo: " + str(saldo) + " euro")
    saldoLabelMenu.place(x=200, y=100, width=400, height=40)

    blackjackKnop = tk.Button(venster_menu, text="Blackjack", command=open_blackjack)
    blackjackKnop.place(x=300, y=180, width=200, height=50)

    rouletteKnop = tk.Button(venster_menu, text="Roulette", command=open_roulette)
    rouletteKnop.place(x=300, y=250, width=200, height=50)

    slotKnop = tk.Button(venster_menu, text="Slot machine", command=open_slotmachine)
    slotKnop.place(x=300, y=320, width=200, height=50)

    stopKnop = tk.Button(venster_menu, text="Stoppen", command=stop_casino)
    stopKnop.place(x=300, y=390, width=200, height=50)

    venster_menu.mainloop()

#knoppen definiëren
def stop_casino():
    #tijd hoelang je in casino bent gebleven
    tijd = round(time.time() - startTijd, 2)
    #eindsalod met tijd laten zien
    messagebox.showinfo("Einde", "Bedankt om te spelen, " + gebruiker + "!\nEindsaldo: " + str(saldo) + " euro\nTijd: " + str(tijd) + " seconden")
    venster_menu.destroy()

#keuze blackjack
def open_blackjack():
    #BJ venster maken
    blackjackVenster = tk.Tk()
    blackjackVenster.title("Blackjack")
    blackjackVenster.geometry("900x600")
#lege lijsten maken voor kaarten/punten
    spelerHand = []
    dealerHand = []
    huidigeInzet = [0]
#labels voor uitleg en overzicht
    titelLabel = tk.Label(blackjackVenster, text="Blackjack", font=("Arial", 22))
    titelLabel.place(x=350, y=20, width=200, height=40)

    uitlegLabel = tk.Label(blackjackVenster, text="Probeer dichter bij 21 te komen dan de dealer.")
    uitlegLabel.place(x=250, y=70, width=400, height=30)

    inzetLabel = tk.Label(blackjackVenster, text="Inzet:")
    inzetLabel.place(x=250, y=120, width=100, height=30)

    inzetInvoer = tk.Entry(blackjackVenster)
    inzetInvoer.place(x=350, y=120, width=150, height=30)

    spelerLabel = tk.Label(blackjackVenster, text="Jouw kaarten:")
    spelerLabel.place(x=50, y=220, width=780, height=40)

    dealerLabel = tk.Label(blackjackVenster, text="Dealer:")
    dealerLabel.place(x=50, y=290, width=780, height=40)

    resultaatLabel = tk.Label(blackjackVenster, text="")
    resultaatLabel.place(x=50, y=360, width=780, height=40)
#spel starten
    def blackjack_starten():
        global saldo
#inzet vastleggen en omvormen nr int
        inzet = int(inzetInvoer.get())
#kijken of inzet mogelijk is
        if inzet <= 0:
            messagebox.showerror("Fout", "Je inzet moet groter zijn dan 0.")
            return

        if inzet > saldo:
            messagebox.showerror("Fout", "Je hebt niet genoeg saldo.")
            return
#inzet van saldo aftrekken, hands leegmaken van spelers
        saldo = saldo - inzet
        huidigeInzet[0] = inzet
        #handen leegmaken
        spelerHand.clear()
        dealerHand.clear()
#random kaarten aan dealer en speler geven, 2x omdat 2 kaarten bij begin
        spelerHand.append(random.choice(kaarten))
        spelerHand.append(random.choice(kaarten))
        dealerHand.append(random.choice(kaarten))
        dealerHand.append(random.choice(kaarten))
#waarde van kaarten en aantal azen definieren voor rekenwerk
        spelerWaarde = 0
        spelerAzen = 0
        spelerTekst = ""
#voor elke kaart die in de speler zijn handen zit volledig uitschrijven in welke waarde van welke soort + waardes optellen en opslaan
        #elke kaart die in je hand zit definieren en uitschrijven (tekst)
        for kaart in spelerHand:
            spelerTekst = spelerTekst + kaart[1] + " van " + kaart[0] + "  "
            #elke kaart heeft bepaalde waarde, waardes staan in csv in kolom 3-> [2], waardes vastzetten en optellen voor vergelijken
            spelerWaarde = spelerWaarde + int(kaart[2])
#kijken of speler een aas heeft, kan 1/11 zijn, later meer            
            if kaart[1] == "aas":
                spelerAzen = spelerAzen + 1
#waarde van aas benoemen, kan 1 of 11 zijn. aas= automatisch 11, maar als je boven 21 hebt en aas bezit gaat je aaswaarde naar 1                
        while spelerWaarde > 21 and spelerAzen > 0:
            spelerWaarde = spelerWaarde - 10
            spelerAzen = spelerAzen - 1
#labels vertellen welke kaarten jij en de dealer hebben
        spelerLabel.config(text="Jouw kaarten: " + spelerTekst + " Waarde: " + str(spelerWaarde))
        dealerLabel.config(text="Dealer: " + dealerHand[0][1] + " van " + dealerHand[0][0] + " en 1 verborgen kaart")
        resultaatLabel.config(text="Kies kaart of pas.")
        saldoLabelMenu.config(text="Speler: " + gebruiker + "    Saldo: " + str(saldo) + " euro")
#staat van knoppen bepalen, als spel nog bezig kan je zowel hitten als passen, als over 21 is spel gedaan dus worden knoppen uitgeschakeld (zie verder)
        hitKnop.config(state="normal")
        pasKnop.config(state="normal")
        startKnop.config(state="disabled")
#hit knop
    def kaart_nemen():
#kaart toevoegen aan je hand als hit
        spelerHand.append(random.choice(kaarten))
#waardes resetten want je kijkt naar ALLE kaarten in spelerhand, niet welke je extra pakt, anders tel je originele kaarten dubbel
        spelerWaarde = 0
        spelerAzen = 0
        spelerTekst = ""
        #weer definieren
        for kaart in spelerHand:
            spelerTekst = spelerTekst + kaart[1] + " van " + kaart[0] + "  "
            spelerWaarde = spelerWaarde + int(kaart[2])
            if kaart[1] == "aas":
                spelerAzen = spelerAzen + 1
        while spelerWaarde > 21 and spelerAzen > 0:
            spelerWaarde = spelerWaarde - 10
            spelerAzen = spelerAzen - 1

        spelerLabel.config(text="Jouw kaarten: " + spelerTekst + " Waarde: " + str(spelerWaarde))
#knoppen uitschakelen als spel gedaan is
        if spelerWaarde > 21:
            resultaatLabel.config(text="Je bent kapot. Je verliest. Nieuw saldo: " + str(saldo) + " euro")
            hitKnop.config(state="disabled")
            pasKnop.config(state="disabled")
            startKnop.config(state="normal")
#principe van pas: geen kaart extra nemen als speler, dealer wel eventueel nog nemen/onthullen
    def passen():
        global saldo
#eerst dealer deel        
#waardes resetten, zelfde principe: ALLE kaarten checken en tellen
        dealerWaarde = 0
        dealerAzen = 0
        for kaart in dealerHand:
            dealerWaarde = dealerWaarde + int(kaart[2])
            if kaart[1] == "aas":
                dealerAzen = dealerAzen + 1
        while dealerWaarde > 21 and dealerAzen > 0:
            dealerWaarde = dealerWaarde - 10
            dealerAzen = dealerAzen - 1
#dealer neemt alleen onder 17 extra (makkelijker)
        while dealerWaarde < 17:
            dealerHand.append(random.choice(kaarten))
            dealerWaarde = 0
            dealerAzen = 0
            for kaart in dealerHand:
                dealerWaarde = dealerWaarde + int(kaart[2])
                if kaart[1] == "aas":
                    dealerAzen = dealerAzen + 1
            while dealerWaarde > 21 and dealerAzen > 0:
                dealerWaarde = dealerWaarde - 10
                dealerAzen = dealerAzen - 1
#spelerdeel van passen, gewoon overschrijven eig, verandert niks
        spelerWaarde = 0
        spelerAzen = 0
        spelerTekst = ""
        for kaart in spelerHand:
            spelerTekst = spelerTekst + kaart[1] + " van " + kaart[0] + "  "
            spelerWaarde = spelerWaarde + int(kaart[2])
            if kaart[1] == "aas":
                spelerAzen = spelerAzen + 1
        while spelerWaarde > 21 and spelerAzen > 0:
            spelerWaarde = spelerWaarde - 10
            spelerAzen = spelerAzen - 1

        dealerTekst = ""
        for kaart in dealerHand:
            dealerTekst = dealerTekst + kaart[1] + " van " + kaart[0] + "  "
#kijken win/verlies
        inzet = huidigeInzet[0]
        if dealerWaarde > 21:
            saldo = saldo + inzet * 2
            resultaat = "Dealer is kapot. Je wint!"
        elif spelerWaarde > dealerWaarde:
            saldo = saldo + inzet * 2
            resultaat = "Je wint!"
        elif spelerWaarde == dealerWaarde:
            saldo = saldo + inzet
            resultaat = "Gelijkspel. Je krijgt je inzet terug."
        else:
            resultaat = "Dealer wint. Je verliest."
#config is tekst veranderen
        spelerLabel.config(text="Jouw kaarten: " + spelerTekst + " Waarde: " + str(spelerWaarde))
        dealerLabel.config(text="Dealer: " + dealerTekst + " Waarde: " + str(dealerWaarde))
        resultaatLabel.config(text=resultaat + " Nieuw saldo: " + str(saldo) + " euro")
        saldoLabelMenu.config(text="Speler: " + gebruiker + "    Saldo: " + str(saldo) + " euro")

        hitKnop.config(state="disabled")
        pasKnop.config(state="disabled")
        startKnop.config(state="normal")
#knoppen aanmaken binnen knop
    startKnop = tk.Button(blackjackVenster, text="Start ronde", command=blackjack_starten)
    startKnop.place(x=520, y=120, width=140, height=30)

    hitKnop = tk.Button(blackjackVenster, text="Kaart", command=kaart_nemen, state="disabled")
    hitKnop.place(x=300, y=450, width=120, height=40)

    pasKnop = tk.Button(blackjackVenster, text="Pas", command=passen, state="disabled")
    pasKnop.place(x=460, y=450, width=120, height=40)


def open_roulette():
#roulette venster aanmaken voor start met alle nodige info/labels    
    rouletteVenster = tk.Tk()
    rouletteVenster.title("Roulette")
    rouletteVenster.geometry("900x600")

    titelLabel = tk.Label(rouletteVenster, text="Roulette", font=("Arial", 22))
    titelLabel.place(x=350, y=20, width=200, height=40)

    uitlegLabel = tk.Label(rouletteVenster, text="Soort: nummer, kleur of even. Keuze: bv. 17, rood, zwart, even of oneven.")
    uitlegLabel.place(x=120, y=80, width=650, height=30)

    inzetLabel = tk.Label(rouletteVenster, text="Inzet:")
    inzetLabel.place(x=220, y=140, width=120, height=30)
    inzetInvoer = tk.Entry(rouletteVenster)
    inzetInvoer.place(x=360, y=140, width=180, height=30)

    soortLabel = tk.Label(rouletteVenster, text="Soort:")
    soortLabel.place(x=220, y=190, width=120, height=30)
    soortInvoer = tk.Entry(rouletteVenster)
    soortInvoer.place(x=360, y=190, width=180, height=30)

    keuzeLabel = tk.Label(rouletteVenster, text="Keuze:")
    keuzeLabel.place(x=220, y=240, width=120, height=30)
    keuzeInvoer = tk.Entry(rouletteVenster)
    keuzeInvoer.place(x=360, y=240, width=180, height=30)

    resultaatLabel = tk.Label(rouletteVenster, text="")
    resultaatLabel.place(x=100, y=360, width=700, height=60)
#draaiknop=start van spel
    def draai_roulette():
        global saldo

        inzet = int(inzetInvoer.get())

        if inzet <= 0:
            messagebox.showerror("Fout", "Je inzet moet groter zijn dan 0.")
            return

        if inzet > saldo:
            messagebox.showerror("Fout", "Je hebt niet genoeg saldo.")
            return
#soort en specifieke keuze binnen de soort vastzetten voor het draaien
        soort = soortInvoer.get()
        keuze = keuzeInvoer.get()
#kijken of je correcte dingen invoerd
        if soort != "nummer" and soort != "kleur" and soort != "even":
            messagebox.showerror("Fout", "Soort moet nummer, kleur of even zijn.")
            return

        saldo = saldo - inzet
#uit de lijst waaruit csv is geimporteerd random kiezen        
        vakje = random.choice(roulette)
#kijken naar kleur/getal/waarde, hangt van kolom af        
        getal = int(vakje[0])
        kleur = vakje[1]
        evenOneven = vakje[2]
#we gaan ervanuit dat we niet gewonnen hebben, veranderd als wel gewonnen        
        gewonnen = False
        winst = 0
#kijken of we gokken op een nummer, kleur of even/oneven
        if soort == "nummer":
            gekozenGetal = int(keuze)

            if gekozenGetal < 0 or gekozenGetal > 36:
                messagebox.showerror("Fout", "Geef een getal van 0 tot 36 in.")
                saldo = saldo + inzet
                return

            if gekozenGetal == getal:
            #verander dat we WEL gewonnen hebben zoals boven vermeld, makkelijker om resultaat te tonen voor alle categorien samen    
                gewonnen = True
                winst = inzet * 36
#la meme chose
        if soort == "kleur":
            if keuze != "rood" and keuze != "zwart" and keuze != "groen":
                messagebox.showerror("Fout", "Kies rood, zwart of groen.")
                saldo = saldo + inzet
                return

            if keuze == kleur:
                gewonnen = True
                if keuze == 'groen':
                    winst= inzet *36
                else:
                    winst = inzet * 2
#la meme chose
        if soort == "even":
            if keuze != "even" and keuze != "oneven":
                messagebox.showerror("Fout", "Kies even of oneven.")
                saldo = saldo + inzet
                return

            if keuze == evenOneven:
                gewonnen = True
                winst = inzet * 2
#resultaten weergeven
        if gewonnen == True:
            saldo = saldo + winst
            resultaat = "De bal valt op " + str(getal) + " " + kleur + " " + evenOneven + ". Je wint!"
        else:
            resultaat = "De bal valt op " + str(getal) + " " + kleur + " " + evenOneven + ". Je verliest."

        resultaatLabel.config(text=resultaat + " Nieuw saldo: " + str(saldo) + " euro")
        saldoLabelMenu.config(text="Speler: " + gebruiker + "    Saldo: " + str(saldo) + " euro")
#knop aanmaken
    draaiKnop = tk.Button(rouletteVenster, text="Draaien", command=draai_roulette)
    draaiKnop.place(x=360, y=300, width=180, height=40)


def open_slotmachine():
#venster + labels/slots aanmaken voor start slotmachine spel
    slotVenster = tk.Tk()
    slotVenster.title("Slot machine")
    slotVenster.geometry("900x600")

    titelLabel = tk.Label(slotVenster, text="Slot machine", font=("Arial", 22))
    titelLabel.place(x=320, y=20, width=260, height=40)

    inzetLabel = tk.Label(slotVenster, text="Inzet:")
    inzetLabel.place(x=260, y=100, width=100, height=30)
    inzetInvoer = tk.Entry(slotVenster)
    inzetInvoer.place(x=360, y=100, width=170, height=30)
#3 slots aanmaken die random worden gekozen
    rol1Label = tk.Label(slotVenster, text="?", font=("Arial", 40))
    rol1Label.place(x=250, y=200, width=100, height=100)

    rol2Label = tk.Label(slotVenster, text="?", font=("Arial", 40))
    rol2Label.place(x=400, y=200, width=100, height=100)

    rol3Label = tk.Label(slotVenster, text="?", font=("Arial", 40))
    rol3Label.place(x=550, y=200, width=100, height=100)

    resultaatLabel = tk.Label(slotVenster, text="")
    resultaatLabel.place(x=100, y=370, width=700, height=60)
#knop om te draaien
    def draai_slotmachine():
        global saldo

        inzet = int(inzetInvoer.get())

        if inzet <= 0:
            messagebox.showerror("Fout", "Je inzet moet groter zijn dan 0.")
            return

        if inzet > saldo:
            messagebox.showerror("Fout", "Je hebt niet genoeg saldo.")
            return

        saldo = saldo - inzet
        teller = 0

#draaieffect (PUUR effect, geen funtie)
        while teller < 10:
            #veranderen van tekens, 10x ververst, door .update aangepast in labels wat zorgt voor draaieffect in combinatie met de tijd
            rol1Label.config(text=random.choice(fruit))
            rol2Label.config(text=random.choice(fruit))
            rol3Label.config(text=random.choice(fruit))
            slotVenster.update()
            time.sleep(0.1)
            teller = teller + 1
#daadwerkelijke keuze van slotmachine
        rol1 = random.choice(fruit)
        rol2 = random.choice(fruit)
        rol3 = random.choice(fruit)
#labels/symbolen aanpassen naar het uiteindelijke symbool
        rol1Label.config(text=rol1)
        rol2Label.config(text=rol2)
        rol3Label.config(text=rol3)
#vergelijken
        if rol1 == rol2 and rol2 == rol3:
            winst = inzet * 26
            saldo = saldo + winst
            resultaat = "Drie dezelfde! Je wint " + str(winst) + " euro."
        elif rol1 == rol2 or rol1 == rol3 or rol2 == rol3:
            winst = inzet * 2
            saldo = saldo + winst
            resultaat = "Twee dezelfde! Je wint " + str(winst) + " euro."
        else:
            resultaat = "Geen combinatie. Je verliest."

        resultaatLabel.config(text=resultaat + " Nieuw saldo: " + str(saldo) + " euro")
        saldoLabelMenu.config(text="Speler: " + gebruiker + "    Saldo: " + str(saldo) + " euro")
#draaiknop aanmaken van slotmachine
    draaiKnop = tk.Button(slotVenster, text="Draaien", command=draai_slotmachine)
    draaiKnop.place(x=360, y=470, width=180, height=40)

#knop van volgende bij inlogscherm aanmaken, helemaal onderaan omdat er tussen allemaal andere knoppen zitten die er 'binnen' horen
volgendeKnop = tk.Button(venster_lobby, text="Volgende", command=start_casino)
volgendeKnop.place(x=330, y=290, width=160, height=50)

venster_lobby.mainloop()