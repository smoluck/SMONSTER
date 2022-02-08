#!/usr/bin/env python

# Uses Smallest Enclosing Circle code which is:
# Copyright (c) 2014 Nayuki Minase
# http://nayuki.eigenstate.org/page/smallest-enclosing-circle

import lx, lxifc, lxu.command, traceback
import lxu.select, math, sys, random

minFloat = float('-inf')
maxFloat = float('inf')
_EPSILON = sys.float_info.epsilon

options_bbox_from = [('group', 'layer', 'all'),
                ('Per Selected Group', 'Per Layer', 'All Layers')]

options_bbox_to = [('each', 'primary'),
                ('Each Layer', 'Primary Layer')]

options_bbox_type = [('aabb', 'aacyl'),
                ('Axis Aligned Bounding Box', 'Axis Aligned Bounding Cylinder')]

options_bbox_axis = [('x', 'y', 'z', 'shortest', 'longest'),
                ('X', 'Y', 'Z', 'Auto Shortest', 'Auto Longest')]

options_bbox_accuracy = [('inside', 'on', 'outside'),
                ('Inside Radius', 'On Radius', 'Enclosing Radius')]

class OptionPopup(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items[0])

    def uiv_PopUserName(self,index):
        return self._items[1][index]

    def uiv_PopInternalName(self,index):
        return self._items[0][index]

class MarkElements(lxifc.Visitor):
    def __init__(self, element, mark_mode):
        self.element = element
        self.mark_mode = mark_mode

    def vis_Evaluate(self):
        self.element.SetMarks(self.mark_mode)

class BBOXVerts(lxifc.Visitor):
    def __init__(self, point):
        self.point = point
        # BBOX = Max X Y Z, Min X Y Z
        self.points = [[],]

    def get_points(self):
        return list (set (self.points[0]),)

    def vis_Evaluate(self):
        try:
            self.points[0].append (self.point.Pos ())
        except:
            lx.out(traceback.format_exc())

class BBOXVertsConnected(lxifc.Visitor):
    def __init__(self, point, mode_selected_unhideunlockunchecked, mode_checked):
        self.point = point
        self.mode_selected_unhideunlockunchecked = mode_selected_unhideunlockunchecked
        self.mode_checked = mode_checked
        self.points = []

    def get_points(self):
        return self.points

    def vis_Evaluate(self):
        try:
            inner_list = []
            outer_list = []

            outer_list.append (self.point.ID ())

            while len(outer_list) > 0:
                point_ID = outer_list[0]

                self.point.Select (point_ID)
                self.point.SetMarks (self.mode_checked)

                inner_list.append (point_ID)
                outer_list.remove (point_ID)

                num_points = self.point.PointCount ()
                point_points = []
                for p in range(num_points):
                    point_points.append(self.point.PointByIndex (p))

                for next_point_ID in point_points:
                    if next_point_ID not in outer_list and next_point_ID not in inner_list:
                        self.point.Select (next_point_ID)
                        if self.point.TestMarks (self.mode_selected_unhideunlockunchecked):
                            outer_list.append (next_point_ID)

            if len(inner_list) > 1:
                # BBOX = Max X Y Z, Min X Y Z
                points = []
                for point_ID in inner_list:
                    self.point.Select (point_ID)
                    points.append (self.point.Pos ())
                self.points.append (set (points))

        except:
            lx.out(traceback.format_exc())

class BBOXEdges(lxifc.Visitor):
    def __init__(self, edge, point):
        self.edge = edge
        self.point = point
        # BBOX = Max X Y Z, Min X Y Z
        self.points = []

    def get_points(self):
        return list (set (self.points[0]),)

    def vis_Evaluate(self):
        try:
            p1, p2 = self.edge.Endpoints ()

            self.point.Select (p1)
            self.points.append (self.point.Pos ())

            self.point.Select (p2)
            self.points.append (self.point.Pos ())
        except:
            lx.out(traceback.format_exc())

