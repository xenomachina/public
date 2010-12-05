#! /usr/bin/env python

import cairo
import pygtk
pygtk.require('2.0')
import gtk

def draw(cr, width, height):
  # Fill background with black
  cr.set_source_rgb(0, 0, 0)
  cr.rectangle(0, 0, width, height)
  cr.fill()

  # draw something
  cr.set_source_rgb(0.0, 0.7, 0.5)
  steps = float(min(width, height) / 16)
  for i in range(int(steps)):
    cr.move_to(width / steps * i, 0)
    cr.line_to(0, height - (height / steps * i))
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
