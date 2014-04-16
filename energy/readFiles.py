# Reads data files: dataFile and PCFile
# 'dataFile' is standardized and has fixed width/space for each number - see dataFile and readData()   

def split_by_length(s,block_size):
        w=[]
        n=len(s)
        alpha=0
        for i in block_size:
                w.append(s[alpha:alpha+i])
                alpha+=i
        return w


def readData(File):
	# Each line in the data file has 12 triplets (f, A and k) or (12*3) numbers
	# The width of each variable: f_i (4 spaces), A_i (4 spaces) and k_i (5 spaces) is standardized and fixed:  

	Ns=12 # 12 triplets of data#

        split_measure = []
        for i in xrange(Ns):
                split_measure.append(4)
                split_measure.append(4)
                split_measure.append(5)


        fs = []
        As = []
        ks = []

        i = 0  

        #Open the file source  
        source = open(File,'r')

        # Reads data as a string and then splits them
        for line in source:
                line.rstrip('\n\r')
                line_=split_by_length(line,split_measure)
		fs.append([])
		As.append([])
		ks.append([])
		i=i+1
                for j in xrange(Ns):
                        fs[i-1].append(eval(line_[j*3])/1000.0)
                        As[i-1].append(eval(line_[1+j*3])/10.0)
                        ks[i-1].append(eval(line_[2+j*3])/100.0)

	print line_
	print i
	print fs[1]
	print fs[-1]

	return fs,As,ks,i

def readPC(File):
# Opens file and reads data to a table (2D list)
	source = open(File,'r')
	PC=[]
	PC.append([])
	PC.append([])
	for line in source:
		line=line.rstrip('\r\n').split()
		PC[0].append(eval(line[0]))
		PC[1].append(eval(line[1]))
	source.close()
	return PC



#import sys
#
#dataFile = sys.argv[1]
#PCFile = sys.argv[2]
#A,k,f,N = readData(dataFile)
#PC = readPC(PCFile)
#

