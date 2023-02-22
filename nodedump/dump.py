import json
import pickle

import bpy

COMMON_ATTRS = {
    "mute",
    "label",
    "is_registered_node_type",
    "width",
    "parent",
    "bl_idname",
    "rna_type",
    "show_preview",
    "bl_height_min",
    "draw_buttons_ext",
    "select",
    "bl_description",
    "bl_width_default",
    "outputs",
    "show_options",
    "update",
    "bl_icon",
    "input_template",
    "height",
    "inputs",
    "width_hidden",
    "use_custom_color",
    "hide",
    "output_template",
    "bl_rna",
    "poll_instance",
    "socket_value_update",
    "type",
    "bl_height_default",
    "internal_links",
    "location",
    "bl_height_max",
    "poll",
    "bl_width_min",
    "bl_width_max",
    "color",
    "bl_label",
    "dimensions",
    "show_texture",
    "draw_buttons",
    "name",
    "bl_static_type",
}


def dump_link(link: bpy.types.NodeLink, nodes: list[bpy.types.Node]):
    return {
        "from_ind": nodes.index(link.from_node),
        "from_socket": link.from_socket.identifier,
        "to_ind": nodes.index(link.to_node),
        "to_socket": link.to_socket.identifier,
    }


def dump_node(node: bpy.types.Node):
    loc = node.location

    # Node specific attributes; e.g. math_node.operation
    attrs = {}
    for attr in dir(node):
        if attr not in COMMON_ATTRS and not attr.startswith("_"):
            value = getattr(node, attr)
            # TODO maybe value is a vector?
            attrs[attr] = value

    # User set inputs for each socket.
    inputs = {}
    for i in range(len(node.inputs)):
        inp = node.inputs[i]
        if not hasattr(inp, "default_value"):
            continue

        value = inp.default_value
        if not isinstance(value, (int, float, str)):
            value = list(value)
        inputs[str(i)] = value

    return {
        "location": (loc[0], loc[1]),
        "width": node.width,
        "hidden": node.hide,
        "type": node.bl_idname,
        "name": node.name,
        "attrs": attrs,
        "inputs": inputs,
    }


def dump_tree(tree: bpy.types.NodeTree):
    nodes = list(tree.nodes)
    return {
        "nodes": [dump_node(node) for node in nodes],
        "links": [dump_link(link, nodes) for link in tree.links],
    }


def dumps(tree: bpy.types.NodeTree, fmt: str = "json") -> str | bytes:
    if fmt == "json":
        return json.dumps(dump_tree(tree), indent=4)
    elif fmt == "pickle":
        return pickle.dumps(dump_tree(tree))
    else:
        raise ValueError(f"Unknown format: {fmt}")


def dump(tree: bpy.types.NodeTree, file, fmt: str = "json"):
    file.write(dumps(tree, fmt))
