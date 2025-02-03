from datetime import datetime, timedelta
import os

def parse_date(text):
    now = datetime.now()

    if "ago" in text:
        parts = text.split()
        number = int(parts[0])
        unit = parts[1]

        if "hour" in unit:
            calculated_time = now - timedelta(hours=number)
        elif "day" in unit:
            calculated_time = now - timedelta(days=number)
        else:
            raise ValueError("Unsupported time unit")
        return calculated_time.strftime("%Y-%m-%d %H:%M:%S")

    else:
        # Remove "Updated" if it's present at the beginning
        text = text.replace("Updated ", "").strip()

        try:
            # Try parsing different date formats
            date_object = datetime.strptime(text, "%b %d, %Y")  # Format: "Aug 1, 2023"
            return date_object.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("Unsupported date format")
        
def output_data(folder_path, file_name, data_frame):
    output_folder = folder_path
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file = os.path.join(output_folder, file_name)
    data_frame.to_excel(output_file, index=False)   