#!/usr/bin/env python3
# pylint: disable=redefined-outer-name
"""Agent tests for the mk_puppet plugin in Checkmk."""

import time
import pytest

from cmk.agent_based.v2 import State
from plugins.mk_puppet.agent_based.mk_puppet import (
    puppet_agent_parse,
    discovery_puppet_agent_events,
    check_puppet_agent_events,
    discovery_puppet_agent_lastrun,
    check_puppet_agent_lastrun,
    discovery_puppet_agent_resources,
    check_puppet_agent_resources,
    _resources_name_table,
)


# Fixtures

@pytest.fixture
def puppet_raw_data():
    return [
        ["last_run:", "1439475966"],
        ["resources_resources:"],
        ["resources_changed:", "3"],
        ["resources_failed:", "0"],
        ["resources_failed_to_restart:", "0"],
        ["resources_out_of_sync:", "3"],
        ["resources_restarted:", "0"],
        ["resources_scheduled:", "0"],
        ["resources_skipped:", "0"],
        ["resources_total:", "77"],
        ["events_events:"],
        ["events_failure:", "0"],
        ["events_success:", "3"],
        ["events_total:", "3"],
    ]


@pytest.fixture
def parsed_section(puppet_raw_data):
    return puppet_agent_parse(puppet_raw_data)


# Tests for puppet_agent_parse


def test_parse_output(parsed_section):
    assert parsed_section["last_run"] == "1439475966"
    assert parsed_section["resources_changed"] == "3"
    assert parsed_section["events_failure"] == "0"


# Discovery tests


def test_discovery_events(parsed_section):
    services = list(discovery_puppet_agent_events(parsed_section))
    assert len(services) == 1


def test_discovery_lastrun(parsed_section):
    services = list(discovery_puppet_agent_lastrun(parsed_section))
    assert len(services) == 1


def test_discovery_resources(parsed_section):
    services = list(discovery_puppet_agent_resources(parsed_section))
    assert len(services) == len(_resources_name_table)


# Check tests for events

@pytest.mark.parametrize("failure_count,state", [
    ("0", State.OK),
    ("3", State.WARN),
    ("6", State.CRIT),
])
def test_check_events_levels(parsed_section, failure_count, state):
    parsed_section["events_failure"] = failure_count
    # Pass levels as ("fixed", (warn, crit))
    params = {"levels": ("fixed", (3, 5))}
    results = list(check_puppet_agent_events(params, parsed_section))
    assert any(r.state == state for r in results)


def test_check_events_missing_key():
    section = {}
    params = {"levels": ("fixed", (3, 5))}
    results = list(check_puppet_agent_events(params, section))
    assert results[0].state == State.UNKNOWN


# Check tests for lastrun


def test_check_lastrun_recent():
    now = int(time.time())
    section = {"last_run": str(now - 60)}  # 1 minute ago
    # Pass levels as ("fixed", (warn, crit))
    params = {"levels": ("fixed", (86400, 604800))}
    results = list(check_puppet_agent_lastrun(params, section))
    assert results[0].state == State.OK


def test_check_lastrun_old():
    now = int(time.time())
    section = {"last_run": str(now - 900000)}  # >10 days ago
    params = {"levels": ("fixed", (86400, 604800))}
    results = list(check_puppet_agent_lastrun(params, section))
    assert any(r.state == State.CRIT for r in results)


def test_check_lastrun_missing_key():
    params = {"levels": ("fixed", (86400, 604800))}
    results = list(check_puppet_agent_lastrun(params, {}))
    assert results[0].state == State.UNKNOWN


# Check tests for resources

@pytest.mark.parametrize("key", list(_resources_name_table.keys()))
def test_check_resource_ok(parsed_section, key):
    item = _resources_name_table[key]
    results = list(check_puppet_agent_resources(item, parsed_section))
    assert results[0].state == State.OK
    assert item in results[0].summary


def test_check_resource_missing_item():
    item = "Unknown Resource"
    section = {}
    # The plugin’s code will attempt to find “Unknown Resource” in _resources_name_table.values(),
    # which raises ValueError. We assert that behavior here.
    with pytest.raises(ValueError):
        _ = list(check_puppet_agent_resources(item, section))
