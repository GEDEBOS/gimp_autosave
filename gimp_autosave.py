#!/usr/bin/python
# -*- encoding: utf-8 -*-
__author__ = "Jean de Bosset"
__copyright__ = "Copyright 2014, Gimp autosave trial"
__credits__ = ["James Henstridge, GIMP Python Doc"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jean de Bosset"
__email__ = "jean@gedebos.ch"
__status__ = "Development"
## TODO would like to implement a rotating version of the saved files by n-version

import os
import sys
import tempfile
from time import *
from gimpfu import *

PREFIX = 'gimp_%s_'


def autosave_gimp():
    bckpint = 60 * 10  # sleeping time 60 sec * number of minutes
    bckpfile = {}
    print "INF, Autosave activated %s" % ctime(time())
    while 1:
        sleep(bckpint)
        print "INF, time %s" % ctime(time())
        curimg = {}
        for k in gimp.image_list():
            curimg[k.ID] = k
        curids = curimg.keys()
        oldids = bckpfile.keys()
        newids = [x for x in curids if x not in oldids]
        delids = [x for x in oldids if x not in curids]
        # create temp placeholder
        for newid in newids:
            prefix = PREFIX % newid
            fn = tempfile.mkstemp(prefix=prefix, suffix='.xcf')
            os.close(fn[0])
            bckpfile[newid] = fn[1]
        # save the current image
        for newid, filename in bckpfile.iteritems():
            img = curimg[newid]
            try:
                print "INF, save " + img.name + '-' + str(newid) + ' to ' + filename
                pdb.gimp_xcf_save(1, img, img.active_drawable, filename, filename)
            except OSError as e:
                print "ERR, ", sys.exc_info()[0], e
        # remove images that have been closed
        for newid in delids:
            filename = bckpfile[newid]
            del (bckpfile[newid])
            try:
                os.remove(filename)
            except OSError as e:
                print "ERR, ", sys.exc_info()[0], e
register(
    "autosave_gimp",
    "Enable autosave",
    "Periodically saves currently opened images to the tmp directory",
    "public domain",
    "public domain",
    "2014",
    "<Toolbox>/File/Enable autosave",
    "RGB*, GRAY*",
    [],
    [],
    autosave_gimp)
main()