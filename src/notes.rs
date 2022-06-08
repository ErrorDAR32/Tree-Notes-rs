use std::collections::HashMap;

use super::note::Note;

//constraints:
//  a u128 must always point to valid note, since unwrap is used
//  root is always a valid note, deleting it will result a new empty root note
//  only root note is allowed to have itself as a parent
#[derive(Debug, serde::Serialize, serde::Deserialize)]
pub struct Notes {
    pub(crate) notes: HashMap<u128, Note>,
    pub(crate) root: u128,
}

impl Notes {
    pub fn new() -> Self {
        let mut notes = Notes {
            notes: HashMap::new(),
            root: 0,
        };

        let root = Note::new();
        notes.root = root.id;
        notes.notes.insert(root.id, root);
        notes
    }

    pub fn get_note_mut(&mut self, id: u128) -> &mut Note {
        self.notes.get_mut(&id).unwrap()
    }

    pub fn get_note(&self, id: u128) -> &Note {
        self.notes.get(&id).unwrap()
    }

    pub fn add_note(&mut self, mut note: Note, father: u128) {
        self.notes.get_mut(&father).unwrap().sons.push(note.id);
        note.father = father;

        self.notes.insert(note.id, note);
    }

    pub fn delete_note(&mut self, id: u128) {
        if id == self.root {
            *self = Notes::new();
            return;
        }

        let father = self.get_note_mut(id).father;
        self.get_note_mut(father).sons.retain(|&x| x != id);

        let mut q = std::collections::vec_deque::VecDeque::from([id]);

        while let Some(id) = q.pop_front() {
            let note = self.notes.remove(&id).unwrap();
            for son in note.sons.iter() {
                q.push_back(*son);
            }
        }
    }
}

impl Default for Notes {
    fn default() -> Self {
        Notes::new()
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn remove_root_node() {
        let mut notes = Notes::new();

        let mut root_note = notes.get_note(notes.root).clone();
        let root_note_id = root_note.id;

        let sub_node = Note::new();
        notes.add_note(sub_node, root_note_id);

        notes.delete_note(root_note_id);


        root_note.sons = vec!();
        assert_ne!(notes.get_note(notes.root).id, root_note.id);
        assert_eq!(*notes.get_note(notes.root).sons, []);
        assert_eq!(notes.notes.len(), 1);
    }

    #[test]
    fn remove_sub_node() {
        let mut notes = Notes::new();


        let mut root_note = notes.get_note(notes.root).clone();
        let root_note_id = root_note.id;

        let sub_node = Note::new();
        let snid = sub_node.id;
        notes.add_note(sub_node, root_note_id);

        notes.delete_note(snid);


        root_note.sons = vec!();
        assert_eq!(notes.get_note(notes.root).id, root_note_id);
        assert_eq!(*notes.get_note(notes.root).sons, []);
        assert_eq!(notes.notes.len(), 1);
    }
}