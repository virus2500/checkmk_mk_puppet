#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

#
# Based on work by
# Writed by Allan GooD: allan.cassaro@gmail.com
# https://github.com/allangood/check_mk/tree/master/plugins/puppet
#

#
# mk_puppet Plugin
# (c) 2021 DECOIT GmbH
# written by Timo Klecker: klecker@decoit.de
#

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

"""
Module for defining check parameters and threshold levels for the
Puppet Agent plugin.

This module provides rule specifications for monitoring Puppet Agent
events failure and last run metrics.
"""

from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Topic,
    HostCondition,
)

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    LevelDirection,
    SimpleLevels,
    DefaultValue,
    Integer,
)


def _parameter_form_puppet_events():
    return Dictionary(
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Puppet Agent Events failure"),
                    help_text=Help(
                        "Set warning/critical levels for Puppet events"
                    ),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(3, 5)),
                ),
            ),
        }
    )


rule_spec_puppet_agent_events = CheckParameters(
    name="puppet_agent_events",
    title=Title("Puppet Agent Events Failure"),
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_parameter_form_puppet_events,
)


def _parameter_form_puppet_lastrun():
    return Dictionary(
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Puppet Agent Last Run"),
                    help_text=Help(
                        "Set warning/critical levels for Puppet last run"
                    ),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(86400, 604800)),
                ),
            ),
        }
    )


rule_spec_puppet_agent_lastrun = CheckParameters(
    name="puppet_agent_lastrun",
    title=Title("Puppet Agent Last Run"),
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_parameter_form_puppet_lastrun,
)
