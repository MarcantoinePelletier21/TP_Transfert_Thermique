import json, numpy as np, matplotlib.pyplot as plt
from calcul_resistance_flux import resistance_convection, resistance_conduction, temperature_harmonique

def load_parameters(path="JSON/donnees_simulation.json"):
    with open(path,"r",encoding="utf-8") as f: return json.load(f)

def TempExt(t,p):
    p=p["temperature_exterieure"]
    return temperature_harmonique(t,p["T_mean"],p["A"],p["t0"],p["phi"])

def TempSol(t,p):
    p=p["temperature_sol"]
    return temperature_harmonique(t,p["T_mean"],p["A"],p["t0"],p["phi"])

def compute_resistances(p):
    prop, geom = p["proprietes"], p["geometrie"]
    Lp, La, Lc, Li = geom["epaisseur_plaque"], geom["epaisseur_asphalte"], geom["epaisseur_ciment"], geom["epaisseur_isolant"]
    h_int, h_ext = prop["h_int"], prop["h_ext"]
    R_ext, R_sol = np.zeros(6), np.zeros(6)
    for i in range(6):
        Apl, Ac = geom[f"A_plaque_p{i+1}"], geom[f"A_ciment_p{i+1}"]
        R_ext[i] = resistance_convection(h_int,Apl)+resistance_conduction(Lp,prop["k_acier"],Apl)+resistance_conduction(La,prop["k_asphalte"],Apl)+resistance_convection(h_ext,Apl)
        R_sol[i] = resistance_convection(h_int,Ac)+resistance_conduction(Lc,prop["k_ciment"],Ac)+resistance_conduction(Li,prop["k_isolant"],Ac)
    return R_ext,R_sol

def compute_Q_aerotherme(i,T,T_ext,heaters,timers,p,dt):
    if timers[i]>0: timers[i]=max(0,timers[i]-dt)
    Tm=.5*(T[0]+T[5]); P=p["chauffage"][f"p{i+1}"]
    if T_ext>-1 or Tm>38.75:
        if heaters[i]==1: heaters[i]=0; timers[i]=5/60
        return 0.
    if T_ext<-1:
        if timers[i]>0: return 0.
        heaters[i]=1; return P
    return 0.

def compute_Q_infiltration(i,T,T_ext,p):
    g=p["infiltration"]; cp=p["proprietes"]["cp_air"]
    if i==0: m=.5*g["gap_1"]+g["gap_front"]
    elif i==1: m=.5*(g["gap_1"]+g["gap_2"])
    elif i==2: m=.5*(g["gap_2"]+g["gap_3"])
    elif i==3: m=.5*(g["gap_3"]+g["gap_4"])
    elif i==4: m=.5*(g["gap_4"]+g["gap_5"])
    elif i==5: m=.5*g["gap_5"]+g["gap_back"]
    else: m=0
    return abs(m)*cp*(T_ext-T[i])

def compute_Q_flow(i,T,f,p):
    cp=p["proprietes"]["cp_air"]
    if i==0: return f["f12"]*cp*(T[1]-T[0])
    if i==1: return f["f21"]*cp*(T[0]-T[1])+f["f23"]*cp*(T[2]-T[1])
    if i==2: return f["f32"]*cp*(T[1]-T[2])+f["f34"]*cp*(T[3]-T[2])
    if i==3: return f["f43"]*cp*(T[2]-T[3])+f["f45"]*cp*(T[4]-T[3])
    if i==4: return f["f54"]*cp*(T[3]-T[4])+f["f56"]*cp*(T[5]-T[4])
    if i==5: return f["f65"]*cp*(T[4]-T[5])
    return 0.

def q_to_Tnew(Ti,Te,Ts,Q,dt,Re,Rs,C):
    dt_s=dt*3600
    A=(C/dt_s)+(1/Re)+(1/Rs)
    B=(C/dt_s)*Ti+(Te/Re)+(Ts/Rs)+Q
    return B/A

def simulate(p,dt=1/60,t_end=48,debug=False):
    C=np.array([p["capacitance_thermique"][f"C{i}"] for i in range(1,7)],float)
    R_ext,R_sol=compute_resistances(p)
    n=int(t_end/dt)+1
    time=np.linspace(0,t_end,n)
    T=np.zeros((n,6)); T[0]=30.
    heaters=np.zeros(6,int); timers=np.zeros(6,float)

    for k in range(1,n):
        t=time[k]
        Te,Ts=TempExt(t,p),TempSol(t,p)
        flow=p["flow_heaterON"] if np.any(heaters==1) else p["flow_heaterOFF"]
        for i in range(6):
            Ti=T[k-1,i]
            Qa=compute_Q_aerotherme(i,T[k-1],Te,heaters,timers,p,dt)
            Qi=compute_Q_infiltration(i,T[k-1],Te,p)
            Qf=compute_Q_flow(i,T[k-1],flow,p)
            Q=Qa+Qi+Qf
            T[k,i]=q_to_Tnew(Ti,Te,Ts,Q,dt,R_ext[i],R_sol[i],C[i])
    return time,T

if __name__=="__main__":
    p=load_parameters()
    t_end,dt=168,1/240
    time,T=simulate(p,dt,t_end)
    print("Dernières températures :",T[-1])
    print("\nTempératures moyennes :")
    for i,m in enumerate(np.mean(T,0)): print(f"T{i+1}_moy = {m:.2f} °C")

    Te_vec=np.array([TempExt(t,p) for t in time])
    Ts_vec=np.array([TempSol(t,p) for t in time])

    plt.figure(figsize=(12,6))
    for i in range(6): plt.plot(time,T[:,i],label=f"T{i+1}")
    plt.plot(time,Te_vec,'--',label="T_ext",lw=2)
    plt.plot(time,Ts_vec,'--',label="T_sol",lw=2)
    plt.xlabel("Temps (h)",fontsize=16)
    plt.ylabel("Température (°C)",fontsize=16)
    plt.legend(); plt.tight_layout(); plt.show()
