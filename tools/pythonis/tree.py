from typing import List
from pythonis.helpers import is_float

class Node:
    def __init__(self, name: str, level=-1, parent=None, children=None):
        if children is None:
            children = []

        # raw string data
        self.raw = name

        self.singleChild = True
        self.children : List[Node] = children
        self.parent: Node = parent
        self.level = level #self.computeLvl()

    def computeLvl(self) -> int:
        level = -1
        curr_node = self
        while curr_node.parent is not None:
            level += 1
            curr_node = curr_node.parent
        return level

    def reset(self, newName=""):
        self.raw = newName
        self.singleChild = True
        self.children = []

    def getSingleChildVal(self) -> str:
        assert self.singleChild
        return self.children[0].getVal()

    def getVal(self) -> str:
        return self.raw

    def getNum(self) -> int:
        if self.raw.isnumeric():
            return int(self.raw)
        return 0

    def setVal(self, value: str) -> None:
        self.raw = value

    def addChild(self, name: str):
        self.children.append(Node(name, self.level + 1, self))
        return self.children[-1] # return reference

    def getChild(self, name: str):
        for child in self.children:
            if child.getVal() == name:
                return child
        return None

    def toText(self) -> str:
        if not self.children:
            return (self.level * "\t") + self.raw + "\n"

        if self.singleChild:
            return (self.level * "\t") + self.raw + " = " + self.children[0].getVal() + "\n"

        childrenStr = ""
        for child in self.children:
            childrenStr += child.toText()
        return (self.level * "\t") + self.raw + " = {\n" + childrenStr + (self.level * "\t") + "}\n"

    def walkTree(self, function):
        function(self)
        for child in self.children:
            child.walkTree(function)


class Tree:
    def __init__(self):
        self.root = Node("")
        self.root.singleChild = False

    def toText(self) -> str:
        childrenStr = ""
        if self.root.children:
            for child in self.root.children:
                childrenStr += child.toText() + "\n"
        return childrenStr

    def walkTree(self, function) -> None:
        """ Apply function on every node in this tree (except root, which is empty)"""
        for child in self.root.children:
            child.walkTree(function)

    def walkTopLevelNodes(self, function) -> None:
        """ Apply function on top level nodes only (children of root)"""
        for child in self.root.children:
            function(child)
