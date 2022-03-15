# Mobu Look - Motionbuilder Marker Look Serializer

Save and load Motionbuilder FBModelMarker look properties to json.

## How to use

We provide a `save` function that dump a list of `FBModelMarker` to a json file:

```python
import mobulook
markers = []  # <- This is the list of FBModelMarker to save
mobulook.save("C:/output.json", markers)
```

And a `load` function that take a path to a previously savec json file, and use
apply its content to the matching marker in scene.

```python
mobulook.load("C:/output.json")
```

The json file contain a mapping of marker_name -> look_data.
Only the marker **Name** is saved, namespace is ommited.

When loading the file, a prefix namespace can be applied to apply the look to
the correct objects.

```python
# Load the content of "output.json" to markers matching names under the
# "Character_Ctrl" namespace
mobulook.load("C:/output.json", namespace="Character_Ctrl")
```

## Examples

### Save all FBModelMarker in hierarchy

```python
import pyfbsdk
import mobulook

def hierarchy(root): # (pyfbsdk.FBModel) -> Generator[pyfbsdk.FBModel, None, None]
    """Iter through models in hierarchy starting from 'root'."""
    root = root or pyfbsdk.FBSystem().SceneRootModel
    stack = [root]
    while stack:
        model = stack.pop()
        yield model
        stack.extend(model.Children)

# Save all FBModelMarkers in the hierarchy of "MyRootModel"
root = pyfbsdk.FBFindModelByName("MyRootModel")
mobulook.save("C:/output.json", hierarchy(root))
```

### Save all FBModelMarker of current character

```python
import pyfbsdk
import mobulook

character = pyfbsdk.FBApplication().CurrentCharacter
markers = []

# Body Nodes (FK)
for node_id in pyfbsdk.FBBodyNodeId.values.values():
    model = character.GetCtrlRigModel(node_id)
    if model:
        markers.append(model)

# Effectors
for effector in pyfbsdk.FBEffectorId.values.values():
    for effector_set in pyfbsdk.FBEffectorSetID.values.values():
        model = character.GetEffectorModel(effector, effector_set)
        if model:
            markers.append(model)

# Extensions
for extension in character.CharacterExtensions
    markers.extend(extension.Components)

mobulook.save("C:/output.json", markers)
```
