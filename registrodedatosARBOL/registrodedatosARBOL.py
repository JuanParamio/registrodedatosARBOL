from tkinter import *
from tkinter import ttk
import sqlite3

#VARIABLES GENERALES
contador = 0
data = []
ventana = 1


conn = sqlite3.connect("mibasededatos.db")
c = conn.cursor()
c.execute("""CREATE TABLE if not exists primera (
    Apellido text,
    Nombre text,
    Asunto text
)""")
c.execute("""SELECT rowid, * FROM primera
            """)
data = c.fetchall()
conn.commit()
conn.close()






#VENTANA
root = Tk()
root.geometry("1280x620")
root.state('zoomed')
root.title("Registro de Entradas")
root.iconbitmap("icon_1.ico")

upw = Frame(root)
upw.pack(side = TOP, fill = "x")
upw.configure(bg="blue")

downw = Frame(root)
downw.pack(side = TOP, fill = "both", expand = "yes")

bottomw = Frame(root)
bottomw.pack(side = BOTTOM, fill = "x")
bottomw.configure(bg="blue")

#SCROLLBAR
scrollbary = Scrollbar(downw, orient=VERTICAL)
#FUNCIONES
def close_root(e):
   root.destroy()




def cargar():
    global contador
    global data
    contadorStr = str(contador)
    apellido = apellidoE.get()
    apellido = apellido[:35]
    nombre = nombreE.get()
    nombre = nombre[:35]
    asunto = asuntoE.get()
    asunto = asunto[:55]
    if apellido == "" or nombre == "" or asunto == "":
        consolaL.config(text ="COMPLETE TODOS LOS CAMPOS.")
        consolaL.configure(bg="red")
    else:
        def subirABase() :
            global contador
            contm1 = contador + 1
            conn = sqlite3.connect("mibasededatos.db")
            c = conn.cursor()
            c.execute("""INSERT INTO primera VALUES (:Apellido, :Nombre, :Asunto
            )""", {
                "Apellido" : apellido,
                "Nombre" : nombre,
                "Asunto" : asunto
                }
                )
            conn.commit()
            
            c.execute("""SELECT rowid, * FROM primera
            """)
            data = c.fetchall()
            conn.close()
            
        subirABase()
        refrescarArbol()
        refrescarContador()
        consolaCargando()

def cargarEnter(event):
    cargar()


def borrar():
   global contador
   if arbol.selection() :
       selected_item = arbol.selection()[0]
       id_fromselection = arbol.focus()
       id_fromselection = arbol.item(id_fromselection)["text"]
       id_fromselection = id_fromselection.replace("#","")
       print(id_fromselection)
       conn = sqlite3.connect("mibasededatos.db")
       c = conn.cursor()
       c.execute("""DELETE FROM primera WHERE ROWID = """ + id_fromselection + """
                """)
       conn.commit()
       conn.close()
       refrescarArbol()
       refrescarContador()
       consolaL.config(text="#" + id_fromselection + " Borrado")
       consolaL.configure(bg="green")
       arbolHeight = len(arbol.get_children())
       if (arbolHeight) == 0:
           consolaL.config(text="...")
           consolaL.configure(bg="grey")
           contador = 0
           idL.config(text="#" + str(contador + 1))
   else:
        consolaL.config(text="NO HAS SELECCIONADO UNA ENTRADA")
        consolaL.configure(bg="red")

def borrarKey(e):
    borrar()

def consolaCargando():
    truelast = arbol.get_children()[-1]
    arbolHeight = len(arbol.get_children())
    consolaL.config(text="#" + str(truelast) + " Cargado")
    consolaL.configure(bg="green")
    
