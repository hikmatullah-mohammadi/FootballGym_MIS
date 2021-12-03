import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import sqlite3
import re
import random
import string

def create_root(x, y):
    global root
    root = tk.Tk()
    root.geometry(f'775x400+{x}+{y}')
    root.resizable(False, False)
    root.config(bg='#ff0080')

# '#ff0080'

# data base
class Database:
    def __init__(self):
        # create a connection
        self.conn = sqlite3.connect('gym.db')
        # create a cursor
        self.cursor = self.conn.cursor()
        # create customers table


        # self.cursor.execute('''CREATE TABLE customers
        #                     (name text,
        #                     ph_number text,
        #                     address text,
        #                     team_a text,
        #                     team_b text,
        #                     date text,
        #                     timing text,
        #                     payment integer
        #                     )
        #                     ''')

    # insert new records
    def insert_record(self, name, ph_number, address, team_a, team_b, date, timing, payment):
        self.cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
                            , (name, ph_number, address, team_a, team_b, date, timing, payment))
        self.conn.commit()


    def delete_record(self, id):
        self.cursor.execute('DELETE FROM customers WHERE rowid=?', (id, ))
        self.conn.commit()

    def all_records(self):
        self.cursor.execute('select * from customers')
        return self.cursor.fetchall()

# times
ALL_TIMES = [
            '12:00-01:00 - AM',
            '01:00-02:00 - AM',
            '02:00-03:00 - AM',
            '03:00-40:00 - AM',
            '04:00-05:00 - AM',
            '05:00-06:00 - AM',
            '06:00-07:00 - AM',
            '07:00-08:00 - AM',
            '08:00-09:00 - AM',
            '09:00-10:00 - AM',
            '10:00-11:00 - AM',
            '11:00-12:00 - AM',
            '12:00-01:00 - PM',
            '01:00-02:00 - PM',
            '02:00-03:00 - PM',
            '03:00-04:00 - PM',
            '04:00-05:00 - PM',
            '05:00-06:00 - PM',
            '06:00-07:00 - PM',
            '07:00-08:00 - PM',
            '08:00-09:00 - PM',
            '09:00-10:00 - PM',
            '10:00-11:00 - PM',
            '11:00-12:00 - PM',
    ]


# functions
def show_home():
    global form_frame
    
    
    try:
        form_frame.place_forget()
    except:
        pass
    try:
        srch_frame.place_forget()
        dlt_record_btn.place_forget()
    except:
        pass

    # form frame
    form_frame = tk.Frame(root, bd=2, relief='sunken', bg='#ff0080')

    form_frame.place(x=200, y=140, height=200, width=500)
    time_lb = tk.Label(form_frame, text="", font=('courier', 25), bg='#ff0080', fg='white') # bg='#8FFF28'
    time_lb.pack()

    h = time.strftime('%I')
    date = f"{str(int(time.strftime('%d')))}, {time.strftime('%m')}, {time.strftime('%y')}"
    a = Database()

    a.cursor.execute('SELECT team_a, team_b FROM customers WHERE timing LIKE ? and date=?', (h+':%', date))
    current = a.cursor.fetchall()
    if current != []:
        current = current[0]
    else:
        current = ('....', '....')
    get_time(time_lb, current)


def get_time(time_lb, current):
    h = time.strftime('%I')
    m = time.strftime('%M')
    s = time.strftime('%S'+' %p')
    y = time.strftime('%Y')

    date = time.strftime('%d')
    day_name = time.strftime('%A')
    month_name = time.strftime('%h')

    tm = f'{day_name}, {date}, {month_name}, {y}\n{h}:{m}:{s}\n\n{current[0]} VS {current[1]}'
    time_lb.config(text=tm)
    time_lb.after(100, lambda: get_time(time_lb, current))


