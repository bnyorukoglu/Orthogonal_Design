from __future__ import print_function
listAllSeq=[]
def createMap(L):
    resultMap={}
    if(len(L)!=0):
        uniqueSet = list(set([ a if a[0]!="-" else a[1:] for a in flatten(L)]))
        #print(uniqueSet)
        i=0

        numberOfValues=[]
        while i < len(uniqueSet):
            index=0
            for tuples in L:#L is sequence of tuples L[[x_0, b, x_1], [x_2, -b, x_3]]
                for symbols in tuples:
                    if uniqueSet[i] in symbols:
                        index=index+1
            i=i+1;
            numberOfValues.append(index)
            resultMap[uniqueSet[i-1]]=index
    return resultMap



# S is a sequence, e.g., [a,b,a]
# k is the shift
def AF(S, k):
    return sum([ S[i]*S[i+k] for i in range(len(S)-k)])
    
# L is a list of sequences, e.g., [[a,b,a],[a,b,-a]]
# k is the shift
#autocorrelation function, multiply variable shifted by k 
def autocorrelation(L, k):
    return sum([ AF(S,k) for S in L])
 
# L=[["a","b","a"],["a","b","-a"]]
# V is ['a', 'b', 'a', 'a', 'b', 'a']
def flat(L):
    V = ([ a if a[0]!="-" else a[1:] for a in flatten(L)])
    return V
# L is a list of sequences, e.g., [["a","b","a"],["a","b","-a"]]
#s is the variable wanted to split. find the number of repeated
def findNewVariable(L,s):
    c = flatten(L).count(s)+flatten(L).count("-"+s)
    newList=["x_t"]+["x_"+str(i) for i in range(c)]
    return newList

#obtain new sequences, algebraic system that implemented
#createSystemForSplit([["a","b","a"],["a","-b","a"]],'a')
def createSystemForSplit(L,s):
    V = list(set([ a if a[0]!="-" else a[1:] for a in flatten(L)]))#["a","b"]
    
    c = flatten(L).count(s)+flatten(L).count("-"+s) #find the number of repeated
    # BR= Multivariate Polynomial Ring in a, b, x_t, x_0, x_1, x_2, x_3 over Rational Field
    BR = PolynomialRing(QQ,V + ["x_t"]+["x_"+str(i) for i in range(c)]) 
    
    #Multivariate Polynomial Ring in x_t, x_0, x_1, x_2, x_3 over Complex Field
    R = PolynomialRing(CC, ["x_t"]+["x_"+str(i) for i in range(c)])
    
    VX = {} 
    for i in ["x_t"]+["x_"+str(i) for i in range(c)]:
        VX[i]=BR.gens_dict()[i] # VX= {'x_t': x_t, 'x_2': x_2, 'x_3': x_3, 'x_0': x_0, 'x_1': x_1}

    VA = {} 
    for i in V:
        VA[i]=BR.gens_dict()[i] #VA={'a': a, 'b': b}
    
    #N=[[a, b, a], [a, -b, a]]
    N = [ [ VA[a] if a[0]!="-" else (-1)*VA[a[1:]] for a in S] for S in L]
    
    #L= L[[x_0, b, x_1], [x_2, -b, x_3]]
    i = 0
    L = []
    print("s"+str(s))
    for S in N:
        tmp =[ ]
        for a in S:
            if (a!=VA[s]) and a!=((-1)*VA[s]):
                tmp.append(a)
            else:
                tmp.append(VX["x_"+str(i)])
                i = i+1
        L.append(tmp)
    #AS=[b*x_0 + b*x_1 - b*x_2 - b*x_3, x_0*x_1 + x_2*x_3]
    AS = [ autocorrelation(L,i) for i in range(1,len(L[0]))]

    #BS=[x_0^4 - 1, x_1^4 - 1, x_2^4 - 1, x_3^4 - 1]
    BS = [ VX["x_"+str(i)]^4-1 for i in range(c)]

    #T1=x_t^2 - 3*x_t + 2
    T1 = prod([ VX["x_t"]-i for i in range(1,floor(c/2)+1)])

    #T2=x_0^2 + x_1^2 + x_2^2 + x_3^2 + 2*x_t - 4
    T2 = sum([ VX["x_"+str(i)]^2 for i in range(c)]) - c + 2* VX["x_t"]

    S = AS + BS + [T1,T2] 
    I = BR * S
    EI = I.elimination_ideal(VA.values())
    REI = R * EI.gens()
    sol_dict = REI.variety()

    return sol_dict,L,s,V,VA

