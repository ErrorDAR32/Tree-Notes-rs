use crate::note::Note;
use crate::notes::Notes;

pub struct Explorer {
    pub(crate) notes: Notes,
    pub(crate) current: u128,
}

impl Explorer {
    pub fn new(notes: Notes) -> Self {
        Explorer {
            current: notes.root,
            notes,
        }
    }

    pub fn go_up(&mut self) {
        let father = self.notes.get_note_mut(self.current).father;
        self.current = father;
    }

    pub fn get_current_note(&mut self) -> &Note {
        self.notes.get_note(self.current)
    }

    pub fn get_current_note_mut(&mut self) -> &mut Note {
        self.notes.get_note_mut(self.current)
    }
}