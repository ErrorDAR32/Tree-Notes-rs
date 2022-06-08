use std::io::{Read, Write};
use std::path::Path;
use std::str::SplitWhitespace;

use crate::explorer::Explorer;
use crate::note::Note;
use crate::notes::Notes;

mod note;
mod notes;
mod explorer;

pub fn save_to_file(notes: &Notes, path: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let mut file = std::fs::File::create(path)?;
    let json = serde_json::to_string(notes)?;
    file.write_all(json.as_bytes())?;
    Ok(())
}

pub fn load_from_file(path: &Path) -> Result<Notes, Box<dyn std::error::Error>> {
    let mut file = std::fs::File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    let notes: Notes = serde_json::from_str(&contents)?;
    Ok(notes)
}

pub fn fold_tokens(tokens: SplitWhitespace) -> String {
    tokens
        .fold(String::new(),
              |mut acc, t| {
                  acc.push_str(t);
                  acc.push(' ');
                  acc
              })
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let notes = Notes::new();
    let mut explorer = Explorer::new(notes);
    let mut input = String::new();

    loop {
        print!(">>> ");
        std::io::stdout().flush()?;

        input.clear();
        std::io::stdin().read_line(&mut input)?;
        let mut tokens = input.trim().split_whitespace();


        let token = if let Some(t) = tokens.next() {
            t
        } else {
            continue;
        };

        match token {
            "save" => {
                save_to_file(&explorer.notes, Path::new(&fold_tokens(tokens)))?;
            }

            "load" => {
                explorer.notes = load_from_file(Path::new(&fold_tokens(tokens)))?;
                explorer.current = explorer.notes.root;
            }

            "get_sons" => {
                for id in &explorer.notes.get_note(explorer.current).sons {
                    let note = explorer.notes.get_note(*id);
                    println!("{}, {}", note.title, note.id);
                }
            }

            "go_up" => {
                explorer.go_up();
            }

            "goto" => {
                if let Some(id) = tokens.next() {
                    if let Ok(id) = id.parse::<u128>() {
                        if explorer.notes.notes.contains_key(&id) {
                            explorer.current = id;
                        } else {
                            println!("No such note");
                        }
                    } else {
                        println!("Invalid id");
                    }
                } else {
                    println!("No id provided");
                }
            }

            "edit" => {
                let new_body = scrawl::with(explorer.get_current_note().body.as_str())?;
                explorer.get_current_note_mut().body = new_body.to_string();
            }

            "clear" => {
                explorer.get_current_note_mut().clear_note();
            }

            "new" => {
                let mut new_note = Note::new();

                new_note.title = fold_tokens(tokens);

                explorer.notes.add_note(new_note, explorer.current);
            }

            "title" => {
                let new_title = fold_tokens(tokens);

                if new_title.is_empty() {
                    println!("No title provided");
                }
                explorer.get_current_note_mut().title = new_title;
            }

            "remove" => {
                if let Some(id) = tokens.next() {
                    if let Ok(id) = id.parse::<u128>() {
                        if explorer.notes.notes.contains_key(&id) {
                            explorer.current = id;
                        } else {
                            println!("Invalid id");
                        }
                    } else {
                        println!("Invalid id");
                    }
                } else {
                    println!("No id provided");
                }
            }

            "current" => {
                let note = explorer.get_current_note();
                println!("{}\n {}", note.title, note.body);
            }

            _ => {
                println!("Unknown command '{} {}'", token, fold_tokens(tokens));
            }
        }
    }
}
