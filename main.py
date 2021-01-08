# Importing Dependencies
from tkinter import *
from utils import db,security
from tkinter.font import Font
import string
import random

# Global State Variables
current_user = None
view_profile = None

# Shift Times
shift_times = [[7,15],[10,16],[11,19],[15,21],[15,23],[19,1],[20,2],[23,7]]

# Fonts
header_font = ("Segoe UI",15,"bold")
button_header_font = ("Segoe UI",10,"bold")
field_label_font = ("Segoe UI",10)
medium_font = ("Segoe UI",13,"bold")

# Theme
theme = ["#3c3c46","#42c0c7","#1e1e28"]

# Page Setup
class DesignProject(Tk):
  def __init__(self):
    Tk.__init__(self)
    Tk.title(self, "Design Project")
    Tk.geometry(self,"800x520")
    Tk.configure(self,bg=theme[0])
    self._frame = None
    self.switch_frame(HomePage)

  # Switches the frame
  def switch_frame(self, frame_class):
    new_frame = frame_class(self)
    if self._frame is not None:
      self._frame.destroy()
    self._frame = new_frame
    self._frame.pack(fill="x")

# Login Page
class LogIn(Frame):
  def __init__(self, master):
    global current_user
    Frame.__init__(self, master,bg=theme[0])
    current_user = None

    Button(self, text = "Register", bg=theme[1],fg="white",height=2,width=10,font=button_header_font,command = lambda: self.master.switch_frame(RegisterPage)).pack(side=RIGHT,anchor=NE, padx=10, pady=10)
    Button(self, text = "Home", bg=theme[1],fg="white",height=2,width=10,font=button_header_font,command = lambda: self.master.switch_frame(HomePage)).pack(side=RIGHT,anchor=NE, padx=5, pady=10)
    Label(self, text = "Login",bg=theme[0],fg="white",font=header_font).pack(fill="x", side=TOP, anchor=N,pady=15)

    self.anyErrors = Label(self, text = "",fg="red",bg=theme[0],font=field_label_font)
    self.anyErrors.pack(fill="x", side = TOP, anchor = N)

    Label(self, text = "Username",bg=theme[0],fg="white",font=field_label_font).pack(pady =3, padx = 10, side = TOP, anchor = N)
    self.usernameEntry = Entry(self)
    self.usernameEntry.pack(pady =3, padx = 10, side = TOP, anchor = N)

    Label(self, text = "Password",bg=theme[0],fg="white",font=field_label_font).pack(pady =3, padx = 10, side = TOP, anchor  = N)
    self.passwordEntry = Entry(self, show ="*")
    self.passwordEntry.pack(pady =3, padx = 10, side = TOP, anchor  = N)

    logInButton = Button(self, text = "Enter",fg="white",bg=theme[1],command = self.LogInCheck)
    logInButton.pack(side = TOP, anchor = S)

  # Authenticates user
  def LogInCheck(self):
    global current_user
    try:
      user = db.get_user(self.usernameEntry.get())
      if "message" in user:
        self.anyErrors["text"] = user["message"]
      else:
        if security.check_password(self.passwordEntry.get(), user["p"]):
          current_user = user
          self.master.switch_frame(HomePage)
        else:
          self.anyErrors["text"] = "Invalid password"
    except Exception as e:
      print(e)
      self.anyErrors["text"] = "Something went wrong"

# Register Page
class RegisterPage(Frame):
  
  def __init__(self, master):
    global current_user
    global theme
    Frame.__init__(self, master,bg=theme[0])
    current_user = None
    Button(self, text = "Login", bg=theme[1],fg="white",height=2,width=10,font=button_header_font,command = lambda: self.master.switch_frame(LogIn)).pack(side=RIGHT,anchor=NE, padx=10, pady=10)
    Button(self, text = "Home", bg=theme[1],fg="white",height=2,width=10,font=button_header_font,command = lambda: self.master.switch_frame(HomePage)).pack(side=RIGHT,anchor=NE, padx=5, pady=10)
    Label(self, text = "Register",bg=theme[0],fg="white",font=header_font).pack(fill="x", side=TOP, anchor=N, pady=15)

    self.anyErrors = Label(self, text = "",fg="red",bg=theme[0],font=field_label_font)
    self.anyErrors.pack(fill="x", side = TOP, anchor = N)

    Label(self, text = "Username",bg=theme[0],fg="white",font=field_label_font).pack(pady =3, padx = 10, side = TOP, anchor = N)
    self.usernameEntry = Entry(self)
    self.usernameEntry.pack(pady =3, padx = 10, side = TOP, anchor = N)
    
    Label(self, text = "Password",bg=theme[0],fg="white",font=field_label_font).pack(pady =3, padx = 10, side = TOP, anchor  = N)
    self.passwordEntry = Entry(self, show ="*")
    self.passwordEntry.pack(pady =3, padx = 10, side = TOP, anchor  = N)

    Button(self, text = "Enter",fg="white",bg=theme[1],command = self.RegisterCheck).pack(side = TOP, anchor = S)
  
  # Authenticates and registers the user
  def RegisterCheck(self):
    global current_user
    try:
      user = db.register_user(self.usernameEntry.get(),self.passwordEntry.get())
      if "message" in user:
        self.anyErrors["text"] = user["message"]
      else:
        current_user = user
        self.master.switch_frame(HomePage)
    except Exception as e:
      print(e)
      self.anyErrors["text"] = "Something went wrong"

