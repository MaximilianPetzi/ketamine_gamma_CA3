: check if g is supposed to be STATE or ASSIGNED
: $Id: MyExp2SynBB.mod,v 1.4 2010/12/13 21:27:51 samn Exp $ 
NEURON {
  POINT_PROCESS MyExp2SynBB_LTPb
  RANGE tau1, tau2, e, i, g, Vwt, gmax, d, p, taud, taup, rec_k, rec_k1, F, pf, pww, kmax, version, sigmaltd, ltdfac, thresh
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
  pww=1
  e=0	(mV)
  F=0
  gmax = 1e9 (uS)
  kmax=2000
  Vwt   = 0 : weight for inputs coming in from vector
  rec_k=0
  rec_k1=0
  pf = 0
  
  p = 0.01 : potentiation factor :for double gaussian, d==p means area is zero
  d = -0.01 : depression(-1) factor
  taup = 16.8 (ms) : Bi & Poo (1998, 2001)
  taud = 16.8 (ms) : depression effectiveness time constant
  version=3  :0 is double exp, 1 is double gaus, 2 is postsyn threshold triplet fake rule, 3 is asym minimal triplet fake rule
  :for double gaussian, p,d,taup,taud are scales, but depressant gaussian is also flatter
  thresh=0.00045
}

ASSIGNED {
  v (mV)
  i (nA)
  g (uS)
  fact
  etime (ms)
  tpost (ms)
  countinputs
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
  countinputs=-1
  net_send(0, 1)
}

BREAKPOINT {
  SOLVE state METHOD cnexp
  g = B - A
  if (g>gmax) {g=gmax}: saturation
  i = g*(v - e)
  :printf("rec_k in BREAKOPINT: %g\n",rec_k)
}

DERIVATIVE state {
  A' = -A/tau1
  B' = -B/tau2
}


FUNCTION factor(Dt (ms), Dt2 (ms)) { 
  if (version==0) {
    factor=factor0(Dt, Dt2)*pf
  }
  if (version==1) {
    factor=factor1(Dt, Dt2)*pf
  }
  if (version==2) {
    factor=factor2(Dt, Dt2)*pf
  }
  if (version==3) {
    factor=factor3(Dt, Dt2)*pf
  }
  factor=factor
  }

FUNCTION factor0(Dt (ms), Dt2 (ms)) { :exponential
: Dt is interval between most recent presynaptic spike
    : and most recent postsynaptic spike
    : calculated as tpost - tpre (i.e. > 0 if pre happens before post)
  : the following rule is the one described by Bi & Poo
  :printf("Dt= %g, exp..= %g\n",Dt,exp(-Dt*Dt/200))
  
  if (Dt>0) {
    factor0 = p*exp(-Dt/taup) : potentiation
  
  } else if (Dt<0) {
    factor0 = -d*exp(Dt/taud) : depression
  } else {
    factor0 = 0 : no change if pre and post are simultaneous
  }
  factor0=factor0
}

FUNCTION factor1(Dt (ms), Dt2 (ms)) { :mexican hat/double gaussian 
  :printf("Dt= %g, exp..= %g\n",Dt,exp(-Dt*Dt/200))
  factor1=p*2*exp(-Dt*Dt/(2*pow(taup,2)))-d*exp(-Dt*Dt/(2*2*pow(taud,2)))  :p,d,taup,taub used same as in double exp factor
  factor1=factor1
}

FUNCTION factor2(Dt (ms), Dt2 (ms)) { :homeostatic LTP:postsynaptic trace has a threshold subtracted from it
                              :similar to (nearest spike) minimal stdp rule, but symmetric and with thresholds
                              :Dt2 always positive
  if (Dt>0) {
    :at the Adend3 synapse, there is a post spike ca every 500ms and a pre spike ca every 1ms
    factor2 = p*exp(-Dt/taup)*(exp(-Dt2/taup)-thresh) : potentiation 
    :printf("LTP by %g, Dt and Dt2: \t%g, \t%g, \t%g_____\n", factor2,Dt, Dt2, exp(Dt2/taud/500))
  } else if (Dt<0) {
    factor2 = -d*(exp(Dt/taud)-thresh) : depression
    :printf(" LTD by %g, Dt and Dt2: \t%g, \t%g\n", factor2,Dt, Dt2)
    }else {
    factor2 = 0
  }
  factor2=factor2
}

FUNCTION factor3(Dt (ms), Dt2 (ms)) {
  if (Dt>0) {
    :currently, ltp happens so rarely that the weights always just decay
    factor3 = p*245*exp(-Dt/taup)*exp(-Dt2/taup/34) : potentiation 
    :printf("LTP by %g, Dt and Dt2: \t%g, \t%g, \t%g_____\n", factor3,Dt, Dt2, exp(Dt2/taud/500))
  } else if (Dt<0) {
    factor3 = d*exp(Dt/taud) : depression
    :printf(" LTD by %g, Dt and Dt2: \t%g, \t%g\n", factor3,Dt, Dt2)
    }else {
    factor3 = 0
  }
  factor3=factor3
}


NET_RECEIVE(w (uS), k, tpre (ms)) {
  
  INITIAL { k = 1  tpre = -1e9 }
  
  if (flag == 0) { :presynaptic spike (after last post so depress)
  :printf("Presyn spike--entry flag=%g t=%g w=%g k=%g tpre=%g tpost=%g\n", flag, t, w, k, tpre, tpost)
    A = A + w*fact*k*pww
    B = B + w*fact*k*pww  :for double exp rise and decay
    
    : g = g + w*k
    
    k = k + factor(tpost - t, t-tpre)
    
    if (k>kmax) {k=kmax}: saturation
    rec_k=k
    if (t-tpre<0){printf("t-tpre________ negative sth went wrong \n")}
    tpre = t
    
    
    }
  
  else if (flag == 2) { F=F-0.9  : postsynaptic spike (after last pre so potentiate)
  :printf("Postsyn spike--entry flag=%g t=%g\n", flag, t)
    countinputs=0
    FOR_NETCONS(w1, k1, tp) { : tp is timing of last pre(?)synaptic spike, for all presynaptic connections, 
    :printf("entry FOR_NETCONS w1=%g k1=%g tp=%g\n", w1, k1, tp)
      k1 = k1+factor(t - tp, t-tpost) :k1 is plasticity factor for the weight
      :printf("\n%g,\t %g, /t %g\n", t,tpost, tp):::this prints that tpost is almost always t
      if (k1>kmax) {k1=kmax}: saturation
      countinputs=countinputs+1

      if (countinputs>1){
        :printf("MORE THAN ONE INPUT?? o_O")
      }
      if (t-tpost<0){printf("%g t-tpost negative, sth went wrong\n", t-tpost)}
      tpost = t :do afterwards, such that the second trace is not updated before it is being used in factor(.,.)
      rec_k1=k1
      :printf("  new k1 %g\n", k1)
      }
  }
  
   else {: flag == 1 from INITIAL block :only called in the beginning
    :printf("entry flag=%g t=%g\n", flag, t)
    WATCH (v > -20) 2 : calls NET_RECEIVE with flag 2, when v>thresh., for all neurons
  }
}

