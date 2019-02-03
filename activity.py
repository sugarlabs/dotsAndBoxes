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


import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk
import sugargame.canvas

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.colorbutton import ColorToolButton
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.graphics.toolbutton import ToolButton

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

        # toolbars
        self.build_size_toolbar(toolbar_box)
        self.build_colors_toolbar(toolbar_box)

        # new game button
        new_game = ToolButton('new-game')
        new_game.connect('clicked', self._new_game)
        new_game.set_tooltip(_('New game'))
        toolbar_box.toolbar.insert(new_game, -1)

        separator = Gtk.SeparatorToolItem()
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        #current
        item = Gtk.ToolItem()
        label = Gtk.Label()
        label.set_text(' %s ' % _('Current player:'))
        item.add(label)
        toolbar_box.toolbar.insert(item, -1)

        #player
        item = Gtk.ToolItem()
        self.current_label = Gtk.Label()
        self.current_label.set_text(' %s ' % _('Player 1'))
        item.add(self.current_label)
        toolbar_box.toolbar.insert(item, -1)

        # end separator
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.show_all()

    def build_size_toolbar(self, toolbox):

        size_bar = Gtk.Toolbar()

        #Horizontal
        item1 = Gtk.ToolItem()
        label1 = Gtk.Label()
        label1.set_text(' %s ' % _('H'))
        item1.add(label1)
        size_bar.insert(item1, -1)

        item2 = Gtk.ToolItem()
        self.h_spin = Gtk.SpinButton()
        self.h_spin.set_range(2, 30)
        self.h_spin.set_increments(1, 2)
        self.h_spin.props.value = self.game_size[0]
        self.h_spin.connect('notify::value', self.h_spin_change)
        item2.add(self.h_spin)
        size_bar.insert(item2, -1)

        #Vertical
        item3 = Gtk.ToolItem()
        label2 = Gtk.Label()
        label2.set_text(' %s ' % _('V'))
        item3.add(label2)
        size_bar.insert(item3, -1)

        item4 = Gtk.ToolItem()
        self.v_spin = Gtk.SpinButton()
        self.v_spin.set_range(2, 20)
        self.v_spin.set_increments(1, 2)
        self.v_spin.props.value = self.game_size[1]
        self.v_spin.connect('notify::value', self.v_spin_change)
        item4.add(self.v_spin)
        size_bar.insert(item4, -1)

        size_bar.show_all()
        size_button = ToolbarButton(label=_('Board size'),
                page=size_bar,
                icon_name='preferences-system')
        toolbox.toolbar.insert(size_button, -1)
        size_button.show()

    def build_colors_toolbar(self, toolbox):

        colors_bar = Gtk.Toolbar()

        ########################################################################
        # Point color
        item = Gtk.ToolItem()
        label = Gtk.Label()
        label.set_text('%s ' % _('Points'))
        item.add(label)
        colors_bar.insert(item, -1)

        # select color
        item = Gtk.ToolItem()
        fill_color = ColorToolButton()
        fill_color.connect('notify::color', self.color_point_change)
        item.add(fill_color)
        colors_bar.insert(item, -1)

        # Separator
        separator = Gtk.SeparatorToolItem()
        colors_bar.insert(separator, -1)
        separator.show()

        ########################################################################
        # Back color
        item = Gtk.ToolItem()
        label = Gtk.Label()
        label.set_text('%s ' % _('Background'))
        item.add(label)
        colors_bar.insert(item, -1)

        # select color
        item = Gtk.ToolItem()
        _fill_color = ColorToolButton()
        c = Gdk.Color(red=21588, green=47546, blue=18504)
        _fill_color.set_color(c)
        _fill_color.connect('notify::color', self.color_back_change)
        item.add(_fill_color)
        colors_bar.insert(item, -1)

        # Separator
        separator = Gtk.SeparatorToolItem()
        colors_bar.insert(separator, -1)
        separator.show()

        ########################################################################
        # Line color
        item = Gtk.ToolItem()
        label = Gtk.Label()
        label.set_text('%s ' % _('Lines'))
        item.add(label)
        colors_bar.insert(item, -1)

        # select color
        item = Gtk.ToolItem()
        _fill_color = ColorToolButton()
        _fill_color.connect('notify::color', self.color_line_change)
        item.add(_fill_color)
        colors_bar.insert(item, -1)

        # Separator
        separator = Gtk.SeparatorToolItem()
        colors_bar.insert(separator, -1)
        separator.show()

        ########################################################################
        # Owner color
        item = Gtk.ToolItem()
        label = Gtk.Label()
        label.set_text('%s ' % _('Owner'))
        item.add(label)
        colors_bar.insert(item, -1)

        # select color
        item = Gtk.ToolItem()
        _fill_color = ColorToolButton()
        c = Gdk.Color(red=65535, green=0, blue=0)
        _fill_color.set_color(c)
        _fill_color.connect('notify::color', self.color_owner_change)
        item.add(_fill_color)
        colors_bar.insert(item, -1)

        colors_bar.show_all()
        colors_button = ToolbarButton(label=_('Colors'),
                page=colors_bar,
                icon_name='toolbar-colors')
        toolbox.toolbar.insert(colors_button, -1)
        colors_button.show()

    def h_spin_change(self, spin, value):
        self.game_size = (int(spin.props.value) + 1, self.game_size[1])
        self.game.set_board_size(self.game_size)

    def v_spin_change(self, spin, value):
        self.game_size = (self.game_size[0], int(spin.props.value) + 1)
        self.game.set_board_size(self.game_size)

    def h_spin_set_max(self, value):
        self.h_spin.set_range(2, value)

    def v_spin_set_max(self, value):
        self.v_spin.set_range(2, value)

    def color_point_change(self, widget, pspec):
        color = widget.get_color()
        new_color = self.color_to_rgb(color)
        self.game.set_point_color(new_color)

    def color_back_change(self, widget, pspec):
        color = widget.get_color()
        new_color = self.color_to_rgb(color)
        self.game.set_back_color(new_color)

    def color_line_change(self, widget, pspec):
        color = widget.get_color()
        new_color = self.color_to_rgb(color)
        self.game.set_line_color(new_color)

    def color_owner_change(self, widget, pspec):
        color = widget.get_color()
        new_color = self.color_to_rgb(color)
        self.game.set_owner_color(new_color)

    def color_to_rgb(self, color):
        r = color.red *255 / 65536
        g = color.green *255 / 65536
        b = color.blue *255 / 65536
        return (r, g, b)

    def set_current_player(self, player):
        if player == 'A':
            self.current_label.set_text(' %s ' % _('Player 1'))
        else:
            self.current_label.set_text(' %s ' % _('Player 2'))

    def _new_game(self, widget):
        self.game.draw_grid()

    def read_file(self, file_path):
        pass

    def write_file(self, file_path):
        pass

