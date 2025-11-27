from manim import *

from manim import Difference

class schema(MovingCameraScene):
    def construct(self):
        
        plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.2
            },
            x_range=(-20, 25),
            y_range=(-10, 10)
        )
        self.add(plane)
        self.camera.frame.scale(2.7)

        t1 = Text("Plan du puits", font_size=60, color=BLUE)
        t1.move_to([-14,8,0])
        self.play(Write(t1))

        points = [
            np.array([-14, -1,  0]),
            np.array([-15, -1,  0]),
            np.array([-15,  1,  0]),
            np.array([-14,  1,  0]),
            np.array([-14,  2,  0]),
            np.array([-11,  2,  0]),
            np.array([-11,  1,  0]),
            np.array([-9,  1,  0]),
            np.array([-9,  2,  0]),
            np.array([-6,  2,  0]),
            np.array([-6,  1,  0]),
            np.array([-4,  1,  0]),
            np.array([-4,  2,  0]),
            np.array([-1,  2,  0]),
            np.array([-1,  1,  0]),
            np.array([1,  1,  0]),
            np.array([1,  2,  0]),
            np.array([5,  2,  0]),
            np.array([5,  1,  0]),
            np.array([7,  1,  0]),
            np.array([7,  2,  0]),
            np.array([11,  2,  0]),
            np.array([11,  1,  0]),
            np.array([13,  1,  0]),
            np.array([13,  2,  0]),
            np.array([16,  2,  0]),
            np.array([16,  1,  0]),
            np.array([17,  1,  0]),
            np.array([17,  -1,  0]),
            np.array([16,  -1,  0]),
            np.array([16,  -2,  0]),
            np.array([13,  -2,  0]),
            np.array([13,  -1,  0]),
            np.array([11,  -1,  0]),
            np.array([11,  -2,  0]),
            np.array([7,  -2,  0]),
            np.array([7,  -1,  0]),
            np.array([5,  -1,  0]),
            np.array([5,  -2,  0]),
            np.array([1,  -2,  0]),
            np.array([1,  -1,  0]),
            np.array([-1,  -1,  0]),
            np.array([-1,  -2,  0]),
            np.array([-4,  -2,  0]),
            np.array([-4,  -1,  0]),
            np.array([-6,  -1,  0]),
            np.array([-6,  -2,  0]),
            np.array([-9,  -2,  0]),
            np.array([-9,  -1,  0]),
            np.array([-11,  -1,  0]),
            np.array([-11,  -2,  0]),
            np.array([-14,  -2,  0]),
            np.array([-14,  -1,  0]),
        ]

        # ligne
        polyline = VMobject().set_points_as_corners(points)

        # Points visibles
        dots = VGroup(*[Dot(p, color=ORANGE) for p in points])

        self.play(Create(polyline), FadeIn(dots), run_time=2)
        self.wait()

        point2 =  [np.array([-16, -3,  0]),
            np.array([-16, 3,  0]),
            np.array([18,  3,  0]),
            np.array([18,  -3,  0]),
            np.array([-16, -3,  0])]
        
        polyline2 = VMobject().set_points_as_corners(point2)
        dots2 = VGroup(*[Dot(p, color=ORANGE) for p in point2])

        self.play(Create(polyline2), FadeIn(dots2), run_time=2)
        self.wait()

        inside_shape = Polygon(*points, color=BLUE)
        inside_shape.set_fill(color=BLUE, opacity=0.25)
        inside_shape.set_stroke(color=WHITE, width=0)
        text_puit = Text("Intérieur du puits", font_size=40, color=BLUE)
        text_puit.move_to([-14,6,0])
        self.play(Write(text_puit))

        # Glow effect en ajoutant une aura
        glow = inside_shape.copy().set_fill(BLUE, opacity=0.40)
        glow.set_stroke(BLUE, width=20, opacity=0.15)

        self.play(FadeIn(glow), FadeIn(inside_shape), run_time=1.5)
        self.play(FadeOut(glow), FadeOut(inside_shape))


        text_isolant = Text("Couche d'isolant", font_size=40, color=BLUE)
        text_isolant.move_to([-14,5,0])
        self.play(Write(text_isolant))
        rect = VMobject().set_points_as_corners(point2)
        rect.set_stroke(color=ORANGE, width=5)

        # Glow autour du contour
        rect_glow = rect.copy().set_stroke(ORANGE, width=25, opacity=0.20)

        self.play(FadeIn(rect_glow), Create(rect), run_time=1.5)
        self.play(FadeOut(rect_glow), FadeOut(rect))

        


        inner_poly = Polygon(*points)
        rect_poly  = Polygon(*point2)
        text_ciment = Text("Murs en ciment", font_size=40, color=BLUE)
        text_ciment.move_to([-14,4,0])
        self.play(Write(text_ciment))

        # Zone = Rectangle moins la forme intérieure
        outer_zone = Difference(rect_poly, inner_poly)

        outer_zone.set_fill(ORANGE, opacity=0.25)
        outer_zone.set_stroke(ORANGE, width=2)
        glow_outer = outer_zone.copy().set_stroke(ORANGE, width=20, opacity=0.18)

        self.play(FadeIn(glow_outer), FadeIn(outer_zone), run_time=1.5)
        self.play(FadeOut(glow_outer), FadeOut(outer_zone))

        self.wait()

        t2 = Text("Changements et simplifications", font_size=60, color=BLUE)
        t2.move_to([-12,8,0])
        self.play(FadeOut(text_ciment), FadeOut(text_isolant), FadeOut(text_puit), Transform(t1,t2))
        self.wait()
        self.play(FadeIn(t2))
        self.wait()

        new_points = [np.array([-15,  -2,  0]),
                      np.array([-15,  2,  0]),
                      np.array([17,  2,  0]),
                      np.array([17,  -2,  0]),
                      np.array([-15,  -2,  0])]
        
        polyline3 = VMobject().set_points_as_corners(new_points)
        dots3 = VGroup(*[Dot(p, color=ORANGE) for p in new_points])
        self.play(Transform(polyline, polyline3), Transform(dots, dots3))
        self.wait()

        # ajout des zones p1,2,3,...

        p1 = [np.array([-15,  -2,  0]),
                      np.array([-15,  2,  0]),
                      np.array([17,  2,  0]),
                      np.array([17,  -2,  0]),
                      np.array([-15,  -2,  0])]
        