def editar():
    arbolHeight = len(arbol.get_children())
    if (arbolHeight) >= 1 and arbol.focus():
        selected_item = arbol.selection()[0]
        takedid = arbol.focus()
        takedid = arbol.item(takedid)["text"]
        idc = takedid.replace("#","")
        print(idc + "jijiji")
        primervalor = arbol.focus()
        primervalor = arbol.item(primervalor)["values"][0]
        segundovalor = arbol.focus()
        segundovalor = arbol.item(segundovalor)["values"][1]
        tercervalor = arbol.focus()
        tercervalor = arbol.item(tercervalor)["values"][2]
        print(primervalor)
        consolaL.config(text=takedid + " Editando")
        consolaL.configure(bg="grey")
        secondw = Tk()
        secondw.geometry("1280x80")
        secondw.title("Editar Entrada " + takedid)
        secondw.iconbitmap("icon_1.ico")
        secondw.configure(bg="blue")
        idswl = Label(secondw, text=takedid)
        idswl.pack(side=LEFT,fill="x",expand="yes",padx=20)
        idswl.configure(bg="blue",fg="white")
        apellidoswl = Label(secondw, text="APELLIDO:")
        apellidoswl.pack(side=LEFT,fill="x",expand="yes",padx=20)
        apellidoswl.configure(bg="blue",fg="white")
        apellidoeswl = Entry(secondw)
        apellidoeswl.pack(side=LEFT,fill="x",expand="yes",padx=20)
        apellidoeswl.insert(0, primervalor)
        nombreswl = Label(secondw, text="NOMBRE:")
        nombreswl.pack(side=LEFT,fill="x",expand="yes",padx=20)
        nombreswl.configure(bg="blue",fg="white")
        nombreeswl = Entry(secondw)
        nombreeswl.pack(side=LEFT,fill="x",expand="yes",padx=20)
        nombreeswl.insert(0, segundovalor)
        asuntoswl = Label(secondw, text="ASUNTO:")
        asuntoswl.pack(side=LEFT,fill="x",expand="yes",padx=20)
        asuntoswl.configure(bg="blue",fg="white")
        asuntoeswl = Entry(secondw)
        asuntoeswl.pack(side=LEFT,fill="x",expand="yes",padx=20)
        asuntoeswl.insert(0, tercervalor)
        def editarConfirm() :
            conn = sqlite3.connect("mibasededatos.db")
            c = conn.cursor()
            c.execute("""UPDATE primera SET 
            Apellido = :Apellido,
            Nombre = :Nombre,
            Asunto = :Asunto

            WHERE ROWID=""" +idc+ """""", {
                "Apellido" : apellidoeswl.get(),
                "Nombre" : nombreeswl.get(),
                "Asunto" : asuntoeswl.get()
                }
                )
            conn.commit()
            conn.close()
            refrescarArbol()
            consolaL.config(text="#" + idc + " Editado")
            consolaL.configure(bg="green")
        editarConfirmB = Button(secondw, text = "Editar", command=editarConfirm)
        editarConfirmB.pack(side = LEFT, fill = "x", padx= 20, pady = 1)
        def close_second():
            secondw.destroy()
            consolaL.config(text="...")
            consolaL.configure(bg="grey")
        editarCancelB = Button(secondw, text = "Cancelar", command=close_second)
        editarCancelB.pack(side = LEFT, fill = "x", padx= 20, pady = 1)
    else:
        consolaL.config(text="NO HAS SELECCIONADO UNA ENTRADA")
        consolaL.configure(bg="red")

def buscar():
    arbolHeight = len(arbol.get_children())
    if arbolHeight > 0:
        elegirfila= arbol.get_children()[0]
        arbol.focus(elegirfila)
        arbol.selection_set(elegirfila)

    

#CONSOLA(PARTE AZUL)
idL = Label(upw, text = "#" + str(contador + 1))
idL.configure(bg="blue", fg= "white")
idL.pack(side = LEFT, fill = "x", padx= 20)
apellidoL = Label(upw, text= "APELLIDO:")
apellidoL.configure(bg="blue", fg= "white")
apellidoL.pack(side = LEFT, fill = "x", padx= 20)
apellidoE = Entry(upw)
apellidoE.pack(side = LEFT, fill = "x", expand="yes")
nombreL = Label(upw, text= "NOMBRE:")
nombreL.configure(bg="blue", fg= "white")
nombreL.pack(side = LEFT, fill = "x", padx= 20)
nombreE = Entry(upw)
nombreE.pack(side = LEFT, fill = "x", expand="yes")
asuntoL = Label(upw, text= "ASUNTO:")
asuntoL.configure(bg="blue", fg= "white")
asuntoL.pack(side = LEFT, fill = "x", padx= 20)
asuntoE = Entry(upw)
asuntoE.pack(side = LEFT, fill = "x", expand="yes")
cargarB = Button(upw, text = "Cargar", command=cargar)
cargarB.pack(side = LEFT, fill = "x", padx= 20, pady = 1)


