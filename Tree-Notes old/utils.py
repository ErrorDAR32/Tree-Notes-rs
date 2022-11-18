import SSS


class Note:
    def __init__(self, text="", name="", subnotes=None, father=None):
        if subnotes is None:
            subnotes = []
            subnotes: list[Note]
        self.text = text
        self.name = name
        self.subnotes = subnotes
        self.father = father

    def addchild(self, *args, **kwargs):
        self.subnotes.append(Note(*args, father=self, **kwargs))


tag_text = "text".encode("UTF-8")
tag_name = "name".encode("UTF-8")


def getroot(note: Note):
    if note.father is None:
        return note
    getroot(note.father)


def note_to_sss(note: Note):
    SSSObj = SSS.SSSObject()
    SSSObj.named_fields[tag_text] = note.text.encode("UTF-8")
    SSSObj.named_fields[tag_name] = note.name.encode("UTF-8")

    for sub in note.subnotes:
        SSSObj.fields.append(note_to_sss(sub))
    return SSSObj


def sss_to_note(sssobj: SSS.SSSObject, father=None):
    n = sssobj.named_fields
    note = Note(
        name=n[tag_name].decode("UTF-8"),
        text=n[tag_text].decode("UTF-8"),
        father=father
    )
    note.subnotes = [sss_to_note(sub, note) for sub in sssobj.fields]
    return note
