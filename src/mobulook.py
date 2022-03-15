"""Save and load Motionbuilder FBModelMarker look properties to json."""
from __future__ import absolute_import, division, print_function

import json

import pyfbsdk


class MarkerLook(object):
    """Store and FBModelMarker Look properties."""

    _LOOKS = (
        pyfbsdk.FBMarkerLook.kFBMarkerLookAimRollGoal,
        pyfbsdk.FBMarkerLook.kFBMarkerLookBone,
        pyfbsdk.FBMarkerLook.kFBMarkerLookBox,
        pyfbsdk.FBMarkerLook.kFBMarkerLookCapsule,
        pyfbsdk.FBMarkerLook.kFBMarkerLookCircle,
        pyfbsdk.FBMarkerLook.kFBMarkerLookCube,
        pyfbsdk.FBMarkerLook.kFBMarkerLookHardCross,
        pyfbsdk.FBMarkerLook.kFBMarkerLookLightCross,
        pyfbsdk.FBMarkerLook.kFBMarkerLookNone,
        pyfbsdk.FBMarkerLook.kFBMarkerLookRigidGoal,
        pyfbsdk.FBMarkerLook.kFBMarkerLookRotationGoal,
        pyfbsdk.FBMarkerLook.kFBMarkerLookSphere,
        pyfbsdk.FBMarkerLook.kFBMarkerLookSquare,
        pyfbsdk.FBMarkerLook.kFBMarkerLookStick,
    )

    def __init__(
        self,
        offset_translation,  # type: pyfbsdk.FBVector3d
        offset_rotation,  # type: pyfbsdk.FBVector3d
        offset_scaling,  # type: pyfbsdk.FBVector3d
        look,  # type: pyfbsdk.FBMarkerLook
        size,  # type: float
        color,  # type: pyfbsdk.FBColor
        parent_link,  # type: bool
        length,  # type: float
    ):  # type: (...) -> None
        super(MarkerLook, self).__init__()

        self.offset_translation = offset_translation
        self.offset_rotation = offset_rotation
        self.offset_scaling = offset_scaling
        self.look = look
        self.size = size
        self.color = color
        self.parent_link = parent_link
        self.length = length

    @classmethod
    def from_model(cls, marker):  # type: (pyfbsdk.FBModelMarker) -> MarkerLook
        """Initialize from a marker."""
        return cls(
            offset_translation=marker.GeometricTranslation,
            offset_rotation=marker.GeometricRotation,
            offset_scaling=marker.GeometricScaling,
            look=marker.Look,
            size=marker.Size,
            color=marker.Color,
            parent_link=marker.PropertyList.Find("Show Parent Link").Data,
            length=marker.Length,
        )

    @classmethod
    def from_serialized(cls, data):  # type: (dict) -> MarkerLook
        """Initialize from a serialized dict."""
        return cls(
            offset_translation=pyfbsdk.FBVector3d(data["offset_translation"]),
            offset_rotation=pyfbsdk.FBVector3d(data["offset_rotation"]),
            offset_scaling=pyfbsdk.FBVector3d(data["offset_scaling"]),
            look=cls._LOOKS[data["look"]],
            size=data["size"],
            color=pyfbsdk.FBColor(data["color"]),
            parent_link=data["parent_link"],
            length=data["length"],
        )

    def __repr__(self):  # type: () -> str
        attrs = ", ".join(
            "{}={}".format(name, repr(value))
            for name, value in self.serialize().items()
        )
        return "{}({})".format(self.__class__.__name__, attrs)

    def serialize(self):  # type: () -> dict
        """Serialize this instance to a dict."""
        return {
            "offset_translation": self.offset_translation.GetList(),
            "offset_rotation": self.offset_rotation.GetList(),
            "offset_scaling": self.offset_scaling.GetList(),
            "look": self._LOOKS.index(self.look),
            "size": self.size,
            "color": self.color.GetList(),
            "parent_link": self.parent_link,
            "length": self.length,
        }

    def apply(self, marker):  # type: (pyfbsdk.FBModelMarker) -> None
        """Set instance data to marker."""
        marker.Look = self.look
        marker.Size = self.size
        marker.GeometricTranslation = self.offset_translation
        marker.GeometricRotation = self.offset_rotation
        marker.GeometricScaling = self.offset_scaling
        marker.Color = self.color
        marker.PropertyList.Find("Show Parent Link").Data = self.parent_link
        marker.Length = self.length


def save(path, markers):  # type: (str, list[pyfbsdk.FBModelMarker]) -> None
    """Save the look of a list of `markers` to a json file `path`.

    Args:
        path: Output json file path.
        markers: List of markers to save.
    """
    data = {}
    for marker in markers:
        if not isinstance(marker, pyfbsdk.FBModelMarker):
            print("Not a FBModelMarker, ignored: {}".format(marker.Name))
        data[marker.Name] = MarkerLook.from_model(marker).serialize()

    with open(path, "w") as openfile:
        json.dump(data, openfile)


def load(path, namespace=None):  # type: (str, str | None) -> None
    """Load json look file at `path` to matching markers names in scene.

    Args:
        path: Json look file to load.
        namespace: Prefix markers names in json with a optional namespace to
            find them in scene.
    """
    with open(path, "r") as openfile:
        serialized_data = json.load(openfile)

    for name, data in serialized_data.items():
        full_name = "{}:{}".format(namespace, name) if namespace else str(name)
        marker = pyfbsdk.FBFindModelByLabelName(full_name)
        marker_look = MarkerLook.from_serialized(data)
        marker_look.apply(marker)
