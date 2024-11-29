import glob
from typing import Dict

from pythonis.tree import Tree


def valid_chars(char: str):
    return char.isalnum() or char == "_"


def treeify(filename: str) -> Tree:
    result = Tree()
    currentNode = result.root

    tokens = []

    with open(filename, "r", encoding="utf-8") as file:
        commentLessLines = []

        # remove comments (they need information about line endings)
        for line in file.readlines():
            line = line.strip()

            if line:
                # comment is comment, maybe do something with it later
                if line[0] == "#":
                    continue

                # process line further
                commentless = line.split("#")[0].strip()
                commentLessLines.append(commentless)

    # process those lines into tokens
    for line in commentLessLines:
        spaceSeparatedTokens = line.split(" ")

        for sst in spaceSeparatedTokens:
            sst = sst.strip()
            if "=" in sst and len(sst) > 1:
                parts = sst.split("=")
                assert len(parts) == 2

                if parts[0]:
                    tokens.append(parts[0])
                tokens.append("=")
                if parts[1]:
                    tokens.append(parts[1])

            elif ("{" in sst or "}" in sst) and len(sst) > 1:
                if "{" in sst or "}" in sst:
                    if "hsv" in sst: # damn paradox and their weird hsv color additions
                        if "{" in sst:
                            sst = "{"
                        if "}" in sst:
                            sst = "}"
                        assert len(sst) == 1
                        tokens.append(sst)
                        continue

                    brSeparatedTokens = sst.split("{")
                    tmpTokens = []
                    for t in brSeparatedTokens:
                        if t:
                            tmpTokens.append(t)
                        tmpTokens.append("{")
                    tmpTokens.pop()

                    for tmpt in tmpTokens:
                        brSeparatedTokens = tmpt.split("}")
                        for t in brSeparatedTokens:
                            if t:
                                tokens.append(t)
                            tokens.append("}")
                        tokens.pop()

            else:
                tokens.append(sst)

    # general sanity check
    l = 0
    r = 0
    for token in tokens:
        if "{" in token or "}" in token:
            assert len(token) == 1

        if token == "{":
            l += 1
        if token == "}":
            r += 1

    assert l == r
    # end of sanity check

    for token in tokens:
        if not token:
            continue

        # end of node, step back
        if token == "}":
            if currentNode.parent is None:
                # duh, this is root
                print("duh")
                continue

            currentNode = currentNode.parent
            continue

        if token == "{":
            if currentNode.parent is None:
                # duh, this is root
                print("duh")
                continue

            assert currentNode.singleChild is True
            currentNode.singleChild = False
            continue

        if token == "=":
            assert currentNode.children

            currentNode = currentNode.children[-1]
            continue

        # else its a node
        currentNode.addChild(token)

        # in this case also step back
        if currentNode.singleChild:
            assert len(currentNode.children) == 1
            currentNode = currentNode.parent

    return result


def to_file(filename: str, tree: Tree):
    with open(".\\generated\\" + filename, "w", encoding="utf-8") as output:
        output.write(tree.toText())


def parse_dir(path: str, recursive=False) -> Dict[str, Tree]:
    trees = dict()

    for filename in glob.glob(path + "*.txt", recursive=recursive):
        if "unwanted" in filename or "unused" in filename:
            continue
        trees[filename] = treeify(filename)

    return trees
