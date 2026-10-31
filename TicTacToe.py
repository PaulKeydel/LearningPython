from tkinter import *  
from tkinter import messagebox


def ist_gewonnen(quiz):
    for zeile in range(3):
        if (quiz[zeile][0] != "") and (quiz[zeile][0] == quiz[zeile][1] == quiz[zeile][2]):
            return True
    for spalte in range(3):
        if (quiz[0][spalte] != "") and (quiz[0][spalte] == quiz[1][spalte] == quiz[2][spalte]):
            return True
    if quiz[1][1] != "":
        if quiz[0][0] == quiz[1][1] == quiz[2][2]:
            return True
        if quiz[0][2] == quiz[1][1] == quiz[2][0]:
            return True
    return False

def ist_unentschieden(quiz):
    felder_leer = quiz[0].count("") + quiz[1].count("") + quiz[2].count("")
    if felder_leer == 0:
        return True
    else:
        return False

def clicked_spielfeld(zeile, spalte, buttons, spielfeld, spieler):
    # Button bereits geklickt?
    if buttons[zeile][spalte].cget("text") != "":
        return

    anzahl_zuege = 9 - spielfeld[0].count("") - spielfeld[1].count("") - spielfeld[2].count("")
    aktueller_spieler = spieler[anzahl_zuege % 2]

    buttons[zeile][spalte].configure(text = aktueller_spieler)
    spielfeld[zeile][spalte] = aktueller_spieler

    if ist_gewonnen(spielfeld):
        messagebox.showinfo("Winner", aktueller_spieler + " hat gewonnen!")
    elif ist_unentschieden(spielfeld):
        messagebox.showinfo("Unentschieden", "Unentschieden!")
    else:
        return
    for zeile in range(3):
        for spalte in range(3):
            buttons[zeile][spalte].configure(state = DISABLED)

def clicked_neu(buttons, spielfeld):
    for zeile in range(3):
        for spalte in range(3):
            buttons[zeile][spalte].configure(state = NORMAL)
            buttons[zeile][spalte].configure(text = "")
            spielfeld[zeile][spalte] = ""


# grafische Benutzeroberfläche erstellen...
app = Tk()
app.title("Tic Tac Toe")
app.resizable(0,0)

# initialisiere alle Listen
buttons = [[None] * 3, [None] * 3, [None] * 3]
spielfeld = [[""] * 3, [""] * 3, [""] * 3]
spieler = ["X", "O"]

# erzeuge Buttons
for i in range(3):
    for j in range(3):
        buttons[i][j] = Button(app,
            height = 4,
            width = 8,
            font = ("Helvetica", "20"),
            command = lambda z=i, s=j, b=buttons, f=spielfeld, p=spieler: clicked_spielfeld(z, s, b, f, p)
        )
        buttons[i][j].grid(row = i, column = j)
# erstelle "Neues Spiel"-Button
btn_neu = Button(app, text = "Neues Spiel", command = lambda b=buttons, f=spielfeld: clicked_neu(b, f))
btn_neu.grid(row = 1, column = 3)

app.mainloop()