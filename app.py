import ttkbootstrap as ttk
#Local moduls

from login import LoginPage
from dashboard import DashboardPage
from create_database import CreateDatabasePage
from active_trials import ActiveTrials
from user_data_base import UserDataBase
from database.database_manager import DatabaseManager



class App(ttk.Window):

    def __init__(self):
        super().__init__(themename="darkly")

        # Windows
        self.title("Clinical Trial Recruitment Intelligence Dashboard")
        self.geometry("1400x800")

        # Main Frame
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Login
        self.show_login()

        self.database_structure= None

        #Database

        self.database=DatabaseManager()

    # Login screen

    def show_login(self):
        self.clear_container()

        self.login_page = LoginPage( #If the login is correct it shows the dashboard
            self.container,
            self.show_dashboard
        )
        self.login_page.pack(fill="both", expand=True)


    # Dashboard screen

    def show_dashboard(self):
        self.clear_container()
        self.dashboard = DashboardPage(
            self.container,
            self.database,
            self.show_create_database,
            self.show_active_trials,
            self.show_login,

        )
        self.dashboard.pack(fill="both", expand=True)
        self.dashboard.refresh() #Makes the dashboard to have th most current data

    def show_create_database(self):
        self.clear_container() #To clean the screen

        self.create_database = CreateDatabasePage(self.container, self.show_user_data_base, self.show_dashboard) #Invocas al nuevo metodo


    def show_active_trials(self):
        self.clear_container()
        self.active_trials = ActiveTrials(
            self.container,#where is it going to appear
            self.database,
            self.show_user_data_base,
            self.show_dashboard
        )
        self.active_trials.pack(fill="both", expand=True)

    def show_user_data_base(self, table_name):
        self.clear_container()

        self.user_data_base = UserDataBase(
            self.container,
            table_name, # needsto know the table name
            self.show_active_trials
            )

    # Clear screen

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()