#L seq of tuples
#s choice character
#S solution
#V unique char eq a,b
S,L,s,V,VA= createSystemForSplit([["a","b","a"],["a","-b","a"]],'a')
print("L"+str(L))
print("V"+str(V))

for s in S:
    print(s)

#listAllSeq=createNewTuples(S,L,'a',V)
def createNewTuples(S,L,choosen,V):
    changeList=[]
    Tuple=[]
    listAllSeq=[]
    flag=0
    
    for x in letter_range("a", "f"):
        flag=0
        for i in V:
            if(i!=x):
                flag=flag+1
        if(flag==len(V)):
            newSymbol=x
            break
    
    for s in S:#S is the solutions
        Tuple=[]
        for tuples in L:#L is sequence of tuples L[[x_0, b, x_1], [x_2, -b, x_3]]
            for symbols in tuples: 
                flag=0
                for variable in s:
                    if(variable==symbols):
                        flag=1
                        if(s[variable]==-1):
                            add='-'+newSymbol 
                            changeList.append(add)
                        elif(s[variable]==1):
                            add=newSymbol
                            changeList.append(add)
                        elif(s[variable]<-1):                       
                            add='-'+choosen
                            changeList.append(add)
                        else:
                            add=choosen
                            changeList.append(add)
                if(flag==0):
                    changeList.append(str(symbols))
                    flag=0
            Tuple.append(changeList)
            changeList=[]
        listAllSeq.append(Tuple)
        changeList=[]
    
    return listAllSeq
              

listAllSeq=[] #in listAllSeq tuple list for every solution
listAllSeq=createNewTuples(S,L,'a',V)
#print(listAllSeq)
print(*listAllSeq, sep="\n")
#in allSeq different tuples are kept
def findDifferentTuples(listAllSeq):
    allSeq=[]
    if(len(listAllSeq)!=0):
        allSeq.append(listAllSeq[0])

        for i in listAllSeq:
            sameElement=0
            for j in allSeq:
                if(j==i):
                    sameElement=sameElement+1
            if(sameElement==0):
                allSeq.append(i)
                
    return allSeq

print("-------------***************")
listAllDif=findDifferentTuples(listAllSeq)
print(*listAllDif, sep="\n")

resultMap={}
resultMap=createMap(listAllSeq[0])
#print(resultMap) #{'a': 2, 'c': 2, 'b': 2}
#print(resultMap.values())

#{(2, 2, 2): ([['a', 'b', 'a'], ['-c', '-b', '-c']]....
def createDictForTuples(resultMap,listAllDif):
    i=0
    returnMap={}
    returnMap[tuple(resultMap.values())]=tuple(listAllDif)
    return returnMap
#print(createDictForTuples(resultMap,listAllDif))

#gerekl
def createNewTuples(S,L,choosen,V):
    changeList=[]
    Tuple=[]
    listAllSeq=[]
    flag=0    
    for x in letter_range('a', 'z'):
        flag=0
        for i in V:
            if(i!=x):
                flag=flag+1
        if(flag==len(V)):
            newSymbol=x
            break    
    for s in S:#S is the solutions
        Tuple=[]
        for tuples in L:#L is sequence of tuples L[[x_0, b, x_1], [x_2, -b, x_3]]
            for symbols in tuples: 
                flag=0
                for variable in s:
                    if(variable==symbols):
                        flag=1
                        if(s[variable]==-1):
                            add='-'+newSymbol 
                            changeList.append(add)
                        elif(s[variable]==1):
                            add=newSymbol
                            changeList.append(add)
                        elif(s[variable]<-1):                       
                            add='-'+choosen
                            changeList.append(add)
                        else:
                            add=choosen
                            changeList.append(add)
                if(flag==0):
                    changeList.append(str(symbols))
                    flag=0
            Tuple.append(changeList)
            changeList=[]
        listAllSeq.append(Tuple)
        changeList=[]    
    return listAllSeq
              

