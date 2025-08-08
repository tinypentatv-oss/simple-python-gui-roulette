import tkinter as tk
import random
import math

class RouletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("룰렛 프로그램")
        self.root.geometry("800x600")

        self.items = []
        # Pre-defined colors for the wedges
        self.colors = ["#FFC0CB", "#ADD8E6", "#90EE90", "#FFD700", "#FFA07A", "#B0E0E6", "#FFB6C1", "#87CEFA", "#F08080", "#98FB98"]

        # --- Top Controls Frame ---
        controls_frame = tk.Frame(root)
        controls_frame.pack(pady=10)

        self.item_entry = tk.Entry(controls_frame, width=30, font=("Helvetica", 12))
        self.item_entry.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(controls_frame, text="추가", font=("Helvetica", 12), command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.spin_button = tk.Button(controls_frame, text="돌리기", font=("Helvetica", 12), command=self.start_spin)
        self.spin_button.pack(side=tk.LEFT, padx=5)

        self.rotation_angle = 0

        # --- Main Content Frame ---
        main_frame = tk.Frame(root)
        main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # --- Canvas for Roulette ---
        self.canvas = tk.Canvas(main_frame, width=500, height=500, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=20)

        # --- Side Frame for Item List and Result ---
        side_frame = tk.Frame(main_frame)
        side_frame.pack(side=tk.RIGHT, padx=20, fill=tk.Y, anchor="n")

        tk.Label(side_frame, text="아이템 목록", font=("Helvetica", 16, "bold")).pack(anchor="w")

        self.item_list_frame = tk.Frame(side_frame)
        self.item_list_frame.pack(pady=5, anchor="w", fill=tk.X)

        tk.Label(side_frame, text="결과", font=("Helvetica", 16, "bold")).pack(anchor="w", pady=(20, 0))

        self.result_label = tk.Label(side_frame, text="", font=("Helvetica", 20, "bold"), fg="red")
        self.result_label.pack(pady=10, anchor="w")

    def add_item(self):
        item = self.item_entry.get()
        if item:
            self.items.append(item)
            self.item_entry.delete(0, tk.END)
            self.update_item_list()
            self.draw_wheel()

    def update_item_list(self):
        # Clear existing labels
        for widget in self.item_list_frame.winfo_children():
            widget.destroy()
        # Add new labels
        for i, item in enumerate(self.items):
            color = self.colors[i % len(self.colors)]
            tk.Label(self.item_list_frame, text=f"■ {item}", fg=color, font=("Helvetica", 12)).pack(anchor="w")

    def draw_wheel(self, rotation_angle=0):
        self.canvas.delete("all")
        center_x, center_y = 250, 250
        radius = 200

        if not self.items:
            self.canvas.create_text(center_x, center_y, text="아이템을 추가하고 돌려보세요!", font=("Helvetica", 16))
            return

        arc_angle = 360 / len(self.items)

        for i, item in enumerate(self.items):
            start_angle = i * arc_angle + rotation_angle

            # Draw wedge
            color = self.colors[i % len(self.colors)]
            self.canvas.create_arc(
                center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                start=start_angle, extent=arc_angle, fill=color, outline="white", width=2
            )

            # Draw text
            text_angle = math.radians(-(start_angle + arc_angle / 2))
            text_radius = radius * 0.7
            text_x = center_x + text_radius * math.cos(text_angle)
            text_y = center_y + text_radius * math.sin(text_angle)
            self.canvas.create_text(text_x, text_y, text=item, font=("Helvetica", 12, "bold"), angle=-(start_angle + arc_angle / 2) + 90)

        # Draw pointer
        self.canvas.create_polygon(center_x - 15, center_y - radius - 20,
                                   center_x + 15, center_y - radius - 20,
                                   center_x, center_y - radius + 5,
                                   fill="black")


    def start_spin(self):
        if len(self.items) < 2:
            self.result_label.config(text="아이템을 2개 이상 추가하세요.", fg="blue")
            return

        self.spin_button.config(state=tk.DISABLED)
        self.add_button.config(state=tk.DISABLED)
        self.result_label.config(text="")

        self.rotation_speed = random.uniform(25, 40)
        self.animate_spin()

    def animate_spin(self):
        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360
        self.draw_wheel(self.rotation_angle)

        self.rotation_speed *= 0.988 # Deceleration factor

        if self.rotation_speed < 0.1:
            self.determine_winner()
            self.spin_button.config(state=tk.NORMAL)
            self.add_button.config(state=tk.NORMAL)
        else:
            self.root.after(15, self.animate_spin) # ~60 FPS

    def determine_winner(self):
        arc_angle = 360 / len(self.items)
        # Pointer is at 90 degrees (top of the circle in tkinter)
        pointer_position = (90 - self.rotation_angle) % 360
        winner_index = int(pointer_position // arc_angle)
        winner = self.items[winner_index]

        self.result_label.config(text=f"{winner}", fg=self.colors[winner_index % len(self.colors)])


if __name__ == "__main__":
    root = tk.Tk()
    app = RouletteApp(root)
    app.draw_wheel() # Draw initial message
    root.mainloop()
