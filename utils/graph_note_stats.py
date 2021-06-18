from math import ceil
from numpy import std
from copy import deepcopy
from matplotlib import pyplot as plt

def stat(L):
    L.sort()
    aux = 0
    n = 0
    for i in L:
        aux += i
        n += 1
    q1 = L[ceil(n/4)]
    q2 = L[ceil(n/2)]
    q3 = L[ceil(3*n/4)]
    moy = aux/n
    return [q1,q2,q3,moy, std(L)]

def parsage(L): #round(0.5) = 0 Renvoie le nombre de note compris entre [i-0.5,i+0.5[ et le nombre de notes total
    R = [0 for i in range(21)]
    n = 0
    for i in L:
        n+=1
        R[round(i)] += 1
    return R,n

def autolabel(bar_plot, ax, bar_label): #fonction trouvée sur internet puis adaptée à notre besoin
    for idx,rect in enumerate(bar_plot):
        height = rect.get_height()
        if height != 0: #les condis sont inutiles (volontaire)
            if idx == 21:
                ax.text(rect.get_x() + 3*rect.get_width()/4., height,bar_label[idx],ha='center', va='bottom', rotation=0, fontsize=6)
            elif idx == 21:
                ax.text(rect.get_x() + rect.get_width()/4., height,bar_label[idx],ha='center', va='bottom', rotation=0, fontsize=6)
            else:
                ax.text(rect.get_x() + rect.get_width()/2., height,bar_label[idx],ha='center', va='bottom', rotation=0, fontsize=6)

def computeGraph(L, label_epreuve):
    S = stat(L)
    bar_x = [i for i in range(21)]
    aux = parsage(L)
    bar_label = aux[0]
    bar_tick_label = [i for i in range(21)]
    bar_height = deepcopy(aux[0])
    for i in range(len(bar_height)):
        bar_height[i] = bar_height[i]/aux[1]

    fig,ax = plt.subplots()
    ax.set_frame_on(False) # retire le cadre
    ax.yaxis.set_visible(False) # retire l'ordonnée

    plt.axhline(y=0, color = "black", linestyle = "-", zorder=4, linewidth=2) #axe abscisse foncé (au dessus des bar)

    plt.xlim(0,20)

    plt.axvline(x=S[0], color = "red", linestyle = "-", zorder=1, linewidth=1) #quartile 1
    plt.axvline(x=S[1], color = "red", linestyle = "-", zorder=1, linewidth=1) #quartile 2
    plt.axvline(x=S[2], color = "red", linestyle = "-", zorder=1, linewidth=1) #quartile 3
    plt.axvline(x=S[3], color = "blue", linestyle = "--",zorder=3, linewidth=1) #moyenne



    bar_plot = plt.bar(bar_x,bar_height,tick_label=bar_tick_label,width = 0.8, color = ['lightgrey' for i in bar_x], edgecolor = ['black' for i in bar_x], linewidth = 1, zorder=2)

    autolabel(bar_plot,ax, bar_label)

    plt.gca().xaxis.set_tick_params(labelsize = 8, color = "black") # règle la taille des caractère de l'abscisse
    ax.set_title(label_epreuve, loc='left',fontweight="bold", fontsize=10) #le titre

    plt.savefig('static/graphs/graphm_' + label_epreuve + '.png')

    return S
#Ecart_type non utilisé à ce jour
