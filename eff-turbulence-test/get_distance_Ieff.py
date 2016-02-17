# 1) Get ambient turbulence, frequency data - read ambient_turbulence.csv file 
# 2) Get case data Iref, Vhub, Ct(Vhub),etc - read case.csv  
# 3) Compute effective ambient turbulence - Ieff_amb
# 4) Get difference: del_I = Iref-Ieff_amb 
# 5) Get equivalent 
import csv 

filename1 = 'ambient_turbulence.csv' 
filename2 = 'frequency.csv' 
filename3 = 'case.csv' 

V_hub=15.0 
Ct = 0.21
Iref = 18.0 
  
with open(filename1, 'rU') as fhandle:
	#next(fhandle) # skip this line 
	data = [[x for x in line.split(',')] for line in fhandle]   

	
	#coordinates = [[data[1+(i-1)*12][0],data[1+(i-1)*12][1]] for i range(len(data)/13)] 
coordinates = [[eval(data[(i)*13][0]),eval(data[(i-1)*13][1])] for i in xrange(len(data)/13)]
energy =  [eval(data[(i)*13][2]) for i in xrange(len(data)/13)] 
avg_ambient_turbulence = [eval(data[(i)*13][3]) for i in xrange(len(data)/13)] 
print "turbulence[0]: ",avg_ambient_turbulence[0] 
print "data[0]: ", data[0][3]
print "coordinates[0]: ", coordinates[0] 

sector_ambient_turbulence = [[eval(data[j][0]) for j in xrange(i+1,i+13)] for i in xrange(len(data)/13)] 
print len(sector_ambient_turbulence), len(sector_ambient_turbulence[0])  
print "", sum(sector_ambient_turbulence[0]) 


with open(filename2, 'rU') as fhandle:
	fr = [[x for x in line.split()] for line in fhandle]   

frequency = [[eval(fr[j][0]) for j in xrange(i,i+12)] for i in xrange(len(fr)/12)] 

print 'len(frequency)',len(frequency)  
print "Avg turbulence[0]", sum(sector_ambient_turbulence[0][j]* frequency[0][j] for j in xrange(len(frequency[0]))) 


Ieff_amb = [0]*len(frequency) 
# Compute effective ambient turbulence: 
del_I = [0]*len(frequency) 
counter = 0 
wake_i = [] 
wake_w = [] 

fout = open("turbulence_con.csv",'w')
destination = csv.writer(fout)
destination.writerow(['\tx\t','y\t','Ieff_amb\t','Iref-Iamb\t','Iwake\t','dist/RD\t'])
for i in xrange(len(frequency)):  
	for j in xrange(len(frequency[0])): 
		Ieff_amb[i] = Ieff_amb[i] + frequency[i][j]*((1.15*sector_ambient_turbulence[i][j]/100)**10)
		#Ieff_amb[i] = Ieff_amb[i] + (frequency[i][j]*1.15*sector_ambient_turbulence[i][j])
	Ieff_amb[i] = 100*(Ieff_amb[i]**(1./10))

	if Ieff_amb[i] < Iref: 
		#del_I[i] = (Iref - Ieff_amb[i])/100   
		del_I[i] = ((((Iref - Ieff_amb[i])/100)**10)/min(frequency[i]))**(1./10) # (18.0 - Ieff_amb[i])/100  
		wake_w.append(1/(1.5+(0.8*5/(Ct**0.5))))  
		wake_i.append( ((1/del_I[i]) - 1.5)*(Ct**0.5)/0.8 ) # del_I[i]*V_hub/100 
		destination.writerow([coordinates[i][0], coordinates[i][1], Ieff_amb[i], del_I[i], wake_w[counter], wake_i[counter]])	
		counter = counter + 1 

print "Counter: ", counter  
# Get difference: del_I 

 
