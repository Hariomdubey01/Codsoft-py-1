# A To-Do List application
from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get().strip()
    if not task_string:
        messagebox.showinfo('Error', 'Field is Empty.')
        return

    tasks.append(task_string)
    the_cursor.execute('INSERT INTO tasks VALUES (?)', (task_string,))
    task_field.delete(0, END)
    list_update()

def list_update():
    clear_list()
    for idx, task in enumerate(tasks, start=1):
        task_listbox.insert(END, f"{idx}. {task}")
    update_task_count()

def delete_task():
    try:
        selection = task_listbox.curselection()
        if not selection:
            raise Exception()
        selected_item = task_listbox.get(selection)
        actual_task = selected_item.split(". ", 1)[1] 
        if actual_task in tasks:
            tasks.remove(actual_task)
            the_cursor.execute('DELETE FROM tasks WHERE title = ?', (actual_task,))
            list_update()
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

def delete_all_tasks():
    confirm = messagebox.askyesno('Delete All', 'Are you sure you want to delete all tasks?')
    if confirm:
        tasks.clear()
        the_cursor.execute('DELETE FROM tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, END)

def close():
    guiWindow.destroy()

def retrieve_database():
    tasks.clear()
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])

def update_task_count():
    task_count_label.config(text=f"Total Tasks: {len(tasks)}")

# GUI
if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("📝 Simple To-Do List")
    guiWindow.geometry("700x500+500+250")
    guiWindow.resizable(False, False)
    guiWindow.configure(bg="#1f1f2e")

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

    tasks = []

    functions_frame = Frame(guiWindow, bg="#2c2c3e", bd=2, relief=FLAT)
    functions_frame.pack(side="top", expand=True, fill="both", padx=15, pady=15)

  
    task_label = Label(functions_frame, text="TO-DO LIST\nEnter Task:",
                       font=("Segoe UI", 14, "bold"), bg="#2c2c3e", fg="#F6BE00")
    task_label.place(x=20, y=20)


    task_field = Entry(functions_frame, font=("Segoe UI", 13), width=50,
                       bg="#1f1f2e", fg="white", insertbackground="white", relief=FLAT)
    task_field.place(x=170, y=35)

   
    add_button = Button(functions_frame, text="Add", width=15, font=("Segoe UI", 12, "bold"),
                        bg="#6C5CE7", fg="white", activebackground="#7e6aed", cursor="hand2", command=add_task)
    del_button = Button(functions_frame, text="Remove", width=15, font=("Segoe UI", 12, "bold"),
                        bg="#d63031", fg="white", activebackground="#ff4d4d", cursor="hand2", command=delete_task)
    del_all_button = Button(functions_frame, text="Delete All", width=15, font=("Segoe UI", 12, "bold"),
                            bg="#e17055", fg="white", activebackground="#ff9861", cursor="hand2", command=delete_all_tasks)
    exit_button = Button(functions_frame, text="Exit / Close", width=62, font=("Segoe UI", 12, "bold"),
                         bg="#2fabd8", fg="white", activebackground="#95a5a6", cursor="hand2", command=close)

    add_button.place(x=18, y=90)
    del_button.place(x=250, y=90)
    del_all_button.place(x=480, y=90)
    exit_button.place(x=17, y=410)
    task_listbox = Listbox(functions_frame, width=70, height=10, font=("Segoe UI", 12),
                           selectmode='SINGLE', bg="#1f1f2e", fg="white",
                           selectbackground="#00cec9", selectforeground="black", relief=FLAT, bd=1)
    task_listbox.place(x=17, y=150)

   
    task_count_label = Label(functions_frame, text="Total Tasks: 0", font=("Segoe UI", 12),
                             bg="#2c2c3e", fg="#F6BE00")
    task_count_label.place(x=17, y=375)

    retrieve_database()
    list_update()

    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()
