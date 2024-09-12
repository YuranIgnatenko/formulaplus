from tkinter import *
import random
import matplotlib.pyplot as plt
import numpy as np
import math

isHiddenFigure = False

def draw_plot(a1,a2,a3,a4,a5,a6,x):
    global figure, isHiddenFigure
    figure, axis = plt.subplots(2, 3)
    figure.set_size_inches((100,100))

    axis[0, 0].plot(x,a1)
    axis[0, 0].set_title("Q1")

    axis[0, 1].plot(x,a2)
    axis[0, 1].set_title("Q2")

    axis[0, 2].plot(x,a3)
    axis[0, 2].set_title("Qet")

    axis[1, 0].plot(x,a4)
    axis[1, 0].set_title("Q1 summa")

    axis[1, 1].plot(x,a5)
    axis[1, 1].set_title("Q2 summa")

    axis[1, 2].plot(x,a6)
    axis[1, 2].set_title("Qet summa")

    if isHiddenFigure == True:
        return
    else:
        plt.show()



def calculate():
    dt_Q1 = []
    dt_Q2 = []
    dt_Q1_summ = 0
    dt_Q2_summ = 0
    dt_Qet = 0

    fio = fio_entry.get()
    F = float(F_entry.get())
    K = float(K_entry.get())
    T0 = 1550
    epsilon_max = float(epsilon_max_entry.get())
    A = float(A_entry.get())
    delta = float(delta_entry.get())
    Qet = 2 * 4.85 * F * T0 / K

    U = 220 + random.uniform(-10, 10)
    I = 50 + random.uniform(-5, 5)
    
    Q1 = U * I
    Q2 = Q1 * delta
    x = random.uniform(0, 1)
    
    T_tor = T0 * (1 - 2.718281828**(-3 * x * Q2 / Qet))
    kt = 2 * 4.85 * F * T_tor * Q2
    L_os = epsilon_max / A * kt

    data=f"Qet: {Qet}\nQ1: {Q1}\nQ2: {Q2}\nT_tor: {T_tor}\nkt: {kt}\nL_os: {L_os}"
    output_label.delete(0.0,END)
    output_label.insert(0.0,data)

    a1,a2,a3,a4,a5,a6,b1 = calc_main(F,K,T0,delta)
    draw_plot(a1,a2,a3,a4,a5,a6,b1)


def calc_Q1():
    U = 220 + random.uniform(-10, 10)
    I = 50 + random.uniform(-5, 5)
    Q1 = U * I
    return Q1

def calc_Q2(delta,Q1=-1):
    if Q1==-1:
        U = 220 + random.uniform(-10, 10)
        I = 50 + random.uniform(-5, 5)
        Q1 = U * I
    Q2 = Q1 * delta
    return Q2

def calc_Qet(F,K,T0):
    Qet = 2 * 4.85 * F * T0 / K
    return Qet

def calc_main(F,K,T0,delta):
    sq1,sq2,sqet = 0,0,-1
    q1,q2,qet = calc_Q1(),calc_Q2(delta,-1),calc_Qet(F,K,T0)
    ayq1,ayq2,ayqet,aysq1,aysq2,aysqet,ax = [],[],[],[],[],[],[]
    
    # while sq2 != sqet:
    for i in range(150):
        q1 = calc_Q1()
        q2 = calc_Q2(delta,q1)
        qet = calc_Qet(F,K,T0)
        sq1 += q1
        sq2 += q2
        sqet += qet
        ayq1.append(q1)
        ayq2.append(q2)
        ayqet.append(qet)
        aysq1.append(sq1)
        aysq2.append(sq2)
        aysqet.append(sqet)
        ax.append(i)
    
    return ayq1,ayq2,ayqet,aysq1,aysq2,aysqet,ax

def save_data_figure():
    isHiddenFigure = True
    calculate()
    isHiddenFigure = False
    figure.savefig(fname_figure_entry.get())


def save_data_text():
    isHiddenFigure = True
    calculate()
    isHiddenFigure = False
    with open(fname_txt_entry.get(),"w") as file:
        file.write(output_label.get(0.0, END))


root = Tk()
root.title("Расчет параметров процесса сваривания")

fio_label = Label(root,text="Введите ФИО:")
fio_label.grid(row=0,column=0)
fio_entry = Entry(root, relief="solid")
fio_entry.grid(row=0,column=1)

F_label = Label(root,text="Сечение свариваемых труб (см2) (F):")
F_label.grid(row=1,column=0)
F_entry = Entry(root, relief="solid")
F_entry.grid(row=1,column=1)

K_label = Label(root, text="Градиент температурного поля (0.2÷0.7см2-1) (K):")
K_label.grid(row=2,column=0)
K_entry = Entry(root, relief="solid")
K_entry.grid(row=2,column=1)

epsilon_max_label = Label(root,text="Относительная максимальная деформация торцов εmax (0.45-0.65):")
epsilon_max_label.grid(row=3,column=0)
epsilon_max_entry = Entry(root, relief="solid")
epsilon_max_entry.grid(row=3,column=1)

A_label = Label(root,text="Коэффициент качества оплавляемой поверхности (1.2-1.4):")
A_label.grid(row=4,column=0)
A_entry = Entry(root, relief="solid")
A_entry.grid(row=4,column=1)

delta_label = Label(root,text="Коэффициент тепловой эффективности процесса оплавления (в %):")
delta_label.grid(row=5,column=0)
delta_entry = Entry(root, relief="solid")
delta_entry.grid(row=5,column=1)

fname_figure_label = Label(root,text="Название файла с графиком")
fname_figure_label.grid(row=6,column=0)
fname_figure_entry = Entry(root, relief="solid")
fname_figure_entry.grid(row=6,column=1)

fname_txt_label = Label(root,text="Название файла с расчетом")
fname_txt_label.grid(row=7,column=0)
fname_txt_entry = Entry(root, relief="solid")
fname_txt_entry.grid(row=7,column=1)

output_label = Text(root, relief="solid", width=60, height=8)
output_label.grid(row=8, column=0, columnspan=2)

calculate_button = Button(root, relief="solid", text="Рассчитать и построить график", command=calculate)
calculate_button.grid(row=9,columnspan=2,ipadx=100,ipady=5)
save_figure_button = Button(root, relief="solid", text="Сохранить График в файл", command=save_data_figure)
save_figure_button.grid(row=10,columnspan=2,ipadx=100,ipady=5)
save_text_button = Button(root, relief="solid", text="Сохранить Расчет в файл", command=save_data_text)
save_text_button.grid(row=11,columnspan=2,ipadx=100,ipady=5)


fio_entry.insert(0,"test")
F_entry.insert(0,"12")
K_entry.insert(0,"0.6")
epsilon_max_entry.insert(0,"0.6")
A_entry.insert(0,"1.3")
delta_entry.insert(0,"60")
fname_figure_entry.insert(0, "data_figure.png")
fname_txt_entry.insert(0, "data_math.txt")



root.mainloop()
