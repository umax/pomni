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
Hildon UI. Dialogs.
"""

import gtk
import hildon
import gobject
from gettext import gettext as _

MIN_FONT_SIZE = 10
MAX_FONT_SIZE = 60


def show_about_dialog():
    """SHows About dialog."""

    dialog = hildon.Dialog()
    dialog.set_title(_('About'))

    program_name_label = gtk.Label()
    program_name_label.set_justify(gtk.JUSTIFY_CENTER)
    program_name_label.set_use_markup(True)
    program_name_label.set_markup("<span foreground='white' size='large'><b>" \
        "Mnemosyne for Maemo</b></span>\n<span foreground='white' size=" \
        "'medium'>" + _('version') + " 2.0.0~beta12</span>\n")

    pannable_area = hildon.PannableArea()
    pannable_area.set_size_request_policy(hildon.SIZE_REQUEST_CHILDREN)
    developers_label = gtk.Label()
    developers_label.set_use_markup(True)
    developers_label.set_markup("<span foreground='white' size='small'><b>" + \
        _("Developers") + ":</b></span>\n<span foreground='white' size='small" \
        "'>Max Usachev |</span> <span foreground='#299BFC' size='small'>" \
        "maxusachev@gmail.com</span>\n<span foreground='white' size=" \
        "'small'>Ed Bartosh |</span> <span foreground='#299BFC' size=" \
        "'small'>bartosh@gmail.com</span>\n<span foreground='white' " \
        "size='small'>Vlad Vasiliev |</span> <span foreground='#299BFC' " \
        "size='small'>vlad@gas.by</span>\n\n<span foreground='white' " \
        "size='small'><b>" + _('Designer') + ":</b>\n</span><span foreground=" \
        "'white' size='small'>Artem Shubin |</span> <span foreground=" \
        "'#299BFC' size='small'>admin@mayan.ru</span>\n\n<span " \
        "foreground='white' size='small'><b>" + _('Development team') + \
        ":</b></span>\n<span foreground='#299BFC' size='small'>pomni@" \
        "googlegroups.com</span><span foreground='white' size='small'><b>" \
        "\n\n" + _('Special Thanks To') + ":</b></span>\n<span foreground=" \
        "'white' size='small'>Peter Bienstman</span>\n<span foreground=" \
        "'#299BFC' size='small'>Peter.Bienstman@ugent.be</span>\n<span " \
        "foreground='#299BFC' size='small'>http://www.mnemosyne-proj.org/" \
        "</span>\n<span size='x-large'></span><span foreground='white' size=" \
        "'small'>\nGSoC 2009</span>\n<span foreground='#299BFC' size='"\
        "small'>http://socghop.appspot.com/</span>\n<span size='x-large'>" \
        "</span><span foreground='white' size='small'>\nMaemo community" \
        "</span>\n<span foreground='#299BFC' size='small'>" \
        "http://maemo.org/</span>")
    pannable_area.add_with_viewport(developers_label)

    dialog.vbox.pack_start(program_name_label, expand=False, fill=True)
    dialog.vbox.pack_start(pannable_area)
    dialog.vbox.set_spacing(10)
    dialog.vbox.show_all()
    dialog.run()
    dialog.destroy()


def show_items_dialog(widget, window, items, caption, cur_item=None):
    """Shows custom PickerDialog with TouchSelector widget."""

    dialog = hildon.PickerDialog(window)
    dialog.set_title(caption)
    selector = hildon.TouchSelector()
    dialog.set_selector(selector)
    selector.set_column_selection_mode( \
        hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE)

    # creating items dict
    items_dict = dict([(index, item) for index, item in enumerate(items)])
    model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
    if cur_item:
        current_item = cur_item
    else:
        current_item = items_dict[0]
        translated_item = widget.get_value()
        for index, item in items_dict.iteritems():
            if translated_item == _(item):
                current_item = item
                break

    # populating list
    for item in items_dict.values():
        model.append((_(item), item))
    selector.append_text_column(model, True)

    # mark active item
    selector.unselect_all(0)
    for key in items_dict:
        if items_dict[key] == current_item:
            selector.set_active(0, key)
            break

    dialog.run()
    selected_item = selector.get_model(0)[selector.get_active(0)][1]
    dialog.destroy()
    if widget is not None:
        widget.set_value(_(selected_item))
        widget.set_data('title', selected_item)
    return selected_item


def create_button(title, value):
    """Creates setting button."""

    button = hildon.Button( \
        gtk.HILDON_SIZE_AUTO | gtk.HILDON_SIZE_FINGER_HEIGHT, \
        hildon.BUTTON_ARRANGEMENT_VERTICAL, title, value)
    button.set_style(hildon.BUTTON_STYLE_PICKER)
    button.set_alignment(0, 0, 0, 0)
    return button


def show_new_tag_dialog():
    """Shows NewTagDialog."""

    dialog = hildon.Dialog()
    dialog.set_title(_('New tag'))
    entry = hildon.Entry(gtk.HILDON_SIZE_AUTO)
    dialog.vbox.pack_start(entry)
    dialog.vbox.show_all()
    dialog.add_button(_('Add'), gtk.RESPONSE_OK)
    dialog.run()
    tag_name = unicode(entry.get_text())
    dialog.destroy()
    return tag_name


def show_tags_selection_dialog(window, title, tags, selected_tags):
    """Shows dialog for selection multiple tags."""

    selector = hildon.TouchSelector(text=True)

    # fill tags list
    for tag in tags:
        selector.append_text(tag)

    selector.set_column_selection_mode( \
        hildon.TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)

    # mark selected tags
    selector.unselect_all(0)
    model = selector.get_model(0)
    for i in range(len(tags)):
        if model[i][0] in selected_tags:
            selector.select_iter(0, model.get_iter(i), False)

    dialog = hildon.PickerDialog(window)
    dialog.set_title(title)
    dialog.set_selector(selector)
    dialog.run()
    indexes_of_selected_tags = [item[0] for item in \
        selector.get_selected_rows(0)]
    model = selector.get_model(0)
    selected_tags = [unicode(model[index][0]) for index in \
        indexes_of_selected_tags]
    dialog.destroy()
    return selected_tags


def show_file_chooser_dialog(widget, directory_mode=False, cur_dir=None):
    """Shows file or directory chooser dialog."""

    if directory_mode:
        mode = gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER
    else:
        mode = gtk.FILE_CHOOSER_ACTION_OPEN
    chooser = gobject.new(hildon.FileChooserDialog, action=mode)
    chooser.set_current_folder(cur_dir or widget.get_value())
    chooser.set_property('show-files', True)
    chooser.run()
    path = chooser.get_filename()
    if path and widget:
        widget.set_value(path)
    chooser.destroy()
    return path


def show_general_settings_dialog(config):
    """Shows General settings dialog."""

    dialog = hildon.Dialog()
    dialog.set_title(_('General settings'))

    # create widgets
    widgets_box = gtk.VBox()
    widgets_box.set_spacing(4)

    sound_button = create_button(_('Sound directory'), config['sounddir'])
    sound_button.connect('clicked', show_file_chooser_dialog, True)
    widgets_box.pack_start(sound_button, expand=False, fill=False)

    image_button = create_button(_('Image directory'), config['imagedir'])
    image_button.connect('clicked', show_file_chooser_dialog, True)
    widgets_box.pack_start(image_button, expand=False, fill=False)

    font_size_button = create_button(_('Font size'), str(config['font_size']))
    font_size_button.connect('clicked', show_items_dialog, dialog, \
        [str(size) for size in range(MIN_FONT_SIZE, MAX_FONT_SIZE)], \
        _('Font size'))
    widgets_box.pack_start(font_size_button, expand=False, fill=False)

    open_review_button = hildon.CheckButton(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT)
    open_review_button.set_label(_('Open Review mode at startup'))
    open_review_button.set_active(config['startup_with_review'])
    widgets_box.pack_start(open_review_button, expand=False, fill=False)

    dialog.vbox.add(widgets_box)
    dialog.vbox.show_all()
    dialog.add_button(_('Save'), gtk.RESPONSE_OK)

    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        config['sounddir'] = sound_button.get_value()
        config['imagedir'] = image_button.get_value()
        config['font_size'] = int(font_size_button.get_value())
        config['startup_with_review'] = open_review_button.get_active()
        config.save()

    dialog.destroy()


def show_tts_settings_dialog(config):
    """Shows TTS settings dialog."""

    import mnemosyne.maemo_ui.tts as tts

    dialog = hildon.Dialog()
    dialog.set_title(_('TTS settings'))

    if not tts.is_available():
        label = gtk.Label(_("TTS is not available on your system!\n" \
            "Install eSpeak first."))
        label.set_justify(gtk.JUSTIFY_CENTER)
        dialog.vbox.pack_start(label)
        dialog.vbox.show_all()
        dialog.run()
        dialog.destroy()
        return

    # create widgets
    widgets_box = gtk.VBox()
    widgets_box.set_spacing(4)

    language_button = create_button(_('Language'), _(config['tts_language']))
    language_button.set_data('title', config['tts_language'])
    language_button.connect('clicked', show_items_dialog, dialog, \
        tts.get_languages(), _('Language'))
    widgets_box.pack_start(language_button, expand=False, fill=False)

    voice_button = create_button(_('Voice'), _(config['tts_voice']))
    voice_button.set_data('title', config['tts_voice'])
    voice_button.connect('clicked', show_items_dialog, dialog, \
        ['Male', 'Female'], _('Voice'))
    widgets_box.pack_start(voice_button, expand=False, fill=False)

    speed_button = create_button(_('Pronunciation speed'), \
        str(config['tts_speed']))
    speed_button.connect('clicked', show_items_dialog, dialog, \
        [str(speed) for speed in range(tts.MIN_SPEED_VALUE, \
        tts.MAX_SPEED_VALUE)], _('Pronunciation speed'))
    widgets_box.pack_start(speed_button, expand=False, fill=False)

    pitch_button = create_button(_('Voice pitch'), str(config['tts_pitch']))
    pitch_button.connect('clicked', show_items_dialog, dialog, [str(pitch) \
        for pitch in range(tts.MIN_SPEED_VALUE, tts.MAX_SPEED_VALUE)], \
        _('Voice pitch'))
    widgets_box.pack_start(pitch_button, expand=False, fill=False)

    dialog.vbox.add(widgets_box)
    dialog.vbox.show_all()
    dialog.add_button(_('Save'), gtk.RESPONSE_OK)

    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        config['tts_language'] = language_button.get_data('title')
        config['tts_voice'] = voice_button.get_data('title')
        config['tts_speed'] = int(speed_button.get_value())
        config['tts_pitch'] = int(pitch_button.get_value())

    dialog.destroy()


def show_import_dialog(file_formats, current_format, database, \
    review_controller, error_box):
    """Shows ImportCards dialog."""

    from mnemosyne.libmnemosyne.file_formats.mnemosyne_XML import MnemosyneXML

    def update_tags(current_format_description, tags_button, selected_tags):
        """Updates tags UI."""

        if current_format_description == MnemosyneXML.description:
            tags_button.set_sensitive(False)
            tags_button.set_value(_('Using XML tags'))
        else:
            tags_button.set_sensitive(True)
            tags_button.set_value(', '.join(selected_tags))

    # callbacks
    def change_format_cb(widget, window, formats, tags_button, \
        selected_tags, update_tags):
        """Changes current file format and updates UI."""

        update_tags(show_items_dialog(widget, window, formats, \
            _('File format')), tags_button, selected_tags)

    def add_new_tag_cb(widget, tags):
        """Creates new tag and updates UI."""

        tag_name = show_new_tag_dialog()
        if tag_name:
            tags.append(tag_name)

    def set_file_cb(widget, import_button):
        """Sets file to import from."""

        fname = show_file_chooser_dialog(widget)
        if fname:
            import_button.set_sensitive(True)

    def select_tags_cb(widget, window, tags, selected_tags, tags_button):
        """Creates TagsSelection dialog UI."""

        # generate all tags list
        for tag in selected_tags:
            if not tag in tags:
                tags.append(tag)

        selected_tags[:] = show_tags_selection_dialog(window, \
            _('Tags for imported cards'), tags, selected_tags)
        tags_button.set_value(', '.join(selected_tags))


    tags = [tag.name for tag in database.get_tags()]
    selected_tags = [_(u'<default>')]

    dialog = hildon.Dialog()
    dialog.set_title(_('Import cards'))

    # create widgets
    format_button = create_button(_('File format'), current_format.description)
    file_button = create_button(_('File to import from'), _('Select file'))
    tags_button = create_button(_('Tags for new cards'), \
        ', '.join(selected_tags))
    new_tag_button = create_button(_('New tag'), '')
    new_tag_button.set_style(hildon.BUTTON_STYLE_NORMAL)
    new_tag_button.set_alignment(0.5, 0.5, 0, 0)
    new_tag_button.show()
    dialog.action_area.pack_end(new_tag_button)

    import_button = dialog.add_button(_('Import'), gtk.RESPONSE_OK)
    import_button.set_sensitive(False)

    # connect signals
    format_button.connect('clicked', change_format_cb, dialog, \
        [f.description for f in file_formats], tags_button, \
        selected_tags, update_tags)
    new_tag_button.connect('clicked', add_new_tag_cb, tags)
    file_button.connect('clicked', set_file_cb, import_button)
    tags_button.connect('clicked', select_tags_cb, dialog, tags, \
        selected_tags, tags_button)

    # packing widgets
    dialog.vbox.pack_start(format_button)
    dialog.vbox.pack_start(file_button)
    dialog.vbox.pack_start(tags_button)
    dialog.vbox.show_all()

    # updates ui
    update_tags(current_format.description, tags_button, selected_tags)

    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        # disable all widgets
        format_button.set_sensitive(False)
        file_button.set_sensitive(False)
        tags_button.set_sensitive(False)
        new_tag_button.set_sensitive(False)
        import_button.set_sensitive(False)
        hildon.hildon_gtk_window_set_progress_indicator(dialog, 1)
        for _format in file_formats:
            if _format.description == format_button.get_value():
                try:
                    _format.do_import(file_button.get_value(), selected_tags)
                    hildon.hildon_gtk_window_set_progress_indicator(dialog, 0)
                    db_path = database._path
                    database.unload()
                    database.load(db_path)
                    review_controller.reload_counters()
                except:
                    error_box(_('Oops! Error occured.'))
                break

    dialog.destroy()


def show_sync_dialog():
    """Shows Sync dialog."""

    dialog = hildon.Dialog()
    dialog.set_title(_('Sync'))

    label = gtk.Label('\n' + _('Sync feature is not implemented yet :(') + \
        '\n' + _('It will be available soon!') + '\n')
    label.set_justify(gtk.JUSTIFY_CENTER)
    dialog.vbox.pack_start(label)
    dialog.vbox.show_all()

    dialog.run()
    dialog.destroy()

