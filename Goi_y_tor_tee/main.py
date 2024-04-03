import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import json

class ZodiacAnalyzer:
    def __init__(self, compatibility_data, colleagues, model):
        self.compatibility_data = compatibility_data
        self.label_encoder = LabelEncoder()
        self.colleagues = colleagues
        self.model = model

    @classmethod
    def from_json(cls, json_file_path, colleagues, model):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return cls(data, colleagues, model)

    def find_compatible_zodiacs(self, zodiac_sign, gender):
        compatible_zodiacs = []

        if zodiac_sign in self.compatibility_data:
            zodiac_info = self.compatibility_data[zodiac_sign]

            if "male" in zodiac_info and gender == "Nam":
                compatible_zodiacs.extend(zodiac_info["male"]["compatible"])
            elif "female" in zodiac_info and gender == "Nữ":
                compatible_zodiacs.extend(zodiac_info["female"]["compatible"])

        # Modify the structure to include 'zodiac_sign', 'gender', and 'dates'
        compatible_zodiacs = [
            {
                'zodiac_sign': zodiac['sign'],
                'gender': zodiac['gender'],
                'dates': zodiac['dates']
            }
            for zodiac in compatible_zodiacs
        ]

        return compatible_zodiacs
    
    def suggest_colleague(self, zodiac_sign, gender):
        input_data = self.label_encoder.transform([[zodiac_sign, gender]])
        predicted_zodiac = self.model.predict(input_data)[0]

        suggested_colleagues = [colleague for colleague in self.colleagues if
                                colleague["zodiac"] == predicted_zodiac and colleague["gender"] != gender]

        return suggested_colleagues

class ZodiacCalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Xác định cung hoàng đạo")

        self.label_date = tk.Label(master, text="Ngày sinh (dd/mm/yyyy):")
        self.entry_date = tk.Entry(master)

        self.label_gender = tk.Label(master, text="Giới tính:")
        self.entry_gender = tk.Entry(master)

        self.result_label = tk.Label(master, text="")
        self.treeview = ttk.Treeview(master, columns=("Zodiac", "Birthdate", "Gender"), show="headings")
        self.treeview.heading("Zodiac", text="Cung hoàng đạo")
        self.treeview.heading("Birthdate", text="Ngày sinh")
        self.treeview.heading("Gender", text="Giới tính")

        self.calculate_button = tk.Button(master, text="Xác định", command=self.calculate_zodiac)

        self.label_date.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_date.grid(row=0, column=1, padx=10, pady=5)

        self.label_gender.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_gender.grid(row=1, column=1, padx=10, pady=5)

        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)
        self.treeview.grid(row=4, column=0, columnspan=2, pady=10)

        # Initialize the ZodiacAnalyzer with actual data
        json_file_path = 'data.json'
        colleagues_data = [...]  # Replace [...] with your actual colleagues data
        model = LogisticRegression()  # Replace with your trained model
        self.zodiac_analyzer = ZodiacAnalyzer.from_json(json_file_path, colleagues_data, model)

    def calculate_zodiac(self):
        try:
            input_date = self.entry_date.get()
            gender = self.entry_gender.get().capitalize()
            birthdate = datetime.strptime(input_date, "%d/%m/%Y")
            zodiac_sign = self.get_zodiac_sign(birthdate.day, birthdate.month)
            compatible_zodiacs = self.zodiac_analyzer.find_compatible_zodiacs(zodiac_sign, gender)

            self.treeview.delete(*self.treeview.get_children())

            if compatible_zodiacs:
                for zodiac in compatible_zodiacs:
                    birthdate_range = zodiac["dates"] if "dates" in zodiac else ""
                    self.treeview.insert("", tk.END, values=(zodiac["zodiac_sign"], birthdate_range, zodiac["gender"]))
            else:
                self.treeview.insert("", tk.END, values=("Không có cung hoàng đạo nào tương thích.", "", ""))

            result_text = f"Cung hoàng đạo của bạn là {zodiac_sign}."
            self.result_label.config(text=result_text)

        except ValueError:
            messagebox.showerror("Lỗi", "Ngày sinh không hợp lệ. Vui lòng nhập lại theo định dạng dd/mm/yyyy.")

    def get_zodiac_sign(self,day, month):
        zodiac_ranges = [
            (20, 1, 18, 2, "Bảo Bình"),
            (19, 2, 20, 3, "Song Ngư"),
            (21, 3, 19, 4, "Bạch Dương"),
            (20, 4, 20, 5, "Kim Ngưu"),
            (21, 5, 20, 6, "Song Tử"),
            (21, 6, 22, 7, "Cự Giải"),
            (23, 7, 22, 8, "Sư Tử"),
            (23, 8, 22, 9, "Xử Nữ"),
            (23, 9, 22, 10, "Thiên Bình"),
            (23, 10, 21, 11, "Bọ Cạp"),
            (22, 11, 21, 12, "Nhân Mã"),
            (22, 12, 31, 12, "Ma Kết"),
        ]

        for start_day, start_month, end_day, end_month, sign in zodiac_ranges:
            if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                return sign

        return "Unknown" 
    
def main():
    root = tk.Tk()
    app = ZodiacCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