class BBOXEdgesConnected(lxifc.Visitor):
    def __init__(self, edge, point, mode_selected_unhideunlockunchecked, mode_checked):
        self.edge = edge
        self.point = point
        self.mode_selected_unhideunlockunchecked = mode_selected_unhideunlockunchecked
        self.mode_checked = mode_checked
        # BBOX = Max X Y Z, Min X Y Z
        self.points = []

    def get_points(self):
        return self.points

    def vis_Evaluate(self):
        try:
            inner_list = []
            outer_list = []

            outer_list.append (self.edge.ID ())

            while len(outer_list) > 0:
                edge_ID = outer_list[0]

                self.edge.Select (edge_ID)
                self.edge.SetMarks (self.mode_checked)

                inner_list.append (edge_ID)
                outer_list.remove (edge_ID)

                endpoints = self.edge.Endpoints ()

                for endpoint in endpoints:
                    self.point.Select (endpoint)
                    num_edges = self.point.EdgeCount ()
                    for e in range(num_edges):
                        next_edge_ID = self.point.EdgeByIndex (e)
                        if next_edge_ID not in outer_list and next_edge_ID not in inner_list:
                            self.edge.Select (next_edge_ID)
                            if self.edge.TestMarks (self.mode_selected_unhideunlockunchecked):
                                outer_list.append (next_edge_ID)

            if len(inner_list) > 0:
                # BBOX = Max X Y Z, Min X Y Z
                points = []
                for edge_ID in inner_list:
                    self.edge.Select (edge_ID)
                    p1, p2 = self.edge.Endpoints ()

                    self.point.Select (p1)
                    points.append (self.point.Pos ())

                    self.point.Select (p2)
                    points.append (self.point.Pos ())
                self.points.append (set (points))

        except:
            lx.out(traceback.format_exc())

class BBOXPolys(lxifc.Visitor):
    def __init__(self, polygon, point):
        self.polygon = polygon
        self.point = point
        self.points = [[],]

    def get_points(self):
        return list (set (points[0]),)

    def vis_Evaluate(self):
        numPoints = self.polygon.VertexCount ()
        for pp in range(numPoints):
            self.point.Select (self.polygon.VertexByIndex(pp))
            self.points[0].append (self.point.Pos ())

class BBOXPolysConnected(lxifc.Visitor):
    def __init__(self, polygon, point, mode_selected_unhideunlockunchecked, mode_checked):
        self.polygon = polygon
        self.point = point
        self.mode_selected_unhideunlockunchecked = mode_selected_unhideunlockunchecked
        self.mode_checked = mode_checked
        self.points = []

    def get_points(self):
        return self.points

    def vis_Evaluate(self):
        try:
            inner_list = []
            outer_list = []

            outer_list.append (self.polygon.ID ())

            while len(outer_list) > 0:
                polygon_ID = outer_list[0]

                self.polygon.Select (polygon_ID)
                self.polygon.SetMarks (self.mode_checked)

                inner_list.append (polygon_ID)
                outer_list.remove (polygon_ID)

                num_points = self.polygon.VertexCount ()

                for p in range(num_points):
                    self.polygon.Select (polygon_ID)
                    point_ID = self.polygon.VertexByIndex (p)
                    self.point.Select (point_ID)
                    num_polys = self.point.PolygonCount ()
                    for pp in range(num_polys):
                        next_polygon_ID = self.point.PolygonByIndex (pp)
                        if next_polygon_ID not in outer_list and next_polygon_ID not in inner_list:
                            self.polygon.Select (next_polygon_ID)
                            if self.polygon.TestMarks (self.mode_selected_unhideunlockunchecked):
                                outer_list.append (next_polygon_ID)

            if len(inner_list) > 0:
                # BBOX = Max X Y Z, Min X Y Z
                points = []
                for polygon_ID in inner_list:
                    self.polygon.Select (polygon_ID)
                    num_points = self.polygon.VertexCount ()

                    for p in range(num_points):
                        point_ID = self.polygon.VertexByIndex (p)
                        self.point.Select (point_ID)
                        points.append (self.point.Pos ())
                self.points.append (set (points))

        except:
            lx.out(traceback.format_exc())





