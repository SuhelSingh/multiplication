# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 22:40:37 2016

@author: SuhelSingh
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 13:05:42 2016

@author: SuhelSingh
"""

# -*- coding: utf-8 -*-

######### Multiplication Machine #########
######### Suhel Singh ######################


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import os.path


############################## Initialize Values ################################
#numberlist = dict()
#problist = dict()
#history = [] #triple of (multiplication combo, time, corrent/incorrect )
#place = 0 


############################## Define global functions ################################
def initialize(l1 = 10, h1 = 99, l2 = 1, h2 = 10):
    global numberlist, problist, place, history, data, exerciseNum
    numberlist = dict()
    problist = dict()    
    #create probability and numberlist
    for r in range(l1,h1):
        for c in range(l2,h2):
            numberlist[ str(r) + ", " + str(c) ] = (r,c)
            problist[ str(r) + ", " + str(c) ] = 100.0
    history = [] #triple of (multiplication combo, time, answer )
    data = pd.DataFrame() ## Dataframe to record and keep track of problems so we can collect data
    place = 0 ## Used with the variable History to track which index was last used before an exercize
    exerciseNum = 0 ## To keep track of how many exercises the user has completed
    normalize()
    

def clearScreen():
    print "\n"*45

def normalize():
    global problist    
    s = sum( problist.values() )   
    problist = { p:q/s for p,q in problist.iteritems() }




############################## Penalty algorithm ################################

def selectNumbers():
    ### Randomly choose multiplication combination
    np.random.seed( int( time.time() % 1000 ) )
    i = np.random.choice( len(numberlist.values() ) , 1, p= list(problist.values()))
    a,b = numberlist.values()[i]
    return (a,b)
    
def selectRandomNumers(length1 = 2, length2= 2):    
    return ( int(np.random.rand()*10**7) % 10**length1) , int((np.random.rand()*10**7) % 10**length2 )



def prompt(combination ):
    global place    
    #### Prompt for answer and recored time
    a,b = combination    
    start_time = time.time()
    answer = input(str(a) + " x " + str(b) + " = ")
    if not ( isinstance(answer, int) | isinstance(answer, float) ) :
        prompt(combination)
    time_ = time.time() - start_time
    history.append(  {'n1':  a, 'n2': b,'answer': answer,'time': time_ }  )
    
    
    
    ###### Penalties for getting something wrong
    ##### Penalties for getting something slowly


##### UNEDITED
def initialResponse( ):  
    global problist, history
    index = len(history)-1
    a = history[index]['n1'] ## input valules for 1) multiplicaiton numbers 
    b = history[index]['n2']
    time = history[index]['time'] ## 2) time it took to answers
    correct = history[index]['answer']==a*b ## 3) whether the answer was correct

    if not correct:
        problist[str(a) + ", " + str(b) ] = problist[ str(a) + ", " + str(b) ] + 0.2
        normalize()
        print "Wrong"
        #print "Time: " + str(time)
        #print "Probability: " + str( problist[str(a) + ", " + str(b) ] )
        print "The right answer is " + str(a*b)
    else :
        problist[ str(a) + ", " + str(b) ] = problist[ str(a) + ", " + str(b) ]/1.5
        normalize()
        print "Correct"
        #print "Time: " + str(time)
        #print "Probability: " + str(problist[str(a) + ", " + str(b) ] )


##### UNEDITED
def summarizeStats():
    clearScreen()
    plt.hist( [x[1] for x in history[place:] ] )
    plt.title('Time Histogram')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency (%)')
    print "Accuracy: " + str( 1.0*sum( [x[2] for x in history[place:] ])/(len(history[place:])) )
    print """Right: {}   Wrong: {} """.format( str( sum( [x[2] for x in history[place:] ])) , 
                                                str(  len(history[place:]) - sum( [x[2] for x in history[place:] ]) )   )   
    print "Average Time: " + str( np.mean( [x[1] for x in history[place:]]   ) )           
    

############################## Driver ################################

##### Ongoing loop ######
def practice():    
    global initialtime, place    
    navigate = ""
    place = len(history)
    while navigate != "stop":
        clearScreen()

        prompt(selectNumbers()  ) #Finds numbers, 
        initialResponse() #updaes probabilities & responds to answer
        
        string = raw_input("continue?")
        if string != "":
            exerciseData(history[place:])
            navigate = "stop"
    #summarizeStats()
        
        
def timedTest(limit = 30):
    global initialtime, place
    initialTime = time.time()
    place = len(history)
    while  time.time() - initialTime <= limit:
        prompt(selectNumbers()  ) #Finds numbers, 
        initialResponse() #updaes probabilities & responds to answer
    #summarizeStats()                           #stores statistics

def numberTest(n = 20):
    global initialtime, place
    place = len(history)
    for i in range(n):
        prompt(selectNumbers()  ) #Finds numbers, 
        initialResponse() #updaes probabilities & responds to answer
    #summarizeStats()                           #stores statistics


#########  
#timedTest()
#practice()
  
############################## After Running the App ################################

### Given a pair of numbers, this will tell you which single digit
### multiplication and addition problems are involved in this problem
def numbersInvolved( combination ):
    p,q = combination
    plist = [int(x) for x in str(p) ]
    qlist = [int(x) for x in str(q) ]
    mlist= []
    alist = []
    #Multiplication problems
    for i in range(len(plist)):
        for j in range(len(qlist)):
            mlist.append( (plist[i], qlist[j]) )
    #Addition Problems
    for i in range(len(plist)):
        for j in range(len(qlist)):
            alist.append( plist[i]* 10**(len(plist)-i-1)*qlist[j]*10**(len(qlist)-j-1) ) 
    #print
    return (mlist, alist)
  
  
  
  

def dropVariables():
    global history, numberlist, place, problist
    del history, numberlist, place, problist


############################## Modifying and Storing Data ################################

def exerciseData( list1 ):
    global exerciseNum, data 
    if not isinstance(list1, list) :
        print 'error'
        return
    exerciseData = pd.DataFrame(list1)
    exerciseData['Exercise ID'] = exerciseNum
    exerciseNum = exerciseNum + 1
    if len(data) == 0:
        data = exerciseData
    else:
        data = data.append(exerciseData).reset_index().drop('index', axis = 1, inplace=False)

def exportSessionToNewFile(name = "storage"):
    data['sessionID'] = 0
    pd.DataFrame(data).to_csv(name)          
    initialize()
            
def exportSessionToExistingFile(name = "storage"):
    storedData = pd.read_csv('storage')
    data['session'] = max(storedData['sessionID'])
    storedData.append(data).reset_index().drop('index', axis = 1, inplace=False)
    data.to_csv('storage', mode='a', header=False) 
    initialize()
    
def exportData(name = 'storage'):
    if os.path.exists(name):
        exportSessionToExistingFile(name)
        print 'exported to new file: ' + name 
    else :
        exportSessionToNewFile(name)
        print 'exported to existing file: ' + name
        
#pd.DataFrame(history).to_csv("mstore1")

