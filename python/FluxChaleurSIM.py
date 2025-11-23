from manim import *
import numpy as np

# -----------------------------------------------------------
# Physical model: q'' = ΔT / (1/h_int + e/k + 1/h_ext)
# -----------------------------------------------------------
def heat_flux(h_int, h_ext, e):
    k = 50
    dT = 37
    return dT / (1/h_int + e/k + 1/h_ext)


class HeatFlux1D(Scene):
    def construct(self):

        # Mean values
        h_int_m = 37.5
        h_ext_m = 22.5
        e_m = 0.02

        # Parameter ranges
        h_int_min, h_int_max = 30, 45
        h_ext_min, h_ext_max = 15, 30
        e_min, e_max = 0.01, 0.03

        # Axes for q''
        axes = Axes(
            x_range=[0,1,0.1],
            y_range=[300,700,50],
            x_length=7,
            y_length=4,
            tips=False
        ).to_edge(DOWN)
        self.play(Create(axes))

        # Value tracker
        t = ValueTracker(0)

        # --- q'' calculation functions for animation ---
        def q_h_int():
            h_int = h_int_min + t.get_value()*(h_int_max-h_int_min)
            return heat_flux(h_int, h_ext_m, e_m)

        def q_h_ext():
            h_ext = h_ext_min + t.get_value()*(h_ext_max-h_ext_min)
            return heat_flux(h_int_m, h_ext, e_m)

        def q_e():
            e = e_min + t.get_value()*(e_max-e_min)
            return heat_flux(h_int_m, h_ext_m, e)

        # Dot for the vertical axis animation
        dot = Dot(color=YELLOW, radius=0.06)
        dot.move_to(axes.c2p(0.5, heat_flux(h_int_m, h_ext_m, e_m)))
        self.play(FadeIn(dot))

        # Real-time text displays
        param_text = Text("...", font_size=32).to_edge(UP)
        q_text = Text("q'' = ... W/m²", font_size=32).next_to(param_text, DOWN)

        self.play(Write(param_text), Write(q_text))

        # Utility to animate and display a parameter change
        def animate_parameter(
            title, 
            compute_q, 
            compute_param_str
        ):
            # Change title
            self.play(param_text.animate.become(Text(title, font_size=32).to_edge(UP)))

            # Real-time updater for q''
            q_text.add_updater(
                lambda m: m.become(
                    Text(
                        f"q'' = {compute_q():.1f} W/m²", 
                        font_size=32
                    ).next_to(param_text, DOWN)
                )
            )

            # Dot updater
            dot.add_updater(
                lambda d: d.move_to(axes.c2p(0.5, compute_q()))
            )

            # Parameter changing text
            param_val = Text("", font_size=28).next_to(q_text, DOWN)
            param_val.add_updater(
                lambda m: m.become(
                    Text(compute_param_str(), font_size=28).next_to(q_text, DOWN)
                )
            )
            self.add(param_val)

            # Animate forward then backward
            self.play(t.animate.set_value(1), run_time=3)
            self.play(t.animate.set_value(0), run_time=3)

            # Clear updaters
            dot.clear_updaters()
            q_text.clear_updaters()
            self.remove(param_val)

        # --- RUN ANIMATIONS ---
        # 1) h_int
        animate_parameter(
            "Variation de h_int",
            compute_q=q_h_int,
            compute_param_str=lambda:
                f"h_int = {h_int_min + t.get_value()*(h_int_max-h_int_min):.1f} W/m²K"
        )

        # 2) h_ext
        animate_parameter(
            "Variation de h_ext",
            compute_q=q_h_ext,
            compute_param_str=lambda:
                f"h_ext = {h_ext_min + t.get_value()*(h_ext_max-h_ext_min):.1f} W/m²K"
        )

        # 3) e
        animate_parameter(
            "Variation de l'épaisseur e",
            compute_q=q_e,
            compute_param_str=lambda:
                f"e = {e_min + t.get_value()*(e_max-e_min):.3f} m"
        )

        # Final state
        final_title = Text("Retour aux valeurs moyennes", font_size=32).to_edge(UP)
        self.play(param_text.animate.become(final_title))

        final_q = heat_flux(h_int_m, h_ext_m, e_m)
        dot.move_to(axes.c2p(0.5, final_q))
        q_text.become(Text(f"q'' = {final_q:.1f} W/m²", font_size=32).next_to(final_title, DOWN))

        self.wait(2)
