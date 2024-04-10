import cv2
import asyncio

async def capture_webcam_snapshots(save_path1="/Users/proddy/IvyHacks/IvyHacks/images/snapshot1.jpg", save_path2="/Users/proddy/IvyHacks/IvyHacks/images/snapshot2.jpg"):
    cap = cv2.VideoCapture(0)  # 0 is the default webcam

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    try:
        # First snapshot
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(save_path1, frame)
            print(f"Snapshot saved to {save_path1}")
        else:
            raise IOError("Failed to capture first snapshot")

        # Wait for 5 seconds asynchronously
        print("Waiting 5 seconds for the next snapshot...")
        await asyncio.sleep(1)

        # Second snapshot
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(save_path1, frame)
            print(f"Snapshot saved to {save_path1}")
        else:
            raise IOError("Failed to capture second snapshot")
        print("Waiting 5 seconds for the next snapshot...")
        
        await asyncio.sleep(3)

        # Second snapshot
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(save_path2, frame)
            print(f"Snapshot saved to {save_path2}")
        else:
            raise IOError("Failed to capture second snapshot")
    finally:
        cap.release()  # Release the webcam

    print("Snapshots taken successfully")
