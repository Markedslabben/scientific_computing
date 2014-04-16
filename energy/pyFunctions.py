import csv
from math import exp as exp

#################### power_curve
def power_curve(table,v):
        #get the right i and i+1 values
        vmin=4
        vmax=25
        i1=0
        i2=1000
        if ((v<vmin) or (v>vmax)):
           return (0.0)

        for i in xrange(len(table[0])):
                if (v>table[0][i] and v>i1):
                        i1=i
                        i2=i+1

        value=table[1][i1] + (v-table[0][i1])*(table[1][i2]-table[1][i1])
        return value


#################### fff
def fff(table,k_cur,A_cur,f_cur,v):
        #print(v)
        #os.system("pause")
        return (((k_cur)/(A_cur))*pow(v/A_cur,k_cur-1)*exp(-pow(v/A_cur,k_cur))*power_curve(table,v)*f_cur)


#################### adaptiveSimpsonsAux 
def adaptiveSimpsonsAux(table, k_cur, A_cur, f_cur, a, b, epsilon, S, fa, fb, fc, bottom):
  c = (a + b)/2.0
  h = b - a
  d = (a + c)/2.0
  e = (c + b)/2.0
  fd = fff(table,k_cur,A_cur,f_cur,d)
  fe = fff(table,k_cur,A_cur,f_cur,e)
  Sleft = (h/12.0)*(fa + 4*fd + fc)
  Sright = (h/12.0)*(fc + 4*fe + fb)
  S2 = Sleft + Sright
  if (bottom <= 0 or abs(S2 - S) <= 15.0*epsilon):
    return S2 + (S2 - S)/15.0
  return (adaptiveSimpsonsAux(table,k_cur,A_cur,f_cur, a, c, epsilon/2.0, Sleft,  fa, fc, fd, bottom-1) + adaptiveSimpsonsAux(table,k_cur,A_cur,f_cur, c, b, epsilon/2.0, Sright, fc, fb, fe, bottom-1))


#################### adaptive_simpsons_rule_2
def adaptive_simpsons_rule_2(table, k_cur, A_cur, f_cur, a, b, epsilon, maxRecursionDepth):
  c = (a + b)/2.0
  h = b - a
  fa = fff(table,k_cur,A_cur,f_cur,a)
  fb = fff(table,k_cur,A_cur,f_cur,b)
  fc = fff(table,k_cur,A_cur,f_cur,c)
  S = (h/6.0)*(fa + 4*fc + fb)
  return adaptiveSimpsonsAux(table, k_cur, A_cur, f_cur, a, b, epsilon, S, fa, fb, fc, maxRecursionDepth)


