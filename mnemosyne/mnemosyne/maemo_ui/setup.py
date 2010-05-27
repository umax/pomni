#!/usr/bin/python -tt

""" Setup """

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PKG = open('debian/changelog').readline().split(' ')[0]

setup(name=PKG,
    description='Learning tool based on spaced repetition technique',
    version=open('debian/changelog').readline().split(' ')[1][1:-1],
    author="Pomni Development team",
    author_email="pomni@googlegroups.com",
    license='GPL 2',
    packages=["mnemosyne.maemo_ui", "mnemosyne.maemo_ui.widgets"],
    package_dir={'mnemosyne.maemo_ui': ''},
    data_files = [
	    ('/opt/maemo/usr/share/%s/hildon-UI' % PKG, \
            [os.path.join('hildon-UI', fname) for fname in \
            os.listdir('hildon-UI') if os.path.isfile( \
    	    os.path.join('hildon-UI', fname))]),
        ('/usr/share/dbus-1/services', ['maemo/%s.service' % PKG]),
        ('/usr/share/applications/hildon', ['maemo/%s.desktop' % PKG]),
        ('/opt/maemo/usr/share/%s/help' % PKG, [os.path.join('help', fname) \
            for fname in os.listdir('help')]),
        ('/usr/share/icons/hicolor/48x48/apps/', \
	        ['./maemo/icons/48x48/%s.png' % PKG]),
        ('/usr/share/icons/hicolor/64x64/apps/', \
            ['./maemo/icons/64x64/%s.png' % PKG])
    ],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries',
    ])
