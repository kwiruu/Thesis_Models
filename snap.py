import os
import time
from roboflow import Roboflow

try:
    from secrets import ROBOFLOW_KEY
except ImportError:
    print("Error: secrets.py not found.")
    exit()

API_KEY = ROBOFLOW_KEY
WORKSPACE_ID = "humai-o2qtg"
PROJECT_ID = "rice-quality-3-3viu5"

def capture_and_upload():

    rf = Roboflow(api_key=API_KEY)
    project = rf.workspace(WORKSPACE_ID).project(PROJECT_ID)

    print("HUMAI DATA COLLECTION TOOL")
    print("-------------------------")

    prefix = input("Enter Rice name and price in format rice_price (e.g. kylo_42    ): ").strip()

    if not prefix:
        prefix = "rice"

    print("Collecting Photos starting name: '{prefix}_'")
    print("Intructions: Arrange rice, then press Enter to snap.")
    print("Type 'q' and press ENTER to quit.\n")

    while True:
        user_input = input(f"[{prefix}] Ready? Press Enter to snap (or 'q' to qu        it): ")

        if user_input.lower() == 'q':
            print("Exiting...")
            break

        timestamp = int(time.time())
        filename = f"{prefix}_{timestamp}.jpg"

        print(f"Snapping: {filename}")

        cmd = f"rpicam-jpeg -o {filename} -t 10000"
        os.system(cmd)


    if os.path.exists(filename):
        print("Uploading to Roboflow")
        
        try: 
            
            project.upload(
                image_path=filename,
                batch_name="rpi_noir_batch",
                tag_names=["rpi_noir", "box_v1"]
             )
            print("Success!, Image uploaded")

            if os.path.exists(filename):
             os.remove(filename)

        except Exception as e:
             print(f"Upload Error: {e}")
    else:
        print("Error: Camera didn't save the image.")

if __name__ == "__main__":
    capture_and_upload()

