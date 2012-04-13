#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Karesansui.
#
# Copyright (C) 2009-2010 HDE, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#

import os
import sys
import logging
from optparse import OptionParser

from ksscommand import KssCommand, KssCommandException, KssCommandOptException

import __cmd__

try:
    import karesansui
    from karesansui import __version__
    from karesansui.lib.parser.iptables import iptablesParser as Parser
    from karesansui.lib.utils import load_locale
except ImportError:
    print >>sys.stderr, "[Error] karesansui package was not found."
    sys.exit(1)

_ = load_locale()

usage = '%prog [options]'

def getopts():
    optp = OptionParser(usage=usage, version=__version__)
    """
    TRANSLATORS:
    翻訳お疲れさまです。
    「設定ファイルのパス」
    """
    optp.add_option('-c', '--config', dest='config', help=_('Path to configuration file'), default=None)
    optp.add_option('-a', '--action', dest='action', help=_('Action'), default=None)
    optp.add_option('-t', '--lint', dest='lint', help=_('Do lint (Specify config file to check)'),  action="store_true", default=False)
    return optp.parse_args()

def chkopts(opts):
    pass

class ControlIptables(KssCommand):

    def process(self):
        (opts, args) = getopts()
        chkopts(opts)
        self.up_progress(10)

        parser = Parser()

        if opts.config is None:
            config = parser.source_file()[0]
        else:
            if not os.path.exists(opts.config):
                error_msg = "ERROR: file not found '%s'." % (opts.config)
                self.logger.error(error_msg)
                raise KssCommandOptException(error_msg)
            config = opts.config

        self.up_progress(10)
        if opts.lint is True:
            (ret, stdout, stderr) = parser.do_lint(open(config).read())
            if ret != 0:
                print stderr

        elif opts.action is not None:
            try:
                exec("func = parser.do_%s" % opts.action)
                self.up_progress(10)
                (ret,res) = func()
                if ret is False:
                    error_msg = "ERROR: failed to %s" % (opts.action)
                    self.logger.error(error_msg)
                    raise KssCommandOptException(error_msg)
                self.up_progress(30)
            except KssCommandOptException, e:
                raise KssCommandOptException(''.join(e.args))
            except:
                error_msg = "ERROR: unknown action '%s'." % (opts.action)
                self.logger.error(error_msg)
                raise KssCommandOptException(error_msg)

        """
        TODO : 実装お疲れ様です。
        実況結果をstdoutにお願いします
        """
        return True

if __name__ == "__main__":
    target = ControlIptables()
    sys.exit(target.run())