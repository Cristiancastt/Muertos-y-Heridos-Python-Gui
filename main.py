import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import os
import time
from tkinter import font

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("System")
# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")
app.title("Mastermind")
app.iconbitmap("icono.ico")
app.resizable(False,False)




patronDebug = '''
██████╗ ███████╗██████╗ ██╗   ██╗ ██████╗ ███╗   ███╗ ██████╗ ██████╗ ███████╗     ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝ ████╗ ████║██╔═══██╗██╔══██╗██╔════╝    ██╔═══██╗████╗  ██║
██║  ██║█████╗  ██████╔╝██║   ██║██║  ███╗██╔████╔██║██║   ██║██║  ██║█████╗      ██║   ██║██╔██╗ ██║
██║  ██║██╔══╝  ██╔══██╗██║   ██║██║   ██║██║╚██╔╝██║██║   ██║██║  ██║██╔══╝      ██║   ██║██║╚██╗██║
██████╔╝███████╗██████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗    ╚██████╔╝██║ ╚████║
╚═════╝ ╚══════╝╚═════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝     ╚═════╝ ╚═╝  ╚═══╝                                                                                           
'''
global debugMode
debugMode = False
global nombre



global numeroAdivinar
numeroAdivinar = 0


global intentos
intentos = 0  # Variable global
numerosIngresados = []


class Temporizador:
    def __init__(self):
        self.inicio = None
        self.tiempo_transcurrido = 0
        self.en_ejecucion = False

    def iniciar(self):
        if not self.en_ejecucion:
            self.inicio = time.time() - self.tiempo_transcurrido
            self.en_ejecucion = True
            if debugMode:
                print("Temporizador iniciado.")

    def detener(self):
        if self.en_ejecucion:
            self.tiempo_transcurrido = time.time() - self.inicio
            self.en_ejecucion = False
            if debugMode:
                print("Temporizador detenido.")


    def reiniciar(self):
        self.tiempo_transcurrido = 0
        self.iniciar()

    def obtener_tiempo_transcurrido(self):
        if self.en_ejecucion:
            return self.tiempo_transcurrido + (time.time() - self.inicio)
        else:
            return self.tiempo_transcurrido


def introducirNombre():
    global debugMode
    dialog = customtkinter.CTkInputDialog(text="Escribe tú nombre:", title="Nombre Jugador")
    global nombre
    nombre = dialog.get_input()
    if(nombre == "debugger"):
        debugMode=True
        print(patronDebug)
        print(f"El número es: {numeroAdivinar}")
    if nombre=="":
        messagebox.showinfo(
            message="Tienes que introducir algun nombre.", title="Error")
        menu()
        return False
    if nombre == None:
        menu()
        return False
    return True

def volver():
    respuesta = messagebox.askquestion(
        message=f"¿Deseas volver al menú?", title="Volver Menú")
    if respuesta == "yes":
        global intentos
        intentos = 0
        global numerosIngresados
        numerosIngresados.clear()
        temporizador.detener()
        ocultar_widgets(app)
        app.geometry("400x240")
        btnJugar.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)
        btnRanking.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        btnExit.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)
        temporizador.detener()
        


def guardarPartida():
    if nombre == "debugger":
        messagebox.showinfo(
            message="Número acertado en modo debugger, no se guardara en el ranking", title="Debugger")
        return
    temporizador.detener()
    
    respuesta = messagebox.askquestion(
        message=f"Adivinaste en {intentos} intentos!!\n ¿Deseas guardar la partida?", title="Adivinaste")
    if respuesta == "yes":
        if debugMode:
            print("Partida guardada.")
            # Nombre del archivo de texto
        archivo = "ranking.txt"
            # Comprobar si el archivo ya existe
        if not os.path.exists(archivo):
                # Si no existe, crear el archivo y escribir un número entero y una marca de tiempo
            with open(archivo, "w") as f:
                nomb = nombre
                numero = intentos
                tiempoPartida = round(
                    temporizador.obtener_tiempo_transcurrido(), 2)
                f.write(f"{nombre}*{numero}*{tiempoPartida}\n")

        else:
            with open(archivo, "a") as f:
                nomb = nombre
                numero = intentos
                tiempoPartida = round(
                    temporizador.obtener_tiempo_transcurrido(), 2)
                f.write(f"{nombre}*{numero}*{tiempoPartida}\n")
        temporizador.reiniciar()

        ocultar_widgets(app)
        app.geometry("400x240")
        btnJugar.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)
        btnRanking.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        btnExit.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)
    elif respuesta == "no":
        if debugMode:
            print("Partida no guardada")
        temporizador.detener()
        ocultar_widgets(app)
        app.geometry("400x240")
        btnJugar.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)
        btnRanking.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        btnExit.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)
    return



