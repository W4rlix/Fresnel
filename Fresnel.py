import tkinter as tk
from tkinter import *
from tkinter import ttk
import math
import json

root = tk.Tk()
root.geometry("450x300")
root.title("Tab")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')
tabControl.pack(expand=1, fill="both")

#--------------------------------------------------------------
#zakladka 1

current_value1 = tk.DoubleVar()
current_value2 = tk.DoubleVar()


def get_current_value_1():
    return '{: .2f}'.format(current_value1.get())

def slider_changed1(event):
    value_label_1.configure(text=get_current_value_1())

slider1 = ttk.Scale(
    tab1,
    from_=100,
    to=0,
    orient='vertical',  # horizontal
    command=slider_changed1,
    variable=current_value1
)

slider1.grid(column=0,row=0)

value_label_1 = ttk.Label(
    tab1,
    text=get_current_value_1()
)

value_label_1.grid(
    row=1,
    column=0,
    columnspan=1,
    sticky='n'
)
#-------------------------------------------------------

def get_current_value_2():
    return '{: .2f}'.format(current_value2.get())

def slider_changed2(event):
    value_label_2.configure(text=get_current_value_2())

slider2 = ttk.Scale(
    tab1,
    from_=100,
    to=0,
    orient='vertical',  # horizontal
    command=slider_changed2,
    variable=current_value2
)

slider2.grid(column=2,row=0)

value_label_2 = ttk.Label(
    tab1,
    text=get_current_value_2()
)

value_label_2.grid(
    row=1,
    column=2,
    columnspan=1,
    sticky='n'
)
#-------------------------------------------------------
R=6371*1000

def oblicz():
    h1 = current_value1.get()
    h2 = current_value2.get()
    d1= math.sqrt(2*(4/3)*R*h1)
    d2 = math.sqrt(2*(4/3)*R*h2)
    d = round(d1 + d2)
    print(d)
    f = int(freq.get())
    fresnel = round(17.31*(math.sqrt((d)/(4*int(f)))),2)
    global LOS 
    global Fresnel
    LOS = d
    Fresnel = fresnel
    wynik.set("LOS dla dwoch masztow wynosi: \n" + str(d) + "m \na średnica strefy fresnela wynosi: \n" + str(fresnel) + "m")


def zapiszDoJSON(event):
    h1 = current_value1.get()
    h2 = current_value2.get()
    f = freq.get()

    dictionary = {
        "wysokosc1": h1,
        "wysokosc2": h2,
        "czestotliwosc": f,
        "LOS": LOS,
        "srednica strefy fresnela": Fresnel
    }

    json_object = json.dumps(dictionary)

    with open("wyniki_dla_dwóch_masztów.json", "w") as outfile:
        outfile.write(json_object)

ttk.Label(tab1, text='Podaj czestotliwosc w GHZ').grid(column=1, row=0,padx = 50)
freq = Entry(tab1)
freq.grid(row = 1, column = 1,padx = 5)

btn1 = Button(tab1, text = 'Oblicz',command=oblicz)
btn2 = Button(tab1, text = 'Zapisz do JSON')
btn2.bind('<Button-1>',zapiszDoJSON)

btn1.grid(row = 3, column = 0)
btn2.grid(row = 3, column = 2)

wynik = StringVar()
wynik.set("Wynik")
label = ttk.Label(tab1, textvariable=wynik).grid(column=1, row=2, pady = 30, padx = 30)


#--------------------------------------------------------------
#zakladka 2

def zapiszDoJSON_2(event):
    current_value=float(wysokosc.get())
    X=lat.get()
    Y=lon.get()
    h = float(current_value)
    d= round(math.sqrt(2*(4/3)*R*h),2)
    LOS = d
    wynik2.set("LOS dla podanego masztu wynosi: \n" + str(d) + "m")

    dictionary = {
        "wysokosc": h,
        "szerokosc i dlugosc geograficzna": [ X ,Y ],
        "LOS": LOS
    }

    json_object = json.dumps(dictionary)

    with open("wynik_dla_jednego_masztu.json", "w") as outfile:
        outfile.write(json_object)


ttk.Label(tab2, text='Wysokosc').grid(column=0, row=0,padx = 50)
wysokosc = Entry(tab2,textvariable='0.0')
wysokosc.grid(row = 0, column = 1,padx = 5)

ttk.Label(tab2, text='szerokość geograficzna').grid(column=0, row=1,padx = 50)
lat = Entry(tab2)
lat.grid(row = 1, column = 1,padx = 5)

ttk.Label(tab2, text='długość geograficzna').grid(column=0, row=2,padx = 50)
lon = Entry(tab2)
lon.grid(row = 2, column = 1,padx = 5)

wynik2 = StringVar()
wynik2.set("Wynik LOS")
label = ttk.Label(tab2, textvariable=wynik2).grid(column=1, row=3, pady = 30, padx = 10)

Jsyn = Button(tab2, text = 'Wyswietl LOS i Zapisz do JSON')
Jsyn.bind('<Button-1>',zapiszDoJSON_2)
Jsyn.grid(row = 4, column = 1)

root.mainloop()