listAllSeq=[]
listAllSeq=createNewTuples(S,L,'a',V)
#print(listAllSeq)
#print(*listAllSeq, sep="\n")




#gerekl
def findDifferentTuples(listAllSeq):
    allSeq=[]
    if(len(listAllSeq)!=0):
        allSeq.append(listAllSeq[0])

        for i in listAllSeq:
            sameElement=0
            for j in allSeq:
                if(j==i):
                    sameElement=sameElement+1
            if(sameElement==0):
                allSeq.append(i)
                
    return allSeq

print("-------------***************")
listAllDif=findDifferentTuples(listAllSeq)
#print(*listAllDif, sep="\n")

resultMap={}
resultMap=createMap(listAllSeq[0])
print(resultMap)
print(resultMap.values())
returnMap={}
def createDictForTuples(resultMap,listAllDif):
    i=0
    
    returnMap[tuple(resultMap.values())]=tuple(listAllDif)
    return returnMap
#print(createDictForTuples(resultMap,listAllDif))

createList=[]

for i in listAllDif:
    createList.append(i)
def recursiveOperation(listTuples,character):

    if (len(listTuples)==0):
        print("finished")
    else:
        print(listTuples[0])
        S,L,s,Vm,VA= createSystemForSplit(listTuples[0],character)
        listAllSeq=createNewTuples(S,L,character,Vm)
        listAllDif=findDifferentTuples(listAllSeq)
        if(len(listAllDif)!=0):
            resultMap={}
            resultMap=createMap(listAllSeq[0])
            createDictForTuples(resultMap,listAllDif)
        
        if(len(S)!=0):
            if(S[0].values()[0]!=0 and len(listTuples)!=0 and len(listAllDif)!=0):
                for i in listAllDif:
                    listTuples.append(i)
                    createList.append(i)
                    
        recursiveOperation(listTuples[1:],character)

            

def funcCallChar(V):
    for i in V:
        recursiveOperation(listAllDif,i)
        print("*******")


#for i in len(set(flattened_list))
#findCoordinate(i,character)
#i define list of tuple eg [['a', 'b', 'a'], ['-c', '-b', '-c']]

def findCoordinate(i,character):
    listTemp=[]
    for x in range (0,len(i)):
        for y in range(0,len(i[x])):
            if(i[x][y]==character):
                listTemp2=[]
                listTemp2.append(x)
                listTemp2.append(y)
                listTemp.append(listTemp2)    
    return listTemp

def findTarget(i,target):
    for x in range (0,len(i)):
        for y in range(0,len(i[x])):
            if(i[x][y]==target):
                return 1
    return 0

#this for loop convert ol list of tuples to dict 
#example={0: {'+': [[0, 0], [0, 2]], '-': []}, 1: {'+': [[0, 1]], '-': [[1, 1]]}, 2: {'+': [], '-': [[1, 0], [1, 2]]}}
def tuplesToDict(L):
    listAllCordinate=[]
    alltuples=[]
    flattened_list = [y for x in L for y in x]   
    flattened_list=set(flattened_list)
    flattened_list=list(flattened_list)

    counter=0
    characternumber_values={}
    for a in flattened_list:
        datas={}
       
        if(a[0]=='-'):
            if(findTarget(L,a[1])==0):
                datas['+']=findCoordinate(L,str("-"+a))    
                datas['-']=findCoordinate(L,a)
                characternumber_values[counter]=datas
                counter=counter+1
                alltuples.append(characternumber_values) 
        else:
                datas['+']=findCoordinate(L,a)    
                datas['-']=findCoordinate(L,str("-"+a))
                characternumber_values[counter]=datas
                counter=counter+1
                alltuples.append(characternumber_values)


    return alltuples[0]

