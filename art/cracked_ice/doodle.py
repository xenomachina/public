#! /usr/bin/env python

import cairo
import pygtk
pygtk.require('2.0')
import gtk

import random
import math
import voronoi
from itertools import *

def theta(p1, p2) :
  p1x, p1y = p1
  p2x, p2y = p2
  dy = p2y - p1y
  if dy == 0:
    if p2x > p1x:
      return 0.0
    else:
      return math.pi
  else:
    result = -math.atan((p2x - p1x) / (p2y - p1y))
    if p2y > p1y:
      result += math.pi * 0.5
    else:
      result += math.pi * 1.5
  return result

tau = math.pi * 2.0
def normangle(th):
  while th >= tau:
    th -= tau
  while th < 0:
    th += tau
  return th

def distance(p1, p2):
  return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def dot(a, b):
  return sum((a * b for a, b in zip(a,b)))

def inside(p, topleft, bottomright):
  return (p[0] >= topleft[0]
       or p[0] < bottomright[0]
       or p[1] >= topleft[1]
       or p[1] < bottomright[1])

def vec_add(p1, p2):
  return tuple(a + b for a, b in zip(p1, p2))

def vec_sub(p1, p2):
  return tuple(a - b for a, b in zip(p1, p2))

def vec_mul(n, v):
  return tuple((n * ve for ve in v))

def project_on_segment(p0, p1, p2):
  seg_vec = vec_sub(p2, p1)
  seg_len = distance(p2, p1)
  t = dot(vec_sub(p0, p1), seg_vec) / seg_len / seg_len
  return vec_add(p1, vec_mul(t, seg_vec))

