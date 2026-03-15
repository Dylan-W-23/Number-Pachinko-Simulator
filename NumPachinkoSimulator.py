# NUMBER PACHINKO SIMULATOR
# Created by Dylan Wijesinghe
# This project is based on Python Tkinter under the GPL-3.0 License.

# Modules
import tkinter as tK
import random
import time

# Settings
FPS = 60
start_delay_time = 1
refresh_time = 0.015
duration_time = 0.25
stop_time = 0.5
app_color = "snow2"

# Variables
num = [1, 2, 3]

# Set color to slot number
def numColor(num):
    if num == 7:
        return "goldenrod2"
    elif num % 2 != 0:
        return "red"
    else:
        return "blue"

# Set chance based on fraction
def fract():
    deci_places = 3
    
    while True:
        print("Enter Fraction Probability (Example - 1/100.0). Type 'back' to go back:")
        chance = input().lower().strip()
        
        if chance == "back":
            return None, None
        
        try:
            tokens = chance.split("/")
            numen = round(float(tokens[0]), deci_places)
            denom = round(float(tokens[1]), deci_places)
            print(f"Chance: {numen}/{denom}")
            return numen, denom
        except Exception:
            print("Error: Invalid input when checking fraction.")

# Set chance based on percentage
def percent():
    while True:
        print("Enter Percentage Probability (Example - 1.0). Type 'back' to go back:")
        chance = input().lower().strip()
        
        if chance == "back":
            return None, None
        
        try:
            chance = float(chance) / 100
            print("Chance: " + str(chance * 100) + "%")
            return chance, 1
        except Exception:
            print("Error: Invalid input when checking percentage.")

# Main Pachinko App
class PachinkoApp:
    def __init__(self, root, numen, denom):
        self.root = root
        self.numen = numen
        self.denom = denom
        self.hit = denom
        self.is_win = False
        
        self.accumulator = 0.0
        self.after_id = None

        # Initialization
        self.root.title("Number Pachinko Simulator")
        self.root.geometry("800x400")
        self.root.resizable(False, False)
        self.root.config(background=app_color)

        self.running = True
        self.attempts = 0

        self.refresh_timer = refresh_time
        self.duration_timer = duration_time
        self.is_dramatic = False
        self.stop_timer = stop_time
        self.start_timer = start_delay_time

        self.last_time = time.perf_counter()

        # Set text and numbers as labels on app, and align them as necessary
        self.num1_label = tK.Label(root, font=("Arial Black", 125), background=app_color)
        self.num2_label = tK.Label(root, font=("Arial Black", 150), background=app_color)
        self.num3_label = tK.Label(root, font=("Arial Black", 125), background=app_color)
        self.attempts_label = tK.Label(root, font=("Arial", 20), background=app_color)

        self.num1_label.place(relx=0.2, rely=0.5, anchor="center")
        self.num2_label.place(relx=0.5, rely=0.5, anchor="center")
        self.num3_label.place(relx=0.8, rely=0.5, anchor="center")
        self.attempts_label.place(x=10, y=10, anchor="nw")

        # Update items by coloring and setting current number of attempts
        self.update_labels()
        
        # Set event when closing the app
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # Begin frame step
        self.tick()

    # Close the Pachinko app
    def close(self):
        self.running = False
        self.root.after_cancel(self.after_id)
        self.root.destroy()

    # Randomize the numbers
    def randomize(self):
        num[0] = random.randint(1, 9)
        num[1] = random.randint(1, 9)
        num[2] = random.randint(1, 9)
    
    # Calculate the chance and set the numbers accordingly
    def calculate(self):
        self.hit = random.uniform(0, denom)
        # Miss
        if self.hit <= self.numen:
            num[0] = random.randint(1, 9)
            num[1] = num[0]
            num[2] = num[0]
            return True
        # Hit
        else:
            while True:
                self.randomize()
                if not (num[0] == num[1] == num[2]):
                    return False

    # Color the numbers and set the current number of attempts
    def update_labels(self):
        self.num1_label.config(text=num[0], fg=numColor(num[0]))
        self.num2_label.config(text=num[1], fg=numColor(num[1]))
        self.num3_label.config(text=num[2], fg=numColor(num[2]))
        self.attempts_label.config(text=f"Attempts: {self.attempts}")

    # Calculate frame time against FPS, and if appropriate, update simulation as a frame
    def tick(self):
        if not self.running:
            return

        now = time.perf_counter()
        frame_time = now - self.last_time
        self.last_time = now

        # Clamp huge spikes (window drag, minimize, etc.)
        frame_time = min(frame_time, 0.25)

        self.accumulator += frame_time
        step = 1.0 / FPS

        while self.accumulator >= step:
            self.update_labels()
            self.update_simulation(step)
            self.accumulator -= step

        self.after_id = self.root.after(1, self.tick)

    # Update the app as a frame
    def update_simulation(self, dT):
        # Wait until it starts
        if self.start_timer > 0:
            self.is_win = False
            self.start_timer -= dT
        
        # Stop/pause until the next
        elif self.stop_timer > 0:
            self.stop_timer -= dT
        
        # Stop the app if you win
        elif self.is_win:
            if self.attempts == 1:
                print(f"HIT! {self.attempts} attempt completed with combination number {num[0]}.")
            else:
                print(f"HIT! {self.attempts} attempts completed with combination number {num[0]}.")
            self.close()

        # Randomize the numbers and countdown for every refresh. Then calculate the chance and pause it.
        elif self.refresh_timer <= 0:
            if self.duration_timer > 0:
                self.randomize()
                self.update_labels()
                self.refresh_timer = refresh_time
            else:
                self.stop_timer = stop_time
                self.duration_timer = duration_time
                self.refresh_timer = refresh_time
                self.attempts += 1
                self.is_win = self.calculate()
                self.update_labels()
        else:
            self.refresh_timer -= dT
            self.duration_timer -= dT

if __name__ == "__main__":
    # Main loop
    while True:
        # Ask to choose either fraction or percent
        print("Choose a mode (Type either '/' or '%'). Type 'exit' to close:")
        choice = input().lower().strip()

        # Choose the mode as such. If the option is invalid, do nothing.
        if choice == "/":
            config = fract()
        elif choice == "%":
            config = percent()
        elif choice == "exit":
            break
        else:
            continue

        numen, denom = config

        if numen == None or denom == None:
            continue

        # Begin the Pachinko app
        root = tK.Tk()
        root.lift()
        root.attributes("-topmost", 1)
        root.attributes("-topmost", 0)
        app = PachinkoApp(root, numen, denom)
        root.mainloop()