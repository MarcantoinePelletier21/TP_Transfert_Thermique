from manim import *
from manim_eng import *

class ThermalCircuitV2(MovingCameraScene):
    def construct(self):
        ni = Node().shift(4*LEFT)
        n_ext = Node().shift(4*RIGHT+UP)
        n_sol = Node().shift(4*RIGHT+DOWN)

        r_ext_conv_IN = Resistor().shift(2*LEFT+UP)
        r_ext_cond_plaque = Resistor().shift(UP)
        r_ext_cond_asphalte = Resistor().shift(UP+2*RIGHT)
        r_ext_conv_OUT = Resistor().shift(UP+4*RIGHT)

        r_sol_conv = Resistor().shift(DOWN+2*LEFT)
        r_sol_cond_ciment = Resistor().shift(DOWN)
        r_sol_cond_isolant = Resistor().shift(DOWN+2*RIGHT)

        circle_node_T1 = Circle(0.1, color=WHITE, fill_opacity=1).shift(3.75*LEFT)
        circle_node_Text = Circle(0.1, color=WHITE, fill_opacity=1).shift(5*RIGHT+UP)
        circle_node_Tsol = Circle(0.1, color=WHITE, fill_opacity=1).shift(3*RIGHT+DOWN)
        arrow = DoubleArrow(max_tip_length_to_length_ratio=0.5).shift(4.7*LEFT)

        t1  = MathTex(r"R_{conv,int}").shift(2*LEFT+1.5*UP).scale(0.6)
        t2  = MathTex(r"R_{cond,plaque}").shift(1.5*UP).scale(0.6)
        t3  = MathTex(r"R_{cond,asphalte}").shift(1.5*UP+2*RIGHT).scale(0.6)
        t4  = MathTex(r"R_{conv,ext}").shift(1.5*UP+4*RIGHT).scale(0.6)
        t5  = MathTex(r"R_{conv,int}").shift(1.5*DOWN+2*LEFT).scale(0.6)
        t6  = MathTex(r"R_{cond,ciment}").shift(1.5*DOWN).scale(0.6)
        t7  = MathTex(r"R_{cond,isolant}").shift(1.5*DOWN+2*RIGHT).scale(0.6)

        t8  = MathTex(r"T_i").shift(3.7*LEFT+0.6*UP)
        t9  = MathTex(r"T_{ext}").shift(5.7*RIGHT+UP)
        t10 = MathTex(r"T_{sol}").shift(3.75*RIGHT+DOWN)
        t11 = MathTex(r"\sum q_{in- out}").shift(5*LEFT+0.75*DOWN)

        wires = [
            Wire(ni.right, r_ext_conv_IN.left).attach(),
            Wire(r_ext_conv_IN.right, r_ext_cond_plaque.left).attach(),
            Wire(r_ext_cond_plaque.right, r_ext_cond_asphalte.left).attach(),
            Wire(r_ext_cond_asphalte.right, r_ext_conv_OUT.left).attach(),
            Wire(ni.right, r_sol_conv.left).attach(),
            Wire(r_sol_conv.right, r_sol_cond_ciment.left).attach(),
            Wire(r_sol_cond_ciment.right, r_sol_cond_isolant.left).attach()
        ]

        for w in wires: self.add(w)

        self.add(
            circle_node_T1, t8,
            r_ext_conv_IN, r_ext_cond_asphalte, r_ext_cond_plaque, r_ext_conv_OUT,
            t1, t2, t3, t4, n_ext, circle_node_Text, t9,
            r_sol_cond_ciment, r_sol_cond_isolant, r_sol_conv,
            circle_node_Tsol, t10, t5, t6, t7, arrow, t11
        )