# Home Page
class HomePage(Frame):
  def __init__(self, master):
    global current_user
    Frame.__init__(self, master,bg=theme[0])
    if current_user is None:
      Button(self, text = "Register", bg=theme[1],fg="white",height=2,width=10,font=button_header_font,command = lambda: self.master.switch_frame(RegisterPage)).pack(side=RIGHT,anchor=NE, padx=10, pady=10)
      Button(self, text = "Login", bg=theme[1],fg="white",height=2,width=10,font=button_header_font,command = lambda: self.master.switch_frame(LogIn)).pack(side=RIGHT,anchor=NE, padx=5, pady=10)
      Label(self, text = "Home Page",bg=theme[0],fg="white",font=header_font).pack(fill="x", side=TOP, anchor=N, pady=15)
    else:
      name = current_user["_id"]
      Button(self, text="Logout",fg="white", bg=theme[1],height=2,width=10,font=button_header_font,command=lambda: self.master.switch_frame(LogIn)).pack(side=RIGHT,anchor=NE, padx=10, pady=10)
      if current_user["h"] == []:
        Label(self, text=f"Welcome {name}",bg=theme[0],fg="white",font=header_font).pack(fill="x", side=TOP,anchor=N, pady=15)
        Label(self, text="You are not a in a hospital",bg=theme[0],fg="white").pack(pady=10, padx=10)
        Button(self, text="Create",bg="#ffb300",height=1,width=15,command=lambda: self.master.switch_frame(CreateHospital)).pack(side=TOP,anchor=N)
        Button(self, text="Join",bg="#ffb300",height=1,width=15,command=lambda: self.master.switch_frame(JoinHospital)).pack(side=TOP,anchor=N)
      else:
        Button(self, text="Shifts",fg="white", bg=theme[1], height=2,width=10,font=button_header_font,command=lambda: self.master.switch_frame(ShiftSelector)).pack(side=RIGHT,anchor=NE,pady=10)
        self.hd = db.get_hospital(current_user["h"][0])
        if self.hd["u"][current_user["_id"]]["r"] == 1:
          Label(self, text=f"Welcome {name}",bg=theme[0],fg="white",font=header_font).pack(fill="x", side=TOP,anchor=N, pady=15)
          joincode = self.hd["join"]
          Label(self, text=f"Join Code:",bg=theme[0],fg="white",font=field_label_font).pack(side=TOP,anchor=N)
          self.joinfield = Text(self, height=1, borderwidth=0, width=11,bg=theme[0],fg="white")
          self.joinfield.insert(1.0, joincode)
          self.joinfield.pack(side=TOP,anchor=N)
          Label(self, text=f"Users",bg=theme[0],fg="white",font=header_font).pack(side=TOP,anchor=N,pady=10)
          def view_user_profile(user):
            global view_profile
            view_profile = user
            self.master.switch_frame(ProfilePage)
          for place,user in enumerate(self.hd["u"],start=1):
            Button(self,text=f"{place}. {user}",bg="#ffb300",height=2,width=15,command=lambda user=self.hd["u"][user]: view_user_profile(user)).pack(side=TOP,anchor=N)
          Label(self, text=f"Admin Controls",bg=theme[0],fg="white",font=header_font).pack(side=TOP,anchor=N,pady=10)
          self.join_changing = Button(self,text=f"Joining", bg="#ffb300",height=2,width=25,fg="white",font=button_header_font,command=lambda: self.update_hospital_settings("can_join"))
          self.join_changing.pack(side=TOP,anchor=N,pady=3)
          self.schedule_changing = Button(self,text=f"Schedule Changing", bg="#ffb300",height=2,width=25,fg="white",font=button_header_font,command=lambda: self.update_hospital_settings("can_change"))
          self.schedule_changing.pack(side=TOP,anchor=N,pady=3)
          Button(self,text="Change Join Code", bg="#ffb300",height=2,width=25,fg="white",font=button_header_font,command=lambda: self.change_join_code()).pack(side=TOP,anchor=N,pady=5)
          self.update_button_colours()
        else:
          Label(self, text=f"Welcome {name}",bg=theme[0],fg="white",font=header_font).pack(fill="x", side=TOP,anchor=N, pady=15)
  def update_button_colours(self):
    self.schedule_changing.configure(bg="green" if self.hd["can_change"] else "red")
    self.join_changing.configure(bg="green" if self.hd["can_join"] else "red")
  def update_hospital_settings(self,stat):
    db.update_hospital(self.hd["_id"],stat,(a := not self.hd[stat]))
    self.hd[stat] = a
    self.update_button_colours()
  def change_join_code(self):
    newcode = "".join(random.choice(string.ascii_letters) for i in range(10))
    self.joinfield.delete(1.0,END)
    self.joinfield.insert(1.0, newcode)
    db.update_hospital(self.hd["_id"],"join",newcode)