class CreateBBOX_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__ (self)

        self.dyna_Add ('type', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add ('from', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add ('to', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add ('sides', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(3, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add ('axis', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(4, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add ('accuracy', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(5, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_QUERY)

        self.dyna_Add ('select', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (6, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_QUERY)

    def arg_UIValueHints(self, index):
        if index == 0:
            return OptionPopup(options_bbox_type)
        elif index == 1:
            return OptionPopup(options_bbox_from)
        elif index == 2:
            return OptionPopup(options_bbox_to)
        elif index == 4:
            return OptionPopup(options_bbox_axis)
        elif index == 5:
            return OptionPopup(options_bbox_accuracy)

    def cmd_Query(self,index,vaQuery):
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 0:
            va.AddString(options_bbox_type[0][0])
        elif index == 1:
            va.AddString(options_bbox_from[0][0])
        elif index == 2:
            va.AddString(options_bbox_to[0][0])
        elif index == 3:
            va.AddInt(8)
        elif index == 4:
            va.AddString(options_bbox_axis[0][1])
        elif index == 5:
            va.AddString(options_bbox_accuracy[0][1])
        elif index == 6:
            va.AddInt(1)
        return lx.result.OK

    def cmd_Interact(self):
        # Stop modo complaining.
        pass

    def cmd_UserName(self):
        return 'Create AABB'

    def cmd_Desc(self):
        return 'Creates an AABB box mesh around the current selection.'

    def cmd_Tooltip(self):
        return 'Creates an AABB box mesh around the current selection.'

    def cmd_Help(self):
        return 'http://www.farfarer.com/'

    def basic_ButtonName(self):
        return 'Create AABB'

    def cmd_Flags(self):
        return lx.symbol.fCMD_SELECT | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Label ('Type')
        elif index == 1:
            hints.Label ('Create From')
        elif index == 2:
            hints.Label ('Create To')
        elif index == 3:
            hints.Label ('Sides')
        elif index == 4:
            hints.Label ('Axis')
        elif index == 5:
            hints.Label ('Circumference Accuracy')
        elif index == 6:
            hints.Label ('Select Results')

    # Disable input to certain fields in the options dialog depending on the current choices.
    def cmd_ArgEnable (self, index):
        if index == 1:
            if self.dyna_IsSet (0):
                if self.dyna_String(0) == options_bbox_from[0][2]:
                    lx.throw (lx.symbol.e_CMD_DISABLED)
        elif index == 2:
            if self.dyna_IsSet (1):
                if self.dyna_String(1) == options_bbox_from[0][2]:
                    lx.throw (lx.symbol.e_CMD_DISABLED)
        elif index == 3:
            if self.dyna_IsSet (0):
                if self.dyna_String(0) != options_bbox_type[0][1]:
                    lx.throw (lx.symbol.e_CMD_DISABLED)
        elif index == 4:
            if self.dyna_IsSet (0):
                if self.dyna_String(0) != options_bbox_type[0][1]:
                    lx.throw (lx.symbol.e_CMD_DISABLED)
        elif index == 5:
            if self.dyna_IsSet (0):
                if self.dyna_String(0) != options_bbox_type[0][1]:
                    lx.throw (lx.symbol.e_CMD_DISABLED)
        return lx.symbol.e_OK

# ############################################################################################################################################
# SED STUFF
# ############################################################################################################################################
    # Data conventions: A point is a pair of floats (x, y). A circle is a triple of floats (center x, center y, radius).
    #
    # Returns the smallest circle that encloses all the given points. Runs in expected O(n) time, randomized.
    # Input: A sequence of pairs of floats or ints, e.g. [(0,5), (3.1,-2.7)].
    # Output: A triple of floats representing a circle.
    # Note: If 0 points are given, None is returned. If 1 point is given, a circle of radius 0 is returned.
    #
    def make_circle (self, points):
        # Convert to float and randomize order
        shuffled = [(float (p[0]), float (p[1])) for p in points]
        random.shuffle(shuffled)

        # Progressively add points to circle or recompute circle
        c = None
        for (i, p) in enumerate (shuffled):
            if c is None or not self._is_in_circle (c, p):
                c = self._make_circle_one_point (shuffled[0 : i + 1], p)
        return c


    # One boundary point known
    def _make_circle_one_point (self, points, p):
        c = (p[0], p[1], 0.0)
        for (i, q) in enumerate (points):
            if not self._is_in_circle (c, q):
                if c[2] == 0.0:
                    c = self._make_diameter (p, q)
                else:
                    c = self._make_circle_two_points (points[0 : i + 1], p, q)
        return c


    # Two boundary points known
    def _make_circle_two_points (self, points, p, q):
        diameter = self._make_diameter (p, q)
        if all (self._is_in_circle (diameter, r) for r in points):
            return diameter

        left = None
        right = None
        for r in points:
            cross = self._cross_product (p[0], p[1], q[0], q[1], r[0], r[1])
            c = self._make_circumcircle (p, q, r)
            if c is None:
                continue
            elif cross > 0.0 and (left is None or self._cross_product (p[0], p[1], q[0], q[1], c[0], c[1]) > self._cross_product (p[0], p[1], q[0], q[1], left[0], left[1])):
                left = c
            elif cross < 0.0 and (right is None or self._cross_product (p[0], p[1], q[0], q[1], c[0], c[1]) < self._cross_product (p[0], p[1], q[0], q[1], right[0], right[1])):
                right = c
        return left if (right is None or (left is not None and left[2] <= right[2])) else right


    def _make_circumcircle (self, p0, p1, p2):
        # Mathematical algorithm from Wikipedia: Circumscribed circle
        ax = p0[0]; ay = p0[1]
        bx = p1[0]; by = p1[1]
        cx = p2[0]; cy = p2[1]
        d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
        if d == 0.0:
            return None
        x = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
        y = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
        return (x, y, math.hypot (x - ax, y - ay))


    def _make_diameter (self, p0, p1):
        return ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0, math.hypot (p0[0] - p1[0], p0[1] - p1[1]) / 2.0)

    def _is_in_circle (self, c, p):
        return c is not None and math.hypot (p[0] - c[0], p[1] - c[1]) < c[2] + _EPSILON

    # Returns twice the signed area of the triangle defined by (x0, y0), (x1, y1), (x2, y2)
    def _cross_product (self, x0, y0, x1, y1, x2, y2):
        return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)

# ############################################################################################################################################



    def make_BBOX (self, mesh, points):
        try:
            # Check for silly single verts.
            if len (points) < 2:
                return []

            # Make bbox.
            bbox = [minFloat, minFloat, minFloat, maxFloat, maxFloat, maxFloat]
            for pointPos in points:
                bbox[0] = max (bbox[0], pointPos[0])
                bbox[1] = max (bbox[1], pointPos[1])
                bbox[2] = max (bbox[2], pointPos[2])
                bbox[3] = min (bbox[3], pointPos[0])
                bbox[4] = min (bbox[4], pointPos[1])
                bbox[5] = min (bbox[5], pointPos[2])

            point = lx.object.Point (mesh.PointAccessor ())
            polygon = lx.object.Polygon (mesh.PolygonAccessor ())
            # 0(-X +Y +Z) 1(+X +Y +Z) 2(+X +Y -Z) 3(-X +Y -Z)
            # 4(-X -Y +Z) 5(+X -Y +Z) 6(+X -Y -Z) 7(-X -Y -Z)
            new_points = (
                point.New ((bbox[3], bbox[1], bbox[2])),
                point.New ((bbox[0], bbox[1], bbox[2])),
                point.New ((bbox[0], bbox[1], bbox[5])),
                point.New ((bbox[3], bbox[1], bbox[5])),
                point.New ((bbox[3], bbox[4], bbox[2])),
                point.New ((bbox[0], bbox[4], bbox[2])),
                point.New ((bbox[0], bbox[4], bbox[5])),
                point.New ((bbox[3], bbox[4], bbox[5]))
            )

            polygon_IDs = []

            poly_storage = lx.object.storage ('p', 4)

            # Front
            poly_vert_list = (new_points[4], new_points[5], new_points[1], new_points[0])
            poly_storage.set (poly_vert_list)
            polygon_IDs.append (polygon.New (lx.symbol.iPTYP_FACE, poly_storage, 4, 0))

            # Back
            poly_vert_list = (new_points[6], new_points[7], new_points[3], new_points[2])
            poly_storage.set (poly_vert_list)
            polygon_IDs.append (polygon.New (lx.symbol.iPTYP_FACE, poly_storage, 4, 0))

            # Left
            poly_vert_list = (new_points[5], new_points[6], new_points[2], new_points[1])
            poly_storage.set (poly_vert_list)
            polygon_IDs.append (polygon.New (lx.symbol.iPTYP_FACE, poly_storage, 4, 0))

            # Right
            poly_vert_list = (new_points[3], new_points[7], new_points[4], new_points[0])
            poly_storage.set (poly_vert_list)
            polygon_IDs.append (polygon.New (lx.symbol.iPTYP_FACE, poly_storage, 4, 0))

            # Top
            poly_vert_list = (new_points[0], new_points[1], new_points[2], new_points[3])
            poly_storage.set (poly_vert_list)
            polygon_IDs.append (polygon.New (lx.symbol.iPTYP_FACE, poly_storage, 4, 0))

            # Bottom
            poly_vert_list = (new_points[7], new_points[6], new_points[5], new_points[4])
            poly_storage.set (poly_vert_list)
            polygon_IDs.append (polygon.New (lx.symbol.iPTYP_FACE, poly_storage, 4, 0))

            return polygon_IDs

        except:
            lx.out(traceback.format_exc())
            return []



    def make_AACYL (self, mesh, points, axis_val, sides, accuracy):
        if len (points) < 2:
            return []

        axes = [0, 1, 2]

        point = lx.object.Point (mesh.PointAccessor ())
        polygon = lx.object.Polygon (mesh.PolygonAccessor ())

        # Make bbox.
        bbox = [minFloat, minFloat, minFloat, maxFloat, maxFloat, maxFloat]
        for pointPos in points:
            bbox[0] = max (bbox[0], pointPos[0])
            bbox[1] = max (bbox[1], pointPos[1])
            bbox[2] = max (bbox[2], pointPos[2])
            bbox[3] = min (bbox[3], pointPos[0])
            bbox[4] = min (bbox[4], pointPos[1])
            bbox[5] = min (bbox[5], pointPos[2])

        # Work out auto axes.
        # Try and default to Y - upright - for square bboxes.
        axis = 1
        if axis_val == -1 or axis_val == -2:
            x_size = abs(bbox[0] - bbox[3])
            y_size = abs(bbox[1] - bbox[4])
            z_size = abs(bbox[2] - bbox[5])

            if axis_val == -1:
                # Longest.
                if x_size > y_size:
                    if z_size > y_size:
                        axis = 2
                else:
                    if x_size > z_size:
                        axis = 0
            if axis_val == -2:
                # Shortest.
                if x_size < y_size:
                    if z_size < y_size:
                        axis = 2
                else:
                    if x_size < z_size:
                        axis = 0
        elif axis_val in axes:
            axis = axis_val
        else:
            return []

        axes.remove (axis)

        planar_points = [(p[axes[0]], p[axes[1]]) for p in points]
        circle = self.make_circle (planar_points)


        if accuracy == 'on' or accuracy == 'outside':
            mid_side = (1.0 / sides) * math.pi * 2
            mid_point = ((math.sin (mid_side) * circle[2]) * 0.5, ((math.cos(mid_side) * circle[2]) + circle[2]) * 0.5)
            if accuracy == 'on':
                mid_point = (mid_point[0] * 0.5, (mid_point[1] + circle[2]) * 0.5)
            mid_point_distance = math.sqrt(mid_point[0]**2 + mid_point[1]**2)
            rad_difference_ratio = circle[2] / mid_point_distance
            if accuracy == 'on':
                circle = (circle[0], circle[1], (circle[2] * rad_difference_ratio))
            elif accuracy == 'outside':
                circle = (circle[0], circle[1], (circle[2] * rad_difference_ratio))

        # Work out axis extents.
        axisExtents = (bbox[axis], bbox[(axis+3)])

        # Build the coords for the cylinder.
        circle_points = []
        for s in range(sides):
            side = (float (s) / float (sides)) * math.pi * 2
            circle_point = ((math.sin (side) * circle[2]) + circle[0], (math.cos(side) * circle[2]) + circle[1])
            circle_points.append (circle_point)

        # Build the points for the top and bottom of the cylinder.
        cylinder_points = []
        for axisExtent in axisExtents:
            for circle_point in circle_points:
                point_pos = [0.0, 0.0, 0.0]
                point_pos [axes[0]] = circle_point[0]
                point_pos [axes[1]] = circle_point[1]
                point_pos [axis] = axisExtent
                cylinder_points.append (point.New (point_pos))

        # Build the polygons.
        polygon_IDs = []

        # Top & bottom polygons.
        poly_storage = lx.object.storage ('p', sides)
        polygon_points = []
        for s in range(sides):
            polygon_points.append (cylinder_points[s])
        poly_storage.set (polygon_points)
        polygon_IDs.append (polygon.New (lx.symbol.iPTYP_FACE, poly_storage, sides, 0))

        polygon_points = []
        for s in range(sides):
            polygon_points.append (cylinder_points[(sides+s)])
        polygon_points.reverse ()
        poly_storage.set (polygon_points)
        polygon_IDs.append (polygon.New (lx.symbol.iPTYP_FACE, poly_storage, sides, 0))

        # Side polygons.
        poly_storage = lx.object.storage ('p', 4)
        for s in range(sides):
            polygon_points = []
            polygon_points.append (cylinder_points[((s+1)%sides)])
            polygon_points.append (cylinder_points[(s%sides)])
            polygon_points.append (cylinder_points[((s%sides)+sides)])
            polygon_points.append (cylinder_points[(((s+1)%sides)+sides)])
            poly_storage.set (polygon_points)
            polygon_IDs.append (polygon.New (lx.symbol.iPTYP_FACE, poly_storage, 4, 0))

        return polygon_IDs


    def basic_Execute(self, msg, flags):
        try:
            # Get settings.

            type_aabb = False
            type_aacyl = False
            if self.dyna_IsSet(0):
                type_val = self.dyna_String(0)
                if type_val == options_bbox_type[0][0]:
                    type_aabb = True
                elif type_val == options_bbox_type[0][1]:
                    type_aacyl = True

            per_element = True
            per_layer = True
            if self.dyna_IsSet(1):
                from_val = self.dyna_String(1)
                if from_val == options_bbox_from[0][1]:
                    per_element = False
                elif from_val == options_bbox_from[0][2]:
                    per_element = False
                    per_layer = False

            to_primary = False
            if self.dyna_IsSet(2):
                to_primary = (self.dyna_String(2) == options_bbox_to[0][1])

            sides = 8
            if self.dyna_IsSet(3):
                sides = self.dyna_Int(3)
            sides = max (sides, 3)

            axis = -1
            axes = ('x', 'y', 'z')
            if self.dyna_IsSet(4):
                axis_val = self.dyna_String(4)
                for a in range(len(axes)):
                    if axis_val == axes[a]:
                        axis = a
                        break

            if axis < -2 or axis > 2:
                return

            accuracy = 'on'
            if self.dyna_IsSet(5):
                accuracy_val = self.dyna_String(5)
                if accuracy_val in options_bbox_accuracy[0]:
                    accuracy = accuracy_val

            select_after = True
            if self.dyna_IsSet(6):
                select_after = self.dyna_Bool(6)

            # Grab the active and background layers.
            layer_svc = lx.service.Layer ()
            layer_scan = lx.object.LayerScan (layer_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_EDIT))
            if not layer_scan.test ():
                return

            # Early out if there are no active layers.
            layer_count = layer_scan.Count ()
            if layer_count == 0:
                return

            # Drop polgyon selection.
            selType = lx.eval1('query layerservice selmode ?')

            if select_after:
                sel_svc = lx.service.Selection ()
                polygon_pkts = []

            # Only deal with visible and unlocked verts.
            mesh_svc = lx.service.Mesh ()
            mode = mesh_svc.ModeCompose ('select', 'hide lock')
            mode_selected_unhideunlock = mesh_svc.ModeCompose ('select', 'hide lock')
            mode_selected_unhideunlockunchecked = mesh_svc.ModeCompose ('select', 'hide lock user4')
            mode_checked = mesh_svc.ModeCompose ('user4', None)
            mode_unchecked = mesh_svc.ModeCompose (None, 'user4')

            # Stuff for treating all layers as one.
            master_points = []

            for layer_idx in range(layer_count):
                # Grab the meshes and their point and meshmap accessors.
                mesh = lx.object.Mesh (layer_scan.MeshEdit (layer_idx))
                mesh_base = lx.object.Mesh (layer_scan.MeshBase (layer_idx))
                if not mesh.test () or not mesh_base.test ():
                    continue

                # Early out if there are no points in the active layer.
                point_count = mesh.PointCount ()
                if point_count == 0:
                    continue

                point = lx.object.Point (mesh.PointAccessor ())
                edge = lx.object.Edge (mesh.EdgeAccessor ())
                polygon = lx.object.Polygon (mesh.PolygonAccessor ())
                if not point.test () or not edge.test () or not polygon.test ():
                    continue

                # Find the BBOX of selected verts.
                if selType == 'vertex':
                    if per_element:
                        clearElements = MarkElements (point, mode_unchecked)
                        point.Enumerate (mode_checked, clearElements, 0)

                        visitor = BBOXVertsConnected (point, mode_selected_unhideunlockunchecked, mode_checked)
                        point.Enumerate (mode_selected_unhideunlockunchecked, visitor, 0)

                        point.Enumerate (mode_checked, clearElements, 0)
                    else:
                        visitor = BBOXVerts (point)
                        point.Enumerate (mode, visitor, 0)

                # Find the BBOX of selected edges.
                elif selType == 'edge':
                    if per_element:
                        clearElements = MarkElements (edge, mode_unchecked)
                        edge.Enumerate (mode_checked, clearElements, 0)

                        visitor = BBOXEdgesConnected (edge, point, mode_selected_unhideunlockunchecked, mode_checked)
                        edge.Enumerate (mode_selected_unhideunlockunchecked, visitor, 0)

                        edge.Enumerate (mode_checked, clearElements, 0)
                    else:
                        visitor = BBOXEdges (edge, point)
                        edge.Enumerate (mode, visitor, 0)

                # Find the BBOX of selected polygons.
                elif selType == 'polygon':
                    if per_element:
                        clearElements = MarkElements (polygon, mode_unchecked)
                        polygon.Enumerate (mode_checked, clearElements, 0)

                        visitor = BBOXPolysConnected (polygon, point, mode_selected_unhideunlockunchecked, mode_checked)
                        polygon.Enumerate (mode_selected_unhideunlockunchecked, visitor, 0)

                        polygon.Enumerate (mode_checked, clearElements, 0)
                    else:
                        visitor = BBOXPolys (polygon, point)
                        polygon.Enumerate (mode, visitor, 0)

                for points in visitor.points:
                    if to_primary:
                        master_points.append (points)
                    else:
                        polygon_IDs = []
                        if type_aabb:
                            polygon_IDs += self.make_BBOX (mesh, points)
                        elif type_aacyl:
                            polygon_IDs += self.make_AACYL (mesh, points, axis, sides, accuracy)
                        if select_after:
                            for polygon_ID in polygon_IDs:
                                polygon_pkts.append ((polygon_ID, mesh_base))

                    layer_scan.SetMeshChange (layer_idx, lx.symbol.f_MESHEDIT_GEOMETRY)

            layer_scan.Apply()

            if to_primary:
                # Not applying per layer, so create one master bbox on the primary layer.
                layer_scan_primary = lx.object.LayerScan (layer_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_PRIMARY | lx.symbol.f_LAYERSCAN_WRITEMESH))
                if layer_scan_primary.test ():
                    layer_count_primary = layer_scan_primary.Count ()
                    if layer_count_primary > 0:
                        mesh_primary = lx.object.Mesh (layer_scan_primary.MeshEdit (0))
                        mesh_base_primary = lx.object.Mesh (layer_scan_primary.MeshBase (0))

                        polygon_IDs = []
                        if per_element:
                            # Creating one bbox for each element layers.
                            for points in master_points:
                                if type_aabb:
                                    polygon_IDs += self.make_BBOX (mesh_primary, points)
                                elif type_aacyl:
                                    polygon_IDs += self.make_AACYL (mesh_primary, points, axis, sides, accuracy)
                        else:
                            # Creating one bbox for all elements.
                            points = [point for points in master_points for point in points]
                            if type_aabb:
                                polygon_IDs += self.make_BBOX (mesh_primary, points)
                            elif type_aacyl:
                                polygon_IDs += self.make_AACYL (mesh_primary, points, axis, sides, accuracy)


                        if select_after:
                            for polygon_ID in polygon_IDs:
                                polygon_pkts.append ((polygon_ID, mesh_base_primary))

                        layer_scan_primary.SetMeshChange (0, lx.symbol.f_MESHEDIT_GEOMETRY)
                layer_scan_primary.Apply()

            if select_after and len(polygon_pkts) > 0:
                sel_type_polygon = sel_svc.LookupType (lx.symbol.sSELTYP_POLYGON)
                sel_svc.Drop (sel_type_polygon)
                poly_pkt_trans = lx.object.PolygonPacketTranslation (sel_svc.Allocate(lx.symbol.sSELTYP_POLYGON))
                sel_svc.StartBatch ()
                for polygon_pkt in polygon_pkts:
                    sel_svc.Select (sel_type_polygon, poly_pkt_trans.Packet (polygon_pkt[0], polygon_pkt[1]))
                sel_svc.EndBatch ()
        except:
            lx.out(traceback.format_exc())

lx.bless(CreateBBOX_Cmd, 'ffr.createAABB')