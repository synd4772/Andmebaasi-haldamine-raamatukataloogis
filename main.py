
from tkinter import *
from sqlite_handler import *
from random import *
from time import *


main_database = SQLHDatabase("data.db")

main_frame = None
buttons_frame = None

autor_date_entry = None
autor_nimi_entry = None
zanr_nimi_entry = None

pealkiri_entry = None
valjaandmise_kuupaev_entry = None
autor_id = None
zanr_id = None

main_frame_bg_color = "#30304d"

def add_columns(table:SQLHTable, columns:list):
    for column in columns:
        if isinstance(column, SQLHColumn):
            table.add_column(column)

def set_tables(database_instance:SQLHDatabase, tables:list):
    for table in tables:
        database_instance.add_table(table)

autors_table = SQLHTable(name="autorid", row_id=True, row_id_name = "autorid_id", alr_exists=True)
autor_name_column = SQLHColumn(name="autor_nimi", type="TEXT", constraint="NOT NULL")
sunnikuupaev_column = SQLHColumn(name="sunnikuupaev", type="DATE", constraint="NOT NULL")
autors_table_columns = [autor_name_column, sunnikuupaev_column]
add_columns(autors_table, autors_table_columns)

zanrid_table = SQLHTable(name="zanrid", row_id=True, row_id_name = "zanrid_id", alr_exists=True)
zanri_nimi_column = SQLHColumn(name="zanri_nimi", type="TEXT", constraint="NOT NULL")
zanrid_table_columns = [zanri_nimi_column]
add_columns(zanrid_table, zanrid_table_columns)

book_table = SQLHTable(name="raamatud", row_id=True, row_id_name = "raamat_id", alr_exists=True)
pealkiri_column = SQLHColumn(name="pealkiri", type="TEXT", constraint="NOT NULL")
valjaandmise_kuupaev_column = SQLHColumn(name="valjaandmise_kuupaev", type="DATE", constraint="NOT NULL")
autor_id_foreign_column = SQLHColumn(name="autor_id", type="INTEGER", constraint="NOT NULL", foreign_key=autors_table)
zanr_id_foreign_column = SQLHColumn (name="zanr_id", type="INTEGER", constraint="NOT NULL", foreign_key=zanrid_table)
book_table_columns = [pealkiri_column, valjaandmise_kuupaev_column, autor_id_foreign_column, zanr_id_foreign_column]
add_columns(book_table, book_table_columns)

all_tables = [autors_table, zanrid_table, book_table]
set_tables(main_database, all_tables)


