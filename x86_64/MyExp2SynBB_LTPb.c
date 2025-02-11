/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__MyExp2SynBB_LTPb
#define _nrn_initial _nrn_initial__MyExp2SynBB_LTPb
#define nrn_cur _nrn_cur__MyExp2SynBB_LTPb
#define _nrn_current _nrn_current__MyExp2SynBB_LTPb
#define nrn_jacob _nrn_jacob__MyExp2SynBB_LTPb
#define nrn_state _nrn_state__MyExp2SynBB_LTPb
#define _net_receive _net_receive__MyExp2SynBB_LTPb 
#define state state__MyExp2SynBB_LTPb 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define tau1 _p[0]
#define tau2 _p[1]
#define pww _p[2]
#define e _p[3]
#define F _p[4]
#define gmax _p[5]
#define kmax _p[6]
#define Vwt _p[7]
#define rec_k _p[8]
#define rec_k1 _p[9]
#define pf _p[10]
#define p _p[11]
#define d _p[12]
#define taup _p[13]
#define taud _p[14]
#define version _p[15]
#define thresh _p[16]
#define i _p[17]
#define g _p[18]
#define A _p[19]
#define B _p[20]
#define fact _p[21]
#define etime _p[22]
#define tpost _p[23]
#define countinputs _p[24]
#define DA _p[25]
#define DB _p[26]
#define v _p[27]
#define _g _p[28]
#define _tsav _p[29]
#define _nd_area  *_ppvar[0]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 /* declaration of user functions */
 static double _hoc_factor3();
 static double _hoc_factor2();
 static double _hoc_factor1();
 static double _hoc_factor0();
 static double _hoc_factor();
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern Prop* nrn_point_prop_;
 static int _pointtype;
 static void* _hoc_create_pnt(_ho) Object* _ho; { void* create_point_process();
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt();
 static double _hoc_loc_pnt(_vptr) void* _vptr; {double loc_point_process();
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(_vptr) void* _vptr; {double has_loc_point();
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(_vptr)void* _vptr; {
 double get_loc_point_process(); return (get_loc_point_process(_vptr));
}
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata(void* _vptr) { Prop* _prop;
 _prop = ((Point_process*)_vptr)->_prop;
   _setdata(_prop);
 }
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 0,0
};
 static Member_func _member_func[] = {
 "loc", _hoc_loc_pnt,
 "has_loc", _hoc_has_loc,
 "get_loc", _hoc_get_loc_pnt,
 "factor3", _hoc_factor3,
 "factor2", _hoc_factor2,
 "factor1", _hoc_factor1,
 "factor0", _hoc_factor0,
 "factor", _hoc_factor,
 0, 0
};
#define factor3 factor3_MyExp2SynBB_LTPb
#define factor2 factor2_MyExp2SynBB_LTPb
#define factor1 factor1_MyExp2SynBB_LTPb
#define factor0 factor0_MyExp2SynBB_LTPb
#define factor factor_MyExp2SynBB_LTPb
 extern double factor3( _threadargsprotocomma_ double , double );
 extern double factor2( _threadargsprotocomma_ double , double );
 extern double factor1( _threadargsprotocomma_ double , double );
 extern double factor0( _threadargsprotocomma_ double , double );
 extern double factor( _threadargsprotocomma_ double , double );
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "tau2", 1e-09, 1e+09,
 "tau1", 1e-09, 1e+09,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "tau1", "ms",
 "tau2", "ms",
 "e", "mV",
 "gmax", "uS",
 "taup", "ms",
 "taud", "ms",
 "A", "uS",
 "B", "uS",
 "i", "nA",
 "g", "uS",
 0,0
};
 static double A0 = 0;
 static double B0 = 0;
 static double delta_t = 0.01;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 
#define _watch_array _ppvar + 3 
 
#define _fnc_index 5
 static void _hoc_destroy_pnt(_vptr) void* _vptr; {
   Prop* _prop = ((Point_process*)_vptr)->_prop;
   if (_prop) { _nrn_free_watch(_prop->dparam, 3, 2);}
   if (_prop) { _nrn_free_fornetcon(&(_prop->dparam[_fnc_index]._pvoid));}
   destroy_point_process(_vptr);
}
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[6]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"MyExp2SynBB_LTPb",
 "tau1",
 "tau2",
 "pww",
 "e",
 "F",
 "gmax",
 "kmax",
 "Vwt",
 "rec_k",
 "rec_k1",
 "pf",
 "p",
 "d",
 "taup",
 "taud",
 "version",
 "thresh",
 0,
 "i",
 "g",
 0,
 "A",
 "B",
 0,
 0};
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
  if (nrn_point_prop_) {
	_prop->_alloc_seq = nrn_point_prop_->_alloc_seq;
	_p = nrn_point_prop_->param;
	_ppvar = nrn_point_prop_->dparam;
 }else{
 	_p = nrn_prop_data_alloc(_mechtype, 30, _prop);
 	/*initialize range parameters*/
 	tau1 = 0.1;
 	tau2 = 10;
 	pww = 1;
 	e = 0;
 	F = 0;
 	gmax = 1e+09;
 	kmax = 2000;
 	Vwt = 0;
 	rec_k = 0;
 	rec_k1 = 0;
 	pf = 0;
 	p = 0.01;
 	d = -0.01;
 	taup = 16.8;
 	taud = 16.8;
 	version = 3;
 	thresh = 0.00045;
  }
 	_prop->param = _p;
 	_prop->param_size = 30;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 7, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 
