import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import shelve
from itertools import groupby
import os
import csv
from time import time


class StartWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.init_start_window()

    def init_start_window(self):
        btn_create_database = tk.Button(text='Создать БД', command=self.create_database,
                                        bg='#d7d8e8', padx="20", pady="8")
        btn_create_database.place(relx=.5, rely=.3, anchor="c")

        btn_open_database = tk.Button(text='Открыть БД', command=self.open_database,
                                      bg='#d7d8e8', padx="20", pady="8")
        btn_open_database.place(relx=.5, rely=.5, anchor="c")

    def create_database(self):
        CreateDatabaseWindow()

    def open_database(self):
        OpenDatabaseWindow()


class CreateDatabaseWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_create_window()

    def init_create_window(self):
        self.title('Создать базу данных')
        self.geometry("400x80+550+350")
        self.resizable(False, False)

        label_file_name = tk.Label(self, text='Название файла')
        label_file_name.place(x=70, y=10)
        self.file_name = tk.StringVar()
        self.entry_file_name = ttk.Entry(self, textvariable=self.file_name)
        self.entry_file_name.place(x=180, y=10)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=195, y=40)

        btn_add = ttk.Button(self, text='Создать')
        btn_add.place(x=115, y=40)
        btn_add.bind('<Button-1>', lambda event: self.create_database(self.entry_file_name.get()))

        self.grab_set()
        self.focus_set()

    def create_database(self, file_name):
        if len(file_name) == 0:
            messagebox.showerror('Ошибка!', 'Поле ввода не должно быть пустым')
        elif os.path.exists(f"ShelveData/{file_name}.bak"):
            messagebox.showerror('Ошибка!', 'База данных уже существует')
        else:
            main_file = shelve.open(f"ShelveData/{file_name}")
            main_file.close()

            keys_file = shelve.open(f"IDs/{file_name}_IDs")
            keys_file['ID'] = 0
            keys_file.close()

            service_file = shelve.open(f"ServiceFiles/{file_name}_service")
            service_file.close()

            db_list_file = open("database_list.csv", "a", encoding='utf-8')
            writer = csv.writer(db_list_file, lineterminator="\r")
            writer.writerow([file_name])
            db_list_file.close()

            DataBaseWindow(file_name)
            CreateDatabaseWindow.destroy(self)


class OpenDatabaseWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.available_databases = self.read_databases()
        self.init_open_window()

    def init_open_window(self):
        self.title('Открыть базу данных')
        self.geometry("400x80+550+350")
        self.resizable(False, False)

        database_labels = tk.Label(self, text='Доступные БД:')
        database_labels.place(x=70, y=10)

        self.field_list = ttk.Combobox(self, values=self.available_databases)
        self.field_list.place(x=170, y=10)
        self.field_list.current(0)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=195, y=40)

        btn_add = ttk.Button(self, text='Открыть')
        btn_add.place(x=115, y=40)
        btn_add.bind('<Button-1>', lambda event: self.open_database(self.field_list.get()))

        self.grab_set()
        self.focus_set()

    def open_database(self, file_name):
        if len(file_name) == 0:
            messagebox.showerror('Ошибка!', 'База данных не выбрана')
        else:
            if os.path.exists(f"ShelveData/{file_name}.bak"):
                DataBaseWindow(file_name)
                OpenDatabaseWindow.destroy(self)
            else:
                messagebox.showerror('Ошибка!', 'База данных не существует')

    def read_databases(self):
        with open("database_list.csv", "r") as db_list_file:
            reader = csv.reader(db_list_file)
            files = []
            for row in reader:
                files.append(row[0])
        return " ".join(files)


