import math
import matplotlib
matplotlib.use('Agg')   # Permet d'empêcher la génération d'exception "Runtime error : main thread is not in main loop" créée par le conflit Flask/matplotlib
import matplotlib.pyplot as plt
import os

def coord(r,teta): # retourne [x,y]
    return [r*math.cos(teta),r*math.sin(teta)]

def deg_to_rad(deg):
    return deg*math.pi/180

def divide_cercle(nombre_note):

    if nombre_note == 0:
        return None
    else:
        return math.pi*2/nombre_note

def points(L):

    X = []
    Y = []
    L_angle = []
    d_angle = divide_cercle(len(L))
    angle = 0
    for i in L:
        L_angle.append(angle)
        a = coord(i,angle)
        X.append(a[0])
        Y.append(a[1])
        angle += d_angle
    return [X,Y,L_angle]

# L = notes du candidat dans les matières
# L_note_moyenne = moyenne des candidats ayant passé cette matière
# L_nom_matiere = liste des matières passées par le candidat

def computeGraph(L,L_note_moyenne, L_nom_matiere):
    if os.path.exists("static/images/graph_notes.png"):
        os.remove("static/images/graph_notes.png")

    L_label_note = [L[i] + 0.5 for i in range(len(L))]
    L_note_max = [20 for i in range(len(L))]
    L_label_matiere = [21 for i in range(len(L))]
    L_label_moyenne = [L_note_moyenne[i] - 0.5 for i in range(len(L))]

    a = points(L)
    X = a[0]
    Y = a[1]
    X.append(X[0])
    Y.append(Y[0])

    a = points(L_note_moyenne)
    X_note_moyenne = a[0]
    Y_note_moyenne = a[1]
    X_note_moyenne.append(X_note_moyenne[0])
    Y_note_moyenne.append(Y_note_moyenne[0])

    fig, ax = plt.subplots()
    ax.yaxis.set_ticks(range(21))
    ax.yaxis.set_tick_params(labelsize = 8)

    ax.xaxis.set_visible(False) # retire valeur l'ordonnée
    ax.set_frame_on(False) #retire trait

    a = points(L_note_max)
    b = points(L_label_matiere)
    c = points(L_label_note)
    d = points(L_label_moyenne)

    for i in range(len(L)):
        plt.plot([0,a[0][i]],[0,a[1][i]], color = "yellow", linewidth = 0.5) # barre jaune

        if (b[2][i] < 0.01 and b[2][i] > -0.01) or  (b[2][i] < math.pi+0.01 and b[2][i] > math.pi - 0.01): #Label matiere
            plt.text(b[0][i],b[1][i],L_nom_matiere[i],verticalalignment = "center", fontweight="bold")
            plt.text(c[0][i],c[1][i],str(L[i]),verticalalignment = "center")
            plt.text(d[0][i],d[1][i],str(L_note_moyenne[i]),verticalalignment = "center", size = 8)
        elif (b[2][i] < math.pi/2 + 0.01 and b[2][i] > math.pi/2 - 0.01) or (b[2][i] < 3*math.pi/2 + 0.01 and b[2][i] > 3*math.pi/2 - 0.01):
            plt.text(b[0][i],b[1][i],L_nom_matiere[i],horizontalalignment = "center", fontweight="bold")
            plt.text(c[0][i],c[1][i],str(L[i]),horizontalalignment = "center")
            plt.text(d[0][i],d[1][i],str(L_note_moyenne[i]),horizontalalignment = "center", size = 8)
        elif b[2][i] > math.pi/2 and b[2][i] < 3*math.pi/2:
            plt.text(b[0][i],b[1][i],L_nom_matiere[i],horizontalalignment = "right", fontweight="bold")
            plt.text(c[0][i],c[1][i],str(L[i]),horizontalalignment = "right")
            plt.text(d[0][i],d[1][i],str(L_note_moyenne[i]),horizontalalignment = "right", size = 8)
        else:
            plt.text(b[0][i],b[1][i],L_nom_matiere[i],horizontalalignment = "left", fontweight="bold")
            plt.text(c[0][i],c[1][i],str(L[i]),horizontalalignment = "left")
            plt.text(d[0][i],d[1][i],str(L_note_moyenne[i]),horizontalalignment = "left", size = 8)

    c1 = plt.Circle((0, 0), 20, color = "darkgray")
    c2 = plt.Circle((0, 0), 10, color = "lightgrey")
    ax.set_aspect(1)
    ax.add_artist(c1)
    ax.add_artist(c2)

    ax.plot(X,Y,marker = ".", color = "black", linewidth = 0.5)
    ax.plot(X_note_moyenne,Y_note_moyenne,marker = ".", color = "red", linewidth = 0.5)

    ax.grid(False)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')

    plt.xlim(-20,20)
    plt.ylim(-20,20)

    plt.savefig('static/graphs/graph_notes.png')
