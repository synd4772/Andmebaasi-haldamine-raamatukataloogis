from cgitb import reset, text
from enum import auto
from json.tool import main
from sre_parse import expand_template
from tkinter import *
from sqlite_handler import *
from random import *
main_database = SQLHDatabase("data.db")

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

def render_menu_buttons(page_buttons):
    frame = Frame(root, bg="#705c83")
    frame.pack(fill=X)
    for page_button in page_buttons:
        see_table_button = Button(frame, text=page_button[0], command=page_button[1], bg="#21063c", fg="#45456e", font=("Arial", 25))
        page_buttons_objects.append(see_table_button)
    for button in page_buttons_objects:
        button.pack(expand=True, side=LEFT, pady=10)
    return frame

def render_main_frame():
    main_frame = Frame(root, bg="#30304d", height=800)
    main_frame.pack(fill=BOTH)

    return main_frame

def table_template(root:Tk, table:SQLHTable, pack:bool = True):

    pass


def changing_menu():
    global buttons_frame, main_frame
    reset_window(editing_page_buttons)
    label = Label(main_frame, text="Siin saab lisada tabelite kirjeid", font = ("Arial", 25), fg="White", bg=main_frame_bg_color)
    label.pack(pady=200)
    space = Label(main_frame, bg=main_frame_bg_color)
    space.pack(pady=1800)
    pass

def render_all_tables():
    pass

def see_all_books():
    print("hallo")
    pass

def add_book():
    # pealkiri_entry = None
    # valjaandmise_kuupaev_entry = None
    # autor_id = None
    # zanr_id = None
    global main_frame, pealkiri_entry, valjaandmise_kuupaev_entry, autor_id, zanr_id
    reset_window(editing_page_buttons)
    space = Label(main_frame, bg = main_frame_bg_color)
    space.pack(pady=40)

    book_nimi_label = Label(main_frame, text="Pealkiri", fg="white", bg=main_frame_bg_color, font = ("Arial", 20))
    book_nimi_label.pack(pady=10)
    book_nimi_entry = Entry(main_frame, font=("Arial", 15) )
    book_nimi_entry.pack()

    book_date = Label(main_frame, text="Valjaandmise kuupaev", fg="white", bg=main_frame_bg_color, font = ("Arial", 20))
    book_date.pack(pady=10)
    book_date_entry = Entry(main_frame, font = ("Arial", 15))
    book_date_entry.pack()

    book_autor_id = Label(main_frame, text="Autor id", fg="white", bg=main_frame_bg_color, font = ("Arial", 20))
    book_autor_id.pack(pady=10)
    autor_id = Entry(main_frame, font = ("Arial", 15))
    autor_id.pack()

    book_zanr_id = Label(main_frame, text="Zanr id", fg="white", bg=main_frame_bg_color, font = ("Arial", 20))
    book_zanr_id.pack(pady=10)
    zanr_id = Entry(main_frame, font = ("Arial", 15))
    zanr_id.pack()

    confirm_button = Button(main_frame, text="Lisa", width=8, height=1, fg="white", bg="gray", font = ("Arial", 15), command=confirm_autor)
    confirm_button.pack(pady=80)
    space2 = Label(main_frame, bg = main_frame_bg_color)
    space2.pack(pady=100)
    pass

def confirm_book():
    pealkiri = pealkiri_entry.get()
    kuupaev = valjaandmise_kuupaev_entry.get()
    autor = autor_id.get()
    zanr = zanr_id.get()

    book_table.add_record([pealkiri, kuupaev, autor, zanr])
    reset_window(page_buttons)

def reset_window(buttons):
    global main_frame, buttons_frame
    main_frame.destroy()
    buttons_frame.destroy()

    buttons_frame = render_menu_buttons(buttons)
    main_frame = render_main_frame()

def confirm_autor():
    global main_frame, buttons_frame

    name = autor_nimi_entry.get()
    date = autor_date_entry.get()
    autors_table.add_record([name, date])

    reset_window(page_buttons)

def confirm_zanr():
    
    zanr = zanr_nimi_entry.get()
    zanrid_table.add_record([zanr])

    reset_window(page_buttons)

