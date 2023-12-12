import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import Toplevel, Label, Button, messagebox
from tkinter import ttk, Entry
from PIL import Image, ImageTk
import webbrowser
import psycopg2
import uuid
class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to the dance studio!")
        self.root.geometry("600x400")

        self.connection = psycopg2.connect(
            dbname="proj5",
            user="postgres",
            password="ineed21u",
            host="localhost",
            port = "5432"
        )
        self.cur = self.connection.cursor()
        self.image_path = "C:/Users/aruza/Downloads/pic13.jpg"
        self.photo = None
        self.label1 = tk.Label(self.root)
        self.label1.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.bind("<Configure>", self.load_background)
        self.load_background(None)

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="About Us", command=self.open_about_us)
        file_menu.add_command(label="Price", command=self.show_price)
        self.about_us_instance = self.AboutUs()

        btn_apply = tk.Button(self.root, text="Sign up with us", command=self.open_application_form,
                              font=('Times New Roman', 14, 'italic'))
        btn_apply.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        def _from_rgb(rgb):
            return "#%02x%02x%02x" % rgb

        social_frame = tk.Frame(self.root, borderwidth=0)
        social_frame.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        social_frame.configure(bg=_from_rgb((59, 3, 68)))
        instagram_image_path = "C:/Users/aruza/Downloads/pic22.jpg"
        whatsapp_image_path = "C:/Users/aruza/Downloads/pic20.jpg"

        instagram_image = Image.open(instagram_image_path)
        whatsapp_image = Image.open(whatsapp_image_path)
        instagram_image = self.resize_image(instagram_image, (100, 100))
        whatsapp_image = self.resize_image(whatsapp_image, (100, 100))

        instagram_image = ImageTk.PhotoImage(instagram_image)
        lbl_instagram = Label(social_frame, image=instagram_image, cursor="hand2", borderwidth=0,
                              background="DarkOrchid4")
        lbl_instagram.image = instagram_image
        lbl_instagram.grid(column=0, row=0, padx=(0, 5), pady=10)
        lbl_instagram.bind("<Button-1>", lambda e: self.open_instagram())

        whatsapp_image = ImageTk.PhotoImage(whatsapp_image)
        lbl_whatsapp = Label(social_frame, image=whatsapp_image, cursor="hand2", borderwidth=0,
                             background="DarkOrchid4")
        lbl_whatsapp.image = whatsapp_image
        lbl_whatsapp.grid(column=1, row=0, padx=(0, 5), pady=10)
        lbl_whatsapp.bind("<Button-1>", lambda e: self.open_whatsapp())

    def create_database_table(self):
        create_table_query = """
                   CREATE TABLE IF NOT EXISTS application_data (
                       id SERIAL PRIMARY KEY,
                       first_name VARCHAR(255) NOT NULL,
                       last_name VARCHAR(255) NOT NULL,
                       phone_number VARCHAR(15) NOT NULL,
                       branch VARCHAR(50) NOT NULL,
                       genre VARCHAR(50) NOT NULL,
                       choreographer VARCHAR(255)
                   );
               """
        self.cur.execute(create_table_query)
        self.connection.commit()

    def display_project_photo(self, selected_project):
        project_photos = {
            "1 фото": "C:/path/to/your/projects/project1.jpg",
            "2 фото": "C:/path/to/your/projects/project2.jpg",
            "3 фото": "C:/path/to/your/projects/project3.jpg"
        }

        if selected_project in project_photos:
            photo_path = project_photos[selected_project]
            photo = Image.open(photo_path)
            photo = photo.resize((400, 400), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(photo)

            if not hasattr(self, 'photo_window') or not self.photo_window:
                self.photo_window = Toplevel(self.root)
                self.photo_window.title("Фото проекта")
                self.photo_window.geometry("500x500")

                self.lbl_photo = tk.Label(self.photo_window, image=photo)
                self.lbl_photo.image = photo
                self.lbl_photo.pack(pady=10)

                btn_close = Button(self.photo_window, text="Закрыть", command=self.close_project_photo)
                btn_close.pack(pady=10)
            else:
                self.lbl_photo.configure(image=photo)
                self.lbl_photo.image = photo
                self.photo_window.title(f"Фото проекта: {selected_project}")
        else:
            messagebox.showwarning("Ошибка", "Выберите проект")

    def close_project_photo(self):
        if self.photo_window:
            self.photo_window.protocol("WM_DELETE_WINDOW", self.photo_window.iconify)
            self.photo_window = None


    def load_background(self, event):
        original_image = Image.open(self.image_path)
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        aspect_ratio = original_image.width / original_image.height
        new_width = int(window_height * aspect_ratio)
        resized_image = original_image.resize((new_width, window_height), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(resized_image)
        self.label1.configure(image=self.photo)
        self.label1.image = self.photo

    def resize_image(self, image, size):
        image.thumbnail(size, Image.ANTIALIAS)
        return image

    def open_application_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Application form")
        form_window.geometry("600x600")

        background_photo_path = "C:/Users/aruza/Downloads/pic23.jpg"
        background_photo = Image.open(background_photo_path)
        background_photo = background_photo.resize((600, 600), Image.ANTIALIAS)
        background_photo = ImageTk.PhotoImage(background_photo)
        background_label = tk.Label(form_window, image=background_photo)
        background_label.image = background_photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Define StringVar variables for each entry
        first_name_var = tk.StringVar()
        last_name_var = tk.StringVar()
        contact_number_var = tk.StringVar()
        branch_var = tk.StringVar()
        genre_var = tk.StringVar()

        labels_and_entries = [
            (tk.Label(form_window, text="First Name:", font=('Times New Roman', 14)),
             Entry(form_window, font=('Times New Roman', 14), textvariable=first_name_var)),
            (tk.Label(form_window, text="Last Name:", font=('Times New Roman', 14)),
             Entry(form_window, font=('Times New Roman', 14), textvariable=last_name_var)),
            (tk.Label(form_window, text="Contact number:", font=('Times New Roman', 14)),
             Entry(form_window, font=('Times New Roman', 14), textvariable=contact_number_var)),
            (tk.Label(form_window, text="Branch:", font=('Times New Roman', 14)),
             Entry(form_window, font=('Times New Roman', 14), textvariable=branch_var)),
            (tk.Label(form_window, text="Genre of dance:", font=('Times New Roman', 14)),
             Entry(form_window, font=('Times New Roman', 14), textvariable=genre_var))
        ]

        total_height = sum(
            label.winfo_reqheight() + entry.winfo_reqheight() + 10 for label, entry in labels_and_entries)
        start_y = (600 - total_height) // 2

        for label, entry in labels_and_entries:
            label.place(relx=0.2, rely=start_y / 600, anchor="w")
            entry.place(relx=0.6, rely=start_y / 600, anchor="w")
            start_y += label.winfo_reqheight() + entry.winfo_reqheight() + 10

        total_height = sum(
            label.winfo_reqheight() + entry.winfo_reqheight() + 10 for label, entry in labels_and_entries)
        start_y = (600 - total_height) // 2

        for label, entry in labels_and_entries:
            label.place(relx=0.2, rely=start_y / 600, anchor="w")
            entry.place(relx=0.6, rely=start_y / 600, anchor="w")
            start_y += label.winfo_reqheight() + entry.winfo_reqheight() + 10

        submit_button = Button(form_window, text="Submit", command=lambda: self.submit_and_print_data(
            first_name_var, last_name_var, contact_number_var, branch_var, genre_var
        ), font=('Times New Roman', 14))
        submit_button.place(relx=0.5, rely=0.8, anchor="center")

        close_button = tk.Button(form_window, text="Close", command=form_window.destroy, font=('Times New Roman', 14))
        close_button.place(relx=0.5, rely=0.9, anchor="center")

    def submit_and_print_data(self, first_name_var, last_name_var, contact_number_var, branch_var, genre_var,
                              ):
        first_name = first_name_var.get()
        last_name = last_name_var.get()
        contact_number = contact_number_var.get()
        branch = branch_var.get()
        genre = genre_var.get()

        # If choreographer is empty, set it to None

        self.create_database_table()
        insert_query = """
                INSERT INTO application_data (first_name, last_name, phone_number, branch, genre)
                VALUES (%s, %s, %s, %s, %s)
            """
        data = (first_name, last_name, contact_number, branch, genre)

        try:
            self.cur.execute(insert_query, data)
            self.connection.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")
            self.connection.rollback()

        # Print the data in the terminal
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Contact Number:", contact_number)
        print("Branch:", branch)
        print("Genre of Dance:", genre)

    def get_user_id(self):
        return str(uuid.uuid4())



    def _del_(self):
        # Закрытие соединения с базой данных при удалении объекта
        self.cur.close()
        self.conn.close()

    def destroy(self):
        self.connection.close()
        self.root.destroy()

    class AboutUs:
        def __init__(self):
            self.root = None
            self.photo_label = None

        def create_about_us_window(self, root):
            self.root = root
            self.root.geometry("700x500")

            background_photo_path = "C:/Users/aruza/Downloads/pic26.jpg"
            background_photo = Image.open(background_photo_path)
            self.photo = ImageTk.PhotoImage(background_photo)

            background_label = tk.Label(self.root, image=self.photo)
            background_label.image = self.photo
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

            category_label = tk.Label(self.root, text="Projects", font=('Times New Roman', 16, 'bold'), bg="white")
            category_label.place(relx=0.05, rely=0.5, anchor='w')
            options = ["project1", "project2", "project3"]
            project_combo_var = tk.StringVar()
            project_combo = ttk.Combobox(self.root, textvariable=project_combo_var, values=options)
            project_combo.set("1 фото")
            project_combo.place(relx=0.05, rely=0.55, anchor='w')

            self.photo_label = tk.Label(self.root)
            self.photo_label.place(relx=0.05, rely=0.6, anchor='w')

            close_button = tk.Button(self.root, text="Close", command=self.root.destroy, font=('Times New Roman', 14))
            close_button.pack(side="bottom", pady=10)

            project_combo.bind("<<ComboboxSelected>>", lambda event: self.show_selected_item(project_combo.get()))

        def show_selected_item(self, selected_item):
            if selected_item == "Choose Choreographer":
                self.show_choreographer_selection()
            else:
                self.show_project_photo(selected_item)

        def show_choreographer_selection(self):
            self.show_choreographer_photo()

        def show_project_photo(self, selected_project):
            project_photos = {
                "project1": "C:/Users/aruza/Downloads/pic31.jpg",
                "project2": "C:/Users/aruza/Downloads/pic32.jpg",
                "project3": "C:/Users/aruza/Downloads/pic33.jpg"
            }

            if selected_project in project_photos:
                photo_path = project_photos[selected_project]
                photo = Image.open(photo_path)
                photo = photo.resize((600, 550), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(photo)

                self.photo_label.configure(image=photo)
                self.photo_label.image = photo

        def show_choreographer_photo(self):
            choreographers = ["Juzz Funk", "Mix Dance", "High Heels", "Kpop Cover"]
            choreographer_frame = tk.Frame(self.root)
            choreographer_frame.place(relx=0.05, rely=0.7, anchor='w')
            self.choreographers = Combobox(choreographer_frame, values=choreographers, state="readonly")
            self.choreographers.set("")
            self.choreographers.set("Select Choreographer")
            self.choreographers.pack(pady=10)
            btn_show_choreographer = Button(choreographer_frame, text="Show Choreographer Photo",
                                            command=self.display_choreographer_photo)
            btn_show_choreographer.pack(pady=10)

        def display_choreographer_photo(self):
            choreographer_name = self.choreographers.get()
            choreographer_photos = {
                "Juzz Funk": "C:/path/to/your/image/pic7.jpg",
                "Mix Dance": "C:/path/to/your/image/pic8.jpg",
                "High Heels": "C:/path/to/your/image/pic9.jpg",
                "Kpop Cover": "C:/path/to/your/image/pic10.jpg"
            }
            if choreographer_name in choreographer_photos:
                photo_path = choreographer_photos[choreographer_name]
                photo = Image.open(photo_path)

                window_width = 600
                window_height = 600

                photo = photo.resize((window_width, window_height), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(photo)
                if hasattr(self, 'photo_window') and self.photo_window:
                    self.photo_window.destroy()

                self.photo_window = Toplevel(self.root)
                self.photo_window.title("Фото хореографа")
                self.photo_window.geometry(f"{window_width}x{window_height}")

                lbl_photo = tk.Label(self.photo_window, image=photo)
                lbl_photo.image = photo
                lbl_photo.pack(pady=10)

                btn_close = Button(self.photo_window, text="Закрыть", command=self.photo_window.destroy)
                btn_close.pack(pady=10)
            else:
                messagebox.showwarning("Ошибка", "Выберите хореографа")

        def destroy(self):
            self.root.destroy()

    def show_price(self):
        price_window = Toplevel(self.root)
        price_window.title("Price")
        price_window.geometry("700x500")

        price_photo = Image.open("C:/Users/aruza/Downloads/pic34.jpg")
        price_photo = price_photo.resize((700, 500), Image.ANTIALIAS)
        price_photo = ImageTk.PhotoImage(price_photo)

        price_photo_label = tk.Label(price_window, image=price_photo)
        price_photo_label.image = price_photo
        price_photo_label.place(x=0, y=0, relwidth=1, relheight=1)

        choreographers = ["Juzz Funk", "Mix Dance", "High Heels", "Kpop Cover"]
        choreographer_frame = tk.Frame(price_window)
        choreographer_frame.place(relx=0.95, rely=0, anchor='ne')
        self.choreographers = Combobox(choreographer_frame, values=choreographers, state="readonly")
        self.choreographers.set("Select Choreographer")
        self.choreographers.pack(pady=10)
        self.choreographers.bind("<<ComboboxSelected>>", lambda event: self.display_choreographer_photo())

    def display_choreographer_photo(self):
        choreographer_name = self.choreographers.get()
        choreographer_photos = {
            "Juzz Funk": "C:/Users/aruza/Downloads/pic7.jpg",
            "Mix Dance": "C:/Users/aruza/Downloads/pic8.jpg",
            "High Heels": "C:/Users/aruza/Downloads/pic9.jpg",
            "Kpop Cover": "C:/Users/aruza/Downloads/pic10.jpg"
        }
        if choreographer_name in choreographer_photos:
            photo_path = choreographer_photos[choreographer_name]
            photo = Image.open(photo_path)
            window_width = photo.width
            window_height = photo.height
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            if window_width > screen_width or window_height > screen_height:
                ratio = min(screen_width / window_width, screen_height / window_height)
                window_width = int(window_width * ratio)
                window_height = int(window_height * ratio)

            photo = photo.resize((window_width, window_height), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(photo)

            photo_window = Toplevel(self.root)
            photo_window.title("Фото хореографа")
            photo_window.geometry(f"{window_width}x{window_height}")

            lbl_photo = tk.Label(photo_window, image=photo)
            lbl_photo.image = photo
            lbl_photo.pack(pady=10)

            btn_close = Button(photo_window, text="Закрыть", command=photo_window.destroy)
            btn_close.pack(pady=10)
        else:
            messagebox.showwarning("Ошибка", "Выберите хореографа")

    def open_instagram(self):
        webbrowser.open("https://www.instagram.com/")

    def open_whatsapp(self):
        webbrowser.open("https://wa.me/7086649801")

    def open_about_us(self):
        if self.about_us_instance is None or not self.about_us_instance.root or not tk._default_root.winfo_exists():
            about_us_window = Toplevel(self.root)
            about_us_window.title("About Us")
            self.about_us_instance = self.AboutUs()
            self.about_us_instance.create_about_us_window(about_us_window)
            about_us_window.protocol("WM_DELETE_WINDOW", self.about_us_instance.destroy)



def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()