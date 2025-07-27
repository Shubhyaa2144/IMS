from tkinter import *
from PIL import ImageTk
from tkinter import messagebox, Toplevel
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import random
import logging

SMTP_SERVER = "sandbox.smtp.mailtrap.io"
PORT = 2525
USERNAME = "5226bf679f8ea9"  # Replace with your Mailtrap username
PASSWORD = "0d1cee232eb975"  # Replace with your Mailtrap password

# Configure logging
logging.basicConfig(level=logging.INFO)

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System | Developed By Shubham")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        self.otp = None
        self.otp_expiry = None  
        
        # Images
        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phone_image = Label(self.root, image=self.phone_image, bd=0).place(x=200, y=50)

        # Login Frame
        self.employee_id = StringVar()
        self.password = StringVar()
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="White")
        login_frame.place(x=650, y=90, width=350, height=460)

        title = Label(login_frame, text="Login System", font=("Elephant", 30, "bold"), bg="white").place(x=0, y=30, relwidth=1)
        lbl_user = Label(login_frame, text="Employee ID", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=100)
        txt_username = Entry(login_frame, textvariable=self.employee_id, font=("times new roman", 15), bg="#ECECEC").place(x=50, y=140, width=250)
        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=200)
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="#ECECEC").place(x=50, y=240, width=250)
        btn_login = Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2").place(x=50, y=300, width=250, height=35)

        hr = Label(login_frame, bg="lightgray").place(x=50, y=370, width=250, height=2)
        hr = Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold")).place(x=150, y=355)

        btn_forget = Button(login_frame, text="Forget Password?", command=self.forget_window, font=("times new roman", 13, "bold"), bg="white", fg="#00759E", activebackground="white", activeforeground="#00759E", bd=0).place(x=100, y=400)

        # Subscribe Frame
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="White")
        register_frame.place(x=650, y=570, width=350, height=60)
        lbl_reg = Label(register_frame, text="SUBSCRIBE | LIKE | SHARE", font=("times new roman", 13), bg="white").place(x=0, y=20, relwidth=1)

        # Image Animation for visual effect
        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image = Label(self.root, bg="white")
        self.lbl_change_image.place(x=367, y=153, width=240, height=428)

        self.animate()

        # Initializing OTP and password variables
        self.var_otp = StringVar()
        self.var_new_pass = StringVar()
        self.var_conf_pass = StringVar()

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror('Error', "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT utype FROM employee WHERE eid=? AND pass=?", (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror('Error', "Invalid USERNAME/PASSWORD", parent=self.root)
                else:
                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def forget_window(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "":
                messagebox.showerror('Error', "Employee ID must be required", parent=self.root)
                return

            cur.execute("SELECT email FROM employee WHERE eid=?", (self.employee_id.get(),))
            email = cur.fetchone()

            if email is None:
                messagebox.showerror('Error', "Invalid Employee ID, try again", parent=self.root)
                return

            receiver_email = email[0]

            # Generate OTP and send it via email
            otp = self.generate_otp()
            self.send_otp_email(receiver_email, otp)

            # Log OTP sent
            logging.info(f"OTP sent to {receiver_email} for password reset.")

            # Create the Reset Password window
            self.create_reset_password_window()

        except sqlite3.DatabaseError as db_error:
            logging.error(f"Database error: {str(db_error)}")
            messagebox.showerror("Error", f"Database error: {str(db_error)}", parent=self.root)

        except Exception as ex:
            logging.error(f"Error occurred: {str(ex)}")
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def create_reset_password_window(self):
        self.forget_win = Toplevel(self.root)
        self.forget_win.title('RESET PASSWORD')
        self.forget_win.geometry('450x390+500+100')
        self.forget_win.focus_force()

        # Window title
        title = Label(self.forget_win, text='Reset Password', font=('goudy old style', 15, 'bold'), bg="#3f51b5", fg="white")
        title.pack(side=TOP, fill=X)

        # OTP Entry
        lbl_reset = Label(self.forget_win, text="Enter OTP Sent on Registered Email", font=("times new roman", 15))
        lbl_reset.pack(pady=10)
        txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15), bg="lightyellow")
        txt_reset.pack(pady=10, padx=20, fill=X)

        self.btn_reset = Button(self.forget_win, text="SUBMIT", font=("times new roman", 15), bg="lightblue", command=self.verify_otp)
        self.btn_reset.pack(pady=10)

        # New Password Fields
        lbl_new_pass = Label(self.forget_win, text="New Password", font=("times new roman", 15))
        lbl_new_pass.pack(pady=5)
        txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, font=("times new roman", 15), bg="lightyellow")
        txt_new_pass.pack(pady=5, padx=20, fill=X)

        lbl_c_pass = Label(self.forget_win, text="Confirm Password", font=("times new roman", 15))
        lbl_c_pass.pack(pady=5)
        txt_c_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, font=("times new roman", 15), bg="lightyellow")
        txt_c_pass.pack(pady=5, padx=20, fill=X)

        self.btn_update = Button(self.forget_win, text="Update", font=("times new roman", 15), bg="lightblue", command=self.update_password)
        self.btn_update.pack(pady=20)

    def generate_otp(self):
        otp = str(random.randint(100000, 999999))
        self.otp = otp
        self.otp_expiry = time.time() + 300  # OTP expires in 5 minutes
        return otp

   

    def send_otp_email(self, receiver_email, otp):
        sender_email = "your_email@example.com"  # Replace with your sender email
        subject = "Your OTP Code"
        body = f"Your login OTP is: {otp}"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            # Connect to the SMTP server
            with smtplib.SMTP(SMTP_SERVER, PORT) as server:
                server.starttls()  # Secure the connection
                server.login(USERNAME, PASSWORD)
                server.sendmail(sender_email, receiver_email, message.as_string())
                logging.info(f"OTP successfully sent to {receiver_email}")
        except smtplib.SMTPAuthenticationError:
            logging.error("Authentication failed when trying to send OTP.")
            messagebox.showerror("Email Error", "Failed to authenticate with the email server. Please check your credentials.", parent=self.root)
        except smtplib.SMTPException as e:
            logging.error(f"Failed to send OTP to {receiver_email}: {str(e)}")
            messagebox.showerror("Email Error", f"Failed to send OTP: {e}", parent=self.root)
        except Exception as ex:
            logging.error(f"An unexpected error occurred while sending OTP: {str(ex)}")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(ex)}", parent=self.root)

    def verify_otp(self):
        entered_otp = self.var_otp.get()
        
        # Check if OTP has expired
        if time.time() > self.otp_expiry:
            messagebox.showerror("Error", "OTP has expired.")
            return

        if entered_otp == self.otp:
            logging.info("OTP verified successfully.")
            self.enable_password_update()
        else:
            logging.error("Invalid OTP entered.")
            messagebox.showerror("Error", "Invalid OTP entered.")

    def update_password(self):
        new_password = self.var_new_pass.get()
        confirm_password = self.var_conf_pass.get()

        if new_password == confirm_password:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()

            try:
                cur.execute("UPDATE employee SET pass=? WHERE eid=?", (new_password, self.employee_id.get()))
                con.commit()
                logging.info(f"Password for employee ID {self.employee_id.get()} updated successfully.")
                messagebox.showinfo("Success", "Password updated successfully.", parent=self.forget_win)
                self.forget_win.destroy()  # Close the reset window
            except Exception as ex:
                logging.error(f"Error updating password: {str(ex)}")
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.forget_win)
            finally:
                con.close()
root = Tk()
obj = Login_System(root)
root.mainloop()