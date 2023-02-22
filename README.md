# NodeDump

Serialize and unpack Blender node trees from the Python API.

## Usage

This is not an add-on; put it in the scripts directory and import it from another program.

```py
import bpy
import nodedump

node_tree = bpy.data.materials["Material"].node_tree

## Saving

# Save to file
with open("file.json", "w") as f:
    nodedump.dump(node_tree, f)

# or return a string
data = nodedump.dumps(node_tree)

## Loading

# Load from file
with open("file.json", "r") as f:
    # Contents of file are written to node tree.
    nodedump.load(node_tree, f)

# or load from string
nodedump.loads(node_tree, data)
```
