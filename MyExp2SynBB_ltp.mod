: $Id: MyExp2SynBB.mod,v 1.4 2010/12/13 21:27:51 samn Exp $ 
NEURON {
  : THREADSAFE
  POINT_PROCESS MyExp2SynBB_ltp
  RANGE tau1, tau2, e, i, g, Vwt, gmax
  NONSPECIFIC_CURRENT i
  RANGE f, tau_T, F, T, myt, mytsyn: , d1, tau_D1, d2, tau_D2
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
  f = 1 (1) < 0, 1e9 >    : facilitation
  tau_T = 94 (ms) < 1e-9, 1e9 >
  F=1
  T=1
  myt=0
  mytsyn=0
}

ASSIGNED {
  v (mV)
  i (nA)
  g (uS)
  factor
  etime (ms)
}

STATE {
  A (uS)
  B (uS)
}

INITIAL {
  LOCAL tp


  Vwt = 0    : testing

  if (tau1/tau2 > .9999) {
    tau1 = .9999*tau2
  }
  A = 0
  B = 0
  tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
  factor = -exp(-tp/tau1) + exp(-tp/tau2)
  factor = 1/factor
}

BREAKPOINT { : Lines in BREAKPOINT: The SOLVE ... METHOD line is ignored. All lines after SOLVE are executed. With a printf() statement, you would see two calls. However, one of the calls does not actually set any state variables. It is used to compute the derivatives.
  SOLVE state METHOD cnexp
  g = B - A
  if (g>gmax) {g=gmax}: saturation
  i = g*(v - e)
}

DERIVATIVE state { : Finally, the DERIVATIVE block: The values for the derivatives (X' = ...) are computed'. Keep in mind, to get the value by which the state variable actually changes, multiply by dt.
  A' = -A/tau1
  B' = -B/tau2
}

: NET_RECEIVE: If there is net_send() an event that targets this mechanism, lines here are executed first. Skipped otherwise.
NET_RECEIVE(w (uS), tsyn (ms)) {LOCAL ww
  ww=w
  INITIAL {:called 3 times in the beginning, then never again
    F = 1
    T=1
    tsyn = t
    printf("start(initial) %g %g %g\n", t, t-tsyn, tsyn)
    
    
}

printf("entry flag=%g \n", flag)

  myt=t ::
  mytsyn=tsyn ::
  T = T*exp(-(t - tsyn)/tau_T)

  
  printf("start %g %g %g, F=%g\n", t, t-tsyn, tsyn,F)

  tsyn = t
  
  A= A + ww*factor
  B=B + ww*factor
  :state_discontinuity(A, A + ww*factor)
  :state_discontinuity(B, B + ww*factor)
  T = T + f
}

