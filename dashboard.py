import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database.database_manager import DatabaseManager


class DashboardPage(ttk.Frame):


    def __init__(self, parent,database,show_create_database, show_active_trials,show_login):
        super().__init__(parent)

        self.pack(fill="both", expand=True) #Use all space
        self.database = database
        self.show_create_database = show_create_database
        self.show_active_trials = show_active_trials
        self.show_login = show_login

        # Main container
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Main area
        self.main_area = ttk.Frame(
            self.container,
            padding=40
        )
        self.main_area.pack(
            fill="both",
            expand=True
        )

        # Central container
        self.content_frame = ttk.Frame(self.main_area)
        self.content_frame.place(
            relx=0.5, #anchor
            rely=0.5, #altura
            anchor="center"
        )

        # Title
        ttk.Label(
            self.content_frame,
            text="Clinical Trial Recruitment Dashboard",
            font=("Helvetica", 24, "bold")
        ).pack(pady=(0, 10))

        # Select an option to continue
        ttk.Label(
            self.content_frame,
            text="Select an option to continue",
            font=("Helvetica", 14)
        ).pack(pady=(0, 25))

        #Frames secondary

        self.stats_frame = ttk.Frame(
            self.content_frame,
            padding=20
        )
        self.stats_frame.pack(pady=(0, 25))

        # Card Total Studies

        self.stats_card = ttk.Frame(
            self.stats_frame,
            padding=20,
            borderwidth=1,
            relief="ridge"
        )
        self.stats_card.grid(row=0, column=0, padx=10)



        self.study_count_label = ttk.Label(
            self.stats_card,
            text="0",
            font=("Helvetica", 42, "bold")
        )
        self.study_count_label.pack()


        ttk.Label(
            self.stats_card,
            text="Total Studies",
            font=("Helvetica", 12)
        ).pack()

        #Card Active Studies

        self.active_card = ttk.Frame(
            self.stats_frame,
            padding=25,
            borderwidth=1,
            relief="ridge"
        )
        self.active_card.grid(row=0, column=1, padx=10)

        self.active_count_label = ttk.Label(
            self.active_card,
            text="0", #Before loading the real data it appear 0
            font=("Helvetica", 40, "bold")
        )
        self.active_count_label.pack()

        ttk.Label(
            self.active_card,
            text="Active Studies",
            font=("Helvetica", 12)
        ).pack()

        #Average card
        self.average_card = ttk.Frame(
            self.stats_frame,
            padding=25,
            borderwidth=1,
            relief="ridge"
        )
        self.average_card.grid(row=0, column=2, padx=10)

        self.avg_label = ttk.Label(
            self.average_card,
            text="0",
            font=("Helvetica", 40, "bold")
        )
        self.avg_label.pack()

        ttk.Label(
            self.average_card,
            text="Avg Subjects/Study",
            font=("Helvetica", 12)
        ).pack()

        # Buttons
        self.create_card(
            self.content_frame,
            "Create New Database",
            self.show_create_database
        )

        self.create_card(
            self.content_frame,
            "Active Trials",
            self.show_active_trials
        )

        self.create_card(
            self.content_frame,
            "Log-off",
            self.show_login
        )

        self.load_data()

    def create_card(self, parent, title, command):

        button = ttk.Button(
            parent,
            text=title,
            bootstyle="outline-primary",
            width=30,
            command=command
        )

        button.pack(
            pady=10,
            ipady=15
        )

    def load_data(self):
        try:
            study_count = self.database.study_number()
            active_count=self.database.active_studies()
            average_subjects=self.database.average_subjects()

            self.study_count_label.config(
                text=str(study_count) #It indicates where in the screens the number of total studies
            )

            self.active_count_label.config(
                text=str(active_count) #It indicates where in the screens goes the number of total active studies
            )

            self.avg_label.config(
                text=str(average_subjects) #It indicates where in the screens goes the average of subjects in the studies
            )

        except Exception as e:
            self.study_count_label.config(
                text="0"
            )
            self.active_count_label.config(
                text="0"
            )
            self.avg_label.config(
                text="0"
            )
            print("Error loading stats:", e)


    def refresh(self):
        self.load_data() #Everytime you open the dashboard it refreshes
