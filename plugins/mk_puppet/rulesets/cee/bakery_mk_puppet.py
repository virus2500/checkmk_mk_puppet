# #!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
'''Bakery Ruleset for mk_puppet plugin'''
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
# the Free Software Foundation in version 2.  mk_puppet Plugin is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.
from collections.abc import Mapping

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    SingleChoice,
    SingleChoiceElement,
    DefaultValue,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic, Help


def _migrate(value: object) -> Mapping[str, object]:
    match value:
        case None:
            return {"deploy": "no"}
        case True:
            return {"deploy": "yes"}
        case dict():
            return value
        case _:
            raise ValueError(value)


def _parameter_form_bakery() -> Dictionary:
    return Dictionary(
        migrate=_migrate,
        elements={
            "deploy": DictElement(
                required=True,
                parameter_form=SingleChoice(
                    title=Title("Puppet agent plugin deployment"),
                    help_text=Help(
                        "Hosts configured via this rule get \
                        the <tt>mk_puppet</tt> plugin"
                    ),
                    prefill=DefaultValue("yes"),
                    elements=[
                        SingleChoiceElement(
                            name="yes",
                            title=Title("Deploy the puppet agent plugin"),
                        ),
                        SingleChoiceElement(
                            name="no",
                            title=Title("Do not deploy puppet agent plugin"),
                        ),
                    ],
                ),
            )
        }
    )


rule_spec_bakery_mkpuppet = AgentConfig(
    name="mk_puppet",
    title=Title("Puppet agent plugin"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_bakery,
)
