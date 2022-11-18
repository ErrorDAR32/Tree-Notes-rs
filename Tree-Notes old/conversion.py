import utils
import commands

class filewrapper:
    def __init__(self, string: str):
        self.string = string
        self.charptr = 0
        self.char = string[0]

    def checkcharptr(self):
        if self.charptr == len(self.string):
            return False
        return True

    def nextchar(self):
        if self.checkcharptr():
            self.charptr += 1
            self.char = self.string[self.charptr]
            return self.string[self.charptr]
        return None

    def currchar(self):
        return self.string[self.charptr]

    def lastchar(self):
        return self.string[self.charptr - 1]


class Node:
    def __init__(self, text="", alias="", childs=None):
        if childs is None:
            childs = []
        self.childs = childs
        self.text = text
        self.alias = alias

    def reset(self):
        self.childs = []
        self.text = ""
        self.alias = ""

    def has_alias(self):
        if (self.alias == "") or (not isinstance(self.alias, str)):
            return False
        else:
            return True


def parsenode(file: filewrapper):
    node = Node()
    props = ("a", "t", "c")
    while True:
        if file.nextchar() in props:
            if file.currchar() == "a":
                node.alias = parseproperty(file)
            elif file.currchar() == "t":
                node.text = parseproperty(file)
            elif file.currchar() == "c":
                node.childs = parseproperty(file)
        elif file.currchar() == "}":
            return node


def parsearray(file: filewrapper):
    array = []
    while True:
        if file.nextchar() == "]":
            return array
        elif file.currchar() == "{":
            array.append(parsenode(file))


def parsestring(file: filewrapper):
    string = ""
    while True:
        file.nextchar()
        if (file.currchar() == '"') and (file.lastchar() != '\ '[0]):
            return string
        string += file.currchar()


def parseproperty(file: filewrapper):
    while True:
        if file.nextchar() == '"':
            return parsestring(file)
        elif file.currchar() == '[':
            return parsearray(file)


def descision(prompt: str, options=[["Y", "y"], ["N", "n"]]):
    while True:
        choice = input(prompt)
        for option in options:
            if isinstance(option, list):
                for version in option:
                    if version == choice:
                        return option
            elif isinstance(option, str):
                if option == choice:
                    return option


def load(args):
    """load <filename>
    used to load a note tree from storage, if no argument is given it will try to use the last file name used by
    save, csave, or load"""
    recent_file = args

    try:
        with open(recent_file, "rt") as f:
            file = filewrapper(f.read())
    except:
        print(f"Error while reading {recent_file}")
        return

    newnode = parsenode(file)
    print(newnode)
    return newnode


tag_text = "text".encode("UTF-8")
tag_name = "name".encode("UTF-8")


def old_to_note(old: Node, father=None):
    note = utils.Note(
        name=old.alias,
        text=old.text,
        father=father
    )
    note.subnotes = [old_to_note(sub, father) for sub in old.childs]
    return note


old = load("notes.trnts")
new = old_to_note(old)
commands.current = new
commands.save("new.trnts")