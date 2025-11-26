from manim import *
from manim_eng import *

class ThermalCircuit(MovingCameraScene):
    def construct(self):

        # ------------------------------------------------------------------
        # OBJETS
        # ------------------------------------------------------------------
        # Objet colonne du haut
        n1 = Node()
        r1 = Resistor().shift(RIGHT)
        n2 = Node().shift(2*RIGHT)
        r2 = Resistor().shift(3*RIGHT)
        n3 = Node().shift(4*RIGHT)
        r3 = Resistor().shift(5*RIGHT)
        n4 = Node().shift(6*RIGHT)
        r4 = Resistor().shift(7*RIGHT)
        n5 = Node().shift(8*RIGHT)
        r5 = Resistor().shift(9*RIGHT)
        n6 = Node().shift(10*RIGHT)

        # Branches verticales de n1
        rt1_1 = Resistor().rotate(90* DEGREES).shift(2*DOWN)
        rt1_2 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(RIGHT)
        # Branches verticales de n2
        rt2_1 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(2*RIGHT)
        rt2_2 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(3*RIGHT)
        # Branches verticales de n3
        rt3_1 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(4*RIGHT)
        rt3_2 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(5*RIGHT)
        # Branches verticales de n4
        rt4_1 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(6*RIGHT)
        rt4_2 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(7*RIGHT)
        # Branches verticales de n5
        rt5_1 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(8*RIGHT)
        rt5_2 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(9*RIGHT)
        # Branches verticales de n6
        rt6_1 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(10*RIGHT)
        rt6_2 = Resistor().rotate(90* DEGREES).shift(2*DOWN).shift(11*RIGHT)

        # nodes pertes de chaleur
        n_ext = Node().shift(5*DOWN)
        n_sol = Node().shift(4*DOWN).shift(RIGHT)

        text1 = MathTex("T_{ext}").next_to(n_ext, DOWN).scale(0.5)
        text2 = MathTex("T_{sol}").next_to(n_sol, DOWN).scale(0.5)
        c1 = Circle(color= WHITE, fill_opacity=1).shift(5*DOWN).scale(0.05)
        c2 = Circle(color= WHITE, fill_opacity=1).shift(4*DOWN).shift(RIGHT).scale(0.05)


        # Sources de chaleur
        q1 = CurrentSource().rotate(-90 * DEGREES).shift(UP)
        q2 = CurrentSource().rotate(-90 * DEGREES).shift(2*RIGHT).shift(UP)
        q3 = CurrentSource().rotate(-90 * DEGREES).shift(4*RIGHT).shift(UP)
        q4 = CurrentSource().rotate(-90 * DEGREES).shift(6*RIGHT).shift(UP)
        q5 = CurrentSource().rotate(-90 * DEGREES).shift(8*RIGHT).shift(UP)
        q6 = CurrentSource().rotate(-90 * DEGREES).shift(10*RIGHT).shift(UP)

        q1.set_current("q_1")
        q2.set_current("q_2")
        q3.set_current("q_3")
        q4.set_current("q_4")
        q5.set_current("q_5")
        q6.set_current("q_6")

        # Ajout brut des objets
        self.add(
            n1, n2, n3, n4, n5, n6,
            r1, r2, r3, r4, r5,
            q1, q2, q3, q4, q5, q6,
            rt1_1, rt1_2, rt2_1, rt2_2,
            rt3_1, rt3_2, rt4_1, rt4_2, rt5_1,
            rt5_2, rt6_1, rt6_2, n_ext, n_sol,
            text1, text2, c1, c2
        )

        wires = []

        # -------------------------------
        # Horizontal resistors R1 à R5
        # -------------------------------
        wires.append(Wire(r1.left,  n1.right).attach())
        wires.append(Wire(r1.right, n2.left ).attach())

        wires.append(Wire(r2.left,  n2.right).attach())
        wires.append(Wire(r2.right, n3.left ).attach())

        wires.append(Wire(r3.left,  n3.right).attach())
        wires.append(Wire(r3.right, n4.left ).attach())

        wires.append(Wire(r4.left,  n4.right).attach())
        wires.append(Wire(r4.right, n5.left ).attach())

        wires.append(Wire(r5.left,  n5.right).attach())
        wires.append(Wire(r5.right, n6.left ).attach())


        # -------------------------------
        # Sources q1 à q6
        # -------------------------------
        wires.append(Wire(q1.left, n1.up).attach())
        wires.append(Wire(q2.left, n2.up).attach())
        wires.append(Wire(q3.left, n3.up).attach())
        wires.append(Wire(q4.left, n4.up).attach())
        wires.append(Wire(q5.left, n5.up).attach())
        wires.append(Wire(q6.left, n6.up).attach())


        # -------------------------------
        # Vertical resistors vers T_ext (rt*_1)
        # -------------------------------
        wires.append(Wire(n1.down, rt1_1.right).attach())
        wires.append(Wire(rt1_1.left, n_ext.up).attach())

        wires.append(Wire(n2.down, rt2_1.right).attach())
        wires.append(Wire(rt2_1.left, n_ext.up).attach())

        wires.append(Wire(n3.down, rt3_1.right).attach())
        wires.append(Wire(rt3_1.left, n_ext.up).attach())

        wires.append(Wire(n4.down, rt4_1.right).attach())
        wires.append(Wire(rt4_1.left, n_ext.up).attach())

        wires.append(Wire(n5.down, rt5_1.right).attach())
        wires.append(Wire(rt5_1.left, n_ext.up).attach())

        wires.append(Wire(n6.down, rt6_1.right).attach())
        wires.append(Wire(rt6_1.left, n_ext.up).attach())


        # -------------------------------
        # Vertical resistors vers T_sol (rt*_2)
        # -------------------------------
        wires.append(Wire(n1.down, rt1_2.right).attach())
        wires.append(Wire(rt1_2.left, n_sol.up).attach())

        wires.append(Wire(n2.down, rt2_2.right).attach())
        wires.append(Wire(rt2_2.left, n_sol.up).attach())

        wires.append(Wire(n3.down, rt3_2.right).attach())
        wires.append(Wire(rt3_2.left, n_sol.up).attach())

        wires.append(Wire(n4.down, rt4_2.right).attach())
        wires.append(Wire(rt4_2.left, n_sol.up).attach())

        wires.append(Wire(n5.down, rt5_2.right).attach())
        wires.append(Wire(rt5_2.left, n_sol.up).attach())

        wires.append(Wire(n6.down, rt6_2.right).attach())
        wires.append(Wire(rt6_2.left, n_sol.up).attach())

        # Ajouter silencieusement au Scene
        for w in wires:
            self.add(w)

        


        # ------------------------------------------------------------------
        # RECENTRAGE AUTOMATIQUE
        # ------------------------------------------------------------------
        # Regrouper tout ce qui a été ajouté
        all_mobs = VGroup(*self.mobjects)

        # Déplacer le circuit vers la gauche
        all_mobs.shift(5 * LEFT)
        all_mobs.shift(2*UP)

        self.update_mobjects(0)

        # Animation de tous les fils
        self.play(*[Create(w) for w in wires], run_time=3)
        self.wait(2)

        # -------------------------------
        # ISOLATION & ZOOM SECTION
        # -------------------------------

        # 1) Définir le groupe d’intérêt
        focus_group = Group(rt1_1, rt1_2)

        # 2) Tout le reste du circuit (doit être un Group, pas VGroup)
        others = Group(*[m for m in self.mobjects if m not in focus_group])

        # 3) Encadré autour des deux résistances
        rect = SurroundingRectangle(focus_group, color=YELLOW, buff=0)
        self.play(Create(rect))

        # 4) Faire disparaître tout le reste
        self.play(FadeOut(others, run_time=1.5))

        # 5) Zoom caméra sur cette section
        self.play(
            self.camera.frame.animate
                .scale(0.4)
                .move_to(focus_group),
            run_time=1
        )
        self.wait(1)
        self.play(FadeOut(rect, run_time  = 1))
        self.play(self.camera.frame.animate
                .scale(3))
        
        def make_series_resistors(n, start_point, direction=DOWN, spacing=0.5):
            """Creates n resistors in series starting at start_point"""
            res_list = []
            current_pos = start_point

            for i in range(n):
                r = Resistor().rotate(90*DEGREES)  # vertical resistor
                r.move_to(current_pos)
                res_list.append(r)
                current_pos = current_pos + spacing * direction

            return res_list
        
        # Série pour la branche T_ext
        rt1_1_series = make_series_resistors(
            n=3,
            start_point=rt1_1.get_center(),
            direction=DOWN,
            spacing=1.5
        )

        # Série pour la branche T_sol
        rt1_2_series = make_series_resistors(
            n=3,
            start_point=rt1_2.get_center(),
            direction=DOWN,
            spacing=1.5
        )
        rt1_1_group = VGroup(*rt1_1_series)
        rt1_2_group = VGroup(*rt1_2_series)


        # Connexion au node venant de n1.down
        wires.append(Wire(n1.down, rt1_1_series[0].right).attach())

        # Connexions série entre les résistances
        for i in range(len(rt1_1_series) - 1):
            wires.append(Wire(rt1_1_series[i].left, rt1_1_series[i+1].right).attach())

        # Connexion à n_ext
        wires.append(Wire(rt1_1_series[-1].left, n_ext.up).attach())

        # Connexion au node venant de n1.down
        wires.append(Wire(n1.down, rt1_2_series[0].right).attach())

        # Connexions série entre résistances
        for i in range(len(rt1_2_series) - 1):
            wires.append(Wire(rt1_2_series[i].left, rt1_2_series[i+1].right).attach())

        # Connexion à n_sol
        wires.append(Wire(rt1_2_series[-1].left, n_sol.up).attach())

        # Disparition morphologique en série
        self.play(
            ReplacementTransform(rt1_1, rt1_1_group),
            ReplacementTransform(rt1_2, rt1_2_group),
            run_time=2)
        focus_mid = Group(rt1_1_group[1], rt1_2_group[1])
        self.play(
            self.camera.frame.animate
                .scale(1)
                .move_to(focus_mid),
            run_time=2)

        def add_endpoints(group, scene, radius_scale=0.05):
            """Add a white circle at the top and bottom of a vertical resistor group."""
            top = group.get_top()
            bottom = group.get_bottom()

            c_top = Circle(color=WHITE, fill_opacity=1).scale(radius_scale).move_to(top)
            c_bottom = Circle(color=WHITE, fill_opacity=1).scale(radius_scale).move_to(bottom)

            scene.add(c_top, c_bottom)
            return c_top, c_bottom
        
       # Ajouter les cercles aux extrémités
        rt1_1_top, rt1_1_bottom = add_endpoints(rt1_1_group, self)
        rt1_2_top, rt1_2_bottom = add_endpoints(rt1_2_group, self)

        # Labels en LaTeX
        text_t1     = MathTex("T_1").next_to(rt1_1_top, LEFT).scale(0.5)
        text_t1_2   = MathTex("T_1").next_to(rt1_2_top, RIGHT).scale(0.5)
        text_t_ext  = MathTex("T_{ext}").next_to(rt1_1_bottom, LEFT).scale(0.5)
        text_t_sol  = MathTex("T_{sol}").next_to(rt1_2_bottom, RIGHT).scale(0.5)
        text_r1  = MathTex("R_{conv, int}").next_to(rt1_1_group[0], LEFT).scale(0.75)
        text_r2  = MathTex("R_{cond, plaque}").next_to(rt1_1_group[1], LEFT).scale(0.75)
        text_r3  = MathTex("R_{conv, ext}").next_to(rt1_1_group[2], LEFT).scale(0.75)
        text_r4  = MathTex("R_{conv, int}").next_to(rt1_2_group[0], RIGHT).scale(0.75)
        text_r5  = MathTex("R_{cond, ciment}").next_to(rt1_2_group[1], RIGHT).scale(0.75)
        text_r6  = MathTex("R_{contact, ext}").next_to(rt1_2_group[2], RIGHT).scale(0.75)

        # Animation
        self.play(
            FadeIn(rt1_1_top),
            FadeIn(rt1_1_bottom),
            FadeIn(rt1_2_top),
            FadeIn(rt1_2_bottom),
            FadeIn(text_t1),
            FadeIn(text_t_ext),
            FadeIn(text_t_sol),
            FadeIn(text_t1_2),
            Write(text_r1),
            Write(text_r2),
            Write(text_r3),
            Write(text_r4),
            Write(text_r5),
            Write(text_r6),
            run_time=0.5
        )
        self.wait(2)







