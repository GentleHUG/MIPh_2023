"""
Программа содержит Класс с различными функциями для симуляции
"""
import Geometry as g
import Visual as vs
import matplotlib.pyplot as plt
import CONFIG as cg
import math as m
from decimal import Decimal
import csv
from copy import deepcopy

params = vs.Usefuldict(a=cg.a, b=cg.b, d=cg.d, d1=cg.d1, e=cg.e, y=cg.y, ns=cg.ns, nq=cg.nq, na=cg.na, nm=cg.nm)

class Simulation:
    @staticmethod
    def find_L_float(args: vs.Usefuldict):
        par = vs.Usefuldict()
        for key in args:
            par[key] = float(args[key])
        a1 = m.atan(par.a / par.b)
        b1 = m.asin(m.sin(a1) * par.ns / par.nq)
        a2 = b1
        b2 = m.asin(m.sin(a2) * par.nq / par.nm)
        a3 = a1 - b2

        b3 = m.asin(m.sin(a3) * par.nm / par.nq)
        a4 = b3
        b4 = m.asin(m.sin(a4) * par.nq / par.na)

        k1 = m.tan(a1) * (par.y - (par.d / 2 / m.sin(a1)) + par.d * m.sin(a1 - b1) / m.cos(b1))

        l1 = par.e * m.tan(b4)
        l2 = par.d1 * m.tan(b3)
        l3 = k1 * m.tan(a3)

        return l1 + l2 + l3
    @staticmethod
    def do_sim_with_params(C) -> Decimal:
        alpha = m.atan(C.a / C.b)
        def set_default_points(pts: vs.Usefuldict) -> None:
            pts.o = g.Point(0, 0)
            pts.l1 = g.Point(0, C.d / 2 / Decimal(m.sin(alpha)))
            pts.r1 = g.Point(C.d / 2 / Decimal(m.cos(alpha)), 0)
            pts.c1 = pts.o + (0, C.b)
            pts.c2 = pts.o + (C.a, 0)
            pts.c3 = g.Point(C.a, C.b)
            pts.r2 = pts.c3 - (0, C.d / 2 / Decimal(m.sin(alpha)))
            pts.l2 = pts.c3 - (C.d / 2 / Decimal(m.cos(alpha)), 0)
            pts.b1 = g.Point(-C.d1, -C.d1)
            pts.b2 = pts.c1 + (-C.d1, C.d1)
            pts.b3 = pts.c3 + (C.d1, C.d1)
            pts.b4 = pts.c2 + (C.d1, -C.d1)
            pts.e1 = pts.b3 + (C.e, 0)
            pts.e2 = pts.b4 + (C.e, 0)

        def set_ray_points(ray_pts: vs.Usefuldict, default_pts: vs.Usefuldict, lines: vs.Usefuldict) -> None:
            ray_pts.a0 = default_pts.b2 - (0, C.y + C.d1)
            lines.lleft = g.Line.from_points(default_pts.l1, default_pts.l2)
            lines.lright = g.Line.from_points(default_pts.r1, default_pts.r2)
            lines.boreder1 = g.Line.from_points(default_pts.c2, default_pts.c3)
            lines.boreder2 = g.Line.from_points(default_pts.b3, default_pts.b4)
            lines.endborber = g.Line.from_points(default_pts.e1, default_pts.e2)

            lines.l1 = g.Line.from_point_and_vec(ray_pts.a0, g.Vector(1, 0))
            lines.l2 = lines.l1.refraction(lines.lleft, C.ns, C.nq)
            ray_pts.a1 = lines.l1 * lines.lleft

            lines.l3 = lines.l2.refraction(lines.lright, C.nq, C.nm)
            ray_pts.a2 = lines.l2 * lines.lright

            lines.l4 = lines.l3.refraction(lines.boreder1, C.nm, C.nq)
            ray_pts.a3 = lines.l3 * lines.boreder1

            lines.l5 = lines.l4.refraction(lines.boreder2, C.nq, C.na)
            ray_pts.a4 = lines.l4 * lines.boreder2

            ray_pts.a5 = lines.l5 * lines.endborber

            # print(*lines.values())
            # print(1, ray_pts.a1)
            # print(2, ray_pts.a2)
            # print(3, ray_pts.a3)
            # print(4, ray_pts.a4)
            # print(5, ray_pts.a5)

        default_points = vs.Usefuldict()
        ray_points = vs.Usefuldict()
        all_lines = vs.Usefuldict()
        alpha = Decimal(m.atan(C.a / C.b))
        set_default_points(default_points)
        set_ray_points(ray_points, default_points, all_lines)
        # print(ray_points.a5.y-ray_points.a4.y, ray_points.a4.y-ray_points.a3.y, ray_points.a3.y-ray_points.a2.y, sep='\n')
        return ray_points.a1.y - ray_points.a5.y

    @staticmethod
    def do_sim_in_range(C: vs.Usefuldict, par_name: str, val_range: list) -> None:
        new_c = deepcopy(C)
        for value in val_range:
            new_c[par_name] = Decimal(value)
            new_c.nm = new_c.ns - Decimal(0.2)
            with open(f'data_{par_name}={value}.csv', 'w', newline='') as csvfile:
                fieldnames = ['L', 'nm']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                try:
                    while new_c.nm < 2:
                        data = {'L': Simulation(new_c).do_sim_with_params(), 'nm': new_c.nm}
                        new_c.nm += Decimal(0.0001)
                        writer.writerow(data)
                except Exception as e:
                    print(f'Program ended nm={new_c.nm}, {e}')
                print(new_c.nm)

    @staticmethod
    def print_sim(C):
        def set_default_points(pts: vs.Usefuldict) -> None:
            alpha = m.atan(C.a/C.b)

            pts.o = g.Point(0,0)
            pts.l1 = g.Point(0, C.d/2 / Decimal(m.sin(alpha)))
            pts.r1 = g.Point(C.d / 2 / Decimal(m.cos(alpha)), 0)
            pts.c1 = pts.o + (0, C.b)
            pts.c2 = pts.o + (C.a, 0)
            pts.c3 = g.Point(C.a, C.b)
            pts.r2 = pts.c3 - (0, C.d/2 / Decimal(m.sin(alpha)))
            pts.l2 = pts.c3 - (C.d / 2 / Decimal(m.cos(alpha)), 0)
            pts.b1 = g.Point(-C.d1, -C.d1)
            pts.b2 = pts.c1 + (-C.d1, C.d1)
            pts.b3 = pts.c3 + (C.d1, C.d1)
            pts.b4 = pts.c2 + (C.d1, -C.d1)
            pts.e1 = pts.b3 + (C.e, 0)
            pts.e2 = pts.b4 + (C.e, 0)

        def print_base_lines(ax, pts: vs.Usefuldict) -> None:
            vs.print_polygone(ax, [pts.l1, pts.c1, pts.l2])
            vs.print_polygone(ax, [pts.r1, pts.r2, pts.c2])
            vs.print_polygone(ax, [pts.b1, pts.b2, pts.b3, pts.b4], 'b')
            vs.print_line_2p(ax, pts.e1, pts.e2, 'g')

        def set_ray_points(ray_pts: vs.Usefuldict, default_pts: vs.Usefuldict, lines: vs.Usefuldict) -> None:
            ray_pts.a0 = default_pts.b2 - (0,cg.y+cg.d1)
            lines.lleft = g.Line.from_points(default_pts.l1, default_pts.l2)
            lines.lright = g.Line.from_points(default_pts.r1, default_pts.r2)
            lines.boreder1 = g.Line.from_points(default_pts.c2, default_pts.c3)
            lines.boreder2 = g.Line.from_points(default_pts.b3, default_pts.b4)
            lines.endborber = g.Line.from_points(default_pts.e1, default_pts.e2)
            print(*lines.values())
            lines.l1 = g.Line.from_point_and_vec(ray_pts.a0, g.Vector(1, 0))
            lines.l2 = lines.l1.refraction(lines.lleft, cg.ns, cg.nq)
            ray_pts.a1 = lines.l1 * lines.lleft
            print(1, ray_pts.a1)
            lines.l3 = lines.l2.refraction(lines.lright, cg.nq, cg.nm)
            ray_pts.a2 = lines.l2 * lines.lright
            print(2, ray_pts.a2)
            lines.l4 = lines.l3.refraction(lines.boreder1, cg.nm, cg.nq)
            ray_pts.a3 = lines.l3 * lines.boreder1
            print(3, ray_pts.a3)
            lines.l5 = lines.l4.refraction(lines.boreder2, cg.nq, cg.na)
            ray_pts.a4 = lines.l4 * lines.boreder2
            print(4, ray_pts.a4)
            ray_pts.a5 = lines.l5 * lines.endborber
            print(5, ray_pts.a5)


        default_points = vs.Usefuldict()
        ray_points = vs.Usefuldict()
        all_lines = vs.Usefuldict()
        alpha = Decimal(m.atan(cg.a / cg.b))

        set_default_points(default_points)
        set_ray_points(ray_points, default_points, all_lines)
        print(f'L={ray_points.a2.y-ray_points.a5.y}')

        sites = g.Vector(2*cg.d1+cg.a+cg.e, 2*cg.d1+cg.b)
        size = (float(15*sites.x / sites.modulo()), float(15*sites.y / sites.modulo()))
        fig, ax = plt.subplots(figsize=size)

        print_base_lines(ax, default_points)
        vs.print_polygone(ax, [ray_points.a0, ray_points.a1, ray_points.a2, ray_points.a3, ray_points.a4, ray_points.a5], color='r', endpoints=False)

        ax.grid(True)
        ax.set_xlabel('x, mm')
        ax.set_ylabel('y, mm')
        ax.set_title('Визуализация модели')

        plt.show()
