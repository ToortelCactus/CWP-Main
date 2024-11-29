from pythonis.parser import parse_dir, to_file
from pythonis.tree import Node
from pythonis.tree import Tree

import os


#helper functions
def thisRegion(node: Node) -> str:
    return '"' + node.parent.parent.getVal().split(':')[1] + '"'

def thisCountry(node: Node) -> str:
    return '"c:' + node.parent.getVal().split(':')[1] + '"'

def thisTag(node: Node) -> str:
    return node.parent.getVal().split(':')[1]


capitals = dict()

# walkers functions
def fetchCapitalStates(node: Node):
    if node.raw == "capital":
        capitals[node.parent.raw] = node.children[0].getVal()

def updateBuilding(node: Node):
    if node.raw == "create_building":
        child: Node = node.getChild("level")

        if child is not None:
            levels = child.children[0].getNum()

            child.reset("add_ownership")
            child.singleChild = False

            # TODO: if something, decide / distribute

            # workers only for now
            b = child.addChild("building")
            b.singleChild = False
            b.addChild("type").addChild('"' + node.getChild("building").getSingleChildVal() + '"')
            b.addChild("country").addChild(thisCountry(node))
            b.addChild("levels").addChild(str(levels))
            b.addChild("region").addChild(thisRegion(node))

            return #DEBUG

            # state owned
            c = child.addChild("country")
            c.singleChild = False
            c.addChild("country").addChild(thisCountry(node))
            c.addChild("levels").addChild(str(levels))

            # workers
            b = child.addChild("building")
            b.singleChild = False
            b.addChild("type").addChild('"' + node.getChild("building").getSingleChildVal() + '"')
            b.addChild("country").addChild(thisCountry(node))
            b.addChild("levels").addChild(str(levels))
            b.addChild("region").addChild(thisRegion(node))

            # private in capital "building_financial_district"
            b = child.addChild("building")
            b.singleChild = False
            b.addChild("type").addChild('"building_financial_district"')
            b.addChild("country").addChild(thisCountry(node))
            b.addChild("levels").addChild(str(levels))
            b.addChild("region").addChild('"' + capitals[thisTag(node)] + '"')

            # local manor
            b = child.addChild("building")
            b.singleChild = False
            b.addChild("type").addChild('"building_manor_house"')
            b.addChild("country").addChild(thisCountry(node))
            b.addChild("levels").addChild(str(levels))
            b.addChild("region").addChild(thisRegion(node))

def removeOwnershipPMs(node: Node):
    if node.raw == "activate_production_methods":
        for child in node.children:
            if "privately_own" in child.raw or \
                    "nt_guilds" in child.raw or \
                    "publicly_own" in child.raw or \
                    "government_ru" in child.raw or \
                    "worker_coop" in child.raw:
                node.children.remove(child)
                return

# get capitals loaded
if os.name == "nt":
    country_trees = parse_dir("..\\common\\country_definitions\\")
else:
    country_trees = parse_dir("../common/country_definitions/")
for tree in country_trees.values():
    tree.walkTree(fetchCapitalStates)

# update the buildings
if os.name == "nt":
    trees = parse_dir("..\\common\\history\\buildings\\")
else:
    trees = parse_dir("../common/history/buildings/")
for tree in trees.values():
    tree.walkTree(updateBuilding)

for file, tree in trees.items():
    to_file(file.split("\\")[-1], tree)