# define a function to display the form to add new record
def add_new_frame():
    global form_frame

    form_frame.place_forget()
    try:
        srch_frame.place_forget()
        dlt_record_btn.place_forget()
    except:
        pass

    # form frame
    form_frame = tk.Frame(root, bd=2, relief='sunken', bg='#ff0080')
    form_frame.place(x=200, y=120, height=250, width=350)

    tk.Label(form_frame, text='Customer Reg', relief='sunken', bg='#ff0080', font=('', 12,'bold')).grid(row=0, column=0, columnspan=3, sticky='ew')
    lbs= ['Name', 'PH Number', 'Address', 'Team A', 'Team B', 'Date\tTime', 'Payment']

    for i in lbs:
        tk.Label(form_frame, text=i, relief='sunken', bg='#ff0080').grid(row=lbs.index(i)+1, column=0, padx=15, pady=3, sticky='ew')

    # entries to get new customers' properties
    name_ent = tk.Entry(form_frame, width=40)
    ph_ent = tk.Entry(form_frame, width=40)
    address_ent = tk.Entry(form_frame, width=40)
    team_a_ent = tk.Entry(form_frame, width=40)
    team_b_ent = tk.Entry(form_frame, width=40)
    payment_ent = tk.Entry(form_frame, width=40)


    # get times which has not been reserved yet
    def get_availible_timing(times):
        updated_times = []    
        a = Database()
        recs = a.all_records()
        # ==== d, m, y
        try:
            date_formatted = f"{day_var.get()}, {time.strftime('%m')}, {time.strftime('%y')}"
        except:
            date_formatted = f"{str(int(time.strftime('%d')))}, {time.strftime('%m')}, {time.strftime('%y')}"

        for i in times:
            for j in recs:
                
                if i == j[6] and date_formatted == j[5]:
                    break
            else:
                updated_times.append(i)
        return updated_times

    def fresh_times(e):
        global time_var
        times = get_availible_timing(ALL_TIMES)
        
        try:
            time_var = tk.StringVar()
            time_var.set(times[0])
            timing_ent = tk.OptionMenu(form_frame, time_var, *times)
            timing_ent.config(bg='#ff0080')
            timing_ent.grid(row=6, column=2, padx=15)
        except:
            pass

    fresh_times(None)
    
    # dates to put into option menu
    days = [day for day in range(int(time.strftime('%d')), 31)]
    
    
    day_var = tk.StringVar()
    day_var.set(days[0])
    date_ent = tk.OptionMenu(form_frame, day_var, *days, command=fresh_times)
    date_ent.config(bg='#ff0080')

    
    name_ent.grid(row=1, column=1, padx=15, columnspan=2)
    ph_ent.grid(row=2, column=1, padx=15, columnspan=2)
    address_ent.grid(row=3, column=1, padx=15, columnspan=2)
    team_a_ent.grid(row=4, column=1, padx=15, columnspan=2)
    team_b_ent.grid(row=5, column=1, padx=15, columnspan=2)
    date_ent.grid(row=6, column=1, padx=15)
    
    payment_ent.grid(row=7, column=1, padx=15, columnspan=2)


    # clear entries after getting values
    def clear_new_customer_entries():
        name_ent.delete(0, 'end')
        ph_ent.delete(0, 'end')
        address_ent.delete(0, 'end')
        team_a_ent.delete(0, 'end')
        team_b_ent.delete(0, 'end')
        # timing_ent.delete(0, 'end')
        payment_ent.delete(0, 'end')

    # define a function to insert new custmer into the database
    def add_new_record(name, ph_number, address, team_a, team_b, date, timing, payment):

        # phone number
        flag1 = False
        pattern1 = '^07[0-9]+'
        # payment
        flag2 = False
        pattern2 = '^[1-9][0-9]+'
        # name, address, teams' names
        flag3 = False
        pattern3 = '^[a-zA-Z]+'


        # make sure that the fields are filled
        if all((name, ph_number, address, team_a, team_b, date, timing, payment)):
            try:
                # validation --- ph-number, payment, name ...
                if len(ph_number)==10 and len(re.findall(pattern1, ph_number)[0])==10:
                    flag1 = True
                if len(re.findall(pattern2, payment)[0])==len(payment):
                    flag2 = True
                if re.search(pattern3, name) and re.search(pattern3, team_a) and re.search(pattern3, team_b)\
                    and re.search(pattern3, address):
                    flag3 = True
            except:
                pass

            # make sure that entered values are valid
            if all((flag1, flag2, flag3)):
                
                date_formatted = f"{date}, {time.strftime('%m')}, {time.strftime('%y')}"
                # date_formatted = date 
                db = Database()
        
                # add the record into the database
                db.insert_record(name, ph_number, address, team_a, team_b, date_formatted, timing, payment)
                clear_new_customer_entries()
                messagebox.showinfo('Info', 'Added!')        
                add_new_frame()
            
            # if any data entered is not valid
            else:
                # if phone number is not valid
                if not flag1:
                    messagebox.showerror('Error', 'PH number should be like 07xxxxxxxx')
                # If payment is not valid
                elif not flag2:
                    messagebox.showerror('Error', 'INVALID PAYMENT!')
                # if name and/or ....  is/are not valid
                elif not flag3:
                    messagebox.showerror('Error', '''The Name, the Teams' names and the Address
                         should start with a letter.''')
                else:
                    pass

        # if any field is vacant
        else:
            messagebox.showerror('Error', 'The fields can\'t be empty')

    # clear all entries
    clear_btn = tk.Button(form_frame, text='Clear', bd=2, relief='sunken', command=clear_new_customer_entries)
    clear_btn.grid(row=8, column=1)

    # Button to add new record into the database
    add_btn = tk.Button(form_frame, text='Add', bd=2, relief='sunken',\
                        command=lambda: add_new_record(name_ent.get(), \
                                        ph_ent.get(), address_ent.get(),\
                                        team_a_ent.get(), team_b_ent.get(),\
                                        day_var.get(), time_var.get()\
                                        , payment_ent.get()))
    add_btn.grid(row=8, column=2, sticky='ew')


