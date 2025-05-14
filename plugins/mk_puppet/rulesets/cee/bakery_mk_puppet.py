# #!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
'''Bakery Ruleset for mk_puppet plugin'''
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
# the Free Software Foundation in version 2.  mk_puppet Plugin is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.rulesets.v1 import Title, Mapping
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    SingleChoice,
    SingleChoiceElement,
    DefaultValue,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic, Help


def _migrate(value) -> Mapping[str, object]:
    match value:
        case None:
            return {"deployment": "do_not_deploy"}
        case True:
            return {"deployment": "deploy"}
        case dict():
            return value
        case _:
            raise ValueError(
                f"Invalid value for mk_puppet: {value}.\
                    Expected None, True, or a dict."
            )


def _parameter_form_bakery() -> Dictionary:
    return Dictionary(
        migrate=_migrate,
        elements={
            "deployment": DictElement(
                required=True,
                parameter_form=SingleChoice(
                    title=Title("Puppet agent plugin deployment"),
                    help_text=Help(
                        "Hosts configured via this rule get \
                        the <tt>mk_puppet</tt> plugin"
                    ),
                    prefill=DefaultValue("deploy"),
                    elements=[
                        SingleChoiceElement(
                            name="deploy",
                            title=Title("Deploy the puppet agent plugin"),
                        ),
                        SingleChoiceElement(
                            name="do_not_deploy",
                            title=Title("Do not deploy puppet agent plugin"),
                        ),
                    ],
                ),
            )
        }
    )


rule_spec_hello_world_bakery = AgentConfig(
    name="puppet_agent_plugin",
    title=Title("Puppet agent plugin"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_bakery,
)
