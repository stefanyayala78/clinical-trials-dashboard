import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class LoginPage(ttk.Frame):

    def __init__(self, parent, on_login_success):
        super().__init__(parent)

        self.on_login_success = on_login_success #Saves the function coming from app

        # CENTER CONTAINER
        self.container = ttk.Frame(self)
        self.container.pack(expand=True, fill= "both")
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        self.center_frame = ttk.Frame(self.container)
        self.center_frame.grid(row=0, column=0)


        #Project title outside login box
        title= ttk.Label(
            self.container,
            text="Clinical Trial Recruitment Intelligence Dashboard",
            font=("Heading 3", 26, "bold"),
            justify="center"
        )
        title.grid(row=0, column=0, pady=(40, 80)) #80 is the distance to the login box


        #Card login box
        self.card = ttk.Frame(
            self.container,
            padding=30,
            borderwidth=2, #Adds a frame
            relief="solid",
        )
        self.card.pack()

        self.card.columnconfigure(0, weight=1)

        #Login title

        self.title= ttk.Label(
            self.card, #It defines where is it going to appear
            text="Login",
            font=("text", 10, "bold"),
        )
        self.title.grid(row=0, column=0, pady=10)

        # USER
        self.username = ttk.Entry(self.card, justify= "left", width=30)
        self.username.grid(row=1, column=0, sticky="ew", pady=10)
        self.username.insert(0, "Username")

        # PASSWORD
        self.password = ttk.Entry(self.card, justify= "left", show="*", width=30)
        self.password.grid(row=2, column=0, sticky="ew", pady=10)
        self.password.insert(0, "Password")

        # BUTTON
        ttk.Button(
            self.card,
            text="Login",
            bootstyle="success",
            command=self.login
        ).grid(row=3, column=0, pady=20, sticky="ew")

    def login(self):
        # use this logic after connecting to the DB
        user = self.username.get()
        pwd = self.password.get()

        if user and pwd:
            self.on_login_success()