# Define a function to display teams
def show_records():
    global form_frame, dlt_record_btn, srch_frame
    form_frame.place_forget()

    try:
        srch_frame.place_forget()
        dlt_record_btn.place_forget()
    except:
        pass
    
    # form frame
    form_frame = tk.Frame(root, bd=2, relief='sunken', bg='#ff0080')
    form_frame.place(x=150, y=140, height=200, width=600)

    
    # define a scrollbar to scroll the tree
    scrollBar = tk.Scrollbar(form_frame, bg='#ff0080')
    scrollBar.pack(side='right', fill='y')


    # define a style for tree
    style = ttk.Style()
    style.theme_use('default')
    style.configure('Treeview',
                    background='#ff0080',
                    fieldbackground='#ff0080'
                    )
    style.map('Treeview', background=[('selected', 'blue')])

    # define a treeview to display records
    my_tree = ttk.Treeview(form_frame, yscrollcommand=scrollBar.set)
    my_tree['columns'] = ('Name', 'PH Num', 'Address', 'Team A', 'Team B', 'Date', 'Time', 'Payment')
    my_tree.pack(side='left')

    # set a command for scrollbar
    scrollBar.config(command=my_tree.yview)

    # add colums
    my_tree.column('#0', width=0, stretch='no')
    my_tree.column('Name', width=70, minwidth=50)
    my_tree.column('PH Num', width=80, minwidth=50)
    my_tree.column('Address', width=80, minwidth=50)
    my_tree.column('Team A', width=55, minwidth=50)
    my_tree.column('Team B', width=55, minwidth=50)
    my_tree.column('Date', width=60, minwidth=50)
    my_tree.column('Time', width=100, minwidth=50)
    my_tree.column('Payment', width=80, minwidth=50)


    # and Heading
    my_tree.heading('#0', text='')
    my_tree.heading('Name', text='Name')
    my_tree.heading('PH Num', text='PH Number')
    my_tree.heading('Address', text='Address')
    my_tree.heading('Team A', text='Team A')
    my_tree.heading('Team B', text='Team B')
    my_tree.heading('Date', text='d, m, y')
    my_tree.heading('Time', text='Time')
    my_tree.heading('Payment', text='Payment')


    # connect to the database
    db = Database()
    db.cursor.execute('SELECT rowid,* FROM customers')
    records = db.cursor.fetchall()

    # insert records
    for record in records:
        my_tree.insert(parent='', index='end', iid=record[0], values=record[1:])
    
    # Delete all the selected records from the database
    def delete_records():
        db = Database()
        recs = my_tree.selection()
        for record in recs:
            db.delete_record(record)
        
        # refresh the window
        search_record(None, srch_entry.get())
    

    # search a record by name in the database
    def search_record(event, query):
        # clean the treeview
        for record in my_tree.get_children():
            my_tree.delete(record)
        
        try:
            # get the current character as well
            if event.char !='??' and not event.keycode in [9, 20, 13, 8]:
                query = query + event.char
            
            # if Backspace is pressed 
            elif event.keycode == 8:
                query = query[:-1]
        except:
            pass

        # connect to the database
        db = Database()
        db.cursor.execute('SELECT rowid,* FROM customers where name LIKE ?', (query+'%', ))
        records = db.cursor.fetchall()

        # insert records
        for record in records:
            my_tree.insert(parent='', index='end', iid=record[0], values=record[1:])

    # define delete button
    dlt_record_btn = tk.Button(root, text='Delete', command=delete_records)
    dlt_record_btn.place(x=705, y=340)

    # define a search bar
    srch_frame = tk.Frame(root)
    srch_frame.place(x=560, y=115)

    tk.Label(srch_frame, text='Search by Name', bg='#ff0080', fg='white').grid(row=0, column=0)
    srch_entry = tk.Entry(srch_frame, width=15)
    srch_entry.grid(row=0, column=1)

    # Search automatically when the user is entering the data
    srch_entry.bind('<Key>', lambda event: search_record(event, srch_entry.get())) 
    srch_entry.bind('<Button>', lambda event: search_record(event, srch_entry.get())) 


