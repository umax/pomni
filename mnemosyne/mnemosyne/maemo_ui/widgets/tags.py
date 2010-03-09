#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai
#
# Mnemosyne. Learning tool based on spaced repetition technique
#
# Copyright (C) 2008 Pomni Development Team <pomni@googlegroups.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
#

"""
Hildon UI. Widgets for Tags mode.
"""

import gtk
import hildon


def create_tags_ui(database):
    """Creates TagsWidget UI."""

    window = hildon.StackableWindow()
    window.set_title(unicode("Tags mode"))

    # create AppMenu
    menu = hildon.AppMenu()
    button_stats = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "Tags statistics")
    menu.append(button_stats)
    menu.show_all()

    selector = hildon.TouchSelector(text=True)
    tags_dict = {}

    # fill tags list
    tags_names = []
    for tag in database.get_tags():
        tags_dict[tag.name] = tag._id
        tags_names.append(tag.name)
        cards_count = database.total_card_count_for__tag_id(tag._id)
        selector.append_text(unicode(tag.name + " (%s cards)" % cards_count))

    if tags_names:
        if len(tags_names) > 1:
            selector.set_column_selection_mode( \
                hildon.TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)
            #mark active tags
            selector.unselect_all(0)
            model = selector.get_model(0)
            criterion = database.current_activity_criterion()
            for i in range(len(tags_names)):
                if tags_dict[tags_names[i]] in criterion.active_tag__ids:
                    selector.select_iter(0, model.get_iter(i), False)
        window.add(selector)
    else:
        label = gtk.Label('There are no tags')
        window.add(label)
              
    window.set_app_menu(menu)
    window.show_all()
    
    return window, selector, button_stats, tags_dict
