#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Boxes
# Copyright (C) 2013 Alan Aguiar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Alan Aguiar <alanjas@gmail.com>

import sys
import gtk
import pygame
import sugargame.canvas

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton
from sugar.graphics.toolbutton import ToolButton
from sugar.activity.widgets import StopButton

from gettext import gettext as _

import main


class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.game_size = (8, 6)
        self.game = main.Game(self)
        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()
        self._pygamecanvas.run_pygame(self.game.run)

    def build_toolbar(self):

        self.max_participants = 1

        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        item1 = gtk.ToolItem()
        label1 = gtk.Label()
        label1.set_text(_('Horizontal'))
        item1.add(label1)
        toolbar_box.toolbar.insert(item1, -1)

        item2 = gtk.ToolItem()
        h_spin = gtk.SpinButton()
        h_spin.set_range(2, 30)
        h_spin.set_increments(1, 2)
        h_spin.props.value = 5
        h_spin.connect('notify::value', self.h_spin_change)
        item2.add(h_spin)
        toolbar_box.toolbar.insert(item2, -1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.show_all()

    def h_spin_change(self, spin, value):
        self.game_size = (int(spin.props.value), self.game_size[1])
        self.game.set_board_size(self.game_size)

    def read_file(self, file_path):
        pass

    def write_file(self, file_path):
        pass

