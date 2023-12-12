import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import tkinter as tk

# Using service account to connect to cloud db
cred = credentials.Certificate(r"C:\Users\alext\OneDrive\Documents\BYUI\Junior\cse310\Sprint6\todolist-8f647-c6da598b8c29.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Initializing data to db
l = 'List'
items = db.collection(l)

# item1 = {'Item': 'Finish Module 6 for CSE310', 'By': '12/13/23', 'Done': False}
# item2 = {'Item': 'Complete a load and put away laundry', 'By': '12/12/23', 'Done': False}
# items.document('Module 6').set(item1)
# items.document('Laundry').set(item2)

# Initializing tkinter window
win = tk.Tk()
win.title("To Do List")
item_frame = tk.Frame()
item_frame.grid(column=0, padx=30)

add_frame = tk.Frame()
add_frame.grid(column = 1, row=0, pady=20)

complete_frame = tk.Frame()
complete_frame.grid(column=1, row=1, pady=20)

delete_frame = tk.Frame()
delete_frame.grid(column=1, row=2, pady=20)

# Displaying all items in list
def display(doc, item_dict, color):
    tk.Label(master=item_frame, fg=color, text=f"{doc.id}: \n{item_dict['Item']}.\nComplete by {item_dict['By']}\nFinished? {'No' if item_dict['Done'] == False else 'Yes'}", justify='left').pack(anchor='w')

def refresh():
    for w in item_frame.winfo_children():
        w.destroy()
    items_list = []
    for doc in items.stream():
        item_dict = doc.to_dict()
        if item_dict['Done'] == False:
            display(doc, item_dict, 'red')
        else:
            display(doc, item_dict, 'green')
        items_list.append(doc.id)  
refresh()

# Labels and entry boxes to add new item
tk.Label(master=add_frame, text="Add new item").pack()
tk.Label(master=add_frame, text='New Item: ').pack()
new = tk.Entry(master=add_frame)
new.pack()

tk.Label(master=add_frame, text='Description: ').pack()
new_des = tk.Entry(master=add_frame)
new_des.pack()

tk.Label(master=add_frame, text='Complete by: ').pack()
new_by = tk.Entry(master=add_frame)
new_by.pack()

# Adding item to cloud db and displaying it to window
def add_item():
    item_name = new.get()
    item_des = new_des.get()
    item_by = new_by.get()
    if item_name == '' or item_by == '' or item_des == '':
        return 1
    
    doc = items.document(item_name)
    doc.set({'Item': item_des, 'By': item_by, 'Done': False})
    item_dict = doc.get().to_dict()
    tk.Label(master=item_frame, text=f"{doc.id}: \n{item_dict['Item']}.\nComplete by {item_dict['By']}\nFinished? {'No' if item_dict['Done'] == False else 'Yes'}", justify='left').pack(anchor='w')

    new.delete(0, tk.END)
    new_des.delete(0, tk.END)
    new_by.delete(0, tk.END)

add_button = tk.Button(master=add_frame, text='Add', command=add_item)
add_button.pack()

# Delete button
def delete():
    item = delete_entry.get()
    items.document(item).delete()
    delete_entry.delete(0, tk.END)
    refresh()

tk.Label(master=delete_frame, text='Delete Item').pack()

delete_entry = tk.Entry(master=delete_frame)
delete_entry.pack()
delete_btn = tk.Button(master=delete_frame, text='Delete', command=delete)
delete_btn.pack()

# Complete Task
def complete():
    item = complete_entry.get()
    items.document(item).update({'Done': True})
    complete_entry.delete(0, tk.END)
    refresh()

tk.Label(master=complete_frame, text='Complete Task').pack()

complete_entry = tk.Entry(master=complete_frame)
complete_entry.pack()
complete_btn = tk.Button(master=complete_frame, text='Complete', command=complete)
complete_btn.pack()

win.mainloop()