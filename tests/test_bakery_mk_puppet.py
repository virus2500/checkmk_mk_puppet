#!/usr/bin/env python3
'''Bakery tests for the mk_puppet plugin in Checkmk.'''

import pytest

from cmk.rulesets.v1.rule_specs import AgentConfig

from plugins.mk_puppet.rulesets.cee.bakery_mk_puppet import (
    rule_spec_bakery_mkpuppet,
    _migrate,
)

# ---------------------------------------
# Bakery Ruleset Definitions
# ---------------------------------------


def test_bakery_ruleset_is_defined():
    assert isinstance(rule_spec_bakery_mkpuppet, AgentConfig)
    assert rule_spec_bakery_mkpuppet.name == "mk_puppet"

    form = rule_spec_bakery_mkpuppet.parameter_form()
    assert "deploy" in form.elements

    deploy = form.elements["deploy"].parameter_form
    options = {e.name for e in deploy.elements}
    assert options == {"yes", "no"}
    assert deploy.prefill.value == "yes"


# ---------------------------------------
# Migration Logic
# ---------------------------------------

@pytest.mark.parametrize("legacy_input, expected", [
    (None, {"deploy": "no"}),
    (True, {"deploy": "yes"}),
    (False, pytest.raises(ValueError)),
    ({"deploy": "yes"}, {"deploy": "yes"}),
])
def test_migrate_legacy_input(legacy_input, expected):
    if isinstance(expected, dict):
        assert _migrate(legacy_input) == expected
    else:
        with expected:
            _migrate(legacy_input)
