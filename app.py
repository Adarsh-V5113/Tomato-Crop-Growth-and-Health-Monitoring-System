from flask import Flask, render_template, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Load sensor data
df = pd.read_excel("cleaned_sensor_data.xlsx")
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
df = df.dropna(subset=["Timestamp"])
df["DateOnly"] = df["Timestamp"].dt.date

# Load all image names from static/images/
image_folder = "static/images"
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(".jpg")])

# Match each image to a unique date (in order)
available_dates = sorted(df["DateOnly"].unique())
mapping = {}

for i, image_file in enumerate(image_files):
    if i < len(available_dates):
        label = os.path.splitext(image_file)[0].upper()  # e.g., r1t1 → R1:T1
        label = label.replace("T", ":T") if "T" in label else label
        mapping[label] = {
            "image": image_file,
            "date": str(available_dates[i])  # YYYY-MM-DD
        }

@app.route("/", methods=["GET"])
def index():
    selected_key = request.args.get("selection")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    image_path = None
    data = []

    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            filtered_df = df[(df["DateOnly"] >= start) & (df["DateOnly"] <= end)]
            data = filtered_df.to_dict(orient="records")

            # Try to show the image for the START DATE
            image_filename = f"{start.strftime('%Y-%m-%d')}.jpg"
            static_image_path = os.path.join("static/images", image_filename)
            full_image_path = os.path.join(image_folder, image_filename)
            if os.path.exists(full_image_path):
                image_path = static_image_path

        except ValueError:
            data = []

    elif selected_key in mapping:
        image_file = mapping[selected_key]["image"]
        image_path = os.path.join("static/images", image_file)
        selected_date = datetime.strptime(mapping[selected_key]["date"], "%Y-%m-%d").date()
        data = df[df["DateOnly"] == selected_date].to_dict(orient="records")

    return render_template("index.html", mapping=mapping, selected_key=selected_key,
                           image_path=image_path, data=data)



if __name__ == "__main__":
    app.run(debug=True)