#ARBOL(Treeview)
arbol = ttk.Treeview(downw)
scrollbary.pack(side=RIGHT, fill="y")
arbol.configure(yscrollcommand=scrollbary.set)
arbol.configure(selectmode="extended")
scrollbary.configure(command=arbol.yview)
arbol.pack(side = TOP, fill = "both", expand = "yes")
arbolStyle = ttk.Style(downw)
arbolStyle.theme_use("clam")
arbolStyle.configure("Treeview", background="black", fieldbackground="black", foreground="white", borderwidth=0)
arbol.configure(
    columns=(
        "Apellido",
        "Nombre",
        "Asunto"
        )
    )
arbol.heading("#0", text="ID", anchor=W)
arbol.heading("Apellido", text="Apellido", anchor=W)
arbol.heading("Nombre", text="Nombre", anchor=W)
arbol.heading("Asunto", text="Asunto", anchor=W)

arbol.column("#0", stretch=YES, width=125)
arbol.column("#1", stretch=YES, width=285)
arbol.column("#2", stretch=YES, width=285)
arbol.column("#3", stretch=YES, width=585)

def refrescarArbol() :
    global data
    conn = sqlite3.connect("mibasededatos.db") 
    c = conn.cursor()    
    c.execute("""SELECT rowid, * FROM primera
                """)
    data = c.fetchall()
    conn.commit()
    conn.close()
    print(data)
    
    arbol.delete(*arbol.get_children())

    for i in data:
        arbol.insert(parent="", index="end", text="#"+str(i[0]), iid=i[0], values=(i[1], i[2], i[3]))

def finalROW() :
    conn = sqlite3.connect("mibasededatos.db") 
    c = conn.cursor()    
    c.execute("""SELECT rowid, * FROM primera ORDER BY rowid DESC LIMIT 1
                """)
    lastRow = c.fetchall()
    lastRow = lastRow[0][0]
    print(lastRow)
    conn.commit()
    conn.close()

def refrescarContador() :
    if len(arbol.get_children()) >= 1:
        conn = sqlite3.connect("mibasededatos.db") 
        c = conn.cursor()    
        c.execute("""SELECT rowid, * FROM primera ORDER BY rowid DESC LIMIT 1
                    """)
        lastRow = c.fetchall()
        lastRow = lastRow[0][0]
        conn.commit()
        conn.close()
        idL.config(text="#"+str(lastRow+1))
    else:
        contador = 0
        idL.config(text="#" + str(contador + 1))
    
refrescarArbol()
refrescarContador()
consolaL = Label(bottomw, text= "...")
consolaL.pack(side=LEFT, fill="x", padx= 20)
consolaL.configure(bg="grey", fg= "white")
borrarB = ttk.Button(bottomw, text="Borrar", command=borrar)
borrarB.pack(side=RIGHT, fill="x", padx= 25, pady = 1)
editarB = ttk.Button(bottomw, text="Editar", command=editar)
editarB.pack(side=RIGHT, fill="x", padx= 25, pady = 1)
buscarB = ttk.Button(bottomw, text="Buscar", command=buscar)
buscarB.pack(side=RIGHT, fill="x", padx= 25, pady = 1)


if ventana == 1:
    root.bind('<Escape>', lambda e: close_root(e))
    root.bind('<Return>', cargarEnter)
    root.bind('<Delete>', lambda e: borrarKey(e))
    

root.mainloop()

