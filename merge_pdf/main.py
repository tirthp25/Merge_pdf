import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter

BACKGROUND = "#1f1f3d"
FOREGROUND = "#f5f5f8"
ACCENT = "#ff7f50"
BUTTON_BG = "#3f4f7f"
BUTTON_FG = "#ffffff"
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_LABEL = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 11, "bold")
FONT_LIST = ("Segoe UI", 11)


def update_status():
    count = pdf_list.size()
    status_text = f"Selected PDFs: {count}"
    status_label.config(text=status_text)
    clear_button.config(state=tk.NORMAL if count else tk.DISABLED)
    has_selection = bool(pdf_list.curselection())
    remove_button.config(state=tk.NORMAL if has_selection else tk.DISABLED)
    up_button.config(state=tk.NORMAL if has_selection else tk.DISABLED)
    down_button.config(state=tk.NORMAL if has_selection else tk.DISABLED)


def add_pdfs():
    files = filedialog.askopenfilenames(
        title="Select PDF files to merge",
        filetypes=[("PDF files", "*.pdf")]
    )
    if files:
        for file in files:
            if file not in pdf_list.get(0, tk.END):
                pdf_list.insert(tk.END, file)
        update_status()


def remove_selected():
    selected_indices = list(pdf_list.curselection())
    if not selected_indices:
        return
    for index in reversed(selected_indices):
        pdf_list.delete(index)
    update_status()


def move_selected(direction: str):
    selected = list(pdf_list.curselection())
    if not selected:
        return
    if direction == "up" and selected[0] == 0:
        return
    if direction == "down" and selected[-1] == pdf_list.size() - 1:
        return

    items = [pdf_list.get(i) for i in selected]
    for index in (selected if direction == "up" else reversed(selected)):
        pdf_list.delete(index)

    if direction == "up":
        target = selected[0] - 1
        for item in items:
            pdf_list.insert(target, item)
            target += 1
    else:
        target = selected[-1] + 1 - len(items)
        for item in items:
            pdf_list.insert(target, item)
            target += 1

    pdf_list.selection_clear(0, tk.END)
    for i, _ in enumerate(items):
        pdf_list.selection_set(target - len(items) + i)
    update_status()


def clear_all():
    pdf_list.delete(0, tk.END)
    update_status()


def merge_pdfs():
    pdfs = list(pdf_list.get(0, tk.END))
    if not pdfs:
        messagebox.showerror("Error", "Please add at least one PDF file first.")
        return

    output_file = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save merged PDF as"
    )
    if not output_file:
        return

    merger = PdfWriter()
    try:
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(output_file)
        merger.close()
        messagebox.showinfo(
            "Success",
            f"Merged {len(pdfs)} PDFs into:\n{os.path.basename(output_file)}"
        )
        status_label.config(text=f"Last merged: {os.path.basename(output_file)}")
    except Exception as exc:
        messagebox.showerror("Merge Failed", f"Unable to merge PDFs:\n{exc}")

root = tk.Tk()
root.title("PDF Merger")
root.configure(bg=BACKGROUND)
root.geometry("740x560")
root.minsize(700, 520)

header = tk.Label(
    root,
    text="PDF Merger Pro",
    font=FONT_TITLE,
    fg=ACCENT,
    bg=BACKGROUND
)
header.pack(pady=(18, 8))

subtitle = tk.Label(
    root,
    text="Add PDF files, reorder them, and merge into one polished document.",
    font=FONT_LABEL,
    fg=FOREGROUND,
    bg=BACKGROUND
)
subtitle.pack(pady=(0, 16))

button_frame = tk.Frame(root, bg=BACKGROUND)
button_frame.pack(pady=(0, 10), fill=tk.X, padx=20)

add_button = tk.Button(
    button_frame,
    text="Add PDFs",
    command=add_pdfs,
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    activebackground=ACCENT,
    activeforeground=BUTTON_FG,
    padx=16,
    pady=12
)
add_button.pack(side=tk.LEFT, padx=8)

remove_button = tk.Button(
    button_frame,
    text="Remove Selected",
    command=remove_selected,
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    activebackground=ACCENT,
    activeforeground=BUTTON_FG,
    padx=16,
    pady=12,
    state=tk.DISABLED
)
remove_button.pack(side=tk.LEFT, padx=8)

clear_button = tk.Button(
    button_frame,
    text="Clear All",
    command=clear_all,
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    activebackground=ACCENT,
    activeforeground=BUTTON_FG,
    padx=16,
    pady=12,
    state=tk.DISABLED
)
clear_button.pack(side=tk.LEFT, padx=8)

reorder_frame = tk.Frame(root, bg=BACKGROUND)
reorder_frame.pack(pady=(0, 6), fill=tk.X, padx=20)

up_button = tk.Button(
    reorder_frame,
    text="Move Up",
    command=lambda: move_selected("up"),
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    activebackground=ACCENT,
    activeforeground=BUTTON_FG,
    padx=16,
    pady=12,
    state=tk.DISABLED
)
up_button.pack(side=tk.LEFT, padx=8)

down_button = tk.Button(
    reorder_frame,
    text="Move Down",
    command=lambda: move_selected("down"),
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    activebackground=ACCENT,
    activeforeground=BUTTON_FG,
    padx=16,
    pady=12,
    state=tk.DISABLED
)
down_button.pack(side=tk.LEFT, padx=8)

list_frame = tk.Frame(root, bg=BACKGROUND)
list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 12))

pdf_list = tk.Listbox(
    list_frame,
    selectmode=tk.EXTENDED,
    bg="#27294d",
    fg=FOREGROUND,
    font=FONT_LIST,
    highlightbackground=ACCENT,
    width=96,
    height=14,
    bd=0,
    activestyle="none",
    selectbackground="#5b6fb8",
    selectforeground=BUTTON_FG
)
pdf_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=pdf_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
pdf_list.config(yscrollcommand=scrollbar.set)

bottom_frame = tk.Frame(root, bg=BACKGROUND)
bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(0, 16))

merge_button = tk.Button(
    bottom_frame,
    text="Merge PDFs Now",
    command=merge_pdfs,
    font=("Segoe UI", 15, "bold"),
    bg=ACCENT,
    fg=BUTTON_FG,
    activebackground="#ffa07a",
    activeforeground=BUTTON_FG,
    padx=18,
    pady=14
)
merge_button.pack(fill=tk.X)

status_label = tk.Label(
    bottom_frame,
    text="Selected PDFs: 0",
    font=FONT_LABEL,
    fg=FOREGROUND,
    bg=BACKGROUND
)
status_label.pack(pady=(10, 4))

footer = tk.Label(
    bottom_frame,
    text="Tip: select files and use Move Up / Move Down to set merge order before merging.",
    font=("Segoe UI", 10),
    fg="#d1d4f1",
    bg=BACKGROUND
)
footer.pack(pady=(0, 4))

pdf_list.bind("<<ListboxSelect>>", lambda event: update_status())
root.mainloop()
