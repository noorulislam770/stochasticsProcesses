from datetime import datetime
from textwrap import wrap
import tkinter as tk
from tkinter import ttk
from turtle import back, width
import PIL
from tkinter import *

from matplotlib.pyplot import margins, text, title
from numpy import double, mat
import pandas as pd
from markovchain import  MarkovChain
from PIL import ImageTk, Image
import numpy as np



def add_name(event):
    while True:
        
        name = entry.get()
        if name == "":
            break
        else:
            temp_label = tk.Label(window,font=("Times 12"), text=name)
            temp_label.pack()
            entry.delete(0,tk.END)


def extract_keys():
    keys = key_text.get(1.0,tk.END)
    # keys = "abcf"
    keys_list = keys.split(",")
    last_elem = keys_list.pop().split("\n")[0].strip("\t")
    keys_list.append(last_elem)
    # print(keys_list)

    matrix = matrix_text.get(1.0, tk.END)
    matrix_list = matrix.split("\n")
    matrix_list_new = []
    for row in matrix_list:
        if row != '':
            new_row = row.split(",")
            new_temp_row = []
            for item in new_row:
                num = double(item)
                new_temp_row.append(num)
            
        matrix_list_new.append(new_temp_row)

    matrix_list_new.pop()


    matrix_dictionary = dict(zip(keys_list,matrix_list_new))
    # print(matrix_dictionary)
    # print(matrix_list_new)
    # return matrix_dictionary
    markov_chain_sim(matrix_dictionary)

def simulate(markovchain):
    sim = []
    sim.append(markovchain.iloc[0].index[0])
    case = np.random.choice(markovchain.iloc[0].index,p=markovchain.iloc[0])
    sim.append(case)
    while len(sim) < 25:
        case = np.random.choice(markovchain.iloc[markovchain.index.get_loc(case)].index,p = markovchain.iloc[markovchain.index.get_loc(case)])
        sim.append(case)

    print("Simulation")
    print(sim)
    # return sim

    
    





def matrix_power(matrix,power):
    if power ==0:
        return np.identity(len(matrix))
    elif power ==1:
        return matrix
    else:
        return np.dot(matrix,matrix_power(matrix,power-1))


def steady_state_matrix(markovchain):
    global main_chunk
    main_chunk = []
    for i in range(1,10,1):
        # steady_statess_matrix_window 
        d = f'n step Transition Matrix at the nth power {i}\n', matrix_power(markovchain.to_numpy(),i),'\n'
        main_chunk.append(d)
        print(d)
    l2info = tk.Label(solution_frame,text="Steady State Matrix ",font=("Times 12"),pady=20)
    l2 = tk.Label(solution_frame,text=d,font=("Times 12"),pady=20)
    l2info.pack()
    l2.pack()
    btnshowfull = tk.Button(solution_frame,text="Show Full", command=show_full_steady)
    btnshowfull.pack()

def show_full_steady():
    new_win = Tk()
    new_win.geometry("500x400")
    new_win.title("Steady State Matrix")
    st_frame = tk.Frame(new_win)    
    l = tk.Label(st_frame,font=("Times 12"),text=main_chunk)
    l.pack()
    st_frame.pack()








def markov_chain_sim(matrix_dict):
    matrix = matrix_dict
    markov_chain = pd.DataFrame(data=matrix,index=matrix.keys())
    print(markov_chain)

    markov_chain_image  =  MarkovChain(markov_chain.to_numpy(), markov_chain.columns.tolist() )
    markov_chain_image.draw("markov_chain.png")

    image = Image.open('./markov_chain.png')
    # The (450, 350) is (height, width)
    image = image.resize((500, 500), Image.Resampling.LANCZOS)
    my_img = ImageTk.PhotoImage(image)
    # Slightly modified, this works for me
    my_lbl = Label(solution_frame,image = my_img)

    # simframe = tk.Frame(solution_frame)
    sim_label = tk.Label(solution_frame,font=("Times 12"),text=markov_chain)
    # close_btn = tk.Button(solution_frame,font=("Arial 14"),text="Close Sim", command=simframe.destroy)
    # sim_label.pack()
    # close_btn.pack()



    global simulation_amount
    sim_amount_label = tk.Label(solution_frame,font=("Times 12"),text="Enter Number Of simulations")
    simulation_amount = tk.Entry(solution_frame)
    temp_chain = markov_chain
    # my_lbl.pack()
    sim_btn = Button(solution_frame,text="Simulate")
    sim_btn.bind("<Button-1>",simulate(markovchain=temp_chain))

    sim_label.pack()
    sim_amount_label.pack()
    simulation_amount.pack()
    sim_btn.pack()

    # simulate(markov_chain)
    steady_state_matrix(markov_chain)


def get_matrix():
    # print(type(entry.get()))
    matrix_size = entry.get()
    if matrix_size == "" or matrix_size =="1":
        entry.insert(1.0,"Please Enter a Number greater than 1")
    else:

        global solution_frame
        solution_frame = tk.Frame(window)
        global key_text
        global matrix_text
        key_label = tk.Label(solution_frame,font=("Times 12"),text="Enter " + matrix_size + " keys seperated by ',' ")
        key_text = tk.Text(solution_frame,font=("Arial 16"), height=2, width=50)
        key_label.pack()
        key_text.pack()
        menu_frame.destroy()

        keys = key_text.get(1.0,tk.END)
        
        matrix_label = tk.Label(solution_frame,font=("Times 12"),text="Enter "+ matrix_size + "x" + matrix_size + " matrix seperated by ',' and new Line ")
        matrix_text = tk.Text(solution_frame,font=("Arial 16"), height=7, width=50)
        matrix_label.pack()
        matrix_text.pack()


        submit_keys_and_matrix = tk.Button(solution_frame,font=("Arial 14"),text="Submit Matrix & keys" ,command=extract_keys)
        # submit_keys_and_matrix.bind("<Button-1>",extract_keys(keys))
        new_question_btn = tk.Button(solution_frame,font=("Arial 14"),text="New Problem! ", command=new_question)
        submit_keys_and_matrix.pack()
        new_question_btn.pack()
        solution_frame.pack()

def new_question():
    solution_frame.destroy()
    show_menu()

window = tk.Tk()
window.geometry("800x800")
window.title("Markov Chains And Steady State Vector")

# win = tk.Frame(root)
# win.pack()

# window = tk.Canvas(win)
# window.pack(side = BOTTOM, fill=BOTH, expand=1)
heading = tk.Label(font= ("Times 16"), padx=20 , text="Markov Chain Solver")
heading.pack()


def show_menu():
    global menu_frame
    menu_frame = tk.Frame(window,background="orange",width=400,height=500)
    label = tk.Label(menu_frame,font=("Times 12"), text="Enter Number of States:")
    global entry 
    entry = tk.Entry(menu_frame,width=40,font=("Times 14"))
    button = tk.Button(menu_frame,font=("Arial 14"), text="Submit", command=get_matrix)
    # button.bind("<Button-1>", get_matrix)
    label.pack()
    entry.pack()
    button.pack()
    menu_frame.pack()


show_menu()
tk.mainloop()