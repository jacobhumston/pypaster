################################### Imports


import clipman
import tkinter
import json
import webbrowser
import os
import sys
import math
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


################################### Variables


application_title = "PyPaster"
json_decoder = json.JSONDecoder()
current_font_size = 12
recommended_word_wrap = current_font_size * 30


################################### Utility functions.


# Load a data file.
def load_data_file() -> list[dict] | None:
    file = filedialog.askopenfile()
    if file == None:
        return None
    else:
        if not file.name.endswith(".json"):
            messagebox.showerror(
                application_title, "The file chosen was not a json file."
            )
            return load_data_file()
        else:
            try:
                json_result = json_decoder.decode(file.read())
                if "data" in json_result:
                    if isinstance(json_result["data"], list):
                        error = None
                        for index, section in enumerate(json_result["data"]):
                            if not isinstance(section, dict):
                                error = f"'data({index})' is not a dict."
                            else:
                                if not "header" in section or not "strings" in section:
                                    error = f"'data({index})' is missing property 'header' or 'strings'."
                                else:
                                    if not isinstance(section["header"], str):
                                        error = f"'data({index})' property 'header' is not a str."
                                    if not isinstance(section["strings"], list):
                                        error = f"'data({index})' property 'strings' is not a list."
                                    else:
                                        for index2, string in enumerate(
                                            section["strings"]
                                        ):
                                            if not isinstance(string, str):
                                                error = f"'data({index})[strings]({index2})' is not a str."
                        if error != None:
                            raise Exception(error)
                        else:
                            return json_result["data"]
                    else:
                        raise Exception("Property 'data' is not a list.")
                else:
                    raise Exception("'data' is not a property of json.")
            except Exception as error:
                messagebox.showerror(
                    application_title,
                    f"Something went wrong while trying to parse the file.\n\n{error}",
                )
                return load_data_file()


# Copy to clipboard.
def copy_to_clipboard(text: str) -> None:
    try:
        clipman.init()
        clipman.copy(text)
    except clipman.exceptions.ClipmanBaseException as error:
        response = messagebox.askyesno(
            application_title,
            f"Failed to copy to clipboard.\n{error}\n\nWould you like to go our help page?",
        )
        if response == True:
            webbrowser.open(
                "https://github.com/jacobhumston/pypaster/wiki/Clipboard-functionality-is-not-supported-on-your-device-by-default"
            )
    return None


# Get path to a file.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


################################### Create the window.


window = tkinter.Tk()
window.title(application_title)
window.resizable(True, True)
window.iconphoto(False, tkinter.PhotoImage(file=resource_path("icon.png")))
window.eval("tk::PlaceWindow . center")
window.configure(padx=15, pady=15)


# Listen for whenever the window is updated.
def window_updated(_):
    global recommended_word_wrap
    children = window.winfo_children()
    recommended_word_wrap = current_font_size * math.floor(
        (window.winfo_width() - 10) / current_font_size
    )
    # print(recommended_word_wrap, window.winfo_width())
    for child in children:
        if isinstance(child, ttk.Label) or isinstance(child, ttk.Button):
            child.configure(
                wraplength=recommended_word_wrap, font=f"Arial {current_font_size}"
            )


window.bind("<Configure>", window_updated)


################################### Create window menu options functions.


# Toggle the window to always be on top.
def toggle_always_on_top():
    current = window.attributes("-topmost") or False
    window.attributes("-topmost", not current)


# Open the help/info/website.
def open_help_page():
    webbrowser.open(
        "https://github.com/jacobhumston/pypaster/wiki/How-to-Setup-PyPaster"
    )


# Modify font size. (Increase.)
def increase_font_size():
    global current_font_size
    current_font_size = current_font_size + 4
    window_updated(None)


# Modify font size. (Decrease.)
def decrease_font_size():
    global current_font_size
    if current_font_size > 12 - 4:
        # print(current_font_size, current_font_size > 12 - 4)
        current_font_size = current_font_size - 4
        window_updated(None)


################################### Create window menu options.


menu = tkinter.Menu(window)

file_menu = tkinter.Menu(window, tearoff=False)
app_menu = tkinter.Menu(window, tearoff=False)
app_settings_menu = tkinter.Menu(window, tearoff=False)
app_utility_menu = tkinter.Menu(window, tearoff=False)

file_menu.add_command(label="Open", command=load_data_file)

app_settings_menu.add_command(
    label="Toggle Always on Top", command=toggle_always_on_top
)

app_settings_menu.add_command(label="Increase Font Size", command=increase_font_size)

app_settings_menu.add_command(label="Decrease Font Size", command=decrease_font_size)

app_utility_menu.add_command(
    label="Test Clipboard Copy",
    command=lambda: copy_to_clipboard("This was copied successfully!"),
)

app_utility_menu.add_command(
    label="Center Window",
    command=lambda: window.eval("tk::PlaceWindow . center"),
)

app_menu.add_cascade(menu=app_settings_menu, label="Settings")
app_menu.add_cascade(menu=app_utility_menu, label="Utility")

app_menu.add_command(
    label="Credits",
    command=lambda: messagebox.showinfo(
        application_title,
        "This application was created by Jacob Humston. (jacobhumston on GitHub)\n\nFree and open source for anyone to use!\nhttps://github.com/jacobhumston/pypaster",
    ),
)

app_menu.add_command(label="Quit", command=window.quit)

menu.add_cascade(menu=file_menu, label="File")
menu.add_cascade(menu=app_menu, label="Application")
menu.add_command(label="Help", command=open_help_page)

window.configure(menu=menu)


################################### Create the label that instructs them to load a file.


instructions_label = ttk.Label(window)
instructions_label.configure(
    text="To get started, use the File menu. If you need help, use the Help menu for extra assistance and instructions.",
    justify="center",
)
instructions_label.grid(row=0, column=0)


################################### Display welcome message and start the main loop of the application.


# messagebox.showinfo(
#    application_title,
#    "To get started, click 'File > Open'. If you have never used this application before, please click the 'Help' button for more instructions.",
# )
window_updated(None)
window.mainloop()
