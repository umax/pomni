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
Hildon UI. Review widget.
"""

from mnemosyne.libmnemosyne.ui_components.review_widget import ReviewWidget
import mnemosyne.maemo_ui.widgets.review as widgets
from mnemosyne.maemo_ui import tts

LARGE_CONTAINER_HEIGHT = 140

class ReviewWdgt(ReviewWidget):
    """Review Widget."""

    def __init__(self, component_manager):
        ReviewWidget.__init__(self, component_manager)
        self._main_widget = self.main_widget()
        self._review_controller = self.review_controller()
        self.renderer = self.component_manager.get_current('renderer')
        self.tts = None
        self.sndtext = None
        self.is_sound_card = False
        # create widgets
        self.window, self.question_text, self.answer_text, \
        self.grades_table, grades, button_stats, self.tts_button, \
        self.edit_button, self.del_button = widgets.create_review_ui()
        self.tts_available = tts.is_available()
        self.tts_button.set_sensitive(False)
        # connect signals
        self.question_text.connect('button-press-event', \
            self.preview_sound_in_review_cb)
        self.answer_text.connect('button-press-event', self.get_answer_cb)
        for grade_button in grades:
            grade_button.connect('clicked', self.grade_cb)
        button_stats.connect('clicked', self.statistics_card_cb)
        self.tts_button.connect('clicked', self.speak_cb)
        self.edit_button.connect('clicked', self.edit_card_cb)
        self.del_button.connect('clicked', self.delete_card_cb)
        self.window.connect("delete-event", self.review_to_main_menu_cb)

    def activate(self):
        """Set necessary switcher page."""

        # move Review window to the top of windows stack
        self.window.show_all()

    def enable_edit_current_card(self, enabled):
        """Enable or disable 'Edit card' button."""

        self.edit_button.set_sensitive(enabled)

    def enable_delete_current_card(self, enabled):
        """Enable or disable 'Delete card' button."""

        self.del_button.set_sensitive(enabled)

    def set_question(self, text):
        """Set question text."""

        print 'set_question'
        self.tts_button.set_sensitive(False)
        self.is_sound_card = False
        self.question_text.set_size_request(-1, -1)
        if "sound src=" in text:
            self.sndtext = text
            self.is_sound_card = True
            self.renderer.render_sound_hint(self.question_text)
            self._main_widget.soundplayer.play(self.sndtext, self)
        else:
            if "img src=" in text:
                self.question_text.set_size_request( \
                    -1, LARGE_CONTAINER_HEIGHT)
            else:
                self.tts_button.set_sensitive(self.tts_available)
            self.renderer.render_html(self.question_text, text)
        tags = [tag.name for tag in self._review_controller.card.tags]
        self.window.set_title("Card tags: " + ', '.join(tags))

    def set_answer(self, text):
        """Set answer text."""

        self.renderer.render_html(self.answer_text, text)

    def clear_question(self): 
        """Clear question text."""

        self.window.set_title("No tags")
        self.tts_button.set_sensitive(False)
        self.renderer.render_html(self.question_text)

    def clear_answer(self):
        """Clear answer text."""

        self.renderer.render_html(self.answer_text)

    def update_show_button(self, text, default, enabled): 
        """Update Show button."""

        self.answer_text.set_sensitive(enabled)
        if enabled:
            self.renderer.render_hint(self.answer_text, text)

    def enable_grades(self, enabled):
        """Enable grades."""

        self.grades_table.set_sensitive(enabled)
        self.enable_edit_current_card(enabled)
        self.enable_delete_current_card(enabled)


    # callbacks
    def speak_cb(self, widget):
        """Hook for 'Speak' button."""

        config = self.config()
        params = {"language": config['tts_language'], "voice": \
            config['tts_voice'], "speed": config['tts_speed'], \
            "pitch": config['tts_pitch']}
        if not self.tts:            
            self.tts = tts.TTS(params['language'], params['voice'], 
                params['pitch'], params['speed'])
        self.tts.set_params(params)
        self.tts.speak(self.renderer.tts_text)

    def preview_sound_in_review_cb(self, widget, event):
        """Hook for 'Play sound' button."""

        if self.is_sound_card:
            self.renderer.render_sound_hint(self.question_text)
            if self._main_widget.soundplayer.stopped():
                self._main_widget.soundplayer.play(self.sndtext, self)
            else:
                self._main_widget.soundplayer.stop()

    def review_to_main_menu_cb(self, widget, event):
        """Hook for 'Main menu' button."""

        # redefine 'delete-event'.
        # Hide window instead of destroying it
        self._main_widget.soundplayer.stop()
        widget.emit_stop_by_name('delete-event')
        widget.hide()
        return True

    def get_answer_cb(self, widget, event):
        """Hook for 'Show answer' button."""

        self._review_controller.show_answer()

    def statistics_card_cb(self, widget):
        """Hook for 'Statistics' button."""

        self.config()["last_variant_for_statistics_page"] = 0
        self.controller().show_statistics()

    def delete_card_cb(self, widget):
        """Hook for 'Delete card' button."""

        self._main_widget.soundplayer.stop()
        self.controller().delete_current_fact()

    def edit_card_cb(self, widget):
        """Hook for 'Edit card' button."""

        self._main_widget.soundplayer.stop()
        self.component_manager.get_current("edit_fact_dialog")\
            (self.component_manager).activate()

    def grade_cb(self, widget):
        """Hook for 'GradeN' button."""

        self._main_widget.soundplayer.stop()
        self._review_controller.grade_answer(int(widget.name[-1]))


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