def ocultar_widgets(ventana):
    for widget in ventana.winfo_children():
        widget.place_forget()

def calcular_muertos_heridos(numero, numero_a_adivinar):
    muertos = 0
    heridos = 0
    for a, b in zip(numero, numero_a_adivinar):
        if a == b:
            muertos += 1
        elif a in numero_a_adivinar:
            heridos += 1
    return muertos, heridos

temporizador = Temporizador()

def tiene_digitos_repetidos(numero):
    digitos = str(numero)
    for i in range(len(digitos)):
        for j in range(i + 1, len(digitos)):
            if digitos[i] == digitos[j]:
                return True
    return False



listaNumeros = []
indiceHistorial = 0
def historialNumeros(event=None):
    global listaNumeros
    listaNumeros = []
    global indiceHistorial
    indiceHistorial = -1  # Inicializar el índice del historial


def menu():
        global intentos
        intentos = 0
        global numerosIngresados
        numerosIngresados.clear()
        temporizador.detener()
        ocultar_widgets(app)
        app.geometry("400x240")
        btnJugar.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)
        btnRanking.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        btnExit.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)
        temporizador.detener()

def comprobarNum(event=None):
    global listaNumeros
    global intentos  # Declarar intentos como global
    numero = entryNumero.get()
    global numerosIngresados

    if tiene_digitos_repetidos(numero):
        messagebox.showinfo(
            message="El número tiene algún dígito repetido", title="Error")
        entryNumero.delete(0, 'end')
        return

    if str(numero) == str(numeroAdivinar):
        if nombre == None:
            respuesta = messagebox.showinfo(message=f"Adivinaste en {intentos} intentos!!", title="Adivinaste")
            ocultar_widgets(app)
            app.geometry("400x240")
            btnJugar.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)
            btnRanking.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
            btnExit.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)
            return
        guardarPartida()

    if intentos >= 14:
        if nombre == None:
            respuesta = messagebox.showinfo(message=f"Llegaste al número máximo de intentos", title="Fin")
            ocultar_widgets(app)
            app.geometry("400x240")
            btnJugar.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)
            btnRanking.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
            btnExit.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)
            return
        messagebox.showinfo(
            message="Llegaste al número máximo de intentos", title="Fin")
        guardarPartida()

    # Validar que el número tenga 4 dígitos y sea numérico
    if len(numero) != 4:
        messagebox.showinfo(
            message="El número debe tener 4 dígitos.", title="Error")
        entryNumero.delete(0, 'end')
        return
    
    if not numero.isdigit():
        messagebox.showinfo(
            message="El número debe ser numérico.", title="Error")
        entryNumero.delete(0, 'end')
        return


    # Validar que el número no esté repetido
    if numero in numerosIngresados:
        messagebox.showinfo(
            message="El número ya ha sido ingresado", title="Error")
        entryNumero.delete(0, 'end')
        return
    intentos = intentos + 1
    muertos, heridos = calcular_muertos_heridos(numero, numeroAdivinar)
    numerosIngresados.append(numero)
    tabla.insert('', 'end', iid=intentos, values=(
        intentos, numero, muertos, heridos))
    listaNumeros.append(numero)
    entryNumero.delete(0, 'end')


def moverHistorial(event):
    global indiceHistorial
    if listaNumeros:
        if event.keysym == 'Up':
            indiceHistorial = (indiceHistorial + 1) % len(listaNumeros)
        elif event.keysym == 'Down':
            indiceHistorial = (indiceHistorial + 1) % len(listaNumeros)
        entryNumero.delete(0, 'end')
        entryNumero.insert(0, listaNumeros[indiceHistorial])

                    

if debugMode:
        print(patronDebug)