def add_autor():
    global main_frame, autor_nimi_entry, autor_date_entry
    reset_window(editing_page_buttons)
    space = Label(main_frame, bg = main_frame_bg_color)
    space.pack(pady=60)
    autor_nimi_label = Label(main_frame, text="Autor nimi", fg="white", bg=main_frame_bg_color, font = ("Arial", 20))
    autor_nimi_label.pack(pady=10)
    autor_nimi_entry = Entry(main_frame, font=("Arial", 15) )
    autor_nimi_entry.pack()
    autor_date = Label(main_frame, text="Autor sünnipaev", fg="white", bg=main_frame_bg_color, font = ("Arial", 20))
    autor_date.pack(pady=10)
    autor_date_entry = Entry(main_frame, font = ("Arial", 15))
    autor_date_entry.pack()

    confirm_button = Button(main_frame, text="Lisa", width=8, height=1, fg="white", bg="gray", font = ("Arial", 15), command=confirm_autor)
    confirm_button.pack(pady=80)
    space2 = Label(main_frame, bg = main_frame_bg_color)
    space2.pack(pady=100)
    pass

def add_zanr():
    global main_frame, zanr_nimi_entry
    reset_window(editing_page_buttons)
    space = Label(main_frame, bg = main_frame_bg_color)
    space.pack(pady=80)
    autor_nimi_label = Label(main_frame, text="Zanr", fg="white", bg=main_frame_bg_color, font = ("Arial", 20))
    autor_nimi_label.pack(pady=10)
    zanr_nimi_entry = Entry(main_frame, font=("Arial", 15) )
    zanr_nimi_entry.pack()
    confirm_button = Button(main_frame, text="Lisa", width=8, height=1, fg="white", bg="gray", font = ("Arial", 15), command=confirm_zanr)
    confirm_button.pack(pady=40)
    space2 = Label(main_frame, bg = main_frame_bg_color)
    space2.pack(pady=190)

def home():
    global buttons_frame, main_frame
    reset_window(page_buttons)
    space = Label(main_frame, bg=main_frame_bg_color)
    label = Label(main_frame, text="Peamenüü, vali, mida soovid ülevalt nuppudega teha", font = ("Arial", 25), fg = "White", bg = main_frame_bg_color)
    label.pack(pady=200)

    space.pack(pady=500)


def see_all_tables():
    reset_window(tables_page_buttons)
    
def tabel_info(tabel:SQLHTable):
    name = tabel.name
    columns = tabel.get_columns()
    start_space = Label(main_frame, bg=main_frame_bg_color)
    start_space.pack(pady=50)

    # TABLE NAME START

    table_name_label = Label(main_frame, bg = main_frame_bg_color, text = f"{name}", fg="White", font=("Arial", 20))
    table_name_label.pack()

    # END

    # -----------------------------------------------------------------------------------------------------------------

    # TABLE COLUMNS START

    table_columns_label = Label(main_frame, bg = main_frame_bg_color, text = f"Tabeli veerud:", fg="White", font=("Arial", 20))
    table_columns_label.pack()

    columns_labels_list = list()
    for column in columns:
        column_label = Label(main_frame, text = column.name, bg="white", fg="black", width=10, height=1)
        columns_labels_list.append(column_label)

    for clmns in columns_labels_list:
        clmns.pack(side = LEFT)

    #trebuetsa dobavit kod dalshe!

    # END

    # ----------------------------------------------------------------------------------------------------------------- 

    # TABLE RECORDS START

    table_records_label = Label(main_frame, bg = main_frame_bg_color, text = f"Tabeli andmed:", fg="White", font=("Arial", 20))
    table_records_label.pack()

    #trebuetsa dobavit kod dalshe!

    # END

    # -----------------------------------------------------------------------------------------------------------------

    end_space = Label(main_frame, bg=main_frame_bg_color)
    end_space.pack(pady=1800)

def see_book_table():

    reset_window(tables_page_buttons)
    tabel_info(book_table)
    pass

def see_autor_table():
    reset_window(tables_page_buttons)
    tabel_info(autors_table)
    pass

def see_zanr_table():
    reset_window(tables_page_buttons)
    tabel_info(zanrid_table)
    pass

root = Tk()
root.title("Database Management")
root.geometry("800x800")
root.resizable(False, False)


tables_page_buttons = [["Kodu menüü", home], ["Raamat", see_book_table], ["Autor", see_autor_table], ["Zanr", see_zanr_table]]
page_buttons = [["Kõik raamatud", see_all_books], ["Redigeerimismenüü", changing_menu], ["Kõik tabelid", see_all_tables]]
editing_page_buttons = [["Kodu menüü", home],["Lisa raamat", add_book], ["Lisa autor", add_autor], ["Lisa zanr", add_zanr]]
page_buttons_objects = list()
buttons_frame = render_menu_buttons(page_buttons)
main_frame = render_main_frame()
home()
root.mainloop()
