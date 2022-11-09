: $Id: MyExp2SynBB.mod,v 1.4 2010/12/13 21:27:51 samn Exp $ 
NEURON {
:  THREADSAFE
  POINT_PROCESS MyExp2SynBB_ltp
  RANGE tau1, tau2, e, i, g, Vwt, gmax
  NONSPECIFIC_CURRENT i
  GLOBAL total123
  : RANGE f, tau_F, d1, tau_D1, d2, tau_D2
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
}

ASSIGNED {
  v (mV)
  i (nA)
  g (uS)
  factor
  etime (ms)
  total123 (umho)
}

STATE {
  A (uS)
  B (uS)
}

INITIAL {
  LOCAL tp
  total123 = 0


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

NET_RECEIVE(w (uS)) {LOCAL ww
  ww=w
  A = A + ww*factor
  B = B + ww*factor
}
