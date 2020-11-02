# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 14:59:20 2018

@author: Cristian
"""
import argparse
import operator
################ '' is chosen to represent the set of all elements
def combination(d1, d2):   
    united=set(d2.keys()).union(set(d1.keys()))
    result=dict.fromkeys(united,0)#init an dictionary with union of keys from both sets 
                                #and init values with 0
    ## Combination
    for i in d1.keys():
        for j in d2.keys():
            if str(i)=='' and str(i) == str(j):#for intersection between '' ''
                result[i]+=d1[i]*d2[j]
            else:
                if str(i)=='':# for case '' 'char'
                    result[j]+=d1[i]*d2[j]
                if str(j)=='':# for case 'char' ''
                    result[i]+=d1[i]*d2[j]
                if str(j)!='' and str(i)!='':
                    st1 =set(str(i)).intersection(set(str(j)))#save intersection
                    for k in result.keys():
                        if (len(st1)!=0 and(st1==set(k))):#check if previous intersection is in dict keys
                            result[k]+=d1[i]*d2[j]#if yes, apply the formula
                            break
    ##Normalisation
    #Round for dict's values
    for i in result.keys():
        result[i] = round(result[i],4)
    #Round for sum of all values
    f= sum(list(result.values()))
    f=round(f,4)
    #divide and round
    for i in result.keys():
        result[i] =round(result[i]/f,4)
    return result

def get_mass(allLines):
    mass = {}
    previousLine = {}
    currentLine = {}
    previousLine = ast.literal_eval(allLines[0])
    for line in range(1,len(allLines)):
        currentLine = ast.literal_eval(allLines[line])
        mass = combination(previousLine,currentLine)
        previousLine=mass
    return mass.copy()

def get_beliefs(masses):
    belief = masses.copy()
    for i in belief.keys():
        for j in belief.keys():
            if(i!=j):
                if set(str(i)).issuperset(set(str(j))) and i!='' and j!='':#if i includes j, add mass of j to beliefs of i
                    belief[i]+=masses[j]
    for i in belief.keys():
        belief[i] = round(belief[i],4) #round with 4 digits
    return belief

def get_plausibility(masses):
    plausibility = masses.copy()
    
    for i in plausibility.keys():
        plausibility[i] = 0 #init elements with 0
    for i in plausibility.keys():
        for j in plausibility.keys():
            if len(set(str(i)).intersection(set(str(j))))!=0 and i!='':# if intersection of i and j is not None and i is not ''
                plausibility[i]+=masses[j];#add mass of j to plausibilities of i
            if j=='':
                plausibility[i]+=masses[j]#if j is '', add its mass to i
         
    for i in plausibility.keys():
        plausibility[i] = round(plausibility[i],4) #round 4 digits
    return plausibility

def filter_results(beliefs, plausibility):
    finalSet = {}
    #Filter elements with same values of beliefs and plausibility with supersets(superset.bel=this.bel, etc...)
    for elem in beliefs.keys():
        ssetFlag = False 
        for elemb in beliefs.keys():
            if elem!=elemb and set(elemb).issuperset(set(elem)) and beliefs[elem]==beliefs[elemb] and plausibility[elem]==plausibility[elemb]:
                ssetFlag = True
                break
        if ssetFlag == False and plausibility[elem]!=0.0:
            finalSet[elem] = beliefs[elem]
    return finalSet
	
def get_final_result(elements, plausibility):
    global decodings
    resultString = ''
    for elem in elements:
        setOfElems = set(elem[0])
        movieTypes = ''
        for letter in setOfElems:
            if decodings[letter]!=None:
                movieTypes += decodings[letter]+', '
        if elem[0] != '':
            resultString += movieTypes[:-2]+' ['+str(elem[1])+', '+str(plausibility[elem[0]])+']\n'
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
#war				r
#westerns			w

decodings = {'a':'action', 'v':'adventure', 'c':'comedy', 
             'g':'crime/gangster', 'd':'drama', 'e':'epics/historical',
             'h':'horror', 'm':'musicals/dance', 's':'science fiction',
             'r':'war', 'w':'westerns'}

parser = argparse.ArgumentParser()
parser.add_argument('--filename', type=str,
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
        mass = get_mass(lines)
        beliefs = get_beliefs(mass)
        plausibility = get_plausibility(mass)
        final_set = filter_results(beliefs, plausibility)
        #order elements
        all_elements=sorted(final_set.items(), key=operator.itemgetter(1),reverse=True)
        
        print("Intervals")
        print(get_final_result(all_elements, plausibility))