# define a function to get info
def show_info():
    global form_frame
    form_frame.place_forget()
    
    try:
        srch_frame.place_forget()
        dlt_record_btn.place_forget()
    except:
        pass

    # form frame
    form_frame = tk.LabelFrame(root, bd=2, relief='sunken', bg='#ff0080')
    form_frame.place(x=200, y=145, height=200, width=500)

    db = Database()
    all_recs = db.all_records()

    budget = 0
    number_of_team_played = 0
    for i in all_recs:
        budget += i[7]
    

    hour = time.strftime('%I')
    if int(hour)<9:
        current_timing = f'{hour}:00-0{int(hour)+1}:00 - {time.strftime("%p")}'
    elif int(hour)==12:
        current_timing = f'{hour}:00-01:00 - {time.strftime("%p")}'
    else:
        current_timing = f'{hour}:00-{int(hour)+1}:00 - {time.strftime("%p")}'
    
    current_date = f"{str(int(time.strftime('%d')))}, {time.strftime('%m')}, {time.strftime('%y')}"
    number_of_recs = len(all_recs)
   
   # 
    for i in all_recs:
        date, timing = i[5], i[6]
        if date == current_date and ALL_TIMES.index(timing) >= ALL_TIMES.index(current_timing):
            continue
        elif date > current_date:
            continue
        else:
            number_of_team_played += 1
    
    number_of_remained_teams = number_of_recs - number_of_team_played

    # number of all records
    tk.Label(form_frame, text = f'\nNumber of all records:', font=('Times New Roman', '18'), bg='#ff0080', fg='white').grid(row=0, column=0)
    tk.Label(form_frame, text = f'\n{number_of_recs}', font=('Times New Roman', '18'), bg='#ff0080', fg='white').grid(row=0, column=1)
    
    # number of teams remained
    tk.Label(form_frame, text = f'Remaining teams:', font=('Times New Roman', '18'), bg='#ff0080', fg='white').grid(row=1, column=0)
    tk.Label(form_frame, text = f'{number_of_remained_teams}', font=('Times New Roman', '18'), bg='#ff0080', fg='white').grid(row=1, column=1)

    # show the how many games have been played so far.
    tk.Label(form_frame, text = f'Games have been played:', font=('Times New Roman', '16'), bg='#ff0080', fg='white').grid(row=2, column=0, padx=80)
    tk.Label(form_frame, text = f'{number_of_team_played}', font=('Times New Roman', '16'), bg='#ff0080', fg='white').grid(row=2, column=1)

    # a Label to show how much have we earned so far
    tk.Label(form_frame, text = f'Budget(Afs):', font=('Times New Roman', '16'), bg='#ff0080', fg='white').grid(row=3, column=0)
    tk.Label(form_frame, text = f'{budget}', font=('Times New Roman', '16'), bg='#ff0080', fg='white').grid(row=3, column=1)



# HEADER FRAME
def display_title():
    
    # header frame
    header_frame = tk.Frame(root, bd=2, relief='sunken', bg='white')
    header_frame.grid(row=0, column=0, columnspan=10, padx=35, pady=30, ipadx=350, ipady=25)

    # create a label to display gym's name
    title = tk.Label(header_frame, text='Barcelona Gymnasium!', font=('courier', '20', 'bold'), bg='white')
    title.place(x=10, y=5)

    # move title right to left,  left to right
    colors = ['red', 'black', 'green', 'blue', 'orange', 'pink', 'silver', 'gold']

    def move_title(x, flag):

        title.config(fg=random.choice(colors))
        title.place(x=x, y=5)

        if x >= 350:
            flag = '<'
        elif x <= 10:
            flag = '>'

        if flag=='>':
            title.after(20, lambda: move_title(x=x+1, flag=flag))
        else:
            title.after(20, lambda: move_title(x=x-1, flag=flag))
    title.after(100, lambda: move_title(x=10, flag='>'))



# MENU FRAME
def display_menu_frame():
    
    # menu frame
    menu_frame = tk.Frame(root, bd=2, relief='sunken', bg='#ff0080')
    menu_frame.grid(row=1, column=0, padx=20, pady=30)

    # create home button
    home_btn = tk.Button(menu_frame, text='Home', command=show_home)
    home_btn.grid(row=0, column=0, pady=8, sticky='ew')

    # create add_new button
    book_btn = tk.Button(menu_frame, text='Book', command=add_new_frame)
    book_btn.grid(row=1, column=0, pady=8, sticky='ew')

    # create edit button
    record_btn = tk.Button(menu_frame, text='Records', command=show_records)
    record_btn.grid(row=2, column=0, pady=8, sticky='ew')

    # create sale button
    info_btn = tk.Button(menu_frame, text='Info', command=show_info)
    info_btn.grid(row=3, column=0, pady=8, sticky='ew')

    # create exit button
    exit_btn = tk.Button(menu_frame, text='Exit', command=root.destroy)
    exit_btn.grid(row=5, column=0, pady=8, sticky='ew')


def main(x, y):
    create_root(x, y)
    display_title()
    display_menu_frame()
    show_home()
    root.mainloop()

