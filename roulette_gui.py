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

        tk.Label(controls_frame, text="아이템:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=(10, 0))
        self.item_entry = tk.Entry(controls_frame, width=20, font=("Helvetica", 12))
        self.item_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(controls_frame, text="비중:", font=("Helvetica", 12)).pack(side=tk.LEFT)
        self.weight_entry = tk.Entry(controls_frame, width=5, font=("Helvetica", 12))
        self.weight_entry.insert(0, "1")
        self.weight_entry.pack(side=tk.LEFT, padx=(5, 10))

        self.add_button = tk.Button(controls_frame, text="추가", font=("Helvetica", 12), command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.spin_button = tk.Button(controls_frame, text="돌리기", font=("Helvetica", 12), command=self.start_spin)
        self.spin_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(controls_frame, text="전체 삭제", font=("Helvetica", 12), command=self.clear_all_items)
        self.clear_button.pack(side=tk.LEFT, padx=5)

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
        item_name = self.item_entry.get()
        weight_str = self.weight_entry.get()

        if item_name:
            try:
                weight = int(weight_str)
                if weight <= 0:
                    weight = 1
            except (ValueError, TypeError):
                weight = 1 # Default weight if empty or invalid

            self.items.append({'name': item_name, 'weight': weight})
            self.item_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)
            self.weight_entry.insert(0, "1")
            self.update_item_list()
            self.draw_wheel()

    def remove_item(self, item_obj_to_remove):
        self.items.remove(item_obj_to_remove)
        # UI refresh will be handled by calling update_item_list and draw_wheel
        self.update_item_list()
        self.draw_wheel()

    def clear_all_items(self):
        self.items.clear()
        self.update_item_list()
        self.draw_wheel()

    def update_item_list(self):
        # Clear existing widgets
        for widget in self.item_list_frame.winfo_children():
            widget.destroy()
        # Add new labels and buttons
        for i, item_obj in enumerate(self.items):
            item_frame = tk.Frame(self.item_list_frame)
            item_frame.pack(fill=tk.X, pady=2)

            color = self.colors[i % len(self.colors)]
            display_text = f"■ {item_obj['name']} (비중: {item_obj['weight']})"
            label = tk.Label(item_frame, text=display_text, fg=color, font=("Helvetica", 12))
            label.pack(side=tk.LEFT, expand=True, anchor="w")

            remove_button = tk.Button(item_frame, text="제거", command=lambda obj=item_obj: self.remove_item(obj))
            remove_button.pack(side=tk.RIGHT)

    def draw_wheel(self, rotation_angle=0):
        self.canvas.delete("all")
        center_x, center_y = 250, 250
        radius = 200

        if not self.items:
            self.canvas.create_text(center_x, center_y, text="아이템을 추가하고 돌려보세요!", font=("Helvetica", 16))
            return

        total_weight = sum(item['weight'] for item in self.items)
        current_start_angle = rotation_angle

        for i, item_obj in enumerate(self.items):
            arc_angle = (item_obj['weight'] / total_weight) * 360

            # Draw wedge
            color = self.colors[i % len(self.colors)]
            self.canvas.create_arc(
                center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                start=current_start_angle, extent=arc_angle, fill=color, outline="white", width=2
            )

            # Draw text
            text_angle_deg = current_start_angle + arc_angle / 2
            text_angle_rad = math.radians(-text_angle_deg)
            text_radius = radius * 0.7
            text_x = center_x + text_radius * math.cos(text_angle_rad)
            text_y = center_y + text_radius * math.sin(text_angle_rad)
            self.canvas.create_text(text_x, text_y, text=item_obj['name'], font=("Helvetica", 12, "bold"), angle=-text_angle_deg + 90)

            current_start_angle += arc_angle

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
        if not self.items:
            return

        total_weight = sum(item['weight'] for item in self.items)
        if total_weight == 0:
            return # Avoid division by zero

        # Pointer is at 90 degrees (top of the circle in tkinter)
        pointer_position = (90 - self.rotation_angle) % 360

        current_angle = 0
        winner_obj = self.items[-1] # Default to last item
        winner_index = len(self.items) - 1

        for i, item_obj in enumerate(self.items):
            arc_angle = (item_obj['weight'] / total_weight) * 360
            if current_angle <= pointer_position < current_angle + arc_angle:
                winner_obj = item_obj
                winner_index = i
                break
            current_angle += arc_angle

        self.result_label.config(text=f"{winner_obj['name']}", fg=self.colors[winner_index % len(self.colors)])


if __name__ == "__main__":
    root = tk.Tk()
    app = RouletteApp(root)
    app.draw_wheel() # Draw initial message
    root.mainloop()
