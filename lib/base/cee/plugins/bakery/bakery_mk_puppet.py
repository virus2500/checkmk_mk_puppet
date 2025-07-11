#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
'''Bakery plugin for mk_puppet plugin'''

#
# Based on work by
# Writen by Allan GooD: allan.cassaro@gmail.com
# https://github.com/allangood/check_mk/tree/master/plugins/puppet
#
#
# (c) 2021 DECOIT GmbH
# written by Timo Klecker: klecker@decoit.de
#

# made compatible with Checkmk > 2.3.0p33 and 2.4.x
# by Michael Kronika

#
# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  mk_puppet Plugin is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.
#

from pathlib import Path
from typing import Any, Dict

from cmk.base.cee.plugins.bakery.bakery_api.v1 import (
    FileGenerator,
    OS,
    Plugin,
    register
)


def get_mk_puppet_files(conf: Dict[str, Any]) -> FileGenerator:
    '''To deploy or not deploy our plugin'''
    if conf.get("deploy") == "no":
        return
    yield Plugin(
        base_os=OS.LINUX,
        source=Path("mk_puppet"),
    )
    yield Plugin(
        base_os=OS.WINDOWS,
        source=Path("mk_puppet.ps1"),
    )


register.bakery_plugin(
    name="mk_puppet",
    files_function=get_mk_puppet_files,
)
