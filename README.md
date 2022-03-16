# Mobu Look - Motionbuilder Marker Look Serializer

Save and load Motionbuilder FBModelMarker look properties to json.

## How to use

We provide a `save` function that dump a list of `FBModelMarker` to a json file:

```python
import mobulook
markers = []  # <- This is the list of FBModelMarker to save
mobulook.save("C:/look.json", markers)
```

And a `load` function that take a path to a previously savec json file, and use
apply its content to the matching marker in scene.

```python
mobulook.load("C:/look.json")
```

The json file contain a mapping of marker_name -> look_data.
Only the marker **Name** is saved, namespace is ommited.

When loading the file, a prefix namespace can be applied to apply the look to
the correct objects.

```python
# Load "look.json" to matching markers under the "Character_Ctrl" namespace
mobulook.load("C:/look.json", namespace="Character_Ctrl")
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

## Contributing

Dev environment setup using **pyenv** and **poetry**.

### Running the tests in cli

Install python 2.7 with **pyenv** and set it as our local env. Then we tell
**poetry** to use this version to create a venv with the necessary dependencies
(mainly **pytest**).

```cmd
pyenv install 2.7.18
pyenv local 2.7.18
for /f "tokens=*" %a in ('pyenv exec python -c "import sys; print(sys.executable)"') do poetry env use %a
poetry install
```

Now that we have a venv compatible with Motionbuilder 2020 (python 2.7.11), we
need to add the `site-packages` directory of our poetry venv to PYTHONPATH (to
find pytest) and the `mobulook/src` directory (to find our module).

```cmd
set PYTHONPATH=<PATH_TO_VENV>\Lib\site-packages;%PYTHONPATH%
set PYTHONPATH=<PATH_TO_MOBULOOK>\src;%PYTHONPATH%
```

#### Motionbuilder 2022 and above

We can now run the tests using the `mobupy` interpreter.

```cmd
mobupy -m pytest
```

#### Motionbuilder 2020 and below

We can't use the mobupy interpreter of Motionbuilder 2020, it crashes as soon as
you use pyfbsdk.

Instead we can use the main application to run our tests.

Create a python runner script. Note that the path to our test file has to be an
absolute path, the `__file__` variable will be undefined in our case.

```python
# runner.py
import pytest
pytest.main(["<PATH_TO_MOBULOOK>/test_mobulook.py", "--capture=sys"])
```

And execute this runner script from Motionbuilder CLI

```cmd
motionbuilder.exe <PATH_TO_RUNNER_SCRIPT>
```

Check the **Python Editor Window** of Motionbuilder for the results.

### Running the tests in VSCode

> This only work with Motionbuilder >= 2022.

Follow the first step of the section above to install a python venv. But instead
of adding to PYTHONPATH in a shell, we can create an `.env` file at the root of
our package directory and reference it in the project settings:

- `mobulook/.env`:

```text
PYTHONPATH=<PATH_TO_VENV>\Lib\site-packages;${PYTHONPATH}
PYTHONPATH=<PATH_TO_MOBULOOK>\src;${PYTHONPATH}
```

- `mobulook/.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "<PATH_TO_MOBUPY>",
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.envFile": "${workspaceFolder}/.env",
}
```

Now you can run the tests in the **Testing** tab of VSCode.