class Doodle(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.size = (width, height)

    spacing = 50
    num_points = ((width * 3 ) * (height * 3) / spacing / spacing)

    # Randomly choose points
    corners = [
      (0,0),
      (0, width - 1),
      (height - 1, width - 1),
      (height - 1, 0),
    ]
    points = set(corners)
    for _ in range(int(num_points * 5)):
      new_p = (random.randint(- width, width * 2),
          random.randint(- width, height * 2))
      if all((distance(new_p, p) > spacing for p in points)):
        points.add(new_p)
        print num_points - len(points)
      else:
        print '*',
    for corner in corners:
      points.remove(corner)
    points = list(points)
    points.extend(corners)
    num_points = len(points)

#    # Spread points out using inverse-square repulsion
#    multiplier = 1500.0
#    steps = int(num_points ** 2)
#    multiplier_step = 1.0 / steps
#    for _ in range(steps):
#      i = random.randint(0, num_points - 1 - len(corners))
#      point = points[i]
#      force = [0, 0]
#      for j in range(num_points):
#        if j != i:
#          other = points[j]
#          dist = float(distance(point, other))
#          other_force = 1.0 / float(dist * dist)
#          other_force = (
#            (point[0] - other[0]) / dist * other_force,
#            (point[1] - other[1]) / dist * other_force)
#          force[0] += other_force[0]
#          force[1] += other_force[1]
#      points[i] = (
#          point[0] + force[0] * multiplier,
#          point[1] + force[1] * multiplier)
#      multiplier -= multiplier_step
#    self.points = points

    # Generate voronoi diagram for points
    self.vpoints, self.vlines, self.vedges = voronoi.computeVoronoiDiagram(points)

    # # Generate Delaunay triangulation. Turns out that this doesn't
    # # look nearly as nice.
    # triangles = voronoi.computeDelaunayTriangulation(points)
    # self.vpoints = points
    # self.vedges = []
    # for a, b, c in triangles:
    #   self.vedges.append((None, a, b))
    #   self.vedges.append((None, b, c))
    #   self.vedges.append((None, c, a))

    # generate adjacency mapping
    adjacency_map = {}
    def addNeighbor(k, v):
      pk = self.vpoints[k]
      pv = self.vpoints[v]
      if inside(pk, vec_mul(-.5, self.size), vec_mul(1.5, self.size)):
        adjacency_map.setdefault(k, set()).add(v)
    for l, p1, p2 in self.vedges:
      addNeighbor(p1, p2)
      addNeighbor(p2, p1)

    # straighten edges
    npoints = self.vpoints[:]
    straigtenings = [0] * len(npoints)
    spaz = [0.0] * len(npoints)
    todo = set(adjacency_map.keys())
    spaz = []
    for _ in range(len(todo) ** 2):
      if not todo: break
      try:
        i = random.choice(tuple(todo))
        todo.remove(i)
        best = math.pi

        # Straighten any angle, even those that cut across another
        # angle. This can sometimes cause "straightening of the cross"
        neighbors = tuple(adjacency_map[i])
        for j in neighbors:
          for k in neighbors:
            if j == k: continue

#        # Straighten angles only between neighbors that are "adjacent"
#        # when going around the circle. ie: "pie slice" angles.
#        neighbors = list(adjacency_map[i])
#        neighbors.sort(key=lambda x:normangle(theta(npoints[i], npoints[x])))
#        neighbors = tuple(neighbors)
#        for j_idx, j in enumerate(neighbors):
#          for k_idx in ((j_idx +1) % len(neighbors)), ((j_idx - 1) % len(neighbors)):
#            k = neighbors[k_idx]

            th_j = theta(npoints[i], npoints[j])
            th_k = theta(npoints[i], npoints[k])
            bent = abs(normangle(th_j - th_k) - math.pi)
            if bent < best:
              best = bent
              best_j = j
              best_k = k

#        # Straighten random angle
#        neighbors = tuple(adjacency_map[i])
#        best_j, best_k = random.sample(neighbors, 2)

        new_point = project_on_segment(npoints[i], npoints[best_j], npoints[best_k])
        if distance(new_point, npoints[i]) > 0.1:
          straigtenings[i] += 1
          npoints[i] = new_point
          for neighbor in neighbors:
            if neighbor in adjacency_map:
              todo.add(neighbor)
          print len(todo)
      except KeyboardInterrupt:
        break
    self.npoints = npoints
    self.straigtenings = straigtenings
    self.todo = todo

  def draw(self, cr):
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    # Fill background with white
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(0, 0, self.width, self.height)
    cr.fill()

#    # Draw triangles
#    cr.set_source_rgb(.5, .5, 0)
#    for p0, p1, p2 in self.spaz:
#      p0 = self.vpoints[p0]
#      p1 = self.vpoints[p1]
#      p2 = self.vpoints[p2]
#      cr.move_to(*p0)
#      cr.line_to(*p1)
#      cr.line_to(*p2)
#      cr.close_path()
#      cr.fill()

#    # Draw points
#    cr.set_source_rgb(1, 1, 1)
#    for point in self.points:
#      cr.move_to(*point)
#      cr.close_path()
#      cr.stroke()

#    # Render discs
#    for i, p, r in izip(range(len(self.npoints)), self.npoints, self.straigtenings):
#      if r:
#        if i in self.todo:
#          cr.set_source_rgb(.9, .7, .7)
#        else:
#          cr.set_source_rgb(.7, .9, .7)
#        cr.new_sub_path()
#        cr.arc(p[0], p[1], math.sqrt(r) * 2.0, 0, tau)
#        cr.close_path()
#        cr.fill()
#    cr.new_sub_path()

    # Render voronoi diagram
    #self.draw_mesh(cr, self.vedges, self.vpoints, (1,1,.5), (.5,1,.5))
    self.draw_mesh(cr, self.vedges, self.npoints)

  def draw_mesh(self, cr, edges, points, color1=(0,0,0), color2=(1,0,0)):
    for l, p1, p2 in edges:
      if min(p1, p2) >= 0:
        p1 = points[p1]
        p2 = points[p2]
        if (inside(p1, (0, 0), self.size)
            and inside(p2, (0, 0), self.size)):
          cr.set_source_rgb(*color1)
        else:
          cr.set_source_rgb(*color2)
        cr.move_to(*p1)
        cr.line_to(*p2)
        cr.stroke()

class Canvas(gtk.DrawingArea):
  def __init__(self, doodle):
    gtk.DrawingArea.__init__(self)
    self.doodle = doodle

  __gsignals__ = { "expose-event": "override" }

  def do_expose_event(self, event):
    cr = self.window.cairo_create()
    area = event.area
    cr.rectangle(area.x, area.y, area.width, area.height)
    cr.clip()
    doodle.draw(cr)

def renderWindow(Widget, doodle):
  window = gtk.Window()
  window.set_default_size(doodle.width, doodle.height)
  window.connect("delete-event", gtk.main_quit)
  widget = Widget(doodle)
  widget.show()
  window.add(widget)
  window.present()
  gtk.main()

def renderSvg(fnam, doodle):
  s1 = cairo.SVGSurface(fnam, doodle.width, doodle.height)
  cr = cairo.Context(s1)
  cr.rectangle(0, 0, doodle.width, doodle.height)
  cr.clip()
  doodle.draw(cr)
  s1.finish()

if __name__ == "__main__":
  #doodle = Doodle(1280, 960)
  doodle = Doodle(640, 480)
  renderWindow(Canvas, doodle)
  renderSvg("image.svg", doodle)
