import ttkbootstrap as ttk
from tkinter import ttk as tkttk
from ttkbootstrap.constants import *
from database.database_manager import DatabaseManager


class ActiveTrials(ttk.Frame):

    def __init__(self, parent,database,show_user_data_base,show_dashboard):
        super().__init__(parent)
        self.database = database
        self.show_user_data_base = show_user_data_base
        self.show_dashboard = show_dashboard

        self.pack(fill="both", expand=True)

        ttk.Label(
            self,
            text="Active Trials",
            font=("Helvetica", 28, "bold")
        ).pack(pady=30)

        #Table
        self.tree = tkttk.Treeview(
            self,
            columns=("name",),
            show="headings"
        )

        self.tree.heading("name", text="Study Name")

        self.tree.column("name", width=400)

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        self.tree.bind("<Double-1>", self.open_study)

        #Back button
        self.back_button=ttk.Button(
            self,
            text="Back",
            bootstyle=SECONDARY,
            command=self.show_dashboard
        )
        self.back_button.pack(pady=10)

        self.load_studies()

    def open_study(self, event):

        selected_item = self.tree.selection()

        if not selected_item:
            return

        study_name = self.tree.item(
            selected_item[0],
            "values"
        )[0]

        self.show_user_database(study_name)

# List of studies
    def load_studies(self):
        db = self.database

        studies = db.get_all_studies()  # debe traer SOLO nombres

        # limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        # insertar SOLO nombres
        for study in studies:
            self.tree.insert("", "end", values=(study[0],))


    def open_study(self,event):
        selected_item=self.tree.selection() #Selection
        if not selected_item:
            return
        study_name=self.tree.item(
            selected_item[0], #Save the study name after the code of of the selected line in SQLite
            "values"
        )[0]

        self.show_user_data_base(study_name)
