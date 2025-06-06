#!/usr/bin/env python3
'''Ruleset tests for the mk_puppet plugin in Checkmk.'''

from cmk.rulesets.v1.rule_specs import CheckParameters

from plugins.mk_puppet.rulesets.mk_puppet import (
    rule_spec_puppet_agent_events,
    rule_spec_puppet_agent_lastrun,
)

# ---------------------------------------
# Check Ruleset Definitions
# ---------------------------------------


def test_events_ruleset_is_defined():
    assert isinstance(rule_spec_puppet_agent_events, CheckParameters)
    assert rule_spec_puppet_agent_events.name == "puppet_agent_events"

    form = rule_spec_puppet_agent_events.parameter_form()
    assert "levels" in form.elements

    levels = form.elements["levels"].parameter_form
    assert levels.prefill_fixed_levels.value == (3, 5)


def test_lastrun_ruleset_is_defined():
    assert isinstance(rule_spec_puppet_agent_lastrun, CheckParameters)
    assert rule_spec_puppet_agent_lastrun.name == "puppet_agent_lastrun"

    form = rule_spec_puppet_agent_lastrun.parameter_form()
    assert "levels" in form.elements

    levels = form.elements["levels"].parameter_form
    assert levels.prefill_fixed_levels.value == (86400, 604800)
