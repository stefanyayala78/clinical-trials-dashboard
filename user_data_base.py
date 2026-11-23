
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from database.database_manager import DatabaseManager


class UserDataBase(ttk.Frame):

    def __init__(self, parent, table_name,show_active_trials):
        super().__init__(parent)

        self.pack(fill=BOTH, expand=True)

        self.table_name = table_name
        self.database =DatabaseManager()
        self.show_active_trials = show_active_trials

        # Get columns from SQLite.
        columns_info = self.database.get_columns(table_name)

        self.columns = [
            col[1] for col in columns_info
        ]


        # Title

        title = ttk.Label(
            self,
            text=table_name,
            font=("Helvetica", 20, "bold")
        )
        title.pack(pady=10)

        #Starts the coding
        # Table (threeview)

        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            show="headings"
        )

        # Headers depending on parameters
        for col in self.columns:

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=150,
                anchor="center"
            )

        self.tree.pack(
            fill=BOTH,
            expand=True,
            padx=20,
            pady=20
        )

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        #Show all studies

        all_studies_button= ttk.Button(
            self,
            text="Show All Studies",
            bootstyle=SECONDARY,
            command=self.show_active_trials
        )
        all_studies_button.pack(pady=10) #This shows the button


        # Add subject

        add_button = ttk.Button(
            button_frame,
            text="Add Subject",
            bootstyle="success",
            command=self.add_subject
        )
        add_button.pack(side=LEFT, padx=20)

        # Delete subject

        delete_button = ttk.Button(
            button_frame,
            text="Delete Subject",
            bootstyle="danger",
            command=self.delete_subject
        )

        delete_button.pack(side=LEFT, padx=20)

        # Edit button

        edit_button = ttk.Button(
            button_frame,
            text="Edit Subject",
            bootstyle="warning",
            command=self.edit_subject
        )

        edit_button.pack(side=LEFT, padx=20)


    def add_subject(self):

        window= ttk.Toplevel(self) #Opens a new window

        window.title("Add Subject")

        window.geometry("400x500")

        self.entries={}

        for col in self.columns: #Get the name of the columns
            if col == "id":
                continue

            ttk.Label(
            window,text=col).pack(anchor="w",padx=10,pady=(10,0))

            entry = ttk.Entry(
                window
            )

            entry.pack( fill="x", padx=10, pady=5
            )

            self.entries[col] = entry

        # Save button it needs to be inside the function cause is where the window is created
        save_button = ttk.Button(
            window,
            text="Save",
            bootstyle="success",
            command=lambda: self.save_subject(window)  # needs to be located in window
         )
        save_button.pack(pady=20)




    def save_subject(self, window):

        values= []

        for col in self.columns:

            if col == "id": #don´t ask for this information since the system will give it
                continue

            value=self.entries[col].get()

            values.append(value)

        row_id= self.database.insert_row(
            self.table_name,
            values)     #Saves what the function returns

        self.tree.insert(
            "",
            "end",
            values=(row_id,*values)
        )
            #The variable values is a list but without the * it takes the whole list as a single element
            # * makes that python consider the items in the list as separated elements and put them in the corresponding columns

        window.destroy()

    def delete_subject(self):

        selected_item=self.tree.selection()

        if not selected_item:
            return

        item_id=selected_item[0] #Part of Tkinter internal identification number

        values=self.tree.item(item_id,"values")

        row_id = values[0]

        self.database.delete_row(
            self.table_name,
            row_id
        ) #To delete on SQL

        self.tree.delete(item_id) #Delete from the interfaz

    def edit_subject(self):

        selected_item = self.tree.selection()

        if not selected_item:
            return

        item_id = selected_item[0]

        values = self.tree.item(item_id, "values")

        window = ttk.Toplevel(self)
        window.title("Edit Subject")
        window.geometry("400x500")

        self.edit_entries = {}

        for i, col in enumerate(self.columns):

            if col == "id":
                continue

            ttk.Label(
                window,
                text=col
            ).pack(anchor="w", padx=10, pady=(10, 0))

            entry = ttk.Entry(window)
            entry.pack(fill="x", padx=10, pady=5)

            entry.insert(0, values[i])

            self.edit_entries[col] = entry

        def save_changes():

            new_values = []

            for col in self.columns:
                if col == "id":
                    continue

                new_values.append(
                    self.edit_entries[col].get()
                )

            row_id = values[0]

            self.database.edit_row(
                self.table_name,
                row_id,
                [c for c in self.columns if c != "id"],
                new_values
            )

            self.tree.item(
                item_id,
                values=(row_id, *new_values)
            )

            window.destroy()

        ttk.Button(
            window,
            text="Save Changes",
            bootstyle="success",
            command=save_changes
        ).pack(pady=20)

