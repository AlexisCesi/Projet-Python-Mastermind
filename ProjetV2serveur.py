# Créé par Alexis, le 06/03/2016 en Python 3.2

import socket, sys, threading, time
import random
from tkinter import *
from PIL import Image, ImageTk


#########################
########## Prof  ########
#########################


dict_joueurs = {}  # dictionnaire qui contiendra la liste des connexions eleves
dict_reponses = {}  # dictionnaire qui contiendra la liste des réponses des eleves

######################################################################################
################### Seules les lignes comportant des commentaires sont à comprendre
######################################################################################

class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        ref_socket[0] = conn
        self.connexion = conn

    def run(self):
        try:
            # en attente de réception
            message_recu = self.connexion.recv(4096)
            message_recu = message_recu.decode(encoding='UTF-8')
        except socket.error:
            pass

ref_socket={}

class ThreadClient(threading.Thread):
    '''dérivation de classe pour gérer la connexion avec un client'''

    def __init__(self,conn):

        threading.Thread.__init__(self)
        self.connexion = conn

        # Mémoriser la connexion dans le dictionnaire

        self.nom = self.getName() # identifiant du thread "<Thread-N>, sorte d'identifiant de l'ordinateur qui se connecte au serveur.
                                 #  Le professeur ne connaitra donc pas l'identité de l'élève
        dict_joueurs[self.nom] = self.connexion

        print("Connexion du client", self.connexion.getpeername(),self.nom ,self.connexion)

        message = bytes("Vous êtes connecté au serveur.\n","utf-8")
        self.connexion.send(message)


    def run(self):

        while 1:
            reponse = self.connexion.recv(4096)
            reponse = reponse.decode(encoding='UTF-8')
            print("Réponse du client",self.nom,">",reponse)
        print("\nFin du thread",self.nom)
        self.connexion.close()


def envoyer(message):
    """ message du serveur vers tous les clients"""
    for joueur in dict_joueurs:
        message=message.encode()
        dict_joueurs[joueur].send(message)

def recevoir():
    msg=ref_socket[0].recv(4096)
    msg=msg.decode()
    return msg



def connexion():


# Initialisation du serveur
# Mise en place du socket avec les protocoles IPv4 et TCP
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    try:
        mySocket.bind((HOST.get(), PORT.get()))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()
    print("Serveur prêt (port",PORT.get(),") en attente de clients...")
    mySocket.listen(5)



    while len(dict_joueurs)<1:  # tant que tous les élèves ne sont pas connectés, le serveur attend.

        # Attente connexion nouveau client
        try:
            connexion, adresse = mySocket.accept()
        except:
            sys.exit()
        th = ThreadClient(connexion)
        th.setDaemon(1)
        th.start()



# Fenetre d'acceuil

Fenetreacceuil = Tk()
Fenetreacceuil.title("Bienvenue dans la fenêtre d'acceuil du célèbre jeux : Mastermind")
Fenetreacceuil.geometry('1169x458')

################
 # Le cadre1
################

cadre=Frame(Fenetreacceuil, bd =4, relief =FLAT, bg= '#ADD8E6')
cadre.pack(padx=10,pady=10)


##############
# cadre 2
##############

cadre2 = Frame(Fenetreacceuil,borderwidth=1,relief=GROOVE, bg="#FFDAB9", bd=15)
cadre2.pack(padx=5,pady=5)

Label(cadre2, text = "Hôte", bg= '#FFDAB9',fg="darkcyan", font='Arial 12 bold').grid(row=0,column=0,padx=5,pady=5,sticky=W)
HOST = StringVar()
HOST.set("192.168.1.4")
Entry(cadre2, textvariable= HOST).grid(row=0,column=1,padx=5,pady=5)

Label(cadre2, text = "Port", bg="#FFDAB9",fg='darkcyan', font= "Arial 12 bold").grid(row=1,column=0,padx=5,pady=5,sticky=W)
PORT = IntVar()
PORT.set(50026)
Entry(cadre2, textvariable= PORT).grid(row=1,column=1,padx=5,pady=5)