print(tuplesToDict([['a', 'b', 'a'], ['-c', '-b', '-c']]))
new=[]        
#new=dictToList(alltuples)
#print(new)

#print(new[0])
#trying to find different tuples
listForInside=[]
#for i in alltuples:
#    print(i)
#    print(i.keys())
#    print(i.values())
#    for insideDictionary in (i.values()):
#        print(insideDictionary['+'])

##########################################

def findDifferentDict(alltuples):
    
    temp=[]
    temp2=[]
    temp3=[]
    temp4=[]
    diffTuples=[]
    sayac1=0
    sayac2=0
    if(len(alltuples)!=0):
        diffTuples.append(alltuples[0])

        for i in alltuples:
            sameElement=0
            for j in diffTuples:
                if(len(i.keys())==len(j.keys())):
                    for insideDictionary in (i.values()):
                        #print(insideDictionary['+'])
                        temp.append(insideDictionary['+'])
                        temp3.append(insideDictionary['-'])
                    for insideTuples in (j.values()):
                        #print(insideTuples['+'])
                        temp2.append(insideDictionary['+'])
                        temp4.append(insideDictionary['-'])
                    if(temp.sort() == temp2.sort()):
                        sayac1=1
                    if(temp3.sort() == temp4.sort()):
                        sayac2=1
                    if(sayac1==1 and sayac2 ==1):
                            sameElement=sameElement+1                                               

            if(sameElement==0):
                diffTuples.append(i)
            temp2=[]
            temp=[]
            temp3=[]
            temp4=[]
            sayac1=0
            sayac2=0
    return diffTuples


def dictToList(diffTuples):
    tempList=[]
    allList=[]
    for i in diffTuples:
        for insideDictionary in (i.values()):
            tempList.append(insideDictionary['+'])
            tempList.append(insideDictionary['-'])
        allList.append(tempList)
    return allList
#print(dictToList(diffTuples))
###########################################




#print(findCoordinate([['a', 'b', 'a'], ['-c', '-b', '-c']],'a'))
#print("Different tuples:")
#print(diffTuples)

#a= {0: {'+': [[0, 0], [0, 2]], '-': []}, 1: {'+': [[1, 0], [1, 2]], '-': []}, 2: {'+': [[0, 1]], '-': [[1, 1]]}}
a={0: {'+': [[0, 0], [0, 2],[1,2],[2,2]], '-': []}, 1: {'+': [[0, 1], [1, 1],[2,0],[2,1]], '-': []}, 2: {'+': [[1, 0]], '-': []}}
def dictToTuple(a):
    listt=[]
    for i in range(0,len(a)):
        for x in range(0,len(a[i].values())):
            listt.append(a[i].values()[x])
    n=0
    m=0
    for k in listt:
        for c in k:
            if(c[0]>n):
                n=c[0]
            if(c[1]>m):
                m=c[1]
    n=n+1
    m=m+1


    #print(listt)#[[[0, 0], [0, 2]], [], [[0, 1]], [[1, 1]], [], [[1, 0], [1, 2]]]

    dictToListTuple = [[0 for j in range(m)] for i in range(n)]

    newList=flatten(listt) #[0, 0, 0, 2, 0, 1, 1, 1, 1, 0, 1, 2]
    tempA=[]
    temp=[]
    for i in range(0,len(newList),2):
        first=newList[i]
        second=newList[i+1]
        temp.append(first)
        temp.append(second)
        tempA.append(temp)
        temp=[]

    tempC=tempA

    for i in range(0, len(a)):

        for x in range(0,len(a.values()[i]['+'])):
            coor1=tempC[x][0]
            coor2=tempC[x][1]
            dictToListTuple[coor1][coor2]=str(a.keys()[i])

        if(len(tempC)!=0): 
            for x in range(0,len(a.values()[i]['+'])):
                    del tempC[0]

        for x in range(0,len(a.values()[i]['-'])):
            coor1=tempC[x][0]
            coor2=tempC[x][1]
            dictToListTuple[coor1][coor2]='-'+str(a.keys()[i])

        if(len(tempC)!=0):     
            for x in range(0,len(a.values()[i]['-'])):
                    del tempC[0]
    return dictToListTuple

