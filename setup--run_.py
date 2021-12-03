import tkinter as tk
import re
import sqlite3
from tkinter import messagebox
import psw_encryption

class Authentication():
    def __init__(self, root):
        self.root = root
        self.root.title("Gym MIS")
        self.frame = tk.Frame(self.root, bd=2, relief='sunken', bg='#ff0080')
        self.frame.place(x=170, y=120, height=200, width=450)
        self.conn = sqlite3.connect('gym.db')
        self.cursor = self.conn.cursor()
        
        self.is_user_registered = False

        self.is_user_authenticated = False

        self.questions = [
            'Who is your first school/collage friend?',
            'What is your favorite color?',
            'Where were you born?',
            'Who is your best friend?',
            'What is your favorite sport?',
            'What is the best place you have ever been?',
            'Who do you love most?'
        ]

    def registerForm(self):

        self.frame.place_forget()
        self.frame = tk.Frame(self.root, bd=2, relief='sunken', bg='#ff0080')
        self.frame.place(x=170, y=120, height=200, width=450)

        tk.Label(self.frame, text='Registeration', font=('', '12', 'bold'), fg='white', bg='#ff0080').place(x=150, y=5)
        tk.Label(self.frame, text='Username ').place(x=100, y=55)
        un_entry = tk.Entry(self.frame)
        un_entry.place(x=200, y=55)
        
        tk.Label(self.frame, text='Password ').place(x=100, y=80)
        psw_entry = tk.Entry(self.frame)
        psw_entry.place(x=200, y=80)

        tk.Label(self.frame, text='Password again ').place(x=100, y=105)
        psw_again_entry = tk.Entry(self.frame)
        psw_again_entry.place(x=200, y=105)
        
        
        def security_q():
            
            self.frame.place_forget()
            self.frame = tk.Frame(self.root, bd=2, relief='sunken', bg='#ff0080')
            self.frame.place(x=170, y=120, height=200, width=450)
            
            tk.Label(self.frame, text='Security Questions', font=('', '12', 'bold'), fg='white', bg='#ff0080').place(x=150, y=5)

            q1_var = tk.StringVar()
            q1_var.set(self.questions[0])
            tk.OptionMenu(self.frame, q1_var, *self.questions).place(x=20, y=70)

            a1_entry = tk.Entry(self.frame, bd=5, relief='sunken')
            a1_entry.place(x=300, y=75)

            q2_var = tk.StringVar()
            q2_var.set(self.questions[1])
            tk.OptionMenu(self.frame, q2_var, *self.questions).place(x=20, y=100)

            a2_entry = tk.Entry(self.frame, bd=5, relief='sunken')
            a2_entry.place(x=300, y=105)

            def register(self, q1, a1, q2, a2):
                if all((a1, a2)): # if answers 1 and 2 are not empty

                    if len(a1) <=16 and len(a2) <= 16:
                        
                        # delete if there is any user
                        self.cursor.execute('delete from authentication')

                        # Encrypt record
                        encrypted_a1 = psw_encryption.encrypt(a1)
                        encrypted_a2 = psw_encryption.encrypt(a2)
                        encrypted_username = psw_encryption.encrypt(self.username_entered)
                        encrypted_psw = psw_encryption.encrypt(self.psw_entered)

                        # insert record into the database
                        record = (encrypted_username, encrypted_psw, q1, encrypted_a1, q2, encrypted_a2)
                        self.cursor.execute('insert into authentication values(?,?,?,?,?,?)',record)
                        self.conn.commit()
                        
                        self.loginForm()
                        messagebox.showinfo('Info!', 'Successfully registered.')
                    else:
                        messagebox.showerror('Error!', 'Your answers\' lengths cannot be more 16 characters!')

                else:
                    messagebox.showerror('Error!', 'Fields cannot be empty.')



            rsg_btn = tk.Button(self.frame, text='Register',\
                command=lambda: register(self, q1_var.get(), a1_entry.get(), q2_var.get(), a2_entry.get()))
            rsg_btn.place(x=300, y=140)

        # password validation
        def is_psw_valid(psw):
            if len(psw) >= 8 and len(psw) <= 16:
                if re.search('[0-9]', psw) and re.search('[a-z]', psw) and re.search('[A-Z]', psw):
                    return True
                else:
                    return False
            # if the password's length is not valid
            else:
                return False

        # after checking password validation, go to security questions
        def next_(un, psw, psw_again):
            
            if all((un, psw, psw_again)): # if all have something in them
                if psw == psw_again:

                    if is_psw_valid(psw):
                        self.username_entered = un
                        self.psw_entered = psw
                        self.frame.pack_forget()
                        security_q()
                    else:
                        messagebox.showerror('Error!', '''Password length should be 8 to 16 charecters.\n
                        It should consist of at least one number,\n
                        one uppercase letter and one lowercase letter.''')
                else:
                    messagebox.showerror('Error!', 'Passwords entered are not the same!')
            else:
                messagebox.showerror('Error!', 'fill out allf the fields.')


        next_btn = tk.Button(self.frame, text='Next', width=10,\
            command=lambda: next_(un_entry.get(), psw_entry.get(), psw_again_entry.get()))
        next_btn.place(x=300, y=150)
    
    def loginForm(self):

        self.frame.place_forget()
        self.frame = tk.Frame(self.root, bd=2, relief='sunken', bg='#ff0080')
        self.frame.place(x=170, y=120, height=200, width=450)

        tk.Label(self.frame, text='Login', font=('', '12', 'bold'), fg='white', bg='#ff0080').place(x=180, y=5)

        tk.Label(self.frame, text='Username ').place(x=100, y=55)
        un_entry = tk.Entry(self.frame)
        un_entry.place(x=180, y=55)

        tk.Label(self.frame, text='Password ').place(x=100, y=80)
        psw_entry = tk.Entry(self.frame, show='*')
        psw_entry.place(x=180, y=80) 

        def login(un, psw):
            # get the coordination points (x, y)
            x, y = self.root.geometry().split('+')[1:]
            

            if all((un, psw)):
                
                encrypted_un = psw_encryption.encrypt(un)
                encrypted_psw = psw_encryption.encrypt(psw)


                self.cursor.execute('select * from authentication')
                for i in self.cursor.fetchall():
                    if encrypted_un == i[0] and encrypted_psw == i[1]:
                        #
                        self.root.destroy()
                        
                        import GymMS
                        # call main function to start the app
                        GymMS.main(x, y)

                    else:
                        messagebox.showerror('Error!', 'Username or/and password is wrong.')
            else:
                messagebox.showerror('Error!', 'Fields cannot be empty!')

        login_btn = tk.Button(self.frame, text='Login', command=lambda: login(un_entry.get(), psw_entry.get()))
        login_btn.place(x=120, y=110)

        forgot_psw_btn = tk.Button(self.frame, text='Forgot Password.', command=self.resetPasswordForm)
        forgot_psw_btn.place(x=200, y=110)
    
    def resetPasswordForm(self):
        self.frame.place_forget()
        self.frame = tk.Frame(self.root, bd=2, relief='sunken', bg='#ff0080')
        self.frame.place(x=170, y=120, height=200, width=450)
    
        tk.Label(self.frame, text='Reset Password', font=('', '12', 'bold'), fg='white', bg='#ff0080').place(x=150, y=5)

        self.cursor.execute('select * from authentication')
        for i in self.cursor.fetchall():
            q1 = i[2]
            a1_db = i[3]
            q2 = i[4]
            a2_db = i[5]

        tk.Label(self.frame, text=q1).place(x=70, y=80)
        q1_entry = tk.Entry(self.frame)
        q1_entry.place(x=300, y=80)

        tk.Label(self.frame, text=q2).place(x=70, y=100)
        q2_entry = tk.Entry(self.frame)
        q2_entry.place(x=300, y=100)
        
        def reset(a1, a2):
            if all((a1, a2)): # a1 and a2 should not be empty
                
                encrypted_a1 = psw_encryption.encrypt(a1)
                encrypted_a2 = psw_encryption.encrypt(a2)

                if encrypted_a1 == a1_db and encrypted_a2 == a2_db:
                    self.registerForm()
                    messagebox.showinfo('Info!', 'You can change password')
                    
                else:
                    messagebox.showerror('Error', 'Wrong answers.')
            else:
                messagebox.showerror('Error!', 'Fields cannot be empty.')


        reset_btn = tk.Button(self.frame, text='ResetPassword',
                            command=lambda: reset(q1_entry.get(), q2_entry.get()))
        reset_btn.place(x=300, y=130)

    def start(self):
        if self.is_user_registered_(): # True or False
            self.loginForm()
        else:
            self.registerForm()
        

    # return True of False
    def is_user_authenticated_(self):
        return self.is_user_authenticated
    
    # return True of False
    # check if the any user is registered
    def is_user_registered_(self):
        self.cursor.execute('select * from authentication')
        if self.cursor.fetchall(): # if there is any record in it
            return True
        else:
            return False
    

def begin():
    
    root = tk.Tk()
    root.geometry('775x400+100+100') 
    root.resizable(False, False)
    root.config(bg='#ff0080')
    
    Authentication(root).start()
    root.mainloop()

#START
begin()