bouton=Button(cadre2, text=" Ouvrir le serveur", command= connexion, bg='#DA70D6',fg='#4169E1', relief=FLAT, font = 'tahoma 13 bold')
bouton.grid(row=0,column=2,rowspan=2,padx=5,pady=5)


canvas = Canvas(Fenetreacceuil, width=658, height=1169)
canvas.pack(fill=BOTH, expand=1)
image = PhotoImage(file='PageMastermindRegle.gif')
canvas.create_image(0, 0, image=image, anchor=NW)

# Choix de la combinaison par l'ordinateur

s=random.randint(0,7)
p=random.randint(0,7)
q=random.randint(0,7)
r=random.randint(0,7)
while p==s:
    p=random.randint(0,7)
while q==p or q==s:
    q=random.randint(0,7)
while r==s or r==p or r==q:
    r=random.randint(0,7)
global s
global p
global q
global r



# La commande commencers

def commencer():
    global s
    global p
    global q
    global r
    envoyer(str(s)+str(p)+str(q)+str(r))
    Fenetreacceuil.destroy()
    print(s)
    print(p)
    print(q)
    print(r)

    Mafenetre = Tk()
    Mafenetre.title("Mastermind")
    Mafenetre.geometry("1300x830")

    imageplaine = PhotoImage(file='FondMastermind.gif')
    canvas = Canvas(Mafenetre, width=1300, height=830)
    canvas.pack(fill=BOTH, expand=1)
    canvas.create_image(0,0,image=imageplaine,anchor=NW)


    cadrejeux = Canvas(Mafenetre, width=315, height=501, bg='#f1f1f0')
    cadrejeux.place(x=480,y=130)




    # La commande quitter

    def quitter():
        Fenetrequitter = Tk()
        Fenetrequitter.title("Fermeture ...")
        Fenetrequitter.geometry("250x50")
        def quitter1():
            Mafenetre.destroy()
            Fenetrequitter.destroy()
        cadre3=Frame(Fenetrequitter, bd= 1, width= 100, height=150)
        cadre3.pack()
        text1=Label(cadre3,text="Êtes-vous sûr de vouloir quitter ?")
        text1.grid(row=0,column=0)
        BoutonFermer=Button (cadre3,text="Oui",command=quitter1)
        BoutonFermer.grid(row=1,column=0)
        BoutonFermer2=Button (cadre3,text="Non",command=Fenetrequitter.destroy)
        BoutonFermer2.grid(row=1,column=1)
        Fenetrequitter.mainloop()

    # Palette de couleur

    palette=["cyan","blue","yellow","pink","red","purple","green","#663301"]

    # Attribuer à n une couleur

    def choixcouleur0 ():
        global n
        n=0

    def choixcouleur1 ():
        global n
        n=1

    def choixcouleur2 ():
        global n
        n=2

    def choixcouleur3 ():
        global n
        n=3

    def choixcouleur4 ():
        global n
        n=4

    def choixcouleur5 ():
        global n
        n=5

    def choixcouleur6 ():
        global n
        n=6

    def choixcouleur7 ():
        global n
        n=7

    def aide ():
        Fenetreaide = Tk()
        Fenetreaide.title("Aide sur le Mastermind")
        Fenetreacceuil.geometry('1000x10')



    # Au début, la couleur des boutons est blanche


    couleur1='white'
    couleur2='white'
    couleur3='white'
    couleur4='white'
    global couleur1
    global couleur2
    global couleur3
    global couleur4

    # Commande pour mettre les boutons selectionnés en couleur

    def couleurpion1 ():
        couleurpion1.configure(bg=palette[n])
        couleur1=palette[n]
        global couleur1

    def couleurpion2 ():
        couleurpion2.configure(bg=palette[n])
        couleur2=palette[n]
        global couleur2

    def couleurpion3 ():
        couleurpion3.configure(bg=palette[n])
        couleur3=palette[n]
        global couleur3

    def couleurpion4 ():
        couleurpion4.configure(bg=palette[n])
        couleur4=palette[n]
        global couleur4


        # Les boutons à mettre en couleur

    couleurpion1=Button(cadrejeux, relief =GROOVE, command=couleurpion1,width=3,height=1,bg='white')
    couleurpion1.grid(row=0,column=0,padx=6,pady=6)

    couleurpion2=Button(cadrejeux, relief =GROOVE, command=couleurpion2,width=3,height=1,bg='white')
    couleurpion2.grid(row=0,column=1,padx=6,pady=6)

    couleurpion3=Button(cadrejeux, relief =GROOVE, command=couleurpion3,width=3,height=1,bg='white')
    couleurpion3.grid(row=0,column=2,padx=6,pady=6)

    couleurpion4=Button(cadrejeux, relief =GROOVE, command=couleurpion4,width=3,height=1,bg='white')
    couleurpion4.grid(row=0,column=3,padx=6,pady=6)

    # Score

    scorejoueur1=0
    scorejoueur2=0

    essai=1
    global essai

    # Commande valider

    def valider():
        testy=recevoir()
        testy=int(testy)
        print(testy)
        if testy==1:
            print("bravo")
        else:
            print("perdu")
        global s
        if s==0:
            s1='cyan'
        elif s==1:
            s1='blue'
        elif s==2:
            s1='yellow'
        elif s==3:
            s1='pink'
        elif s==4:
            s1='red'
        elif s==5:
            s1='purple'
        elif s==6:
            s1='green'
        else:
            s1="#663301"

        global p
        if p==0:
            p1='cyan'
        elif p==1:
            p1='blue'
        elif p==2:
            p1='yellow'
        elif p==3:
            p1='pink'
        elif p==4:
            p1='red'
        elif p==5:
            p1='purple'
        elif p==6:
            p1='green'
        else:
            p1="#663301"

        global q
        if q==0:
            q1='cyan'
        elif q==1:
            q1='blue'
        elif q==2:
            q1='yellow'
        elif q==3:
            q1='pink'
        elif q==4:
            q1='red'
        elif q==5:
            q1='purple'
        elif q==6:
            q1='green'
        else:
            q1="#663301"

        global r
        if r==0:
            r1='cyan'
        elif r==1:
            r1='blue'
        elif r==2:
            r1='yellow'
        elif r==3:
            r1='pink'
        elif r==4:
            r1='red'
        elif r==5:
            r1='purple'
        elif r==6:
            r1='green'
        else:
            r1="#663301"

        global s1
        global p1
        global q1
        global r1

        global essai

        while essai==12:
            pion48=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion48.grid(row=1,column=0,padx=6,pady=6)

            pion47=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion47.grid(row=1,column=1,padx=6,pady=6)

            pion46=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion46.grid(row=1,column=2,padx=6,pady=6)

            pion45=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion45.grid(row=1,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=1,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1



            couleurpion1.destroy()
            couleurpion2.destroy()
            couleurpion3.destroy()
            couleurpion4.destroy()

            essai=essai+1

        while essai==11:
            pion44=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion44.grid(row=2,column=0,padx=6,pady=6)

            pion43=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion43.grid(row=2,column=1,padx=6,pady=6)

            pion42=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion42.grid(row=2,column=2,padx=6,pady=6)

            pion41=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion41.grid(row=2,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=2,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1

        while essai==10:
            pion40=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion40.grid(row=3,column=0,padx=6,pady=6)

            pion39=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion39.grid(row=3,column=1,padx=6,pady=6)

            pion38=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion38.grid(row=3,column=2,padx=6,pady=6)

            pion37=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion37.grid(row=3,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=3,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1

        while essai==9:
            pion36=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion36.grid(row=4,column=0,padx=6,pady=6)

            pion35=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion35.grid(row=4,column=1,padx=6,pady=6)

            pion34=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion34.grid(row=4,column=2,padx=6,pady=6)

            pion33=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion33.grid(row=4,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=4,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1

        while essai==8:
            pion32=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion32.grid(row=5,column=0,padx=6,pady=6)

            pion31=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion31.grid(row=5,column=1,padx=6,pady=6)

            pion30=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion30.grid(row=5,column=2,padx=6,pady=6)

            pion29=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion29.grid(row=5,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=5,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1

        while essai==7:
            pion28=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion28.grid(row=6,column=0,padx=6,pady=6)

            pion27=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion27.grid(row=6,column=1,padx=6,pady=6)

            pion26=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion26.grid(row=6,column=2,padx=6,pady=6)

            pion25=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion25.grid(row=6,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=6,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1

        while essai==6:
            pion24=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion24.grid(row=7,column=0,padx=6,pady=6)

            pion23=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion23.grid(row=7,column=1,padx=6,pady=6)

            pion22=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion22.grid(row=7,column=2,padx=6,pady=6)

            pion21=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion21.grid(row=7,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=7,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1

        while essai==5:
            pion20=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion20.grid(row=8,column=0,padx=6,pady=6)

            pion19=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion19.grid(row=8,column=1,padx=6,pady=6)

            pion18=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion18.grid(row=8,column=2,padx=6,pady=6)

            pion17=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion17.grid(row=8,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=8,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1

        while essai==4:
            pion16=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion16.grid(row=9,column=0,padx=6,pady=6)

            pion15=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion15.grid(row=9,column=1,padx=6,pady=6)

            pion14=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion14.grid(row=9,column=2,padx=6,pady=6)

            pion13=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion13.grid(row=9,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=9,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1

        while essai==3:
            pion12=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion12.grid(row=10,column=0,padx=6,pady=6)

            pion11=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion11.grid(row=10,column=1,padx=6,pady=6)

            pion10=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion10.grid(row=10,column=2,padx=6,pady=6)

            pion9=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion9.grid(row=10,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=10,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1

        while essai==2:
            pion8=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion8.grid(row=11,column=0,padx=6,pady=6)

            pion7=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion7.grid(row=11,column=1,padx=6,pady=6)

            pion6=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion6.grid(row=11,column=2,padx=6,pady=6)

            pion5=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion5.grid(row=11,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=11,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1

        while essai==1:
            pion4=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur1)
            pion4.grid(row=12,column=0,padx=6,pady=6)

            pion3=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur2)
            pion3.grid(row=12,column=1,padx=6,pady=6)

            pion2=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur3)
            pion2.grid(row=12,column=2,padx=6,pady=6)

            pion1=Button(cadrejeux, relief =GROOVE,width=3,height=1,bg=couleur4)
            pion1.grid(row=12,column=3,padx=6,pady=6)

            cancercle = Canvas(cadrejeux, width=70, height=25,bg='#f1f1f0',border=0)
            cancercle.grid(row=12,column=4)

            nbrgreen=0
            nbrorange=0
            nbrred=0
            if couleur1==s1 :
                nbrgreen=nbrgreen+1
            elif couleur1==p1 or couleur1==q1 or couleur1==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur2==p1 :
                nbrgreen=nbrgreen+1
            elif couleur2==s1 or couleur2==q1 or couleur2==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur3==q1 :
                nbrgreen=nbrgreen+1
            elif couleur3==p1 or couleur3==s1 or couleur3==r1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1
            if couleur4==r1 :
                nbrgreen=nbrgreen+1
            elif couleur4==s1 or couleur4==q1 or couleur4==p1:
                nbrorange=nbrorange+1
            else:
                nbrred=nbrred+1

            if nbrgreen==0:
                if nbrorange==0:
                    cancercle.create_oval(3, 6, 17, 20, fill='red',outline='red')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==3:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(3, 6, 17, 20, fill='orange',outline='orange')
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==1:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(20, 6, 34, 20, fill='red',outline='red')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==2:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(20, 6, 34, 20, fill='orange',outline='orange')
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==2:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(37, 6, 51, 20, fill='red',outline='red')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                elif nbrorange==1:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(37, 6, 51, 20, fill='orange',outline='orange')
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            elif nbrgreen==3:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                if nbrorange==0:
                    cancercle.create_oval(54, 6, 68, 20, fill='red',outline='red')
                else:
                    cancercle.create_oval(54, 6, 68, 20, fill='orange',outline='orange')
            else:
                cancercle.create_oval(3, 6, 17, 20, fill='green',outline='green')
                cancercle.create_oval(20, 6, 34, 20, fill='green',outline='green')
                cancercle.create_oval(37, 6, 51, 20, fill='green',outline='green')
                cancercle.create_oval(54, 6, 68, 20, fill='green',outline='green')
                lacase1=Label(cadrejeux,width=4,height=2)
                lacase1.grid(row= 0, column=0)
                lacase2=Label(cadrejeux,width=4,height=2)
                lacase2.grid(row= 0, column=1)
                lacase3=Label(cadrejeux,width=4,height=2)
                lacase3.grid(row= 0, column=2)
                lacase4=Label(cadrejeux,width=4,height=2)
                lacase4.grid(row= 0, column=3)
                lacase1.configure(bg=palette[s])
                lacase2.configure(bg=palette[p])
                lacase3.configure(bg=palette[q])
                lacase4.configure(bg=palette[r])
                cadreresultat = Canvas(Mafenetre, width=200, height=50)
                cadreresultat.place(x=600,y=85)
                textresultat=Label(cadreresultat,text="Bravo ! Tu as réusis en "+str(essai)+" essais.")
                textresultat.pack()
                scorejoueur1=scorejoueur1+1
            couleurpion1.configure(bg='white')
            couleurpion2.configure(bg='white')
            couleurpion3.configure(bg='white')
            couleurpion4.configure(bg='white')

            essai=essai+1




    # Boutons valider et quitter


    imagevalider = PhotoImage(file='Valider.gif')
    boutonvalider = Button(canvas, image=imagevalider,border=0,width=115,height=54,command=valider)
    boutonvalider.place(x=510,y=650)

    imagequitter = PhotoImage(file='Quitter.gif')
    boutonquitter = Button(canvas, image=imagequitter,border=0,width=113,height=52,command=quitter)
    boutonquitter.place(x=675,y=654)



    # Les boutons en forme de pions

    imagepioncyan = PhotoImage(file='pioncyan.gif')
    button = Button(canvas, image=imagepioncyan,border=0,bg='#ff9b4c',width=52,height=30,command=choixcouleur0)
    button.place(x=935,y=470)

    imagepionbleu = PhotoImage(file='pionbleu.gif')
    button = Button(canvas, image=imagepionbleu,border=0,bg='#ff9b4c',width=52,height=30,command=choixcouleur1)
    button.place(x=1010,y=470)

    imagepionjaune = PhotoImage(file='pionjaune.gif')
    button = Button(canvas, image=imagepionjaune,border=0,bg='#ff9b4c',width=52,height=30,command=choixcouleur2)
    button.place(x=1080,y=490)

    imagepionrose = PhotoImage(file='pionrose.gif')
    button = Button(canvas, image=imagepionrose,border=0,bg='#ff9b4c',width=52,height=30,command=choixcouleur3)
    button.place(x=1080,y=540)

    imagepionrouge = PhotoImage(file='pionrouge.gif')
    button = Button(canvas, image=imagepionrouge,border=0,bg='#ff9b4c',width=52,height=30,command=choixcouleur4)
    button.place(x=1010,y=565)

    imagepionviolet = PhotoImage(file='pionviolet.gif')
    button = Button(canvas, image=imagepionviolet,border=0,bg='#ff9b4c',width=52,height=30,command=choixcouleur5)
    button.place(x=935,y=565)

    imagepionvert = PhotoImage(file='pionvert.gif')
    button = Button(canvas, image=imagepionvert,border=0,bg='#ff9b4c',width=52,height=30,command=choixcouleur6)
    button.place(x=870,y=540)

    imagepionmarron = PhotoImage(file='pionmarron.gif')
    button = Button(canvas, image=imagepionmarron,border=0,bg='#ff9b4c',width=52,height=30,command=choixcouleur7)
    button.place(x=870,y=490)

    # Bouton d'aide

    pioninterrogation = PhotoImage(file='boutonaide.gif')
    buttonpioninterrogation = Button(Mafenetre, image=pioninterrogation,border=0,bg='#f1f1f0',width=16,height=16,command=aide)
    buttonpioninterrogation.place(x=800,y=85)


    Mafenetre.mainloop()




# Bouton de la page d'acceuil

photo = PhotoImage(file='Boutoncommencerlapartie.gif')
button = Button(canvas, image=photo,command=commencer)
button.place(x=460,y=320)
button.config(bg='blue')

Fenetreacceuil.mainloop()