print(dictToTuple(a))


def tupleWithX(parameterTuple):
    newTuple=[]
    temp=[]
    for i in parameterTuple:
        temp=[]
        for a in i:
            if(a[0]=='-'):
                b='-'+'x'+a[1]
            else:
                b='x'+a
            temp.append(b)
        newTuple.append(temp)
    return newTuple

def tupleWithoutX(parameterTuple):
    newTuple=[]
    temp=[]
    for i in parameterTuple:
        temp=[]
        for a in i:
            if(a[0]=='-'):
                b='-'+a[2]
            else:
                b=a[1]
            temp.append(b)
        newTuple.append(temp)
    return newTuple
bas=flatten([['0', '2', '0'], ['1', '-2', '1']])
print(bas)
def findBiggestNumber(parameterTuple):
    if(parameterTuple[0]!='-'):
        maxa = parameterTuple[0]
    else:
        maxa = parameterTuple[1]
    for i in parameterTuple:
        for j in parameterTuple:
            if(parameterTuple[0]!='-'):
                if i > j and i > maxa:
                    maxa = i
    return maxa



def createNewTuples2(S,L,choosen,V,maxNumber):
    changeList=[]
    Tuple=[]
    
    choosen="x"+str(i)
    paramForNew=int(maxNumber)+1
    newSymbol=paramForNew

    for s in S:#S is the solutions
        Tuple=[]
        for tuples in L:#L is sequence of tuples L[[x_0, b, x_1], [x_2, -b, x_3]]
            for symbols in tuples: 
                flag=0
                for variable in s:
                    if(variable==symbols):
                        flag=1
                        if(s[variable]==-1):
                            add='-'+'x'+str(newSymbol) 
                            changeList.append(add)
                        elif(s[variable]==1):
                            add='x'+str(newSymbol)
                            changeList.append(add)
                        elif(s[variable]<-1): 
                            add='-'+'x'+str(newSymbol)
                            changeList.append(add)
                        else:
                            add=choosen
                            changeList.append(add)
                if(flag==0):
                    changeList.append(str(symbols))
                    flag=0
            Tuple.append(changeList)
            changeList=[]
        listAllSeq.append(Tuple)

        changeList=[]  
    listAllSeqWithoutX=[]
    print("listAllSeq"+str(listAllSeq))
    for y in listAllSeq:
        listAllSeqWithoutX.append(tupleWithoutX(y))
    return listAllSeqWithoutX

AllDifferentDict=[]#save all tuple while loop
a= {0: {'+': [[0, 0], [0, 2]], '-': []}, 1: {'+': [[1, 0], [1, 2]], '-': []}, 2: {'+': [[0, 1]], '-': [[1, 1]]}}
#a={0: {'+': [[0, 0], [0, 1],[0,2]], '-': []}, 1: {'+': [[1, 0], [1, 1],[1,2]], '-': []}, 2: {'+': [[2, 0], [2, 1],[2,2]], '-': []}}
#a={0: {'+': [[0, 0], [0, 2],[1,2],[2,2]], '-': []}, 1: {'+': [[0, 1], [1, 1],[2,0],[2,1]], '-': []}, 2: {'+': [[1, 0]], '-': []}}
#print("findKeys"+str(a.keys()))
for i in a.keys():
    #parameterTuple=[['x0', 'x2', 'x0'], ['x1', '-x2', 'x1']]
    S,L,s,V,VA= createSystemForSplit2(a,i)
    listAllSeq=[] #in listAllSeq tuple list for every solution
    maxNumber=a.keys()[0]

    for b in a.keys():
        if(maxNumber<b):
            maxNumber=b

    listAllWithoutX=createNewTuples2(S,L,i,V,maxNumber)#withx
    #print("listAllWithoutX="+str(listAllWithoutX))

    allDict=[]
    for y in listAllWithoutX:
        dicts=tuplesToDict(y)
        allDict.append(dicts)

    DifDicts=findDifferentDict(allDict)
    #print("DifDicts="+str(DifDicts))
    #print("AlllDicts=="+str(allDict))

    for y in DifDicts:
        AllDifferentDict.append(y)



