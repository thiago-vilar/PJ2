import tkinter as tk
import subprocess
import os
import re
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

class PrescriptionUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Prescription UI")
        self.mode = tk.StringVar(value="Free")
        self.language = tk.StringVar(value="Eng")
        self.data_table = []

        self.load_image()
        tk.Label(root, text="Medical Prescription Generator", font=("Arial", 14, "bold")).pack(pady=10)
        self.create_language_selector()
        self.create_mode_selector()
        self.create_main_frames()
        self.show_mode()

    def load_image(self):
        img_path = os.path.join(os.path.dirname(__file__), "ampoule.png")
        self.img = tk.PhotoImage(file=img_path).subsample(4, 4)
        tk.Label(self.root, image=self.img).pack(pady=5)

    def create_language_selector(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Label(frame, text="Select Language:").pack(side=tk.LEFT)
        for lang, name in [("Eng", "English"), ("Bra", "Português (BRA)")]:
            tk.Radiobutton(frame, text=name, variable=self.language, value=lang).pack(side=tk.LEFT)

    def create_mode_selector(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Label(frame, text="Select Mode:").pack(side=tk.LEFT)
        for mode, name in [("Free", "Free Style"), ("Guided", "Guided Style")]:
            tk.Radiobutton(frame, text=name, variable=self.mode, value=mode, command=self.show_mode).pack(side=tk.LEFT)

    def create_main_frames(self):
        self.frames = {
            "Free": self.create_free_mode(),
            "Guided": self.create_guided_mode(),
            "Table": self.create_table_frame()
        }

    def create_free_mode(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Enter Prescription:", font=("Arial", 12)).pack(pady=5)
        self.free_text = tk.Text(frame, width=60, height=5)
        self.free_text.pack(pady=5)
        tk.Button(frame, text="Generate Table Data", command=self.parse_with_gf).pack(pady=5)
        return frame

    def create_guided_mode(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Fill Prescription Details", font=("Arial", 12)).pack(pady=5)
        self.medication = self.create_field(frame, "Medication:")
        self.dosage = self.create_field(frame, "Dosage:")
        self.unit = self.create_field(frame, "Unit:")
        self.frequency = self.create_field(frame, "Frequency:")
        self.body_part = self.create_field(frame, "Body Part (Optional):")
        tk.Button(frame, text="Generate Prescription", command=self.generate_and_validate).pack(pady=5)
        return frame

    def create_table_frame(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Prescription Table", font=("Arial", 12, "bold")).pack()
        self.table = ttk.Treeview(frame, columns=("Medication", "Dosage", "Unit", "Frequency", "BodyPart"), show="headings")
        for col in ["Medication", "Dosage", "Unit", "Frequency", "BodyPart"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=120)
        self.table.pack()
        return frame

    def create_field(self, parent, label_text):
        frame = tk.Frame(parent)
        frame.pack(pady=3, anchor="w")
        tk.Label(frame, text=label_text, width=15, anchor="w").pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=30)
        entry.pack(side=tk.LEFT)
        return entry

    def show_mode(self):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[self.mode.get()].pack(pady=10)
        self.frames["Table"].pack(pady=10)

    def call_gf_shell(self, command):
        try:
            process = subprocess.Popen(["gf", "--run"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate(input=command)
            if error.strip():
                return f"GF Error: {error.strip()}"
            return output.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def parse_with_gf(self):
        text = self.free_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter a prescription.")
            return

        try:
            gf_command = self.map_free_text_to_gf(text)
            if not gf_command:
                raise ValueError("Invalid input format. Use proper syntax like 'Apply 2 drops to the affected eye twice a day'.")

            result = self.call_gf_shell(f"import PrescriptionGrammarEng.gf\nlinearize {gf_command}")
            if "GF Error" in result:
                raise ValueError(result)

            self.add_to_table(self.extract_table_parts(result))
            messagebox.showinfo("Success", f"GF Output: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def map_free_text_to_gf(self, text):
        text = text.lower()

        # Dicionários de mapeamento
        dosage_map = {"1": "One", "2": "Two", "3": "Three", "4": "Four"}
        unit_map = {"tablet": "Tablet", "drop": "Drop", "drops": "Drop"}
        frequency_map = {
            "once a day": "OnceADay",
            "twice a day": "TwiceADay",
            "three times a day": "ThreeTimesADay",
            "every 6 hours": "Every6Hours"
        }
        body_part_map = {"eye": "AffectedEye", "oral": "Oral", "ear": "AffectedEar"}

        # Expressão regular para capturar os elementos de forma mais genérica
        pattern = re.compile(r"(apply|take)\s+(\d+)\s+(\w+)\s+(?:to the\s+|of\s+)?(\w+)?\s*(.*?)$", re.IGNORECASE)

        match = pattern.search(text)

        if not match:
            return None

        action, dosage, unit, body_part, frequency = match.groups()

        # Mapeia os elementos para GF
        dosage_gf = dosage_map.get(dosage, "One")
        unit_gf = unit_map.get(unit, "Tablet")
        body_part_gf = body_part_map.get(body_part, "")
        frequency_gf = frequency_map.get(frequency.strip(), "")

        if action == "apply":
            return f"Prescribe (Apply {dosage_gf} {unit_gf} {body_part_gf} {frequency_gf})"
        elif action == "take":
            return f"Prescribe (Take Aspirin {dosage_gf} {unit_gf} {frequency_gf})"

        return None



    def extract_table_parts(self, result):
        # Extrai os valores para preencher a tabela
        parts = result.replace("Prescribe:", "").strip().split()
        medication = parts[3] if "Take" in parts else "drops"
        dosage = parts[1] if parts[1].isdigit() else "2"
        unit = parts[2] if "drop" in parts else "tablet"
        frequency = " ".join(parts[4:]) if len(parts) > 4 else ""
        body_part = parts[-1] if "to" in parts else ""
        return [medication, dosage, unit, frequency, body_part]

    def add_to_table(self, data):
        self.table.insert("", "end", values=data)
        self.data_table.append(data)

    def generate_and_validate(self):
        med = self.medication.get()
        dose = self.dosage.get()
        unit = self.unit.get()
        freq = self.frequency.get()
        part = self.body_part.get()
        if not all([med, dose, unit, freq]):
            messagebox.showerror("Error", "Please fill all fields.")
            return
        gf_input = f"Prescribe (Take {med} {dose} {unit} {freq})"
        result = self.call_gf_shell(f"import PrescriptionGrammarEng.gf\nlinearize {gf_input}")
        self.add_to_table([med, dose, unit, freq, part])

if __name__ == "__main__":
    root = tk.Tk()
    app = PrescriptionUI(root)
    root.mainloop()
