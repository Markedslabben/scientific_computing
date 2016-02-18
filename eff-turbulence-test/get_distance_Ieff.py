# 1) Get ambient turbulence, frequency data - read ambient_turbulence.csv file 
# 2) Get case data Iref, Vhub, Ct(Vhub),etc - read case.csv  
# 3) Compute effective ambient turbulence - Ieff_amb
# 4) Get equivalent max/min wake, difference from Iref: del_I = Iref-Ieff_amb 
# 5) Get equivalent min/max distance to enable effective turbulence (with wake) to be limited to Iref.   

# Assumptions:
# 1) 12 sectors (constant) - used in file reading  
# 2) V_hub constant (15) - not used presently  
# 3) Ct, Thrust coefficient constant (0.21), - used in  
# 4) Iref, Acceptable turbulence 18%
# 5) m, Wohler coeffiecient, 10.0  

import csv 

filename1 = 'ambient_turbulence.csv' 
filename2 = 'frequency.csv' 
filename3 = 'case.csv' 

V_hub=15.0 
Ct = 0.21
Iref = 18.0 
m = 10.0 
 
# Read data from ambient turbulence file  
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

# Read data from frequency file 
with open(filename2, 'rU') as fhandle:
	fr = [[x for x in line.split()] for line in fhandle]   

frequency = [[eval(fr[j][0]) for j in xrange(i,i+12)] for i in xrange(len(fr)/12)] 

print 'len(frequency)',len(frequency)  
print "Avg turbulence[0]", sum(sector_ambient_turbulence[0][j]* frequency[0][j] for j in xrange(len(frequency[0]))) 


Ieff_amb = [0]*len(frequency) 
# Compute effective ambient turbulence: 
del_I_min = [0]*len(frequency) 
del_I_max = [0]*len(frequency) 
counter = 0 
wake_i_min = [] 
wake_i_max = [] 
wake_w = [] 

fout = open("turbulence_con.csv",'w')
destination = csv.writer(fout)
destination.writerow(['\tx\t','y\t', 'Ieff_amb\t', 'Iwake_comp_max\t', 'Iwake_formula\t', 'max dist/RD\t', 'min dist/RD\t', 'Iwake_comp_min\t'])
for i in xrange(len(frequency)):  
	#for j in xrange(len(frequency[0])): 
	temp = [frequency[i][j]*((1.15*sector_ambient_turbulence[i][j]/100)**m) for j in xrange(len(frequency[0]))]  
	fsum = sum(temp)  
	Ieff_amb[i] = fsum #Ieff_amb[i] + frequency[i][j]*((1.15*sector_ambient_turbulence[i][j]/100)**m)
		#Ieff_amb[i] = Ieff_amb[i] + (frequency[i][j]*1.15*sector_ambient_turbulence[i][j])
	Ieff_amb[i] = 100*(Ieff_amb[i]**(1./m))

	if Ieff_amb[i] < Iref: 
		#del_I[i] = (Iref - Ieff_amb[i])/100  
		k_min = temp.index(min(temp)) 
		k_max = temp.index(max(temp)) 
		p_k_min = frequency[i][k_min]
		p_k_max =  frequency[i][k_max]  
		if p_k_min <= 0.000: 
			#temp2 = temp[:]
			p_not_0 = [j for j,x in enumerate(temp) if x !=0 ] 
			temp2 = [temp[j] for j,x in enumerate(temp) if x !=0 ]
			k = p_not_0[temp2.index(min(temp2))]  
			#del temp2[k] 
			#k2 = temp2.index 
			p_k_min = frequency[i][k] 	
		Iam_k_min = sector_ambient_turbulence[i][k_min]/100 
		Iam_k_max = sector_ambient_turbulence[i][k_max]/100 


#		if (p_k < 0.0001): 
#			print 'i, k, p_k: ', i, k , p_k 
#			print 'frequency[i]: ', frequency[i]  
		del_I_max[i] = (fsum*(((Iref/Ieff_amb[i])**m)-1)/p_k_min) + (Iam_k_min**m) # ((((Iref - Ieff_amb[i])/100)**10)/min(frequency[i]))**(1./10) # (18.0 - Ieff_amb[i])/100  
		del_I_max[i] = ((del_I_max[i]**(2.0/m)) - Iam_k_min**2)**0.5  
		del_I_min[i] = (fsum*(((Iref/Ieff_amb[i])**m)-1)/p_k_max) + (Iam_k_max**m) # ((((Iref - Ieff_amb[i])/100)**10)/min(frequency[i]))**(1./10) # (18.0 - Ieff_amb[i])/100  
		del_I_min[i] = ((del_I_min[i]**(2.0/m)) - Iam_k_max**2)**0.5  

		wake_w.append(1/(1.5+(0.8*2.29/(Ct**0.5))))  
		wake_i_min.append( ((1/del_I_max[i]) - 1.5)*(Ct**0.5)/0.8 ) # del_I[i]*V_hub/100
 		wake_i_max.append( ((1/del_I_min[i]) - 1.5)*(Ct**0.5)/0.8 ) # del_I[i]*V_hub/100
		destination.writerow([coordinates[i][0], coordinates[i][1], Ieff_amb[i], del_I_max[i], wake_w[counter], wake_i_min[counter], wake_i_max[counter], del_I_min[i]])	
		counter = counter + 1 

print "Counter: ", counter  
# Get difference: del_I 

 