# Profile Page
class ProfilePage(Frame):
  def __init__(self, master):
    global view_profile
    Frame.__init__(self, master,bg=theme[0])
    name = view_profile["u"]
    shifts = ""
    for s in view_profile["s"]:
      shifts += f"{s}\n"
    role = "doctor" if view_profile["r"] == 0 else "admin"
    Button(self, text="Logout", bg=theme[1],fg="white", height=2,width=10,font=button_header_font,command=lambda: self.master.switch_frame(LogIn)).pack(side=RIGHT,anchor=NE, padx=10, pady=10)
    Button(self, text="Home", bg=theme[1],fg="white", height=2,width=10,font=button_header_font,command=lambda: self.master.switch_frame(HomePage)).pack(side=RIGHT,anchor=NE, pady=10)
    Label(self, text=f"{name}'s Profile",bg=theme[0],fg="white",font=header_font).pack(fill="x", side=TOP,anchor=N, pady=15)
    Label(self, text=f"Schedule Data",bg=theme[0],fg="white",font=button_header_font).pack(side=TOP,anchor=N)
    Label(self, text=f"{shifts}",bg=theme[0],fg="white",font=field_label_font).pack(side=TOP,anchor=N)
    Label(self, text=f"Role: {role}",bg=theme[0],fg="white",font=button_header_font).pack(side=TOP,anchor=N)

# Shift Selector Page
class ShiftSelector(Frame):
  def __init__(self, master):
    global current_user
    Frame.__init__(self, master,bg=theme[0])
    Button(self, text="Logout", bg=theme[1],fg="white",height=2,width=10,font=button_header_font,command=lambda: self.master.switch_frame(LogIn)).pack(side=RIGHT,anchor=NE, padx=10, pady=10)
    Button(self, text="Home", bg=theme[1],fg="white",height=2,width=10,font=button_header_font,command=lambda: self.master.switch_frame(HomePage)).pack(side=RIGHT,anchor=NE, pady=10)
    Label(self, text = "Shift Selector",bg=theme[0],fg="white",font=header_font).pack(fill="x", side=TOP, anchor=N, pady=15)
    Button(self, text="Save",fg="white",width=10,font=button_header_font,bg=theme[1],command=lambda: self.save_schedule()).pack(side=BOTTOM,anchor=SE)
    Button(self, text="Next Day",fg="white",width=10,font=button_header_font,bg=theme[1],command=lambda: self.change_day()).pack(side=BOTTOM,anchor=SE)
    self.day_number = 1
    self.user_schedule = a if (a := db.get_hospital(current_user["h"][0])["u"][current_user["_id"]]["s"]) != [] else []
    self.schedulecolours = ["#ed5555","#ede555","#777877","#55ed5f"]
    self.schedule_legend = ["No","Not Prefered", "Neutral", "Yes"]
    self.schedule_buttons = []
    for s in range(len(self.schedulecolours)):
      Label(self,text=f"{self.schedule_legend[s]}", fg=self.schedulecolours[s],bg="#1e1e28",font=button_header_font,width=20).pack(side=TOP,anchor=N)
    self.day_name = Label(self,text=f"Day {self.day_number}",bg=theme[0],fg="white",font=medium_font)
    self.day_name.pack(side=TOP,anchor=N,pady=10)
    for i in range(len(shift_times)):
      shift = " - ".join(str(x) for x in shift_times[i])
      self.schedule_buttons.append(a := Button(self, text=f"{shift}" ,bg=self.schedulecolours[self.user_schedule[self.day_number-1][i]],height=1,width=20,font=button_header_font,command=lambda i=i: self.change_schedule(i)))
      a.pack(side=TOP,anchor=N)
      
  # Updates single button colour
  def update_single_button_colour(self,i):
    self.schedule_buttons[i].configure(bg=self.schedulecolours[self.user_schedule[self.day_number-1][i]])

  def update_all_buttons(self):
    for i in range(len(shift_times)):
      self.schedule_buttons[i].configure(bg=self.schedulecolours[self.user_schedule[self.day_number-1][i]])

  def change_day(self):
    if self.day_number >= 7:
      self.day_number = 1
    else:
      self.day_number += 1
    self.update_all_buttons()
    self.day_name["text"] = f"Day {self.day_number}"

  # Change schedule locally
  def change_schedule(self,i):
    if self.user_schedule[self.day_number-1][i] >= 3:
      self.user_schedule[self.day_number-1][i] = 0
    else:
      self.user_schedule[self.day_number-1][i] += 1
    self.update_single_button_colour(i)

  # Change save schedule to user model
  def save_schedule(self):
    resp = db.update_schedule(current_user["h"][0],current_user["_id"],self.user_schedule)
    self.master.switch_frame(HomePage)

