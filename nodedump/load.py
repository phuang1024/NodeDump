import json
import pickle

import bpy


def load_link(tree: bpy.types.NodeTree, nodes: list[bpy.types.Node], data: dict):
    from_node = nodes[data["from_ind"]]
    from_socket = from_node.outputs[data["from_socket"]]
    to_node = nodes[data["to_ind"]]
    to_socket = to_node.inputs[data["to_socket"]]
    tree.links.new(from_socket, to_socket)


def load_node(tree: bpy.types.NodeTree, data: dict):
    node = tree.nodes.new(data["type"])
    node.location = data["location"]
    node.hide = data["hidden"]
    node.name = data["name"]

    for attr, value in data["attrs"].items():
        setattr(node, attr, value)

    for i, value in data["inputs"].items():
        node.inputs[int(i)].default_value = value

    return node


def load_tree(tree: bpy.types.NodeTree, data: dict):
    nodes = [load_node(tree, node_data) for node_data in data["nodes"]]
    for link_data in data["links"]:
        load_link(tree, nodes, link_data)


def loads(tree: bpy.types.NodeTree, data: str | bytes, fmt: str = "json"):
    if fmt == "json":
        load_tree(tree, json.loads(data))
    elif fmt == "pickle":
        load_tree(tree, pickle.loads(data))
    else:
        raise ValueError(f"Unknown format: {fmt}")


def load(tree: bpy.types.NodeTree, file, fmt: str = "json"):
    loads(tree, file.read(), fmt)
