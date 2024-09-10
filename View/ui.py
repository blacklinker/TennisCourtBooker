import json
from threading import Timer
from Controller.controller import Controller
import tkinter as tk

class View(tk.Frame):
    time_left = 0
    timer_id = None
    def __init__(self, root: tk.Tk, controller: Controller):
        super().__init__(root)
        self.controller = controller

        self.root = root
        self.root.title("Brossard Tennis booker")
        self.root.geometry("450x320")
        self.root.minsize(500, 320)

        self.countDownLabel = tk.Label(root, text="Count Down:")
        self.countDownLabel.grid(row=0, column=0, padx=20)
        self.secondLabel = tk.Label(root, text=f"{self.time_left} seconds")
        self.secondLabel.grid(row=1, column=0, padx=20)

        self.label = tk.Label(root, text="BCITI ID:")
        self.label.grid(row=2, column=0, padx=20)
        self.bciti_id = tk.Entry(root, width=30)
        self.bciti_id.grid(row=3, column=0, padx=20)

        self.label = tk.Label(root, text="Date of birth: YYYY-MM-DD")
        self.label.grid(row=4, column=0, padx=20)
        self.dob = tk.Entry(root, width=30)
        self.dob.grid(row=5, column=0, padx=20)

        self.label = tk.Label(root, text="Email:")
        self.label.grid(row=6, column=0, padx=20)
        self.email = tk.Entry(root, width=30)
        self.email.grid(row=7, column=0, padx=20)

        self.label = tk.Label(root, text="Time:")
        self.label.grid(row=0, column=2, padx=20)
        self.time = tk.StringVar(value="20:00-21:00")

        self.radio1 = tk.Radiobutton(root, text="08:00-09:00", variable=self.time, value="08:00-09:00")
        self.radio2 = tk.Radiobutton(root, text="09:00-10:00", variable=self.time, value="09:00-10:00")
        self.radio3 = tk.Radiobutton(root, text="10:00-11:00", variable=self.time, value="10:00-11:00")
        self.radio4 = tk.Radiobutton(root, text="11:00-12:00", variable=self.time, value="11:00-12:00")
        self.radio5 = tk.Radiobutton(root, text="12:00-13:00", variable=self.time, value="12:00-13:00")
        self.radio6 = tk.Radiobutton(root, text="13:00-14:00", variable=self.time, value="13:00-14:00")
        self.radio7 = tk.Radiobutton(root, text="14:00-15:00", variable=self.time, value="14:00-15:00")
        self.radio8 = tk.Radiobutton(root, text="15:00-16:00", variable=self.time, value="15:00-16:00")
        self.radio9 = tk.Radiobutton(root, text="16:00-17:00", variable=self.time, value="16:00-17:00")
        self.radio10 = tk.Radiobutton(root, text="17:00-18:00", variable=self.time, value="17:00-18:00")
        self.radio11 = tk.Radiobutton(root, text="18:00-19:00", variable=self.time, value="18:00-19:00")
        self.radio12 = tk.Radiobutton(root, text="19:00-20:00", variable=self.time, value="19:00-20:00")
        self.radio13 = tk.Radiobutton(root, text="20:00-21:00", variable=self.time, value="20:00-21:00")
        self.radio14 = tk.Radiobutton(root, text="21:00-22:00", variable=self.time, value="21:00-22:00")
        self.radio15 = tk.Radiobutton(root, text="22:00-23:00", variable=self.time, value="22:00-23:00")

        self.radio1.grid(row=1, column=2, padx=20)
        self.radio2.grid(row=2, column=2, padx=20)
        self.radio3.grid(row=3, column=2, padx=20)
        self.radio4.grid(row=4, column=2, padx=20)
        self.radio5.grid(row=5, column=2, padx=20)
        self.radio6.grid(row=6, column=2, padx=20)
        self.radio7.grid(row=7, column=2, padx=20)
        self.radio8.grid(row=8, column=2, padx=20)
        self.radio9.grid(row=1, column=3, padx=20)
        self.radio10.grid(row=2, column=3, padx=20)
        self.radio11.grid(row=3, column=3, padx=20)
        self.radio12.grid(row=4, column=3, padx=20)
        self.radio13.grid(row=5, column=3, padx=20)
        self.radio14.grid(row=6, column=3, padx=20)
        self.radio15.grid(row=7, column=3, padx=20)

        self.submit_button = tk.Button(root, text="Book!", command=self.submit_action)
        self.submit_button.grid(row=10, column=3, padx=10, pady=10)

        self.cancel_button = tk.Button(root, text="Cancel", command=self.cancel_action)
        self.cancel_button.grid(row=11, column=3, padx=10, pady=5)

        self.bciti_id.insert(0, self.controller.get_bciti_id())
        self.dob.insert(0, self.controller.get_dob())
        self.time.set(self.controller.get_time())
        self.email.insert(0, self.controller.get_email())

        self.root.protocol("WM_DELETE_WINDOW", self.close_action)

        self.grid()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.secondLabel.config(text=f"{self.time_left} seconds to start")
            self.timer_id = self.root.after(1000, self.update_timer) # Call the function again after 1000ms (1 second)
        else:
            self.secondLabel.config(text="Start booking!")

    def submit_action(self):
        self.toggle_all_buttons("disabled")
        with open("user_input.json", "w") as file:
            file.write("")  # Writing an empty string clears the file
        file.close()

        id = self.bciti_id.get()
        birth = self.dob.get()
        email = self.email.get()
        time = self.time.get()
        countDown = self.controller.calculateTime(time)
        print(f"count down is {countDown}")
        self.controller.timer = Timer(countDown, self.controller.callBookService, args=(time, birth, id, email,))
        self.controller.timer.start()

        self.time_left = countDown
        self.update_timer()

        data = {"id": id, "birth": birth, "time": time, "email": email}
        with open("user_input.json", "a") as file: 
            file.write(json.dumps(data) + "\n")

    def toggle_all_buttons(self, toggle):
        self.bciti_id.config(state=toggle)
        self.dob.config(state=toggle)
        self.email.config(state=toggle)
        self.radio1.config(state=toggle)
        self.radio2.config(state=toggle)
        self.radio3.config(state=toggle)
        self.radio4.config(state=toggle)
        self.radio5.config(state=toggle)
        self.radio6.config(state=toggle)
        self.radio7.config(state=toggle)
        self.radio8.config(state=toggle)
        self.radio9.config(state=toggle)
        self.radio10.config(state=toggle)
        self.radio11.config(state=toggle)
        self.radio12.config(state=toggle)
        self.radio13.config(state=toggle)
        self.radio14.config(state=toggle)
        self.radio15.config(state=toggle)
        self.submit_button.config(state=toggle)

    def cancel_action(self):
        self.time_left = 0
        if(self.timer_id is not None):
            self.root.after_cancel(self.timer_id)
        if self.controller.timer != None:
            self.controller.timer.cancel()
        self.secondLabel.config(text=f"{self.time_left} seconds")
        self.toggle_all_buttons("normal")


    def close_action(self):
        if(self.timer_id is not None):
            self.root.after_cancel(self.timer_id)
        if self.controller.timer != None:
            self.controller.timer.cancel()
        self.root.destroy()