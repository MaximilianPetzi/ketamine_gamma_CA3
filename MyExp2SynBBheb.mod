: check if g is supposed to be STATE or ASSIGNED
: $Id: MyExp2SynBB.mod,v 1.4 2010/12/13 21:27:51 samn Exp $ 
NEURON {
  POINT_PROCESS MyExp2SynBBheb
  RANGE tau1, tau2, e, i, g, Vwt, gmax, d, p, taud, taup, rec_k, rec_k1
  NONSPECIFIC_CURRENT i
}

UNITS {
  (nA) = (nanoamp)
  (mV) = (millivolt)
  (uS) = (microsiemens)
}

PARAMETER {
  tau1=.1 (ms) <1e-9,1e9>
  tau2 = 10 (ms) <1e-9,1e9>
  e=0	(mV)
  gmax = 1e9 (uS)
  Vwt   = 0 : weight for inputs coming in from vector

  d = 0.0053 <0,1>: depression factor
  p = 0.0096 <0, 1e9>: potentiation factor
  taud = 34 (ms) : depression effectiveness time constant
  taup = 16.8 (ms) : Bi & Poo (1998, 2001)
  rec_k=-1
  rec_k1=-1
}

ASSIGNED {
  v (mV)
  i (nA)
  g (uS)
  fact
  etime (ms)
  tpost (ms)
}

STATE {
  A (uS)
  B (uS)
}

INITIAL {
  LOCAL t_p :for double exp decay

  Vwt = 0    : testing

  if (tau1/tau2 > .9999) {
    tau1 = .9999*tau2
  }
  A = 0
  B = 0
  t_p = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
  fact = -exp(-t_p/tau1) + exp(-t_p/tau2)
  fact = 1/fact


  tpost = -1e9
  net_send(0, 1)
}

BREAKPOINT {
  SOLVE state METHOD cnexp
  g = B - A
  if (g>gmax) {g=gmax}: saturation
  i = g*(v - e)
}

DERIVATIVE state {
  A' = -A/tau1
  B' = -B/tau2
}

FUNCTION factor(Dt (ms)) { : Dt is interval between most recent presynaptic spike
    : and most recent postsynaptic spike
    : calculated as tpost - tpre (i.e. > 0 if pre happens before post)
  : the following rule is the one described by Bi & Poo
  if (Dt>0) {
    factor = 1 + p*exp(-Dt/taup) : potentiation
  } else if (Dt<0) {
    factor = 1 - d*exp(Dt/taud) : depression
  } else {
    factor = 1 : no change if pre and post are simultaneous
  }
}

NET_RECEIVE(w (uS), k, tpre (ms), countinputs) {
  
  INITIAL { k = 1  tpre = -1e9  countinputs=0}
  
  if (flag == 0) { : presynaptic spike (after last post so depress)
printf("Presyn spike--entry flag=%g t=%g w=%g k=%g tpre=%g tpost=%g\n", flag, t, w, k, tpre, tpost)
    
    A = A + w*fact
    B = B + w*fact   :for double exp rise and decay
    
    g = g + w*k
    tpre = t
    k = k * factor(tpost - t)
    rec_k=k
printf("  new k %g, tpre %g\n", k, tpre)
  }
  
  else if (flag == 2) { : postsynaptic spike (after last pre so potentiate)
printf("Postsyn spike--entry flag=%g t=%g tpost=%g\n", flag, t, tpost)
    
    tpost = t
    countinputs=0
    FOR_NETCONS(w1, k1, tp, countinputs) { : also can hide NET_RECEIVE args
printf("entry FOR_NETCONS w1=%g k1=%g tp=%g\n", w1, k1, tp)
      k1 = k1*factor(t - tp) :k1 is plasticity factor for the weight
      countinputs=countinputs+1
      if (countinputs>1){
        printf("MORE THAN ONE INPUT?? o_O")
      }
      rec_k1=k1
printf("  new k1 %g\n", k1)

    }
  }
  
   else { : flag == 1 from INITIAL block
printf("entry flag=%g t=%g\n", flag, t)
    WATCH (v > -20) 2
  }
}


