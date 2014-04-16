# Reads data files: dataFile and PCFile
# 'dataFile' is standardized and has fixed width/space for each number - see dataFile and readData()  
# Computes energy 

import sys
import time
from readFiles import *
from pyFunctions import *

dataFile = sys.argv[1]
PCFile = sys.argv[2]

# Read dataFile and PCFile
print "Time before reading dataFile"
print (time.strftime("%H:%M:%S"))
f,A,k,N = readData(dataFile)
print "Time after reading dataFile" 
print (time.strftime("%H:%M:%S")) 

print "Time before reading PCFile" 
print (time.strftime("%H:%M:%S")) 
PC = readPC(PCFile)
print "Time after reading PCFile" 
print (time.strftime("%H:%M:%S")) 

# Intiatialie parameters
Ns = 12 # 12 triplets of data in A, k, f 
Amin=4.0
Amax=25.0
recursion_depth=10
epsi = 0.0001 # tolerance level

AE=[]

outputFile='output.csv'
fout = open(outputFile,'w')
destination = csv.writer(fout)

print "Time before energy Computation" 
print (time.strftime("%H:%M:%S")) 
for i in xrange(N):
	AE.append(0)
	for j in xrange(Ns):
		AE[i]+=adaptive_simpsons_rule_2(PC,k[i][j],A[i][j],f[i][j],Amin,Amax,epsi,10)

	destination.writerow([AE[i]])

print "Time after energy computation" 
print (time.strftime("%H:%M:%S")) 
