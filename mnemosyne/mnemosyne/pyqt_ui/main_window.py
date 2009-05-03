#
# main_window.py <Peter.Bienstman@UGent.be>
#

import sys
import os


import gettext
_ = gettext.gettext

from PyQt4 import QtCore, QtGui

import review_wdgt

from ui_main_window import Ui_MainWindow
from add_cards_dlg import AddCardsDlg
from edit_fact_dlg import EditFactDlg
from card_appearance_dlg import CardAppearanceDlg
from activate_plugins_dlg import ActivatePluginsDlg
from cloned_card_types_list_dlg import ClonedCardTypesListDlg
#from import_dlg import *
#from export_dlg import *
#from edit_item_dlg import *
#from clean_duplicates import *
#from statistics_dlg import *
#from edit_items_dlg import *
#from activate_categories_dlg import *
#from config_dlg import *
#from product_tour_dlg import *
#from tip_dlg import *
#from about_dlg import *
from mnemosyne.libmnemosyne.ui_components import MainWidget
from mnemosyne.libmnemosyne.component_manager import database
from mnemosyne.libmnemosyne.component_manager import component_manager
from mnemosyne.libmnemosyne.component_manager import ui_controller_main

# The folloving is need to determine the location of the translations.
# TODO: needed?
prefix = os.path.dirname(__file__)


class MainWindow(QtGui.QMainWindow, Ui_MainWindow, MainWidget):

    def __init__(self, filename, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

    def after_mnemosyne_init(self):
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     ui_controller_review().rollover)
        self.timer.start(1000 * 60 * 5)
        
    def init_review_widget(self):
        w = self.centralWidget()
        if w:
            w.close()
            del w
        ui_controller_review().widget = \
            component_manager.get_current("review_widget")(parent=self)
        self.setCentralWidget(ui_controller_review().widget)

    def information_box(self, message):
        QtGui.QMessageBox.information(None, _("Mnemosyne"), message, _("&OK"))

    def question_box(self, question, option0, option1, option2):
        return QtGui.QMessageBox.question(None,  _("Mnemosyne"),
            question, option0, option1, option2, 0, -1)

    def error_box(self, message):  
        QtGui.QMessageBox.critical(None, _("Mnemosyne"), message,
            _("&OK"), "", "", 0, -1)

    def save_file_dialog(self, path, filter, caption=""):
        return unicode(QtGui.QFileDialog.getSaveFileName(self, caption, path,
                                                         filter))
    
    def open_file_dialog(self, path, filter, caption=""):
        return unicode(QtGui.QFileDialog.getOpenFileName(self, caption, path,
                                                         filter))

    def set_window_title(self, title):
        self.setWindowTitle(title)

    def add_cards(self):
        ui_controller_main().add_cards()

    def edit_current_card(self):
        ui_controller_main().edit_current_card()
        
    def delete_current_fact(self):
        ui_controller_main().delete_current_fact()
        
    def file_new(self):
        ui_controller_main().file_new()

    def file_open(self):
        ui_controller_main().file_open()
        
    def file_save(self):
        ui_controller_main().file_save()
        
    def file_save_as(self):
        ui_controller_main().file_save_as()
        
    def manage_card_types(self):
        ui_controller_main().manage_card_types()
        
    def card_appearance(self):
        ui_controller_main().card_appearance()
        
    def activate_plugins(self):
        ui_controller_main().activate_plugins()
        
    def run_add_cards_dialog(self):
        dlg = AddCardsDlg(self)
        dlg.exec_()

    def run_edit_fact_dialog(self, fact, allow_cancel=True):
        dlg = EditFactDlg(fact, allow_cancel, self)
        dlg.exec_()
        
    def run_manage_card_types_dialog(self):
        dlg = ClonedCardTypesListDlg(self)
        dlg.exec_()
        
    def run_card_appearance_dialog(self):
        dlg = CardAppearanceDlg(self)
        dlg.exec_()

    def run_activate_plugins_dialog(self):
        dlg = ActivatePluginsDlg(self)
        dlg.exec_()
        
    def Import(self):
        stopwatch.pause()
        from xml.sax import saxutils, make_parser
        from xml.sax.handler import feature_namespaces
        dlg = ImportDlg(self)
        dlg.exec_loop()
        if self.card == None:
            self.newQuestion()
        self.updateDialog()
        stopwatch.unpause()

    def export(self):
        stopwatch.pause()
        dlg = ExportDlg(self)
        dlg.exec_loop()
        stopwatch.unpause()

    def editCards(self):
        stopwatch.pause()
        dlg = EditCardsDlg(self)
        dlg.exec_()
        rebuild_revision_queue()
        if not in_revision_queue(self.card):
            self.newQuestion()
        else:
            remove_from_revision_queue(self.card) # It's already being asked.
        ui_controller_review().update_dialog(redraw_all=True)
        self.updateDialog()
        stopwatch.unpause()

    def cleanDuplicates(self):
        stopwatch.pause()
        self.statusbar.message(_("Please wait..."))
        clean_duplicates(self)
        rebuild_revision_queue()
        if not in_revision_queue(self.card):
            self.newQuestion()
        self.updateDialog()
        stopwatch.unpause()

    def showStatistics(self):
        stopwatch.pause()
        dlg = StatisticsDlg(self)
        dlg.exec_()
        stopwatch.unpause()

    def activateCategories(self):
        stopwatch.pause()
        dlg = ActivateCategoriesDlg(self)
        dlg.exec_()
        rebuild_revision_queue()
        if not in_revision_queue(self.card):
            self.newQuestion()
        else:
            remove_from_revision_queue(self.card) # It's already being asked.
        self.updateDialog()
        stopwatch.unpause()

    def configuration(self):
        stopwatch.pause()
        dlg = ConfigurationDlg(self)
        dlg.exec_loop()
        rebuild_revision_queue()
        if not in_revision_queue(self.card):
            self.newQuestion()
        else:
            remove_from_revision_queue(self.card) # It's already being asked.
        self.updateDialog()
        stopwatch.unpause()

    def closeEvent(self, event):
        from mnemosyne.libmnemosyne.exceptions import MnemosyneError
        try:
            database().backup()
            database().unload()
        except MnemosyneError, e:
            self.show_exception(e)
            event.ignore()
        else:
            event.accept()

    def productTour(self):
        return
        stopwatch.pause()
        dlg = ProductTourDlg(self)
        dlg.exec_()
        stopwatch.unpause()

    def Tip(self):
        return
        stopwatch.pause()
        dlg = TipDlg(self)
        dlg.exec_()
        stopwatch.unpause()

    def helpAbout(self):
        stopwatch.pause()
        dlg = AboutDlg(self)
        dlg.exec_()
        stopwatch.unpause()

