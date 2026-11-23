import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database.database_manager import DatabaseManager
from ttkbootstrap.dialogs import Messagebox


class LoginPage(ttk.Frame):

    def __init__(self, parent, on_login_success):
        super().__init__(parent)

        self.on_login_success = on_login_success
        self.database=DatabaseManager()


        # Center container
        self.container = ttk.Frame(self)
        self.container.pack(expand=True, fill="both")

        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        # Center
        self.center_frame = ttk.Frame(self.container)
        self.center_frame.grid(row=0, column=0)

        #Project title
        title = ttk.Label(
            self.center_frame,
            text="Clinical Trial Recruitment Intelligence Dashboard",
            font=("Helvetica", 26, "bold"),
            justify="center"
        )
        title.grid(row=0, column=0, pady=(40, 80))

        # Card login box
        self.card = ttk.Frame(
            self.center_frame,
            padding=60,
            width=60,
            height=60,
            borderwidth=2,
            relief="solid"
        )
        self.card.grid(row=1, column=0)

        self.card.columnconfigure(0, weight=1)

        #Register button

        ttk.Button(
            self.card,
            text="Create Account",
            bootstyle="secondary",
            command=self.open_register_window
        ).grid(row=4, column=0, pady=10, sticky="ew")

        # Login Title
        self.title = ttk.Label(
            self.card, #self.card indica donde va a ir esa label
            text="Login",
            font=("Helvetica", 14, "bold")
        )
        self.title.grid(row=0, column=0, pady=10)

        # User
        self.username = ttk.Entry(self.card, justify="left", width=30)
        self.username.grid(row=1, column=0, sticky="ew", pady=10)
        self.username.insert(0, "Username")

        # Password
        self.password = ttk.Entry(self.card, justify="left", show="*", width=30)
        self.password.grid(row=2, column=0, sticky="ew", pady=10)
        self.password.insert(0, "Password")

        # Button login
        ttk.Button(
            self.card,
            text="Login",
            bootstyle="success",
            command=self.login
        ).grid(row=3, column=0, pady=20, sticky="ew")

    def open_register_window(self):
        self.register_window = ttk.Toplevel(self)

        self.register_window.title("Create Account")
        self.register_window.geometry("350x250")

        #Register window buttons
        #Username
        ttk.Label(
            self.register_window,
            text="Username"
        ).pack(pady=(20, 5))

        self.new_username = ttk.Entry(
            self.register_window,
            width=30
        )
        self.new_username.pack()
        #Password
        ttk.Label(
            self.register_window,
            text="Password"
        ).pack(pady=(10, 5))

        self.new_password = ttk.Entry(
            self.register_window,
            show="*",
            width=30
        )
        self.new_password.pack()

        #Confirm password

        ttk.Label(
            self.register_window,
            text="Confirm Password"
        ).pack(pady=(10, 5))

        self.confirm_password = ttk.Entry(
            self.register_window,
            show="*",
            width=30
        )
        self.confirm_password.pack()

        #Create button

        ttk.Button(
            self.register_window,
            text="Create",
            bootstyle="success",
            command=self.register
        ).pack(pady=20)

    def login(self):
        username=self.username.get()
        password=self.password.get()

        user=self.database.login_user(username, password)

        if user:
            self.on_login_success()

        else:
            Messagebox.show_error(
                "Invalid username or password",
                "Error"
            )

    def register(self):
        username=self.new_username.get()
        password=self.new_password.get()
        confirm=self.confirm_password.get()

    #Check fields no empty
        if not username or not password or not confirm:
            Messagebox.show_error(
                "Username already exists",
                "Error"
            )
            return

    #Check password
        if password != confirm:
            Messagebox.show_error(
                "Passwords do not match",
                "Error"
            )
            return

        success = self.database.register_user(
            username,
            password
        )

        if success:
            Messagebox.show_info(
                "Account created successfully!",
                "Success"
            )
            self.register_window.destroy()
        else:
            Messagebox.show_error(
                "Username already exists",
                "Error"
            )