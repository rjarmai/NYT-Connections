import json
from tkinter import *
from tkinter import messagebox

COLORS = ['YELLOW', 'GREEN', 'BLUE', 'PURPLE']


def save_to_json():
    selected_lang = language_var.get()
    if selected_lang == "English":
        file_name = "categories_eng.json"
    else:
        file_name= "categories_hun.json"
    new_data = {}

    for i in range(4):
        explanation = explanation_entries[i].get().strip().upper()
        words = [word_entries[i][j].get().strip().upper() for j in range(4)]

        if not explanation or any(not w for w in words):
            messagebox.showerror("Error", f"Fill all entries in {i + 1}. category!")
            return

        new_data[f'category{i+1}'] = {
            "words": words,
            "color": COLORS[i],
            "explanation": explanation
        }
    try:
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                current_data = json.load(file)
                if not isinstance(current_data, list):
                    current_data = [current_data]
        except (FileNotFoundError, json.JSONDecodeError):
            current_data = []

        current_data.append(new_data)

        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(current_data, file, ensure_ascii=False, indent=4)

        messagebox.showinfo("Success", f"Categories succesfully saved to {file_name}")

        for i in range(4):
            explanation_entries[i].delete(0, END)
            for j in range(4):
                word_entries[i][j].delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Unable to save:\n{e}")



root = Tk()
root.title("Connections - Game editor")
root.config(padx=10, pady=10)


language_var = StringVar(root)
language_var.set("Magyar")

lang_frame = Frame(root)
lang_frame.grid(row=0, column=0, pady=(0, 10), sticky="w", padx=10)

Label(lang_frame, text="Language:", font=("Arial", 10, "bold")).pack(side=LEFT)
lang_menu = OptionMenu(lang_frame, language_var, "Magyar", "English")
lang_menu.config(width=10)
lang_menu.pack(side=LEFT, padx=10)


explanation_entries = []
word_entries = []

for i in range(4):
    frame = LabelFrame(root, text=f"{i + 1}. Category ({COLORS[i].upper()})", padx=10, pady=10)
    frame.grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")

    Label(frame, text="Explanation: ").grid(row=0, column=0, sticky="e")
    expl_entry = Entry(frame, width=50)
    expl_entry.grid(row=0, column=1, columnspan=4, pady=5)
    explanation_entries.append(expl_entry)

    Label(frame, text="4 words:").grid(row=1, column=0, sticky="e")

    cat_words = []
    for j in range(4):
        word_entry = Entry(frame, width=15)
        word_entry.grid(row=1, column=j + 1, padx=2)
        cat_words.append(word_entry)

    word_entries.append(cat_words)

save_btn = Button(root, text="Save", command=save_to_json, bg="#445A67", fg="white",
                     font=("Arial", 12, "bold"))
save_btn.grid(row=5, column=0, pady=20)

root.mainloop()