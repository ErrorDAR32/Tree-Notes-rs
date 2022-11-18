use uuid::Uuid;

#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct Note {
    pub title: String,
    pub body: String,
    pub(crate) id: u128,
    pub(crate) father: u128,
    pub(crate) sons: Vec<u128>,
}

impl Note {
    pub fn new() -> Note {
        let uuid = Uuid::new_v4().as_u128();
        Note {
            title: String::new(),
            body: String::new(),
            id: uuid,
            father: uuid,
            sons: vec![],
        }
    }

    pub fn clear_note(&mut self) {
        self.title.clear();
        self.body.clear();
    }
}

impl Default for Note {
    fn default() -> Self {
        Note::new()
    }
}
