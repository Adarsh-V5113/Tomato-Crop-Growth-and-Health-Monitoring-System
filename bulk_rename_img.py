import os
import shutil
from datetime import datetime

# CONFIGURATION
root_folder = "drive_images"            # Root folder with all nested folders from Drive
destination_folder = "static/images"    # Final folder inside your Flask project
overwrite_existing = False              # Set to True to replace existing files

def ensure_destination():
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

def get_image_date(filepath):
    # Use last modified time of the image file
    modified_time = os.path.getmtime(filepath)
    return datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d")

def walk_and_rename_images():
    ensure_destination()
    seen_dates = set()
    count = 0

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                source_path = os.path.join(dirpath, filename)
                date_str = get_image_date(source_path)

                # Ensure filename uniqueness for images on the same date
                new_filename = date_str
                suffix = 1
                while new_filename in seen_dates:
                    new_filename = f"{date_str}_{suffix}"
                    suffix += 1
                seen_dates.add(new_filename)

                new_filename += ".jpg"
                destination_path = os.path.join(destination_folder, new_filename)

                if not overwrite_existing and os.path.exists(destination_path):
                    print(f"SKIPPED (exists): {new_filename}")
                    continue

                shutil.copy2(source_path, destination_path)
                print(f"{filename} -> {new_filename}")
                count += 1

    print(f"\nDONE: {count} image(s) renamed and moved.")

if __name__ == "__main__":
    walk_and_rename_images()
