import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
import shutil, os

BG_COLOR = "#202020"
BTN_BG_COLOR = "#343a40"
ACTIVE_BTN_BG_COLOR = "#495057"
FG_COLOR = "#FFFFFF"
FG_COLOR_2 = "#C2C2C2"

folders = ['None']

file_types = {
    'documents': ('.docx', '.pdf', '.txt', '.pptx', '.xlsx'),
    'images': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'),
    'audio': ('.mp3', '.wav', '.aac', '.flac', '.ogg'),
    'videos': ('.mp4', '.mov', '.avi', '.wmv', '.mkv'),
    'archives': ('.zip', '.rar', '.7z'),
    'programs': ('.html', '.css', '.js', '.py', '.java', '.cpp', '.ts')
}


def create_header_label(parent, text: str) -> tk.Label:
    label = tk.Label(parent, text=text, background=BG_COLOR, foreground=FG_COLOR, font=("Arial", 23))

    return label


def create_paragraph_label(parent, text: str) -> tk.Label:
    label = tk.Label(parent, text=text, background=BG_COLOR, foreground=FG_COLOR_2, font=("Arial", 13))

    return label


def create_button(parent, text: str, command=None) -> tk.Button:
    button = tk.Button(
        parent, text=text, background=BTN_BG_COLOR, activebackground=ACTIVE_BTN_BG_COLOR, activeforeground=FG_COLOR,
        foreground=FG_COLOR, font=("Arial", 13), command=command, bd=0, padx=7, pady=3, cursor="hand2"
    )

    return button


def choose_source_location() -> None:
    source_folder = filedialog.askdirectory(initialdir="/", title="Select source location")

    source_entry_widget.delete(0, tk.END)
    source_entry_widget.insert(0, source_folder)


def choose_destination_location() -> None:
    source_folder = filedialog.askdirectory(initialdir="/", title="Select destination location")

    destination_entry_widget.delete(0, tk.END)
    destination_entry_widget.insert(0, source_folder)


def create_combo_box(parent, string_var) -> ttk.Combobox:
    combo_box = ttk.Combobox(parent, width=27, textvariable=string_var, state='readonly', foreground=FG_COLOR)
    combo_box['values'] = folders
    combo_box.current(0)

    return combo_box


def create_entry(parent, length: int, string_var) -> tk.Entry:
    entry = tk.Entry(parent, width=length, background=BTN_BG_COLOR, foreground=FG_COLOR,
                     highlightcolor=FG_COLOR, font=("Arial", 12), justify="left", bd=0, textvariable=string_var)

    return entry


def add_folder(folder_name) -> None:
    if folder_name in folders:
        messagebox.showerror("Error", "Folder already exists.")
        add_folder_entry.delete(0, tk.END)
        return

    folders.append(folder_name)

    update_combo_boxes()

    add_folder_entry.delete(0, tk.END)


def update_combo_boxes():
    for combo_box in [
        documents_folder_box,
        images_folder_box,
        audio_folder_box,
        videos_folder_box,
        archives_folder_box,
        programs_folder_box
    ]:
        combo_box['values'] = folders


def arrange_files(source, destination, **kwargs) -> None:
    if not source or not destination:
        messagebox.showerror("Error", "Source and destination paths must not be empty!")
        return

    types_and_folders = {k: v for k, v in kwargs.items() if v != "None"}

    directory = Path(source)

    for file_path in directory.iterdir():
        if file_path.is_file():
            file_prefix = str(file_path)[str(file_path).rfind('.'):]

            for category, types in file_types.items():
                if file_prefix in types and category in types_and_folders:
                    folder = f"{destination}/{types_and_folders[category]}/"

                    if not os.path.exists(folder):
                        os.makedirs(folder)

                    shutil.move(file_path, folder)


root = tk.Tk()
root.title("Arrangify")
root.geometry('1280x780')
root.configure(bg="#202020")
root.resizable(False, False)

# Source location widgets

source_label = create_header_label(root, text="Source location")
source_label.place(x=50, y=50)

source_location = tk.StringVar()

source_entry_widget = create_entry(root, 60, source_location)
source_entry_widget.place(x=50, y=120)

choose_source_button = create_button(root, text="Select source location", command=choose_source_location)
choose_source_button.place(x=50, y=165)

# Destination location widgets