#define _tqitem &(_ppvar[2]._pvoid)
 static void _net_receive(Point_process*, double*, double);
 extern int _nrn_netcon_args(void*, double***);
 static void _net_init(Point_process*, double*, double);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _MyExp2SynBB_LTPb_reg() {
	int _vectorized = 1;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex, 1,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 30, 7);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "netsend");
  hoc_register_dparam_semantics(_mechtype, 3, "watch");
  hoc_register_dparam_semantics(_mechtype, 4, "watch");
  hoc_register_dparam_semantics(_mechtype, 5, "fornetcon");
  hoc_register_dparam_semantics(_mechtype, 6, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_init[_mechtype] = _net_init;
 pnt_receive_size[_mechtype] = 3;
 add_nrn_fornetcons(_mechtype, _fnc_index);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 MyExp2SynBB_LTPb /home/maximilian/Desktop/work/neymotin/LTP_neymotin/MyExp2SynBB_LTPb.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[2], _dlist1[2];
 static int state(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset = 0; {
   DA = - A / tau1 ;
   DB = - B / tau2 ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
 DA = DA  / (1. - dt*( ( - 1.0 ) / tau1 )) ;
 DB = DB  / (1. - dt*( ( - 1.0 ) / tau2 )) ;
  return 0;
}
 /*END CVODE*/
 static int state (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) { {
    A = A + (1. - exp(dt*(( - 1.0 ) / tau1)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau1 ) - A) ;
    B = B + (1. - exp(dt*(( - 1.0 ) / tau2)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau2 ) - B) ;
   }
  return 0;
}
 
double factor ( _threadargsprotocomma_ double _lDt , double _lDt2 ) {
   double _lfactor;
 if ( version  == 0.0 ) {
     _lfactor = factor0 ( _threadargscomma_ _lDt , _lDt2 ) * pf ;
     }
   if ( version  == 1.0 ) {
     _lfactor = factor1 ( _threadargscomma_ _lDt , _lDt2 ) * pf ;
     }
   if ( version  == 2.0 ) {
     _lfactor = factor2 ( _threadargscomma_ _lDt , _lDt2 ) * pf ;
     }
   if ( version  == 3.0 ) {
     _lfactor = factor3 ( _threadargscomma_ _lDt , _lDt2 ) * pf ;
     }
   _lfactor = _lfactor ;
   
return _lfactor;
 }
 
static double _hoc_factor(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  factor ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 return(_r);
}
 
double factor0 ( _threadargsprotocomma_ double _lDt , double _lDt2 ) {
   double _lfactor0;
 if ( _lDt > 0.0 ) {
     _lfactor0 = p * exp ( - _lDt / taup ) ;
     }
   else if ( _lDt < 0.0 ) {
     _lfactor0 = - d * exp ( _lDt / taud ) ;
     }
   else {
     _lfactor0 = 0.0 ;
     }
   _lfactor0 = _lfactor0 ;
   
return _lfactor0;
 }
 
static double _hoc_factor0(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  factor0 ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 return(_r);
}
 
double factor1 ( _threadargsprotocomma_ double _lDt , double _lDt2 ) {
   double _lfactor1;
 _lfactor1 = p * 2.0 * exp ( - _lDt * _lDt / ( 2.0 * pow ( taup , 2.0 ) ) ) - d * exp ( - _lDt * _lDt / ( 2.0 * 2.0 * pow ( taud , 2.0 ) ) ) ;
   _lfactor1 = _lfactor1 ;
   
return _lfactor1;
 }
 
static double _hoc_factor1(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  factor1 ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 return(_r);
}
 
double factor2 ( _threadargsprotocomma_ double _lDt , double _lDt2 ) {
   double _lfactor2;
 if ( _lDt > 0.0 ) {
     _lfactor2 = p * exp ( - _lDt / taup ) * ( exp ( - _lDt2 / taup ) - thresh ) ;
     }
   else if ( _lDt < 0.0 ) {
     _lfactor2 = - d * ( exp ( _lDt / taud ) - thresh ) ;
     }
   else {
     _lfactor2 = 0.0 ;
     }
   _lfactor2 = _lfactor2 ;
   
return _lfactor2;
 }
 
static double _hoc_factor2(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  factor2 ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 return(_r);
}
 
double factor3 ( _threadargsprotocomma_ double _lDt , double _lDt2 ) {
   double _lfactor3;
 if ( _lDt > 0.0 ) {
     _lfactor3 = p * 245.0 * exp ( - _lDt / taup ) * exp ( - _lDt2 / taup / 34.0 ) ;
     }
   else if ( _lDt < 0.0 ) {
     _lfactor3 = d * exp ( _lDt / taud ) ;
     }
   else {
     _lfactor3 = 0.0 ;
     }
   _lfactor3 = _lfactor3 ;
   
return _lfactor3;
 }
 
static double _hoc_factor3(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  factor3 ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 return(_r);
}
 
static double _watch1_cond(_pnt) Point_process* _pnt; {
 	double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
	_thread= (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;
 	_p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
	v = NODEV(_pnt->node);
	return  ( v ) - ( - 20.0 ) ;
}
 
static void _net_receive (_pnt, _args, _lflag) Point_process* _pnt; double* _args; double _lflag; 
{  double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   int _watch_rm = 0;
   _thread = (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;   _p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
  if (_tsav > t){ extern char* hoc_object_name(); hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t;   if (_lflag == 1. ) {*(_tqitem) = 0;}
 {
   if ( _lflag  == 0.0 ) {
       if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = A;
    double __primary = (A + _args[0] * fact * _args[1] * pww) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau1 ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau1 ) - __primary );
    A += __primary;
  } else {
 A = A + _args[0] * fact * _args[1] * pww ;
       }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = B;
    double __primary = (B + _args[0] * fact * _args[1] * pww) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau2 ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau2 ) - __primary );
    B += __primary;
  } else {
 B = B + _args[0] * fact * _args[1] * pww ;
       }
 _args[1] = _args[1] + factor ( _threadargscomma_ tpost - t , t - _args[2] ) ;
     if ( _args[1] > kmax ) {
       _args[1] = kmax ;
       }
     rec_k = _args[1] ;
     if ( t - _args[2] < 0.0 ) {
       printf ( "t-tpre________ negative sth went wrong \n" ) ;
       }
     _args[2] = t ;
     }
   else if ( _lflag  == 2.0 ) {
     F = F - 0.9 ;
     countinputs = 0.0 ;
     {int _ifn1, _nfn1; double* _fnargs1, **_fnargslist1;
	_nfn1 = _nrn_netcon_args(_ppvar[_fnc_index]._pvoid, &_fnargslist1);
	for (_ifn1 = 0; _ifn1 < _nfn1; ++_ifn1) {
 	 _fnargs1 = _fnargslist1[_ifn1];
 {
       _fnargs1[1] = _fnargs1[1] + factor ( _threadargscomma_ t - _fnargs1[2] , t - tpost ) ;
       if ( _fnargs1[1] > kmax ) {
         _fnargs1[1] = kmax ;
         }
       countinputs = countinputs + 1.0 ;
       if ( countinputs > 1.0 ) {
         }
       if ( t - tpost < 0.0 ) {
         printf ( "%g t-tpost negative, sth went wrong\n" , t - tpost ) ;
         }
       tpost = t ;
       rec_k1 = _fnargs1[1] ;
       }
     	}}
 }
   else {
       _nrn_watch_activate(_watch_array, _watch1_cond, 1, _pnt, _watch_rm++, 2.0);
 }
   } }
 
