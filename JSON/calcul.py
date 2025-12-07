import json

def load_parameters(path="JSON/donnees_simulation.json"):
    with open(path,"r",encoding="utf-8") as f: return json.load(f)

if __name__=="__main__":
    p=load_parameters()
    g=p["geometrie"]; prop=p["proprietes"]

    A1=(2*g["p1_x"]*g["scale_x"]*g["pi_z"])+(g["pi_y"]*g["scale_y"]*g["pi_z"])+(g["p1_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"])
    A2=(2*g["p2_x"]*g["scale_x"]*g["pi_z"])+(g["p2_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"])
    A3=(2*g["p3_x"]*g["scale_x"]*g["pi_z"])+(g["p3_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"])
    A4=(2*g["p4_x"]*g["scale_x"]*g["pi_z"])+(g["p4_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"])
    A5=(2*g["p5_x"]*g["scale_x"]*g["pi_z"])+(g["p5_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"])
    A6=(2*g["p6_x"]*g["scale_x"]*g["pi_z"])+(g["pi_y"]*g["scale_y"]*g["pi_z"])+(g["p6_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"])

    A7=g["p1_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"]
    A8=g["p2_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"]
    A9=g["p3_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"]
    A10=g["p4_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"]
    A11=g["p5_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"]
    A12=g["p6_x"]*g["pi_y"]*g["scale_x"]*g["scale_y"]

    rho=prop["rho_air"]; cp=prop["cp_air"]
    H=g["pi_z"]; W=g["pi_y"]*g["scale_y"]

    L=[g[f"p{i}_x"]*g["scale_x"] for i in range(1,7)]
    V=[L[i]*W*H for i in range(6)]
    m=[rho*v for v in V]
    C=[mi*cp for mi in m]

    for i,c in enumerate(C,1): print(f"C{i} = {c}")
