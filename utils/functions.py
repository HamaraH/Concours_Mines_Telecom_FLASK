
def appartient(L,x): #vérifie si x appartient à L
    for i in L:
        if i == x:
            return True
    return False

def add(val): # regarde si la case est vide, si oui remplace nan par None
    if str(val) == 'nan':
        return None
    else:
        return val

def bien_numerote(st): # prend en entrée un némro fixe et le renvoie avec la bonne ecriture ; FORMAT +33 (0)x xx xx xx xx
    if st == None:
        return None
    elif st[0] == '+':
        if st[4] == '(':
            return st
        else:
            return st[0:4]+'(0)'+st[4:]
    else:
        if st[2] == ' ':
            return '+33 ('+ st[0] +')'+st[1:]
        else:
            return '+33 (' + st[0] + ')' + st[1] + ' ' + st[2:4] + ' ' + st[4:6] + ' ' + st[6:8] + ' ' + st[8:10]

def retire_saut_de_ligne(st):
    if st[-1] == '\n':
        n = len(st)
        return st[:n-1]
    else:
        return st

def select_type_etab(nm):
    i = 0
    while nm[i] != ' ':
        i+=1
    return nm[:i]

def select_id_csv(val,i):
    i = i+1
    deb = 0
    fin = 0
    n = len(val)
    if i == 1:
        while val[fin] != ";":
            fin+=1
        return val[:fin]
    while i != 0:
        fin = fin + 1
        deb = fin
        while val[fin] != ";":
            fin+=1
            if fin == n:
                return val[deb:]
        i=i-1
    return val[deb:fin]