static void _net_init(Point_process* _pnt, double* _args, double _lflag) {
       double* _p = _pnt->_prop->param;
    Datum* _ppvar = _pnt->_prop->dparam;
    Datum* _thread = (Datum*)0;
    _NrnThread* _nt = (_NrnThread*)_pnt->_vnt;
 _args[1] = 1.0 ;
   _args[2] = - 1e9 ;
   }
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 (_p, _ppvar, _thread, _nt);
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol_instance1(_threadargs_);
 }}

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  A = A0;
  B = B0;
 {
   double _lt_p ;
 Vwt = 0.0 ;
   if ( tau1 / tau2 > .9999 ) {
     tau1 = .9999 * tau2 ;
     }
   A = 0.0 ;
   B = 0.0 ;
   _lt_p = ( tau1 * tau2 ) / ( tau2 - tau1 ) * log ( tau2 / tau1 ) ;
   fact = - exp ( - _lt_p / tau1 ) + exp ( - _lt_p / tau2 ) ;
   fact = 1.0 / fact ;
   tpost = - 1e9 ;
   countinputs = - 1.0 ;
   net_send ( _tqitem, (double*)0, _ppvar[1]._pvoid, t +  0.0 , 1.0 ) ;
   }
 
}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _tsav = -1e20;
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel(_p, _ppvar, _thread, _nt);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   g = B - A ;
   if ( g > gmax ) {
     g = gmax ;
     }
   i = g * ( v - e ) ;
   }
 _current += i;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
 	}
 _g = (_g - _rhs)/.001;
 _g *=  1.e2/(_nd_area);
 _rhs *= 1.e2/(_nd_area);
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
 {   state(_p, _ppvar, _thread, _nt);
  }}}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(A) - _p;  _dlist1[0] = &(DA) - _p;
 _slist1[1] = &(B) - _p;  _dlist1[1] = &(DB) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/maximilian/Desktop/work/neymotin/LTP_neymotin/MyExp2SynBB_LTPb.mod";