#print("AllDifferentDict=="+str(AllDifferentDict))
convertTuple=[]
def recursive_Operation(AllDifferentDict,c):

    convertTuple2=[]
    if (len(AllDifferentDict)==0):
        print("finished")
        #print(*createList, sep="\n")
    else:
 
        S,L,s,V,VA= createSystemForSplit2(AllDifferentDict[0],c)
        listAllSeq=[] #in listAllSeq tuple list for every solution
        maxNumber=0
        for b in AllDifferentDict[0].keys():
            if(maxNumber<b):
                maxNumber=b

        listAllWithoutX=createNewTuples2(S,L,c,V,maxNumber)#withx
        for k in listAllWithoutX:
            listAllSeq.append(k)
        #print(listAllWithoutX)#[['0', '2', '-3'], ['1', '-2', '1']]
        allDict=[]
        for y in listAllSeq:
            dicts=tuplesToDict(y)
            allDict.append(dicts)
        
        DifDicts=findDifferentDict(allDict)
        forLoopDifDicts=DifDicts
        #print("DifDicts="+str(DifDicts))
        #print("AlllDicts=="+str(allDict))

        for y in DifDicts:
            convertTuple2.append(dictToTuple(y))
                    
        if(len(S)!=0):
            if(S[0].values()[0]!=0 and len(AllDifferentDict)!=0 and len(convertTuple2)!=0):
                for i in convertTuple2:
                    convertTuple.append(i)
                #n=[]    
                #for k in convertTuple:
                #    temp=tuplesToDict(k)
                #    n.append(temp)
                #for m in n:
                #    AllDifferentDict.append(m)
                #DifDicts=findDifferentDict(AllDifferentDict)
                #AllDifferentDict=DifDicts
        #for w in DifDicts:
        #    for y in w.keys():
        #        S,L,s,V,VA= createSystemForSplit2(w,y)
        #        listAllSeq=[] #in listAllSeq tuple list for every solution
        #        maxNumber=0
        #        for b in w.keys():
        #            if(maxNumber<b):
        #                maxNumber=b

        #       listAllWithoutX=createNewTuples2(S,L,y,V,maxNumber)#withx

                #print(listAllWithoutX)#[['0', '2', '-3'], ['1', '-2', '1']]
        #        allDict=[]
        #        for y in listAllWithoutX:
        #            dicts=tuplesToDict(y)
        #            allDict.append(dicts)
    
        #        DifDicts=findDifferentDict(allDict)
        #        for y in DifDicts:
        #            convertTuple2.append(dictToTuple(y))

        #        if(len(S)!=0):
        #            if(S[0].values()[0]!=0 and len(AllDifferentDict)!=0 and len(convertTuple2)!=0):
        #                for i in convertTuple2:
        #                    convertTuple.append(i)                

                    
        recursive_Operation(AllDifferentDict[1:],c)
#a= {0: {'+': [[0, 0], [0, 2]], '-': []}, 1: {'+': [[1, 0], [1, 2]], '-': []}, 2: {'+': [[0, 1]], '-': [[1, 1]]}}
a={0: {'+': [[1, 0], [1, 1]], '-': []}, 1: {'+': [[0, 0], [0, 1]], '-': []}, 2: {'+': [[2, 0], [2, 1]], '-': []}}
for b in a.keys():
    recursive_Operation(AllDifferentDict,b)
    print("*******")
print(convertTuple)
listAllSeq=[]
print("\n")
print("\n")
print("\n")
print("\n")
dictionaryToFile=[]
for t in convertTuple:
    temp=tuplesToDict(t)
    dictionaryToFile.append(temp)
print("Different dictionaries:  "+str(dictionaryToFile))