class DatabaseUI(object):
  
  def __init__(self, root):
    self.root = root
    self.root.title = "Database Management"
    self.root.geometry("800x800")
    self.root.resizable(False, False)

    self.main_frame = None
    self.buttons_frame = None

    self.autor_date_entry = None
    self.autor_nimi_entry = None
    self.zanr_nimi_entry = None

    self.pealkiri_entry = None
    self.valjaandmise_kuupaev_entry = None
    self.autor_id = None
    self.zanr_id = None

    self.main_frame_bg_color = "#30304d"

    self.tables_page_buttons = [["Kodu menüü", self.home], ["Raamat", self.see_book_table], ["Autor", self.see_autor_table], ["Zanr", self.see_zanr_table]]
    self.page_buttons = [["Kõik raamatud", self.see_all_books], ["Redigeerimismenüü", self.changing_menu], ["Kõik tabelid", self.see_all_tables]]
    self.editing_page_buttons = [["Kodu menüü", self.home],["Lisa raamat", self.add_book], ["Lisa autor", self.add_autor], ["Lisa zanr", self.add_zanr]]

    self.home()

  def home_page():
    pass

  def render_menu_buttons(self, page_buttons):
    if self.buttons_frame is None:
        self.buttons_frame = Frame(root, bg="#705c83")
        self.buttons_frame.pack(fill=X)
    else:
        self.clear_frame(self.buttons_frame)

    for page_button in page_buttons:
        button = Button(self.buttons_frame, text=page_button[0], command=page_button[1], bg="#21063c", fg="#45456e", font=("Arial", 25))
        button.pack(expand=True, side=LEFT, pady=10)

    return self.buttons_frame

  def render_main_frame(self):
      if self.main_frame is None:
          self.main_frame = Frame(root, bg=main_frame_bg_color, height=800)
          self.main_frame.pack(fill=BOTH)
      return self.main_frame


  def clear_frame(self, frame):
    for widget in frame.winfo_children():
        widget.destroy()

  def see_all_books(self):
    pass

  def changing_menu(self):
      self.reset_window(self.editing_page_buttons)
      label = Label(self.main_frame, text="Siin saab lisada tabelite kirjeid", font = ("Arial", 25), fg="White", bg=self.main_frame_bg_color)
      label.pack(pady=200)
      space = Label(self.main_frame, bg=self.main_frame_bg_color)
      space.pack(pady=1800)
      pass

  def add_book(self):
      # pealkiri_entry = None
      # valjaandmise_kuupaev_entry = None
      # autor_id = None
      # zanr_id = None
      self.reset_window(self.editing_page_buttons)
      space = Label(self.main_frame, bg = self.main_frame_bg_color)
      space.pack(pady=40)

      book_nimi_label = Label(self.main_frame, text="Pealkiri", fg="white", bg=self.main_frame_bg_color, font = ("Arial", 20))
      book_nimi_label.pack(pady=10)
      self.pealkiri_entry = Entry(self.main_frame, font=("Arial", 15) )
      self.pealkiri_entry.pack()

      book_date = Label(self.main_frame, text="Valjaandmise kuupaev", fg="white", bg=self.main_frame_bg_color, font = ("Arial", 20))
      book_date.pack(pady=10)
      self.valjaandmise_kuupaev_entry = Entry(self.main_frame, font = ("Arial", 15))
      self.valjaandmise_kuupaev_entry.pack()

      book_autor_id = Label(self.main_frame, text="Autor id", fg="white", bg=self.main_frame_bg_color, font = ("Arial", 20))
      book_autor_id.pack(pady=10)
      self.autor_id = Entry(self.main_frame, font = ("Arial", 15))
      self.autor_id.pack()

      book_zanr_id = Label(self.main_frame, text="Zanr id", fg="white", bg=main_frame_bg_color, font = ("Arial", 20))
      book_zanr_id.pack(pady=10)
      self.zanr_id = Entry(self.main_frame, font = ("Arial", 15))
      self.zanr_id.pack()

      confirm_button = Button(self.main_frame, text="Lisa", width=8, height=1, fg="white", bg="gray", font = ("Arial", 15), command=self.confirm_book)
      confirm_button.pack(pady=80)
      space2 = Label(self.main_frame, bg = self.main_frame_bg_color)
      space2.pack(pady=100)
      pass

  def confirm_book(self):
      pealkiri = self.pealkiri_entry.get()
      kuupaev = self.valjaandmise_kuupaev_entry.get()
      autor = self.autor_id.get()
      zanr = self.zanr_id.get()

      book_table.add_record([pealkiri, kuupaev, autor, zanr])
      self.reset_window(self.page_buttons)
      self.tabel_info(book_table)

  def reset_window(self, buttons):
      if self.buttons_frame is not None:
        self.clear_frame(self.buttons_frame)
      self.buttons_frame = self.render_menu_buttons(buttons)

      if self.main_frame is not None:
        self.clear_frame(self.main_frame)

      self.main_frame = self.render_main_frame()
      
      
      
      

  def confirm_autor(self):
      name = self.autor_nimi_entry.get()
      date = self.autor_date_entry.get()
      autors_table.add_record([name, date])

      self.reset_window(self.page_buttons)

  def confirm_zanr(self):
      zanr = self.zanr_nimi_entry.get()
      zanrid_table.add_record([zanr])

      self.reset_window(self.page_buttons)

  def add_autor(self):
      self.reset_window(self.editing_page_buttons)
      space = Label(self.main_frame, bg = self.main_frame_bg_color)
      space.pack(pady=60)
      autor_nimi_label = Label(self.main_frame, text="Autor nimi", fg="white", bg=self.main_frame_bg_color, font = ("Arial", 20))
      autor_nimi_label.pack(pady=10)
      self.autor_nimi_entry = Entry(self.main_frame, font=("Arial", 15) )
      self.autor_nimi_entry.pack()
      autor_date = Label(self.main_frame, text="Autor sünnipaev", fg="white", bg=self.main_frame_bg_color, font = ("Arial", 20))
      autor_date.pack(pady=10)
      self.autor_date_entry = Entry(self.main_frame, font = ("Arial", 15))
      self.autor_date_entry.pack()

      confirm_button = Button(self.main_frame, text="Lisa", width=8, height=1, fg="white", bg="gray", font = ("Arial", 15), command=self.confirm_autor)
      confirm_button.pack(pady=80)
      space2 = Label(self.main_frame, bg = self.main_frame_bg_color)
      space2.pack(pady=100)

  def add_zanr(self):
      self.reset_window(self.editing_page_buttons)
      space = Label(self.main_frame, bg = self.main_frame_bg_color)
      space.pack(pady=80)
      autor_nimi_label = Label(self.main_frame, text="Zanr", fg="white", bg=self.main_frame_bg_color, font = ("Arial", 20))
      autor_nimi_label.pack(pady=10)
      self.zanr_nimi_entry = Entry(self.main_frame, font=("Arial", 15) )
      self.zanr_nimi_entry.pack()
      confirm_button = Button(self.main_frame, text="Lisa", width=8, height=1, fg="white", bg="gray", font = ("Arial", 15), command=self.confirm_zanr)
      confirm_button.pack(pady=40)
      space2 = Label(self.main_frame, bg = self.main_frame_bg_color)
      space2.pack(pady=190)

  def home(self):
      self.reset_window(self.page_buttons)
      space = Label(self.main_frame, bg=self.main_frame_bg_color)
      label = Label(self.main_frame, text="Peamenüü, vali, mida soovid ülevalt nuppudega teha", font = ("Arial", 25), fg = "White", bg = self.main_frame_bg_color)
      label.pack(pady=200)
      space.pack(pady=500)


  def see_all_tables(self):
      self.reset_window(self.tables_page_buttons)
      
  def tabel_info(self, tabel:SQLHTable):
      name = tabel.name
      columns = tabel.get_columns()
      start_space = Label(self.main_frame, bg=self.main_frame_bg_color)
      start_space.pack(pady=50)

      # TABLE NAME START

      table_name_label = Label(self.main_frame, bg = self.main_frame_bg_color, text = f"{name}", fg="White", font=("Arial", 20))
      table_name_label.pack()

      # END

      # -----------------------------------------------------------------------------------------------------------------

      # TABLE COLUMNS START

      columns_labels_list = list()
      columns_labels_frame = Frame(self.main_frame, bg = self.main_frame_bg_color)
      columns_labels_frame.pack()
      for column in columns:
          column_label = Label(columns_labels_frame, text = column.name, bg="#181436", fg="white", width=19, height=1, font=("Arial",10), borderwidth=1, relief="solid")
          columns_labels_list.append(column_label)
          column_label.pack(side=LEFT)
      else:
          edit_button = Button(columns_labels_frame, bg='#181436', fg='white', width=6, height=1, borderwidth=1, relief="solid", font=("Arial",7))
          edit_button.pack(side=LEFT)
      #trebuetsa dobavit kod dalshe!

      # END

      # ----------------------------------------------------------------------------------------------------------------- 

      # TABLE RECORDS START

      records = tabel.get_records(rows = True)
      print(records)
      record_labels_list = list()
      count = 0
      for column_index, row in enumerate(records):
        temp_frame = Frame(self.main_frame, bg = self.main_frame_bg_color)
        temp_frame.pack()
        row_id = row[0]
        print(records, 'LETSGOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
        for record in row:
          record_label = Label(temp_frame, text = record, bg='#181436', fg='white', width=19, height=1, font=("Arial",10), borderwidth=1, relief="solid")
          record_labels_list.append(record_label)
          record_label.pack(side=LEFT)
        Button(temp_frame, text = "edit", bg='#181436', fg='white', width=6, height=1, font=("Arial",7), borderwidth=1, relief="solid", command=lambda record_id = row_id: self.edit_record(table = tabel, record = record_id)).pack(side=RIGHT, expand=True)
      
      #trebuetsa dobavit kod dalshe!

      # END

      # -----------------------------------------------------------------------------------------------------------------

      end_space = Label(self.main_frame, bg=self.main_frame_bg_color)
      end_space.pack(pady=1800)

  def edit_record(self, table, record):
    row = table.get_row_by_id(record)
    self.reset_window(self.tables_page_buttons)
    start_space = Label(self.main_frame, bg=self.main_frame_bg_color)
    start_space.pack(pady=120)
    columns = table.get_columns()
    columns_labels_list = list()
    columns_labels_frame = Frame(self.main_frame, bg = self.main_frame_bg_color)
    columns_labels_frame.pack()
    for column in columns:
        column_label = Label(columns_labels_frame, text = column.name, bg="#181436", fg="white", width=19, height=1, font=("Arial",10), borderwidth=1, relief="solid")
        columns_labels_list.append(column_label)
        column_label.pack(side=LEFT)

    temp_frame = Frame(self.main_frame, bg = self.main_frame_bg_color)
    temp_frame.pack()
    entrys_list = list()
    for index, t_record in enumerate(row):
      if index != 0:
        record_label = Entry(temp_frame, bg='#181436', fg='white', width=22, font=("Arial",10), borderwidth=1, relief="solid")
        record_label.insert(0, t_record)
        record_label.pack(side=LEFT)
        entrys_list.append({columns[index]:record_label})
      else:
        record_label = Label(temp_frame, text = t_record, bg='#181436', fg='white', width=19, font=("Arial",10), borderwidth=1, relief="solid")
        record_label.pack(side=LEFT)

    second_space = Label(self.main_frame, bg=self.main_frame_bg_color)
    second_space.pack(pady=10)

    cd_frame = Frame(self.main_frame, bg='#181436')
    cd_frame.pack()
    confirm_button = Button(cd_frame, font=("Arial",10), text="Confirm", command=lambda entrys = entrys_list: self.confirm_change(table=table, id=record, entrys=entrys))
    confirm_button.pack(side=LEFT)
    delete_button = Button(cd_frame, font=("Arial",10), text="Delete", command=lambda cmd_id = record: self.delete_record(table, cmd_id))
    delete_button.pack(side=LEFT)

    end_space = Label(self.main_frame, bg=self.main_frame_bg_color)
    end_space.pack(pady=1800)

  def confirm_change(self, table, id, entrys):
    for entry_list in entrys:
      for key, value in entry_list.items():
        # main_database.change_record_table(table=table.name, condition=[key.name, (f"'{value.get()}'" if not value.get().isdigit() else value.get()), table.primary_key.name, id])
        table.change_record(table.get_column_dict(key)["column_object"].name, (f"'{value.get()}'" if not value.get().isdigit() else value.get()), id, live=True)
    self.reset_window(self.tables_page_buttons)
    
    self.tabel_info(table)

  def delete_record(self, table, id):
    table.delete_record(id, live=True)
    self.reset_window(self.tables_page_buttons)
    self.tabel_info(table)
    pass

  def see_book_table(self):

      self.reset_window(self.tables_page_buttons)
      self.tabel_info(book_table)
      pass

  def see_autor_table(self):
      self.reset_window(self.tables_page_buttons)
      self.tabel_info(autors_table)
      pass

  def see_zanr_table(self):
      self.reset_window(self.tables_page_buttons)
      self.tabel_info(zanrid_table)
      pass


if __name__ == "__main__":
  root = Tk()
  app = DatabaseUI(root)
  root.mainloop()
    