# Create Hospital Page
class CreateHospital(Frame):

  def __init__(self, master):
    global current_user
    Frame.__init__(self, master,bg=theme[0])

    Button(self, text="Logout",fg="white", bg=theme[1], height=2,width=10,font=button_header_font,command=lambda: self.master.switch_frame(LogIn)).pack(side=RIGHT,anchor=NE,padx=10,pady=10)
    Button(self, text="Home",fg="white", bg=theme[1], height=2,width=10,font=button_header_font,command=lambda: self.master.switch_frame(HomePage)).pack(side=RIGHT,anchor=NE,pady=10)
    Label(self, text=f"Create Hospital",bg=theme[0],fg="white",font=header_font).pack(fill="x", side=TOP,anchor=N, pady=15)

    self.anyErrors = Label(self, text = "",fg="red",bg=theme[0],font=field_label_font)
    self.anyErrors.pack(side = TOP, anchor = N)

    Label(self, text = "Hospital Name",bg=theme[0],fg="white",font=field_label_font).pack(fill="x",side = TOP, anchor = N)
  
    self.nameEntry = Entry(self)
    self.nameEntry.pack(side = TOP, anchor = N)

    logInButton = Button(self, text = "Create",fg="white",bg=theme[1],command = self.RegisterCheck)
    logInButton.pack(side = TOP, anchor = S,pady=3)

  # Authenticates creating hospital details, creates hospital
  def RegisterCheck(self):
    global current_user
    try:
      user = db.create_hospital(self.nameEntry.get(),current_user["_id"])
      if "message" in user:
        self.anyErrors["text"] = user["message"]
      else:
        current_user = user
        self.master.switch_frame(HomePage)
    except Exception as e:
      print(e)
      self.anyErrors["text"] = "Something went wrong"

# Join Hospital Page
class JoinHospital(Frame):

  def __init__(self, master):
    global current_user
    Frame.__init__(self, master,bg=theme[0])
    Button(self, text="Logout", bg=theme[1],fg="white", height=2,width=10,font=button_header_font,command=lambda: self.master.switch_frame(LogIn)).pack(side=RIGHT,anchor=NE,padx=10,pady=10)
    Button(self, text="Home", bg=theme[1],fg="white", height=2,width=10,font=button_header_font,command=lambda: self.master.switch_frame(HomePage)).pack(side=RIGHT,anchor=NE,pady=10)
    Label(self, text=f"Join Hospital",bg=theme[0],fg="white",font=header_font).pack(fill="x", side=TOP,anchor=N, pady=15)
    self.anyErrors = Label(self, text = "",fg="red",bg=theme[0],font=field_label_font)
    self.anyErrors.pack(side = TOP, anchor = N)

    Label(self, text="Hospital Name",bg=theme[0],fg="white",font=field_label_font).pack(pady =3, padx = 10, side = TOP, anchor = N)
  
    self.nameEntry = Entry(self)
    self.nameEntry.pack(pady =3, padx = 10, side = TOP, anchor = N)
    Label(self, text = "Hospital Join Code",bg=theme[0],fg="white",font=field_label_font).pack(pady =3, padx = 10, side = TOP, anchor = N)
    self.joinEntry = Entry(self)
    self.joinEntry.pack(pady =3, padx = 10, side = TOP, anchor = N)

    logInButton = Button(self, text = "Join",fg="white",bg=theme[1],command = self.JoinCheck)
    logInButton.pack(side = TOP, anchor = S)

  # Authenticates the join hosipital details and joins hospital
  def JoinCheck(self):
    global current_user
    try:
      user = db.join_hospital(self.nameEntry.get(),self.joinEntry.get(),current_user["_id"])
      if "message" in user:
        self.anyErrors["text"] = user["message"]
      else:
        current_user = user
        self.master.switch_frame(HomePage)
    except Exception as e:
      self.anyErrors["text"] = "Something went wrong"

if __name__ == "__main__":
  app = DesignProject()
  app.mainloop()
