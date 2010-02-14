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
Hildon UI. Import widget.
"""

import mnemosyne.maemo_ui.widgets.tags as widgets
from mnemosyne.maemo_ui.widgets.importcards import \
    create_importcard_ui, show_filechooser_dialog
from mnemosyne.libmnemosyne.ui_component import UiComponent


class ImportCardsWidget(UiComponent):
    """Import Widget."""

    def __init__(self, component_manager ):
        UiComponent.__init__(self, component_manager)
        self.formats = [desc.description for desc in \
            self.component_manager.get_all("file_format")]
        # create widgets 
        self.page, self.switcher, self.format_label, self.format_button, \
            self.tags_box, self.tags_button, self.tags_name_label, \
            self.file_chooser_button, self.file_name_label, \
            self.menu_button, self.convert_button, self.format_prev_button, \
            self.format_next_button, new_tag_button, self.new_tag_entry = \
            create_importcard_ui(self.main_widget().switcher, \
            self.component_manager.get_current("file_format").description)
        self.tags_mode = False
        self.selected_tags = [u"<default>"]
        self.fname = None
        # connect signals
        self.format_prev_button.connect('clicked', self.change_format_cb)
        self.format_next_button.connect('clicked', self.change_format_cb)
        self.menu_button.connect('clicked', self.back_to_main_menu_cb)
        self.file_chooser_button.connect('clicked', self.choose_file_cb)
        self.tags_button.connect('clicked', self.show_tags_dialog_cb)
        self.convert_button.connect('clicked', self.convert_cb)
        new_tag_button.connect('clicked', self.add_new_tag_cb)
        # update widgets content
        self.tags_name_label.set_text('Tags for new cards: <default>')

    def activate(self):
        """Set necessary switcher page."""

        self.main_widget().switcher.set_current_page(self.page)

    def activate_widgets(self, enable=False):
        """Disable or enable all widgets."""

        self.format_prev_button.set_sensitive(enable)
        self.format_next_button.set_sensitive(enable)
        self.format_button.set_sensitive(enable)
        self.file_chooser_button.set_sensitive(enable)
        self.convert_button.set_sensitive(enable)
        self.menu_button.set_sensitive(enable)

    def add_new_tag_cb(self, widget):
        """Create new tag."""

        new_tag = self.new_tag_entry.get_text()
        box_tags = [hbox.get_children()[1].get_label() for \
            hbox in self.tags_box.get_children()]
        if new_tag and not new_tag in box_tags:
            tag_widget = widgets.create_tag_checkbox(new_tag, True)
            self.tags_box.pack_start(tag_widget)
            self.tags_box.reorder_child(tag_widget, 0)
            self.new_tag_entry.set_text("")

    def choose_file_cb(self, widget):
        """Show FileChooser dialog."""

        fname = show_filechooser_dialog(self.main_widget().window)
        if fname:
            self.fname = fname
            self.file_name_label.set_text(self.fname)
            self.convert_button.set_sensitive(True)

    def show_tags_dialog_cb(self, widget):
        """Show Tags dialog."""

        self.tags_mode = True
        tags_box = self.tags_box
        self.switcher.set_current_page(1)
        for child in tags_box.get_children():
            tags_box.remove(child)
        for tag in self.database().get_tags():
            tag = widgets.create_tag_checkbox(unicode(tag.name), \
                tag.name in self.selected_tags)
            tags_box.pack_start(tag)
        if not tags_box.get_children():
            tag = widgets.create_tag_checkbox(u"<default>", True)
            tags_box.pack_start(tag)

    def hide_tags_dialog(self):
        """Close Tags dialog."""

        self.tags_mode = False
        self.selected_tags = []
        for hbox in self.tags_box.get_children():
            children = hbox.get_children()
            if children[0].get_active():
                self.selected_tags.append(unicode(children[1].get_label()))
        if not self.selected_tags:
            self.selected_tags = [u"<default>"]
        self.tags_name_label.set_text(\
            'Tags for new cards: ' + ', '.join(self.selected_tags))
        self.switcher.set_current_page(0)

    def convert_cb(self, widget):
        """Convert file to database."""

        self.activate_widgets(False)

        for format in self.component_manager.get_all("file_format"):
            if format.description == self.format_label.get_text():
                try:
                    format.do_import(self.fname, self.selected_tags)
                except:
                    self.main_widget().error_box( \
                        'Oops! Maybe you selected wrong format?')
                break

        self.activate_widgets(True)
        self.convert_button.set_sensitive(False)
        self.file_name_label.set_text( \
            'Press to select file to import from ...')
        self.fname = None
        self.scheduler().rebuild_queue()
        review_controller = self.review_controller()
        review_controller.reload_counters()
        review_controller.new_question()

    def change_format_cb(self, widget):
        """Changes current format file."""

        format_index = self.formats.index(self.format_label.get_text())
        direction = 1
        if widget == self.format_prev_button:
            direction = -1
        try:
            new_format = self.formats[format_index + direction]
        except IndexError:
            if direction:
                new_format = self.formats[0]
            else:
                new_format = self.formats[-1]
        finally:
            self.format_label.set_text(new_format)

    def back_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        if self.tags_mode:
            self.hide_tags_dialog()
        else:
            self.main_widget().switcher.remove_page(self.page)
            self.main_widget().menu_('importcards')

