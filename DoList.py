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
item_frame.pack(anchor='w')

# Displaying all items in list
items_list = []
for doc in items.stream():
    item_dict = doc.to_dict()
    tk.Label(master=item_frame, text=f"{doc.id}: \n{item_dict['Item']}.\nComplete by {item_dict['By']}\nFinished? {'No' if item_dict['Done'] == False else 'Yes'}", justify='left').pack(anchor='w')
    items_list.append(doc.id)  

# Labels and entry boxes to add new item
tk.Label(text="Add new item").pack()
tk.Label(text='New Item: ').pack()
new = tk.Entry()
new.pack()

tk.Label(text='Description: ').pack()
new_des = tk.Entry()
new_des.pack()

tk.Label(text='Complete by: ').pack()
new_by = tk.Entry()
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

add_button = tk.Button(text='Add', command=add_item)
add_button.pack()

# Delete buttons
def delete():
    item = delete_entry.get()
    items.document(item).delete()
    

delete_btn = tk.Button(text='Delete', command=delete)
delete_entry = tk.Entry()
delete_entry.pack()

win.mainloop()