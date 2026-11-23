import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database.database_manager import DatabaseManager

class CreateDatabasePage(ttk.Frame):

    def __init__(self, parent, show_user_data_base, show_dashboard):
        super().__init__(parent)

        self.pack(fill=BOTH, expand=True, padx=20, pady=20)

        self.columns = []
        self.show_user_data_base= show_user_data_base
        self.show_dashboard = show_dashboard

        # Title
        title = ttk.Label(
            self,
            text="Create Study",
            font=("Helvetica", 22, "bold")
        )
        title.pack(pady=(0, 20))

        # Table name
        ttk.Label(
            self,
            text="Table Name"
        ).pack(anchor="w")

        self.table_name_entry = ttk.Entry(
            self,
            width=40
        )
        self.table_name_entry.pack(fill="x", pady=(5, 15))

        # Column name
        ttk.Label(
            self,
            text="Column Name"
        ).pack(anchor="w")

        self.column_name_entry = ttk.Entry(
            self,
            width=40
        )
        self.column_name_entry.pack(fill="x", pady=(5, 15))

        # Data Type
        ttk.Label(
            self,
            text="Data Type"
        ).pack(anchor="w")

        self.type_combobox = ttk.Combobox(
            self,
            values=[
                "TEXT",
                "INTEGER",
                "REAL",
                "DATE",
                "BOOLEAN"
            ],
            state="readonly"
        )

        self.type_combobox.current(0)
        self.type_combobox.pack(fill="x", pady=(5, 15))

        # Add column botton
        add_button = ttk.Button(
            self,
            text="Add Column",
            bootstyle="primary",
            command=self.add_column
        )

        add_button.pack(pady=10)

        #Delete column button

        delete_button = ttk.Button(
            self,
            text="Delete",
            bootstyle="danger",
            command=self.delete
        )

        delete_button.pack(pady=5)


        # Table of columns
        self.columns_tree = ttk.Treeview(
            self,
            columns=("column", "datatype"),
            show="headings",
            height=8
        )

        self.columns_tree.heading(
            "column",
            text="Column Name"
        )

        self.columns_tree.heading(
            "datatype",
            text="Data Type"
        )

        self.columns_tree.column(
            "column",
            width=250,
            anchor="center"
        )

        self.columns_tree.column(
            "datatype",
            width=150,
            anchor="center"
        )

        self.columns_tree.pack(
            fill="both",
            expand=True,
            pady=20
        )

        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill= "x",pady=20,padx=150)

        # Create study button
        create_button = ttk.Button(
            button_frame,
            text="Create Study",
            bootstyle="success",
            command= self.create_study
        )

        create_button.pack(side="right")

        #Back button

        back_button = ttk.Button(
            button_frame,
            text="Back",
            bootstyle="secondary",
            command=self.show_dashboard
        )

        back_button.pack(side="left")

    def add_column(self):

        column_name = self.column_name_entry.get().strip()

        data_type = self.type_combobox.get()

        if not column_name:
            return

        self.columns.append(
            (column_name, data_type)
        )

        self.columns_tree.insert(
            "",
            "end",
            values=(column_name, data_type)
        )

        self.column_name_entry.delete(0, "end")

    def create_study(self):
        table_name = self.table_name_entry.get().strip() #Strip removes spaces from the beginning and the end of a string

        if not table_name:
            return

        database =DatabaseManager() #Calls the class to create an object of this type.

        database.create_table( #Call the method and add the information required
            table_name,
            self.columns
        )

        self.show_user_data_base(
            table_name
        )

    def delete(self):
        selected_item=self.columns_tree.selection() #returns the selected values

        if not selected_item:
            return

        item_id=selected_item[0]

        values=self.columns_tree.item(
            item_id,
            "values"
        )

        column_name = values[0]
        data_type = values[1]

        if (column_name, data_type) in self.columns:
            self.columns.remove(
                (column_name, data_type)
            )

        self.columns_tree.delete(item_id)


class App(ttk.Window):

    def __init__(self):
        super().__init__(themename="flatly")

        self.title("Clinical Trial Recruitment Dashboard")

        self.geometry("800x600")

        CreateDatabasePage(self)


if __name__ == "__main__":
    app.mainloop()