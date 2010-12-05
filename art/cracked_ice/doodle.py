#! /usr/bin/env python

import cairo
import pygtk
pygtk.require('2.0')
import gtk

import random
import math
import voronoi

class Struct(object):
  def __init__(self, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)
    self.__keys = kwargs.keys()
    self.__hash = None

  def __eq__(self, other):
    return all((getattr(self, k) == getattr(other, k) for k in self.__keys))

  def __ne__(self, other):
    return not (self == other)

  def __hash__(self):
    if self.__hash is None:
      result = 0
      for k in self.__keys:
        result ^= hash(getattr(self, k))
      self.__hash = result
    return self.__hash

def draw(cr, width, height):
  cr.set_line_cap(cairo.LINE_CAP_ROUND)
  # Fill background with black
  cr.set_source_rgb(0, 0, 0)
  cr.rectangle(0, 0, width, height)
  cr.fill()

  # draw something
  cr.set_source_rgb(1, 1, 1)

  num_points = width * height / 32 / 32
  # TODO: comment out
  num_points = 100

  # Randomly choose points
  points = set()
  for i in range(num_points):
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    points.add(Struct(x=x, y=y))

    cr.move_to(x, y)
    cr.close_path()
    cr.stroke()
  points = list(points)

  # Spread points out using inverse-square repulsion
  for _ in range(num_points * num_points):
    i = random.randint(0, num_points - 1)
    point = points[i]
    force = [0, 0]
    for j in range(num_points):
      if j != i:
        other = points[j]
        dist = float(math.hypot(other.x - point.x, other.y - point.y))
        other_force = 1.0 / float(dist * dist)
        other_force = [
          (point.x - other.x) / dist * other_force,
          (point.y - other.y) / dist * other_force]
        force[0] += other_force[0]
        force[1] += other_force[1]
    point.x += force[0] * 1000.0
    point.y += force[1] * 1000.0

  # Draw new points
  cr.set_source_rgb(0, 0, 1)
  for point in points:
    cr.move_to(point.x, point.y)
    cr.close_path()
    cr.stroke()

  # render voronoi diagram for points
  vpoints, vlines, vedges = voronoi.computeVoronoiDiagram(points)
  for l, p1, p2 in vedges:
    cr.set_source_rgb(1, 0, 0)
    if min(p1, p2) >= 0:
      p1 = vpoints[p1]
      p2 = vpoints[p2]
      if (p1[0] < 0 or p1[0] > width
          or p2[0] < 0 or p2[0] > width
          or p1[1] < 0 or p1[1] > height
          or p2[1] < 0 or p2[1] > height):
        cr.set_source_rgb(0, 1, 0)
      cr.move_to(*p1)
      cr.line_to(*p2)
      cr.stroke()


class Canvas(gtk.DrawingArea):
  __gsignals__ = { "expose-event": "override" }

  def do_expose_event(self, event):
    cr = self.window.cairo_create()
    area = event.area
    cr.rectangle(area.x, area.y, area.width, area.height)
    cr.clip()
    draw(cr, *self.window.get_size())

def renderWindow(Widget, size):
  window = gtk.Window()
  new_size = []
  def quit(*args):
    new_size.append(window.get_size())
    gtk.main_quit(*args)
  window.set_default_size(*size)
  window.connect("delete-event", quit)
  widget = Widget()
  widget.show()
  window.add(widget)
  window.present()
  gtk.main()
  return new_size[0]

def renderSvg(fnam, size):
  s1 = cairo.SVGSurface(fnam, *size)
  draw(cairo.Context(s1), *size)
  s1.finish()

if __name__ == "__main__":
  size = renderWindow(Canvas, (640, 480))
  renderSvg("image.svg", size)
