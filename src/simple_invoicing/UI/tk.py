from tkinter import Menu, Tk
from tkinter.ttk import Style
from src.simple_invoicing.UI.views.family_view import FamilyView
from tests.unit.test_ui import FakeFamilyModel
from src.simple_invoicing.UI.controllers.family_controller import FamilyController

def get_geometry(top_level):
    screen_width = top_level.winfo_screenwidth()
    screen_height = top_level.winfo_screenheight()
    app_width = screen_width * 0.8
    app_height = screen_height * 0.8
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    return f"{int(app_width)}x{int(app_height)}+{int(x)}+{int(y)}"

def main():
    root = Tk()
    root.title("App")
    root.geometry(get_geometry(root))
    s = Style()
    s.configure("debug.TFrame", background="red")

    main_menu = Menu(root)
    file_menu = Menu(main_menu)
    main_menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.quit)
    root.config(menu=main_menu)

    view = FamilyView(root, padding=3)
    view.pack(expand=True, fill="both")

    controller = FamilyController(view, FakeFamilyModel())

    root.iconify()
    root.mainloop()

if __name__ == "__main__":
    main()