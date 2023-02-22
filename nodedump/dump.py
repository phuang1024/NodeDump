import json
import pickle

import bpy


def dump_link(link: bpy.types.NodeLink, nodes: list[bpy.types.Node]):
    return {
        "from_ind": nodes.index(link.from_node),
        "from_socket": link.from_socket.identifier,
        "to_ind": nodes.index(link.to_node),
        "to_socket": link.to_socket.identifier,
    }


def dump_node(node: bpy.types.Node):
    loc = node.location
    return {
        "location": (loc[0], loc[1]),
        "hidden": node.hide,
        "type": node.bl_idname,
        "name": node.name,
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
