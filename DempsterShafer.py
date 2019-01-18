# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 14:59:20 2018

@author: Cristian
"""
import argparse
import operator
################ '' is chosen to represent the set of all elements
def Combinare(d1, d2):   
    united=set(d2.keys()).union(set(d1.keys()))
    result=dict.fromkeys(united,0)#initializam un dictionary cu uniunea de chei dintre 
                                #cele 2 multimi si initializam cu valorile 0
    ## Combinarea
    for i in d1.keys():
        for j in d2.keys():
            if str(i)=='' and str(i) == str(j):#pentru intersectie '' ''
                result[i]+=d1[i]*d2[j]
            else:
                if str(i)=='':# pentru caz '' 'char'
                    result[j]+=d1[i]*d2[j]
                if str(j)=='':# pentru caz 'char' ''
                    result[i]+=d1[i]*d2[j]
                if str(j)!='' and str(i)!='':
                    st1 =set(str(i)).intersection(set(str(j)))#retinem intersectia
                    for k in result.keys():
                        if (len(st1)!=0 and(st1==set(k))):#verificam daca intersectia precedenta se regaseste in cheile dictionar
                            result[k]+=d1[i]*d2[j]#daca da, atunci aplicam formula
                            break
    ##normalizare
    #aplicam round pt valorile vectorului
    for i in result.keys():
        result[i] = round(result[i],4)
    #aplicam round pt valoarea de la numitor( = suma valorilor din dictionar)
    f= sum(list(result.values()))
    f=round(f,4)
    #realizam impartirea si aplicam round
    for i in result.keys():
        result[i] =round(result[i]/f,4)
    return result

def getMass(allLines):
    mass = {}
    previousLine = {}
    currentLine = {}
    previousLine = ast.literal_eval(allLines[0])
    for line in range(1,len(allLines)):
        currentLine = ast.literal_eval(allLines[line])
        mass = Combinare(previousLine,currentLine)
        previousLine=mass
    return mass.copy()

def getBeliefs(masses):
    belief = masses.copy()
    for i in belief.keys():
        for j in belief.keys():
            if(i!=j):
                if set(str(i)).issuperset(set(str(j))) and i!='' and j!='':#daca i include j, adaugam la i masa lui j
                    belief[i]+=masses[j]
    for i in belief.keys():
        belief[i] = round(belief[i],4) #round cu 4 zecimale
    return belief

def getPlauzibilitati(masses):
    plauzibil = masses.copy()
    
    for i in plauzibil.keys():
        plauzibil[i] = 0 #initializam elementele cu 0
    for i in plauzibil.keys():
        for j in plauzibil.keys():
            if len(set(str(i)).intersection(set(str(j))))!=0 and i!='':#daca intersectia dintre i si j e diferit de multime vida si i!=''
                plauzibil[i]+=masses[j];#adauga la i masa lui j
            if j=='':
                plauzibil[i]+=masses[j]#daca j este '', adauga masa lui la i
         
    for i in plauzibil.keys():
        plauzibil[i] = round(plauzibil[i],4) #round 4 zecimale
    return plauzibil

def filterResults(beliefs, plauzibilities):
    finalSet = {}
    #Filtram elementele cu aceleasi valori de belief si plauzibilitate cu un superset
    for elem in beliefs.keys():
        ssetFlag = False 
        for elemb in beliefs.keys():
            if elem!=elemb and set(elemb).issuperset(set(elem)) and beliefs[elem]==beliefs[elemb] and plauzibilities[elem]==plauzibilities[elemb]:
                ssetFlag = True
                break
        if ssetFlag == False and plauzibil[elem]!=0.0:
            finalSet[elem] = belief[elem]
    return finalSet
	
def getFinalResult(elements):
    global decodings
    resultString = ''
    for elem in elements:
        setOfElems = set(elem[0])
        movieTypes = ''
        for letter in setOfElems:
            if decodings[letter]!=None:
                movieTypes += decodings[letter]+', '
        if elem[0] != '':
            resultString += movieTypes[:-2]+' ['+str(elem[1])+', '+str(plauzibil[elem[0]])+']\n'
    return resultString

    
##Genres
#action             a
#adventure          v
#comedy             c
#crime/gangster     g
#drama              d
#epics/historical   e
#horror             h
#musicals/dance     m
#science fiction    s
#war				     r
#westerns			  w

decodings = {'a':'action', 'v':'adventure', 'c':'comedy', 
             'g':'crime/gangster', 'd':'drama', 'e':'epics/historical',
             'h':'horror', 'm':'musicals/dance', 's':'science fiction',
             'r':'war', 'w':'westerns'}

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str,
                   help='Path to file with reviews including file name')
args = parser.parse_args()
print(str(args.filename))

pathToFile = args.filename
from pathlib import Path
import ast
mass={}
my_file = Path(pathToFile)
if my_file.is_file():
    with open(pathToFile) as f:
        lines = f.readlines()
    if len(lines)>1:
        mass = getMass(lines)
        belief = getBeliefs(mass)
        plauzibil = getPlauzibilitati(mass)
        finalSet = filterResults(belief, plauzibil)
        #ordonam elementele
        allElements=sorted(finalSet.items(), key=operator.itemgetter(1),reverse=True)
        
        print("Intervale")
        print(getFinalResult(allElements))
