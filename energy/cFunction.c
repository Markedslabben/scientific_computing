double PowerCurve(  double v,           // Scalar value
                    double * table){    // table

    int     i1,i2;
    int i;

    if ((v<table[0]) || (v>table[PowerCurveTable_rows-1])) mexErrMsgTxt("v is outside of interval");

    if((v<vmin)||(v>vmax)) return(0);

    i1=0;
    i2=1000;

    // Get 2 closest indexes; i1,i2.
    for(i=0;i<PowerCurveTable_rows;i++)
        if(v>table[i] && v>i1){ i1=i; i2=i+1;};

    return(table[i1+PowerCurveTable_rows]+((table[i2+PowerCurveTable_rows]-table[i1+PowerCurveTable_rows])*(v-table[i1])));
    }

// fff function
//
//
double fff(     double v){       

    return((((k_cur)/(A_cur))*pow((v/(A_cur)),k_cur-1)*exp(-pow((v/A_cur),k_cur))*PowerCurve(v,PowerCurveTable)*f_cur));
    }


// -----------------------------------------------------------------------
// Adaptive Simpson's Rule
//
double adaptiveSimpsonsAux(double (*f)(double), double a, double b, double epsilon,
                         double S, double fa, double fb, double fc, int bottom) {
  double c = (a + b)/2, h = b - a;
  double d = (a + c)/2, e = (c + b)/2;
  double fd = f(d), fe = f(e);
  double Sleft = (h/12)*(fa + 4*fd + fc);
  double Sright = (h/12)*(fc + 4*fe + fb);
  double S2 = Sleft + Sright;
  if (bottom <= 0 || fabs(S2 - S) <= 15*epsilon)
    return S2 + (S2 - S)/15;
  return adaptiveSimpsonsAux(f, a, c, epsilon/2, Sleft,  fa, fc, fd, bottom-1) +
         adaptiveSimpsonsAux(f, c, b, epsilon/2, Sright, fc, fb, fe, bottom-1);
}
double adaptiveSimpsons(double (*f)(double),        // ptr to function
                           double a, double b,      // interval [a,b]
                           double epsilon,          // error tolerance
                           int maxRecursionDepth) { // recursion cap
  double c = (a + b)/2, h = b - a;
  double fa = f(a), fb = f(b), fc = f(c);
  double S = (h/6)*(fa + 4*fc + fb);
  return adaptiveSimpsonsAux(f, a, b, epsilon, S, fa, fb, fc, maxRecursionDepth);
}
// ---------------------------------------------------------------------------