static const char* nmodl_file_text = 
  ": check if g is supposed to be STATE or ASSIGNED\n"
  ": $Id: MyExp2SynBB.mod,v 1.4 2010/12/13 21:27:51 samn Exp $ \n"
  "NEURON {\n"
  "  POINT_PROCESS MyExp2SynBB_LTPb\n"
  "  RANGE tau1, tau2, e, i, g, Vwt, gmax, d, p, taud, taup, rec_k, rec_k1, F, pf, pww, kmax, version, sigmaltd, ltdfac, thresh\n"
  "  NONSPECIFIC_CURRENT i\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "  (nA) = (nanoamp)\n"
  "  (mV) = (millivolt)\n"
  "  (uS) = (microsiemens)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "  tau1=.1 (ms) <1e-9,1e9>\n"
  "  tau2 = 10 (ms) <1e-9,1e9>\n"
  "  pww=1\n"
  "  e=0	(mV)\n"
  "  F=0\n"
  "  gmax = 1e9 (uS)\n"
  "  kmax=2000\n"
  "  Vwt   = 0 : weight for inputs coming in from vector\n"
  "  rec_k=0\n"
  "  rec_k1=0\n"
  "  pf = 0\n"
  "  \n"
  "  p = 0.01 : potentiation factor :for double gaussian, d==p means area is zero\n"
  "  d = -0.01 : depression(-1) factor\n"
  "  taup = 16.8 (ms) : Bi & Poo (1998, 2001)\n"
  "  taud = 16.8 (ms) : depression effectiveness time constant\n"
  "  version=3  :0 is double exp, 1 is double gaus, 2 is postsyn threshold triplet fake rule, 3 is asym minimal triplet fake rule\n"
  "  :for double gaussian, p,d,taup,taud are scales, but depressant gaussian is also flatter\n"
  "  thresh=0.00045\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "  v (mV)\n"
  "  i (nA)\n"
  "  g (uS)\n"
  "  fact\n"
  "  etime (ms)\n"
  "  tpost (ms)\n"
  "  countinputs\n"
  "}\n"
  "\n"
  "STATE {\n"
  "  A (uS)\n"
  "  B (uS)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "  LOCAL t_p :for double exp decay\n"
  "\n"
  "  Vwt = 0    : testing\n"
  "\n"
  "  if (tau1/tau2 > .9999) {\n"
  "    tau1 = .9999*tau2\n"
  "  }\n"
  "  A = 0\n"
  "  B = 0\n"
  "  t_p = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)\n"
  "  fact = -exp(-t_p/tau1) + exp(-t_p/tau2)\n"
  "  fact = 1/fact\n"
  "\n"
  "\n"
  "  tpost = -1e9\n"
  "  countinputs=-1\n"
  "  net_send(0, 1)\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "  SOLVE state METHOD cnexp\n"
  "  g = B - A\n"
  "  if (g>gmax) {g=gmax}: saturation\n"
  "  i = g*(v - e)\n"
  "  :printf(\"rec_k in BREAKOPINT: %g\\n\",rec_k)\n"
  "}\n"
  "\n"
  "DERIVATIVE state {\n"
  "  A' = -A/tau1\n"
  "  B' = -B/tau2\n"
  "}\n"
  "\n"
  "\n"
  "FUNCTION factor(Dt (ms), Dt2 (ms)) { \n"
  "  if (version==0) {\n"
  "    factor=factor0(Dt, Dt2)*pf\n"
  "  }\n"
  "  if (version==1) {\n"
  "    factor=factor1(Dt, Dt2)*pf\n"
  "  }\n"
  "  if (version==2) {\n"
  "    factor=factor2(Dt, Dt2)*pf\n"
  "  }\n"
  "  if (version==3) {\n"
  "    factor=factor3(Dt, Dt2)*pf\n"
  "  }\n"
  "  factor=factor\n"
  "  }\n"
  "\n"
  "FUNCTION factor0(Dt (ms), Dt2 (ms)) { :exponential\n"
  ": Dt is interval between most recent presynaptic spike\n"
  "    : and most recent postsynaptic spike\n"
  "    : calculated as tpost - tpre (i.e. > 0 if pre happens before post)\n"
  "  : the following rule is the one described by Bi & Poo\n"
  "  :printf(\"Dt= %g, exp..= %g\\n\",Dt,exp(-Dt*Dt/200))\n"
  "  \n"
  "  if (Dt>0) {\n"
  "    factor0 = p*exp(-Dt/taup) : potentiation\n"
  "  \n"
  "  } else if (Dt<0) {\n"
  "    factor0 = -d*exp(Dt/taud) : depression\n"
  "  } else {\n"
  "    factor0 = 0 : no change if pre and post are simultaneous\n"
  "  }\n"
  "  factor0=factor0\n"
  "}\n"
  "\n"
  "FUNCTION factor1(Dt (ms), Dt2 (ms)) { :mexican hat/double gaussian \n"
  "  :printf(\"Dt= %g, exp..= %g\\n\",Dt,exp(-Dt*Dt/200))\n"
  "  factor1=p*2*exp(-Dt*Dt/(2*pow(taup,2)))-d*exp(-Dt*Dt/(2*2*pow(taud,2)))  :p,d,taup,taub used same as in double exp factor\n"
  "  factor1=factor1\n"
  "}\n"
  "\n"
  "FUNCTION factor2(Dt (ms), Dt2 (ms)) { :homeostatic LTP:postsynaptic trace has a threshold subtracted from it\n"
  "                              :similar to (nearest spike) minimal stdp rule, but symmetric and with thresholds\n"
  "                              :Dt2 always positive\n"
  "  if (Dt>0) {\n"
  "    :at the Adend3 synapse, there is a post spike ca every 500ms and a pre spike ca every 1ms\n"
  "    factor2 = p*exp(-Dt/taup)*(exp(-Dt2/taup)-thresh) : potentiation \n"
  "    :printf(\"LTP by %g, Dt and Dt2: \\t%g, \\t%g, \\t%g_____\\n\", factor2,Dt, Dt2, exp(Dt2/taud/500))\n"
  "  } else if (Dt<0) {\n"
  "    factor2 = -d*(exp(Dt/taud)-thresh) : depression\n"
  "    :printf(\" LTD by %g, Dt and Dt2: \\t%g, \\t%g\\n\", factor2,Dt, Dt2)\n"
  "    }else {\n"
  "    factor2 = 0\n"
  "  }\n"
  "  factor2=factor2\n"
  "}\n"
  "\n"
  "FUNCTION factor3(Dt (ms), Dt2 (ms)) {\n"
  "  if (Dt>0) {\n"
  "    :currently, ltp happens so rarely that the weights always just decay\n"
  "    factor3 = p*245*exp(-Dt/taup)*exp(-Dt2/taup/34) : potentiation \n"
  "    :printf(\"LTP by %g, Dt and Dt2: \\t%g, \\t%g, \\t%g_____\\n\", factor3,Dt, Dt2, exp(Dt2/taud/500))\n"
  "  } else if (Dt<0) {\n"
  "    factor3 = d*exp(Dt/taud) : depression\n"
  "    :printf(\" LTD by %g, Dt and Dt2: \\t%g, \\t%g\\n\", factor3,Dt, Dt2)\n"
  "    }else {\n"
  "    factor3 = 0\n"
  "  }\n"
  "  factor3=factor3\n"
  "}\n"
  "\n"
  "\n"
  "NET_RECEIVE(w (uS), k, tpre (ms)) {\n"
  "  \n"
  "  INITIAL { k = 1  tpre = -1e9 }\n"
  "  \n"
  "  if (flag == 0) { :presynaptic spike (after last post so depress)\n"
  "  :printf(\"Presyn spike--entry flag=%g t=%g w=%g k=%g tpre=%g tpost=%g\\n\", flag, t, w, k, tpre, tpost)\n"
  "    A = A + w*fact*k*pww\n"
  "    B = B + w*fact*k*pww  :for double exp rise and decay\n"
  "    \n"
  "    : g = g + w*k\n"
  "    \n"
  "    k = k + factor(tpost - t, t-tpre)\n"
  "    \n"
  "    if (k>kmax) {k=kmax}: saturation\n"
  "    rec_k=k\n"
  "    if (t-tpre<0){printf(\"t-tpre________ negative sth went wrong \\n\")}\n"
  "    tpre = t\n"
  "    \n"
  "    \n"
  "    }\n"
  "  \n"
  "  else if (flag == 2) { F=F-0.9  : postsynaptic spike (after last pre so potentiate)\n"
  "  :printf(\"Postsyn spike--entry flag=%g t=%g\\n\", flag, t)\n"
  "    countinputs=0\n"
  "    FOR_NETCONS(w1, k1, tp) { : tp is timing of last pre(?)synaptic spike, for all presynaptic connections, \n"
  "    :printf(\"entry FOR_NETCONS w1=%g k1=%g tp=%g\\n\", w1, k1, tp)\n"
  "      k1 = k1+factor(t - tp, t-tpost) :k1 is plasticity factor for the weight\n"
  "      :printf(\"\\n%g,\\t %g, /t %g\\n\", t,tpost, tp):::this prints that tpost is almost always t\n"
  "      if (k1>kmax) {k1=kmax}: saturation\n"
  "      countinputs=countinputs+1\n"
  "\n"
  "      if (countinputs>1){\n"
  "        :printf(\"MORE THAN ONE INPUT?? o_O\")\n"
  "      }\n"
  "      if (t-tpost<0){printf(\"%g t-tpost negative, sth went wrong\\n\", t-tpost)}\n"
  "      tpost = t :do afterwards, such that the second trace is not updated before it is being used in factor(.,.)\n"
  "      rec_k1=k1\n"
  "      :printf(\"  new k1 %g\\n\", k1)\n"
  "      }\n"
  "  }\n"
  "  \n"
  "   else {: flag == 1 from INITIAL block :only called in the beginning\n"
  "    :printf(\"entry flag=%g t=%g\\n\", flag, t)\n"
  "    WATCH (v > -20) 2 : calls NET_RECEIVE with flag 2, when v>thresh., for all neurons\n"
  "  }\n"
  "}\n"
  "\n"
  ;
#endif