global entryNumero
def jugar():   
    if introducirNombre():
        global listaNumeros
        listaNumeros.clear()
        global numeroAdivinar
        
        # Generar un número aleatorio de 4 dígitos con ceros al principio
        digitos_disponibles = list(range(10))
        # Baraja la lista para que los dígitos estén en un orden aleatorio
        random.shuffle(digitos_disponibles)
        
        numeroAdivinar = ""
        for i in range(4):
            numeroAdivinar += str(digitos_disponibles[i])
        if debugMode:
            print(f"El número es: {numeroAdivinar}")
        global entryNumero
        entryNumero = customtkinter.CTkEntry(
        app, placeholder_text="Introduce un número", width=300, font=ctFontBtn)     
        
        for row in tabla.get_children():
            tabla.delete(row)
        global intentos
        intentos = 0
        global numerosIngresados
        numerosIngresados.clear()
        temporizador.iniciar()
        ocultar_widgets(app)
        app.geometry("900x640")
        entryNumero.place(relx=0.5, rely=0.15, anchor=customtkinter.CENTER)
        entryNumero.delete(0, 'end')
        btnIntroducirNum.place(relx=0.5, rely=0.21, anchor=customtkinter.CENTER)
        titlulo.place(relx=0.5, rely=0.08, anchor=customtkinter.CENTER)
        tabla.pack()
        tabla.place(relx=0.5, rely=0.60, anchor=customtkinter.CENTER)
        btnVolver.place(relx=0.1, rely=0.04, anchor=customtkinter.CENTER)
        entryNumero.bind("<Return>", comprobarNum)
        entryNumero.bind('<Up>', moverHistorial)
        entryNumero.bind('<Down>', moverHistorial)
        entryNumero.focus_set()
        entryNumero.delete(0, 'end')

    
    

def leer_ranking(nombre_archivo):
    ranking = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            datos = linea.strip().split('*')
            ranking.append(datos)
    return ranking

# Función para ordenar la lista por intentos y tiempos
def ordenar_ranking(ranking):
    ranking.sort(key=lambda x:(int(x[1]), float(x[2])))

def ranking():
    archivo_ranking = 'ranking.txt'
    try:
        open(archivo_ranking)
    except FileNotFoundError:
        messagebox.showinfo(
            message="El fichero ranking no existe, juega para crearlo", title="Error")
        return

    ocultar_widgets(app)
    
    ranking = leer_ranking(archivo_ranking)
    ordenar_ranking(ranking)
    app.geometry("700x400")
    tabla = ttk.Treeview(app, selectmode='browse', height=12)
    tabla["columns"] = ("1", "2", '3')
    tabla['show'] = 'headings'
    tabla.heading("1", text="Nombre")
    tabla.heading("2", text="Intentos")
    tabla.heading("3", text="Tiempo")
    for datos in ranking:
        tabla.insert("", "end", values=(datos[0], datos[1], f"{datos[2]} s"))
    tabla.pack()
    titluloRanking.place(relx=0.5, rely=0.10, anchor=customtkinter.CENTER)
    tabla.place(relx=0.5, rely=0.50, anchor=customtkinter.CENTER)
    btnVolver.place(relx=0.1, rely=0.04, anchor=customtkinter.CENTER)

def salir():
    app.destroy()
    exit

ctfont = customtkinter.CTkFont(family='Helvetica', size=30)
ctFontBtn = customtkinter.CTkFont(family='Helvetica', size=18)
titluloRanking = customtkinter.CTkLabel(
    app, text="RANKING", fg_color="transparent", font=ctfont)
btnVolver = customtkinter.CTkButton(
    master=app, text="Volver", command=volver, fg_color="red", hover_color="red4")
btnJugar = customtkinter.CTkButton(
    master=app, text="Jugar", command=jugar, font=ctFontBtn, fg_color="Green4", hover_color="Green")
btnRanking = customtkinter.CTkButton(
    master=app, text="Ranking", command=ranking, font=ctFontBtn)
btnExit = customtkinter.CTkButton(
    master=app, text="Salir", command=salir, font=ctFontBtn, fg_color="red", hover_color="red4")

titlulo = customtkinter.CTkLabel(
    app, text="MUERTOS Y HERIDOS", fg_color="transparent", font=ctfont)
btnIntroducirNum = customtkinter.CTkButton(
    master=app, text="Comprobar", command=comprobarNum, font=ctFontBtn)

style = ttk.Style()
tabla = ttk.Treeview(app, selectmode='browse', height=20)
tabla["columns"] = ("1", "2", "3", "4")
tabla['show'] = 'headings'
tabla.heading('1', text='Intento')
tabla.heading('2', text='Número')
tabla.heading('3', text='Muertos')
tabla.heading('4', text='Heridos')

btnJugar.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)
btnRanking.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
btnExit.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)

app.mainloop()