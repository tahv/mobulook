"""Test suite for the mobulook package."""
from __future__ import absolute_import, division, print_function

import json
import tempfile
import uuid

import pyfbsdk
import pytest

import mobulook


@pytest.fixture(scope="function", autouse=True)
def new_file():  # type: () -> None
    """Create a new file before each test."""
    pyfbsdk.FBApplication().FileNew(False, True)


@pytest.fixture
def marker():  # type: () -> pyfbsdk.FBModelMarker
    """Fixture creating and returning a new FBModelMarker with a random name."""
    return pyfbsdk.FBModelMarker(str(uuid.uuid4()))


@pytest.fixture
def lookfile():  # type: () -> str
    """Fixture creating en returning an empty json file to store look data."""
    _, filepath = tempfile.mkstemp(prefix="mobulook_", suffix=".json")
    return filepath


def test_save_name(marker, lookfile):  # type: (pyfbsdk.FBModelMarker, str) -> None
    """It save the name in saved json data."""
    mobulook.save(lookfile, [marker])
    with open(lookfile, "r") as openfile:
        saved_data = json.load(openfile)

    assert marker.Name in saved_data


def test_save_marker_look(
    marker, lookfile
):  # type: (pyfbsdk.FBModelMarker, str) -> None
    """It save the look data in saved json."""
    marker.Color = pyfbsdk.FBColor(1, 2, 3)
    mobulook.save(lookfile, [marker])
    with open(lookfile, "r") as openfile:
        saved_data = json.load(openfile)

    assert saved_data[marker.Name]["color"] == marker.Color.GetList()


def test_load(marker, lookfile):  # type: (pyfbsdk.FBModelMarker, str) -> None
    """It load saved data to an existing marker."""
    marker.Color = pyfbsdk.FBColor(1, 1, 1)
    mobulook.save(lookfile, [marker])

    marker.Color = pyfbsdk.FBColor()
    mobulook.load(lookfile, namespace=None)

    assert marker.Color == pyfbsdk.FBColor(1, 1, 1)


def test_load_with_namespace(
    marker, lookfile
):  # type: (pyfbsdk.FBModelMarker, str) -> None
    """It load saved data to an existing marker with given namespace in scene."""
    marker.Color = pyfbsdk.FBColor(1, 1, 1)
    mobulook.save(lookfile, [marker])

    marker.Color = pyfbsdk.FBColor()
    marker.LongName = "test:" + marker.Name
    mobulook.load(lookfile, namespace="test")
    assert marker.Color == pyfbsdk.FBColor(1, 1, 1)


def test_markerlook_from_model(marker):  # type: (pyfbsdk.FBModelMarker) -> None
    """It can initialize MarkerLook from a marker in scene."""
    marker.Color = pyfbsdk.FBColor(1, 1, 1)
    marker_look = mobulook.MarkerLook.from_model(marker)

    assert marker_look.color == marker.Color


def test_markerlook_serialize(marker):  # type: (pyfbsdk.FBModelMarker) -> None
    """It can serialize data from MarkerLook instance."""
    marker.Color = pyfbsdk.FBColor(1, 1, 1)
    data = mobulook.MarkerLook.from_model(marker).serialize()

    assert data["color"] == marker.Color.GetList()


def test_markerlook_deserialize(marker):  # type: (pyfbsdk.FBModelMarker) -> None
    """It can initialize MarkerLook from serialized data."""
    marker.Color = pyfbsdk.FBColor(1, 1, 1)
    data = mobulook.MarkerLook.from_model(marker).serialize()

    marker_look = mobulook.MarkerLook.from_serialized(data)
    assert marker_look.color == pyfbsdk.FBColor(1, 1, 1)


def test_markerlook_apply(marker):  # type: (pyfbsdk.FBModelMarker) -> None
    """It can apply MarkerLook data to a given marker."""
    marker_look = mobulook.MarkerLook.from_model(marker)
    marker_look.color = pyfbsdk.FBColor(1, 1, 1)
    marker_look.apply(marker)

    assert marker.Color == pyfbsdk.FBColor(1, 1, 1)