class DataBaseWindow(tk.Toplevel):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.permission = 0
        # self.key = self.create_id()
        root.withdraw()
        self.init_database_window()
        self.refresh()

    def init_database_window(self):
        self.title('Второе окно')
        self.geometry('665x350+450+200')
        self.resizable(False, False)

        self.main_menu = tk.Menu()

        self.file_menu = tk.Menu()
        self.file_menu.add_command(label="Поиск", command=self.open_search_window)
        self.file_menu.add_command(label="Удалить", command=self.delete_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Выход", command=self.back)

        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)
        self.main_menu.add_cascade(label="Добавить запись", command=self.open_add_window)
        self.main_menu.add_cascade(label="Редактировать", command=self.open_update_window)
        self.main_menu.add_cascade(label="Удалить", command=self.delete_line)
        '''command=lambda: [self.delete_line(), self.refresh()]'''
        self.main_menu.add_cascade(label="Обновить", command=self.refresh)

        self.config(menu=self.main_menu)

        self.tree = ttk.Treeview(self, columns=('ID', 'full_name', 'weight_category', 'sports_title'), height=15,
                                 show='headings')
        self.tree.column('ID', width=160, anchor=tk.CENTER)
        self.tree.column('full_name', width=160, anchor=tk.CENTER)
        self.tree.column('weight_category', width=160, anchor=tk.CENTER)
        self.tree.column('sports_title', width=160, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('full_name', text='ФИО')
        self.tree.heading('weight_category', text='Весовая категория')
        self.tree.heading('sports_title', text='Спортивный разряд')
        self.tree.place(x=2, y=0)

        self.tree.bind('<<TreeviewSelect>>', self.let_to_open)

        self.scrollbar = tk.Scrollbar(self, command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grab_set()
        self.focus_set()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        with shelve.open(f"ShelveData/{self.file_name}") as main_file:
            for key in main_file:
                self.tree.insert("", 'end', values=(key, main_file[key][0], main_file[key][1], main_file[key][2]))

    def back(self):
        root.deiconify()
        DataBaseWindow.destroy(self)

    def delete_file(self):
        if messagebox.askokcancel("Удаление", "Вы хотите удалить базу данных?"):
            os.remove(f"ShelveData/{self.file_name}.bak")
            os.remove(f"ShelveData/{self.file_name}.dat")
            os.remove(f"ShelveData/{self.file_name}.dir")
            os.remove(f"ServiceFiles/{self.file_name}_service.bak")
            os.remove(f"ServiceFiles/{self.file_name}_service.dat")
            os.remove(f"ServiceFiles/{self.file_name}_service.dir")
            os.remove(f"IDs/{self.file_name}_IDs.bak")
            os.remove(f"IDs/{self.file_name}_IDs.dat")
            os.remove(f"IDs/{self.file_name}_IDs.dir")
            with open("database_list.csv", "r", encoding='utf-8') as db_list_file:
                reader = csv.reader(db_list_file, lineterminator="\r")
                list = []
                for line in reader:
                    list.append(line[0])
                    print(list)
                list.remove(self.file_name)

            with open("database_list.csv", "w", encoding='utf-8') as db_list_file:
                writer = csv.writer(db_list_file, lineterminator="\r")
                for i in list:
                    writer.writerow([i])
                    print(i)
            root.deiconify()
            DataBaseWindow.destroy(self)
            messagebox.askokcancel("Успех!", "База данных удалена")
            return 0

    def delete_line(self):
        # start = time()
        try:
            num_of_line_to_delete = self.tree.set(self.tree.selection()[0], '#1')
            surname_of_line_to_delete = self.tree.set(self.tree.selection()[0], '#2')
            with shelve.open(f"ShelveData/{self.file_name}") as main_file:
                start = time()
                del main_file[num_of_line_to_delete]
                print("Время удаления в основном файле - ", time() - start)
            with shelve.open(f"ServiceFiles/{self.file_name}_service") as service_file:
                start = time()
                if type(service_file[surname_of_line_to_delete]) == str:
                    del service_file[surname_of_line_to_delete]
                else:
                    id_list = []
                    for i in range(len(service_file[surname_of_line_to_delete])):
                        id_list.append(service_file[surname_of_line_to_delete][i])
                    for i in range(len(service_file[surname_of_line_to_delete])):
                        if service_file[surname_of_line_to_delete][i] == num_of_line_to_delete:
                            del id_list[i]
                    service_list = [el for el, _ in groupby(id_list)]
                    if len(service_list) == 1:
                        service_file[surname_of_line_to_delete] = service_list[0]
                    else:
                        service_file[surname_of_line_to_delete] = service_list
                print("Время удаления в сервисном файле - ", time() - start)
        except IndexError as ie:
            messagebox.showerror('Не выбрана ни одна ячейка', ie)
        # print("Время удаления - ", time() - start)

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы хотите выйти?"):
            root.destroy()

    def let_to_open(self, event):
        self.permission = 1

    def open_add_window(self):
        AddWindow(self.file_name)

    def open_update_window(self):
        print(self.permission)
        if self.permission == 1:
            UpdateWindow(self.file_name, self.tree)
            self.permission = 0
        else:
            messagebox.showerror('Ошибка!', 'Ни одна ячейка не выбрана')

    def open_search_window(self):
        SearchWindow(self.file_name, self.tree)


class AddWindow(tk.Toplevel):
    def __init__(self, file_name):
        super().__init__()
        self.init_add_window()
        self.file_name = file_name
        # self.db = db

    def init_add_window(self):
        self.title('Третье окно')
        self.geometry('400x220+550+300')
        self.resizable(False, False)

        label_full_name = tk.Label(self, text='ФИО')
        label_full_name.place(x=50, y=50)
        self.full_name = tk.StringVar()
        self.entry_full_name = ttk.Entry(self, textvariable=self.full_name)
        self.entry_full_name.place(x=200, y=50)

        label_weight_category = tk.Label(self, text='Весовая категория')
        label_weight_category.place(x=50, y=80)
        self.weight_category = tk.StringVar()
        self.entry_weight_category = ttk.Entry(self, textvariable=self.weight_category)
        self.entry_weight_category.place(x=200, y=80)

        label_sports_title = tk.Label(self, text='Спортивный разряд')
        label_sports_title.place(x=50, y=110)
        self.sports_title = tk.StringVar()
        self.entry_sports_title = ttk.Entry(self, textvariable=self.sports_title)
        self.entry_sports_title.place(x=200, y=110)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind('<Button-1>', lambda event: [self.insert_data(self.entry_full_name.get(),
                                                                        self.entry_weight_category.get(),
                                                                        self.entry_sports_title.get()),
                                                       self.clear_fields()])

        self.grab_set()
        self.focus_set()

    def clear_fields(self):
        self.entry_full_name.delete(0, tk.END)
        self.entry_weight_category.delete(0, tk.END)
        self.entry_sports_title.delete(0, tk.END)

    def check_data(self, full_name, weight_category, sports_title):
        try:
            if len(full_name) < 1:
                raise ValueError('Поле "ФИО" не должно быть пустым')
            if any(map(str.isdigit, full_name)):
                raise ValueError('Поле "ФИО" не должно содержать чисел')
            if len(full_name) < 1:
                raise ValueError('Поле "Весовая категория" не должно быть пустым')
            if not weight_category.isdigit():
                raise ValueError('Поле "Весовая категория" должно содержать целочисленные значения')
            if int(weight_category) < 30:
                raise ValueError('Поле "Весовая категория" должно содержать значения > 30')
            if len(sports_title) < 1:
                raise ValueError('Поле "Спортивный разряд" не должно быть пустым')
            if not sports_title.isalnum():
                raise ValueError('Поле "Спортивный азряд" не должно содержать чисел')
        except ValueError as ve:
            messagebox.showerror('Ошибка!', ve)
            return ve
        else:
            return full_name, weight_category, sports_title

    def insert_data(self, full_name, weight_category, sports_title):
        values = self.check_data(full_name, weight_category, sports_title)
        if type(values) == ValueError:
            return 0
        else:
            id = self.set_id()
            # start = time()
            with shelve.open(f"ShelveData/{self.file_name}") as main_file:
                main_file[id] = [full_name, weight_category, sports_title]
                # print('Основной файл: ')
                # for i in main_file:
                    # print(i, ' - ', main_file[i])
            with shelve.open(f"ServiceFiles/{self.file_name}_service") as service_file:
                try:
                    changed_surname_value = service_file[full_name]  # если существует фамилия после редактирования

                    if type(changed_surname_value) == str:  # добавляем текущий номер строки к существующей фамилии
                        service_list = [changed_surname_value, id]  # одно существ значение
                        service_file[full_name] = service_list
                    else:
                        changed_surname_value.append(id)
                        service_list = changed_surname_value  # несколько
                        service_file[full_name] = service_list
                except KeyError:
                    service_file[full_name] = id
                # print('Служебный файл: ')
                # for i in service_file:
                    # print(i, ' - ', service_file[i])
            # print("Время добавления - ", time() - start)

    def set_id(self):
        with shelve.open(f"IDs/{self.file_name}_IDs") as keys_file:
            keys_file['ID'] += 1
            return str(keys_file['ID'])


class UpdateWindow(AddWindow):
    def __init__(self, file_name, tree):
        super().__init__(file_name)
        self.file_name = file_name
        self.tree = tree
        self.init_update_window()
        self.set_default_data()
        self.num_of_changing_line = self.get_tree_line_num()
        self.surname_before_changing = self.tree.set(self.tree.selection()[0], '#2')

    def init_update_window(self):
        self.title('Редактирование')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=210, y=170)
        self.btn_add.destroy()
        btn_edit.bind('<Button-1>', lambda event: [self.edit_data(self.entry_full_name.get(),
                                                                  self.entry_weight_category.get(),
                                                                  self.entry_sports_title.get()),
                                                   UpdateWindow.destroy(self)])

    def edit_data(self, full_name, weight_category, sports_title):
        values = self.check_data(full_name, weight_category, sports_title)
        if type(values) == ValueError:
            return 0
        else:
            with shelve.open(f"ShelveData/{self.file_name}") as main_file:
                main_file[self.num_of_changing_line] = [full_name, weight_category, sports_title]
                # print('Основной файл: ')
                # for i in main_file:
                    # print(i, ' - ', main_file[i])
            print("Фамилия до редактирования: ", self.surname_before_changing)
            print("Фамилия после редактирования: ", full_name)
            with shelve.open(f"ServiceFiles/{self.file_name}_service") as service_file:
                try:
                    changed_surname_value = service_file[full_name]  # если существует фамилия после редактирования

                    if type(changed_surname_value) == str:  # добавляем текущий номер строки к существующей фамилии
                        service_list = [changed_surname_value, self.num_of_changing_line]  # одно существ значение
                    else:
                        changed_surname_value.append(self.num_of_changing_line)
                        service_list = changed_surname_value  # несколько
                    service_list = [el for el, _ in groupby(service_list)]
                    if len(service_list) == 1:  # также убираем массив при случайном нажатии Редактировать
                        service_file[full_name] = service_list[0]
                    else:
                        service_file[full_name] = service_list
                    '''теперь нужно удалить строку до изменения'''
                    if self.surname_before_changing != full_name:  # проверка на случайное нажатие Редактировать
                        if type(service_file[self.surname_before_changing]) == str:  # если в строке было одно значение
                            del service_file[self.surname_before_changing]
                        else:  # если в строке был массив - удаляем одно значение из массива
                            id_list = []
                            for i in range(len(service_file[self.surname_before_changing])):
                                id_list.append(service_file[self.surname_before_changing][i])
                            for element in range(len(service_file[self.surname_before_changing])):
                                if service_file[self.surname_before_changing][element] == self.num_of_changing_line:
                                    del id_list[element]
                            service_list = [el for el, _ in groupby(id_list)]
                            if len(service_list) == 1:
                                service_file[self.surname_before_changing] = service_list[0]
                            else:
                                service_file[self.surname_before_changing] = service_list
                except KeyError:
                    '''теперь нужно удалить строку до изменения'''
                    if type(service_file[self.surname_before_changing]) == str:  # если в строке было одно значение
                        service_file[full_name] = self.num_of_changing_line  # изменение тут
                        del service_file[self.surname_before_changing]
                    else:  # если в строке был массив - удаляем одно значение из массива
                        id_list = []
                        for i in range(len(service_file[self.surname_before_changing])):
                            id_list.append(service_file[self.surname_before_changing][i])
                        for element in range(len(service_file[self.surname_before_changing])):
                            if service_file[self.surname_before_changing][element] == self.num_of_changing_line:
                                service_file[full_name] = id_list[element]  # изменение тут
                                del id_list[element]
                        service_list = [el for el, _ in groupby(id_list)]
                        if len(service_list) == 1:
                            service_file[self.surname_before_changing] = service_list[0]
                        else:
                            service_file[self.surname_before_changing] = service_list
                # print('Служебный файл: ')
                # for i in service_file:
                    # print(i, ' - ', service_file[i])

    def set_default_data(self):
        num_of_line = self.get_tree_line_num()
        with shelve.open(f"ShelveData/{self.file_name}") as main_file:
            self.entry_full_name.insert(0, main_file[num_of_line][0])
            self.entry_weight_category.insert(0, main_file[num_of_line][1])
            self.entry_sports_title.insert(0, main_file[num_of_line][2])

    def get_tree_line_num(self):
        return self.tree.set(self.tree.selection()[0], '#1')


class SearchWindow(tk.Toplevel):
    def __init__(self, file_name, tree):
        super().__init__()
        self.file_name = file_name
        self.tree = tree
        self.init_search_window()

    def init_search_window(self):
        self.title('Поиск')
        self.geometry('300x150+550+300')
        self.resizable(False, False)

        label_choose_field = tk.Label(self, text='Выберите поле')
        label_choose_field.place(x=30, y=20)
        self.field_list = ttk.Combobox(self, values=["ID", "ФИО", "Весовая категория", "Разряд"])
        self.field_list.place(x=125, y=20)
        self.field_list.current(1)

        label_search = tk.Label(self, text='Значение')
        label_search.place(x=45, y=50)
        self.search = tk.StringVar()
        self.entry_search = ttk.Entry(self, textvariable=self.search)
        self.entry_search.place(x=105, y=50, width=155)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=80)

        self.btn_search = ttk.Button(self, text='Поиск')
        self.btn_search.place(x=105, y=80)
        self.btn_search.bind('<Button-1>', lambda event: [self.search_data(self.field_list.get(),
                                                                           self.entry_search.get()),
                                                          SearchWindow.destroy(self)])

        self.grab_set()
        self.focus_set()

    def search_data(self, field, value):
        # start = time()
        with shelve.open(f"ShelveData/{self.file_name}") as main_file:
            if field == 'ФИО':
                try:
                    with shelve.open(f"ServiceFiles/{self.file_name}_service") as service_file:
                        print('service_value', service_file[value])
                        link = service_file[value]
                        '''[el for el, _ in groupby(service_file[value])]'''
                        print('link', link)
                        # print('Служебный файл: ')
                        # for i in service_file:
                            # print(i, ' - ', service_file[i])
                    self.tree.delete(*self.tree.get_children())
                    if type(link) == str:
                        self.tree.insert("", 'end',
                                         values=(link, main_file[link][0], main_file[link][1], main_file[link][2]))
                    else:
                        for key in link:
                            self.tree.insert("", 'end',
                                             values=(key, main_file[key][0], main_file[key][1], main_file[key][2]))
                    # print("Время поиска - ", time() - start)
                except KeyError:
                    messagebox.showerror('Упс!', 'Значение не существует')
            elif field == 'ID':
                try:
                    self.tree.delete(*self.tree.get_children())
                    self.tree.insert("", 'end',
                                     values=(value, main_file[value][0], main_file[value][1], main_file[value][2]))
                except KeyError:
                    messagebox.showerror('Упс!', 'Значение не существует')
            # print('Основной файл: ')
            # for i in main_file:
                # print(i, ' - ', main_file[i])


if __name__ == "__main__":
    root = tk.Tk()
    app = StartWindow(root)
    app.pack()

    root.title("Первое окно")
    root.geometry("400x220+550+300")
    root.resizable(False, False)
    root.mainloop()
