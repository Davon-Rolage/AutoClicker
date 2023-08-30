import tkinter as tk
import pyautogui as pg
from datetime import datetime
import re


class AutoClickerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x600")
        self.master.title("Auto Clicker")
        self.frame_left = tk.Frame(self.master)
        self.frame_right = tk.Frame(self.master)
        self.frame_settings = tk.Frame(self.master)
        self.click_points = []  # List to store click point coordinates
        self.grid()
        self.create_widgets()
        self.create_log()

    def create_widgets(self):
        self.frame_left.grid(row=0, column=0, sticky='nw', padx=10)
        self.frame_right.grid(row=0, column=1, sticky='n', padx=10)
        self.frame_settings.grid(row=1, column=1, sticky='n')
        
        # Left frame widgets
        self.iterations_label = tk.Label(self.frame_left, text="Number of Iterations:")
        self.iterations_label.grid(row=0, column=0, columnspan=2)
        self.iterations_entry = tk.Entry(self.frame_left, width=5, font=("Arial", 24), justify="center")
        self.iterations_entry.insert(0, "5")
        self.iterations_entry.grid(row=1, column=0, columnspan=2)
        
        self.start_button = tk.Button(self.frame_left, text="Start", command=self.auto_click, bg="#6184d8", justify='center', width=10)
        self.start_button.grid(row=2, column=0)

        self.mouse_info_button = tk.Button(self.frame_left, text="Mouse Info (2 sec delay)", command=self.display_mouse_info, bg='#FFFFE0')
        self.mouse_info_button.grid(row=2, column=1)
        
        # Right frame widgets
        self.click1_label = tk.Label(self.frame_right, text="Click Point 1 (x,y):")
        self.click1_label.grid(row=1, column=0)
        self.click1_entry = tk.Entry(self.frame_right)
        self.click1_entry.grid(row=1, column=1)

        self.new_label = tk.Label(self.frame_right, text="Click Point 2 (x,y):")
        self.new_label.grid(row=2, column=0)
        self.new_entry = tk.Entry(self.frame_right)
        self.new_entry.grid(row=2, column=1)
        self.click_points.append((self.click1_label, self.click1_entry))
        self.click_points.append((self.new_label, self.new_entry))
        
        self.add_button = tk.Button(self.frame_right, text="Add Click Point", command=self.add_click_point, bg="#50c5b7")
        self.add_button.grid(row=0, column=0)

        self.remove_button = tk.Button(self.frame_right, text="Remove Last Click Point", command=self.remove_click_point, bg="#da4167")
        self.remove_button.grid(row=0, column=1)
        
        # Settings frame widgets
        self.duration_label = tk.Label(self.frame_settings, text="Click duration (sec)")
        self.duration_label.grid(row=0, column=0, sticky='s')
        self.duration_entry = tk.Entry(self.frame_settings, width=5, font=("Arial", 24), justify="center")
        self.duration_entry.insert(0, "0.2")
        self.duration_entry.grid(row=1, column=0, sticky='s')
        
        self.pause_label = tk.Label(self.frame_settings, text="Loop pause (sec)")
        self.pause_label.grid(row=0, column=1, sticky='s')
        self.pause_entry = tk.Entry(self.frame_settings, width=5, font=("Arial", 24), justify="center")
        self.pause_entry.insert(0, "0.5")
        self.pause_entry.grid(row=1, column=1, sticky='s')
        
        self.how_to_stop = tk.Label(self.master, text="To stop the loop, move your mouse to any corner of the screen.")
        self.how_to_stop.place(x=30, y=480)

    def create_log(self):
        # Log Widget
        self.log_label = tk.Label(self.frame_left, text="Log:")
        self.log_label.grid(row=5, column=0)
        self.log_text = tk.Text(self.frame_left, height=15, width=40)
        self.log_text.grid(row=6, column=0, columnspan=2)
        self.log_clear = tk.Button(self.frame_left, text="Clear Log", command=self.clear_log)
        self.log_clear.grid(row=7, column=0)
        
        # Log Scrollbar
        self.log_scrollbar = tk.Scrollbar(self.frame_left, orient="vertical", command=self.log_text.yview)
        self.log_scrollbar.grid(row=6, column=2, sticky="nsw")
        self.log_text.configure(yscrollcommand=self.log_scrollbar.set)
        self.log_text.see("end")
        
    def add_click_point(self):
        n_click_points = len(self.click_points)
        
        new_label = tk.Label(self.frame_right, text=f"Click Point {n_click_points+1} (x,y):")
        new_label.grid(row=n_click_points+1, column=0)
        new_entry = tk.Entry(self.frame_right)
        new_entry.grid(row=n_click_points+1, column=1)

        self.click_points.append((new_label, new_entry))

    def remove_click_point(self):
        # Remove the last click point label and entry from the GUI and the list
        if len(self.click_points) >= 1:
            if len(self.click_points) == 1:
                self.click_points[-1][1].delete(0, tk.END)
            else:    
                self.click_points[-1][0].destroy()
                self.click_points[-1][1].destroy()
                self.click_points.pop()

    def validate_iterations(self):
        try:
            iterations = int(self.iterations_entry.get())
            if iterations > 0:
                return iterations
            raise ValueError
        
        except ValueError:
            self.log_text.insert(tk.END, "Invalid number of iterations.\n")
            return False

    def validate_point_coordinates(self):
        for point in self.click_points:
            point_coords = point[1].get()
            if point_coords == "":
                self.log_text.insert(tk.END, "Click points must not be empty.\n")
                return False
            
            try:
                point_coords = int(point_coords.split(",")[1])

            except ValueError:
                self.log_text.insert(tk.END, "Invalid click point coordinates.\n")
                return False
                
        return True
        
    def validate_duration(self):
        try:
            durations = float(self.duration_entry.get())
            if durations > 0:
                return durations
            raise ValueError
        
        except ValueError:
            self.log_text.insert(tk.END, "Invalid click duration.\n")
            return False
        
    def validate_pause(self):
        try:
            loop_pause = float(self.pause_entry.get())
            if loop_pause > 0:
                return loop_pause
            raise ValueError

        except ValueError:
            self.log_text.insert(tk.END, "Invalid loop pause.\n")
            return False
    
    def auto_click(self):
        iterations = self.validate_iterations()        
        point_coordinates_error = self.validate_point_coordinates()
        click_duration = self.validate_duration()
        loop_pause = self.validate_pause()
        no_errors = (iterations, click_duration, point_coordinates_error, loop_pause)
        if not all(no_errors):
            return None
        
        pg.sleep(1)
        
        started_at = datetime.now()
        started_at_f = started_at.strftime("%H:%M:%S %d/%m/%Y")
        self.log_text.insert(tk.END, f"Task started at {started_at_f}\n")
        
        try:
            for i in range(iterations):
                pg.sleep(loop_pause)
                self.log_text.insert(tk.END, f"Iteration {i+1} started\n")
                self.log_text.update()
                for point in self.click_points:
                    pg.leftClick(tuple(map(int, point[1].get().split(','))), duration=click_duration)
        except pg.FailSafeException:
            self.log_text.insert(tk.END, f"Task ended prematurely (Fail Safe)\n")
            
        finished_at = datetime.now()
        finished_at_f = finished_at.strftime("%H:%M:%S %d/%m/%Y")
        self.log_text.insert(tk.END, f"Task finished at {finished_at_f}\n")
        self.calculate_elapsed_time(started_at, finished_at)
        
    def calculate_elapsed_time(self, started_at, finished_at):
        elapsed_time = finished_at - started_at
        days, hours, minutes, seconds = elapsed_time.days, elapsed_time.seconds // 3600, (elapsed_time.seconds // 60) % 60, elapsed_time.seconds % 60
        if days > 0:
            self.log_text.insert(tk.END, f"It took {elapsed_time.days} days, {hours} hours, {minutes} minutes, and {seconds} seconds to complete\n")
        elif hours > 0:
            self.log_text.insert(tk.END, f"It took {hours} hours, {minutes} minutes, and {seconds} seconds to complete\n")
        elif minutes > 0:
            self.log_text.insert(tk.END, f"It took {minutes} minutes and {seconds} seconds to complete\n")
        else:
            self.log_text.insert(tk.END, f"It took {seconds} seconds to complete\n")

        self.log_text.insert(tk.END, "____________________________________\n")
        
    def display_mouse_info(self, event=None):
        pg.sleep(2)
        x, y = pg.position()
        self.log_text.insert(tk.END, f"Current x,y: {x},{y}\n")
        for click_point in self.click_points:
            if click_point[1].get() == "":
                click_point[1].insert(0, f"{x},{y}")
                break
    
    def clear_log(self, event=None):
        self.log_text.delete(1.0, tk.END)


root = tk.Tk()
root.wm_attributes("-topmost", 1)  # Make window always be on top
app = AutoClickerGUI(master=root)
app.mainloop()
