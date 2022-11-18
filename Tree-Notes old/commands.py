import utils
import SSS
import editor
# this have to be defined in order for most commands to work
current = utils.Note()

# this one is used by save and load to "use" the "last filename"
lastfile = None


def exit(*args,**kwargs):
    raise


def goup(*args, **kwargs):
    """go to the note above in the tree, until you are on the root note"""
    global current
    if current.father is not None:
        current = current.father
    else:
        print("at the root already!")


def goto(*args, **kwargs):
    """go to <name> note."""
    name = args[0]
    global current
    for sub in current.subnotes:
        if sub.name == name:
            current = sub
            break
    else:
        print("invalid name!")


def see(*args, **kwargs):
    """see the contents of <name> note"""
    if args:
        name = args[0]
        for sub in current.subnotes:
            if sub.name == name:
                note = sub
                break
        else:
            print("invalid name")
            return
    else:
        note = current
    print(note.text)


def create(*args, **kwargs):
    """create a subnote of the current note named <name>"""
    if args:
        name = args[0]
    else:
        print("name required")
        return
    if name == '':
        print("invalid name!")
        return

    for sub in current.subnotes:
        if sub.name == name:
            print("name already used!")
            return
    current.addchild(name=name)


def delete(*args, **kwargs):
    """delete <name> note"""
    name = args[0]
    for sub in range(len(current.subnotes)):
        if current.subnotes[sub].name == name:
            current.subnotes.pop(sub)
            return
    else:
        print("Invalid name")


def ls(*args, **kwargs):
    """see the names of the subnotes of the current note"""
    if len(current.subnotes) == 0:
        print("None!")
    for sub in current.subnotes:
        print(sub.name)


def save(*args, **kwargs):
    global lastfile

    serialized = utils.note_to_sss(utils.getroot(current))
    serialized = SSS.serialize(serialized)
    if args:
        lastfile = open(args[0], "wb+")

    if lastfile is not None:
        lastfile.seek(0)
        lastfile.write(serialized)
        lastfile.flush()
    else:
        print("filename required")


def load(*args, **kwargs):
    global lastfile
    global current

    if args:
        lastfile = open(args[0], "rb+")
    if lastfile is not None:
        notes = SSS.parse(lastfile)
        notes = utils.sss_to_note(notes)
        current = notes
    else:
        print("filename required")


def edit(*args, **kwargs):
    if args:
        name = args[0]
        for sub in current.subnotes:
            if sub.name == name:
                note = sub
                break
        else:
            print("invalid name")
            return
    else:
        note = current

    note.text = editor.editor(note.text)


def search(*args, note=None, route="", **kwargs):
    if note is None:
        note = utils.getroot(current)
    route += "/" + note.name
    for arg in args:
        if note.text.find(arg) != (-1):
            print(f"match found in text of {route}")
        if note.name.find(arg) != (-1):
            print(f"match found at {route}")
    for sub in note.subnotes:
        search(*args, note=sub, route=route)


funcs = [create, delete, see, goto, goup, ls, save, load, edit, exit, search]
