################################### Imports


import clipman
import tkinter
import json
import webbrowser
import os
import sys
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


################################### Variables


application_title = "PyPaster"
json_decoder = json.JSONDecoder()


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
window.resizable(False, False)
window.iconphoto(False, tkinter.PhotoImage(file=resource_path("icon.png")))


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


################################### Create window menu options.


menu = tkinter.Menu(window)

file_menu = tkinter.Menu(window, tearoff=False)
app_menu = tkinter.Menu(window, tearoff=False)

file_menu.add_command(label="Open", command=load_data_file)
app_menu.add_command(
    label="Test Clipboard Copy",
    command=lambda: copy_to_clipboard("This was copied successfully!"),
)
app_menu.add_command(label="Toggle Always on Top", command=toggle_always_on_top)
app_menu.add_command(label="Quit", command=window.quit)
menu.add_command(label="Help", command=open_help_page)

menu.add_cascade(menu=file_menu, label="File")
menu.add_cascade(menu=app_menu, label="Application")
window.configure(menu=menu)


################################### Start the main loop of the application.

window.mainloop()
