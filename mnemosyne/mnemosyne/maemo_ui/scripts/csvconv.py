#!/usr/bin/python -tt
#vim: sw=4 ts=4 expandtab ai

""" Converter from CSV
    to Mnemosyne (http://www.mnemosyne-proj.org) database format 
"""

__copyright__ = """
Copyright (C) 2008 Ed Bartosh <bartosh@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.  THE SOFTWARE IS PROVIDED "AS
IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import os
import csv

from optparse import OptionParser
from mnemosyne.libmnemosyne import Mnemosyne
from mnemosyne.libmnemosyne.ui_component import UiComponent

class TextOut(object):
    """ Text output """

    def __init__(self, fptr=sys.stdout):
        self.fptr = fptr
    
    def out(self, row):
        """Output to fptr."""
        
        print 'row:', row[0], row[1]
        self.fptr.write("%s\n%s" % (row[0], row[1]))

class MnemosyneOut(Mnemosyne, UiComponent):
    """ Output to Mnemosyne Db """
    
    def __init__(self, datadir=None, category=None):
        
        Mnemosyne.__init__(self)

        self.components.insert(0, ("mnemosyne.libmnemosyne.translator",
                                  "GetTextTranslator"))
        self.components.append(\
                    ("mnemosyne.libmnemosyne.ui_components.review_widget",
                     "ReviewWidget"))
        self.components.append(\
                    ("mnemosyne.libmnemosyne.ui_components.main_widget",
                     "MainWidget"))

        self.components.append(("mnemosyne.maemo_ui.factory", "ConfigHook"))
        
        if datadir:
            datadir = os.path.abspath(datadir)
        elif os.path.exists(os.path.join(os.getcwdu(), ".mnemosyne")):
            datadir = os.path.abspath(os.path.join(os.getcwdu(), ".mnemosyne"))
        else:
            datadir = os.path.abspath(os.path.join(os.path.expanduser("~"), 
                        ".mnemosyne"))


        self.initialise(datadir)
        self.review_controller().reset()

        self.card_type = [ct for ct in self.card_types() \
                            if ct.name == "Front-to-back only"][0]
        self.saved = False
        
        self.category = category #Category(category)

    def out(self, row):
        """Main entry point. Create mnemosyne card."""

        data = {"q": row[0], "a": row[1]}

        self.controller().create_new_cards(data, self.card_type, -1, 
                                            [self.category])

    def savedb(self):
        """Save the database if not saved yet."""

        if not self.saved:
            self.database().save(self.config()["path"])
            self.saved = True

    def __del__(self):
        """Save the database on exit."""

        self.savedb()
        self.finalise()

def parse_commandline(argv):
    """Parse commandline, check options."""
    
    parser = OptionParser(usage = "%prog [options] <csv file>")

    parser.add_option("-c", "--category", help="specify category name", 
        metavar="category", default="English-Russian")
    parser.add_option("-f", "--format", type="choice", 
        choices=("mnemosyne", "text"), default="mnemosyne", metavar="format",
        help="output format: mnemosyne or text, [default: %default]")
    parser.add_option("-s", "--delimiter", default="|", metavar="delimiter",
        help="specify delimiter_ [default: %default]")
    parser.add_option("-o", "--outdir", help="output directory")
    parser.add_option("-r", "--records", type="int",
        help="amount of records to load")

    options, argv = parser.parse_args(argv)

    if len(argv) < 2:
        parser.error("missed mandatory parameter <csv file>")
    if not os.access(argv[1], os.R_OK):
        parser.error("file %s isn't readable or doesn't exist" % argv[1])

    return (options, argv)

def main(argv):
    """Main"""

    opts, argv = parse_commandline(argv)

    reader = csv.reader(open(argv[1], "r"), delimiter=opts.delimiter)

    if not opts.format or opts.format == "mnemosyne":
        out = MnemosyneOut(opts.outdir, opts.category)
    else:
        out = TextOut()

    records = opts.records
    for row in reader:
        print row[0]
        if records:
            records -= 1
            if not records:
                break
        out.out(row)
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