destination_label = create_header_label(root, text="Destination location")
destination_label.place(x=675, y=50)

destination_location = tk.StringVar()

destination_entry_widget = create_entry(root, 60, destination_location)
destination_entry_widget.place(x=675, y=120)

choose_destination_button = create_button(root, text="Select destination location", command=choose_destination_location)
choose_destination_button.place(x=675, y=165)

# Combo box styles

style = ttk.Style()
combobox_style = ttk.Style()
combobox_style.theme_create(
    'combobox_style', parent='alt', settings={
        'TCombobox': {
            'configure': {
                'selectbackground': BTN_BG_COLOR,
                'fieldbackground': BTN_BG_COLOR,
                'background': BTN_BG_COLOR,
                'font': ("Arial", 13),
                'padding': (10, 5),
                'arrowcolor': FG_COLOR,
                'borderwidth': 0
            }
        }
    }
)

combobox_style.theme_use('combobox_style')

# Document Files widgets

documents_label = create_header_label(root, text="Document Files Folder")
documents_label.place(x=50, y=230)

documents_types_label = create_paragraph_label(root, text="(.docx, .pdf, .txt, .pptx, .xlsx)")
documents_types_label.place(x=50, y=280)

documents_folder = tk.StringVar()
documents_folder_box = create_combo_box(root, documents_folder)
documents_folder_box.place(x=50, y=330)

# Image Files widgets

images_label = create_header_label(root, text="Image Files Folder")
images_label.place(x=500, y=230)

image_types_label = create_paragraph_label(root, text="(.jpg, .jpeg, .png, .gif, .bmp, .svg)")
image_types_label.place(x=500, y=280)

images_folder = tk.StringVar()
images_folder_box = create_combo_box(root, images_folder)
images_folder_box.place(x=500, y=330)

# Audio Files widgets

audio_label = create_header_label(root, text="Audio Files Folder")
audio_label.place(x=950, y=230)

audio_types_label = create_paragraph_label(root, text="(.mp3, .wav, .aac, .flac, .ogg)")
audio_types_label.place(x=950, y=280)

audio_folder = tk.StringVar()
audio_folder_box = create_combo_box(root, audio_folder)
audio_folder_box.place(x=950, y=330)

# Video Files widgets

videos_label = create_header_label(root, text="Video Files Folder")
videos_label.place(x=50, y=430)

video_types_label = create_paragraph_label(root, text="(.mp4, .mov, .avi, .wmv, .mkv)")
video_types_label.place(x=50, y=480)

videos_folder = tk.StringVar()
videos_folder_box = create_combo_box(root, videos_folder)
videos_folder_box.place(x=50, y=530)

# Archive Files widgets

archives_label = create_header_label(root, text="Archive Files Folder")
archives_label.place(x=500, y=430)

archive_types_label = create_paragraph_label(root, text="(.zip, .rar, .7z)")
archive_types_label.place(x=500, y=480)

archives_folder = tk.StringVar()
archives_folder_box = create_combo_box(root, archives_folder)
archives_folder_box.place(x=500, y=530)

# Program Files widgets

programs_label = create_header_label(root, text="Program Files Folder")
programs_label.place(x=950, y=430)

program_types_label = create_paragraph_label(root, text="(.html, .css, .js, .py, .java, .cpp, .ts)")
program_types_label.place(x=950, y=480)

programs_folder = tk.StringVar()
programs_folder_box = create_combo_box(root, programs_folder)
programs_folder_box.place(x=950, y=530)

# Add folder widgets

add_folder_label = create_header_label(root, text="Add new folder")
add_folder_label.place(x=50, y=600)

new_folder = tk.StringVar()

add_folder_entry = create_entry(root, 30, new_folder)
add_folder_entry.place(x=50, y=665)

add_folder_button = create_button(root, text="Add Folder", command=lambda: add_folder(new_folder.get()))
add_folder_button.place(x=50, y=710)

# Arrange button

arrange_button = create_button(root, text="Arrange files", command=lambda: arrange_files(
    source_location.get(),
    destination_location.get(),
    documents=documents_folder.get(),
    images=images_folder.get(),
    audio=audio_folder.get(),
    videos=videos_folder.get(),
    archives=archives_folder.get(),
    programs=programs_folder.get(),
))
arrange_button.place(x=1100, y=710)

root.mainloop()
