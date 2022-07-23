import pygame
import pygame.camera
import time
from moviepy.editor import *

# ======================== Config your filming plan here ===========================

hours = 8  # number of hours to take pictures
film_length_minutes = 10  # length of film in minutes

# ==================================================================================

# Calculate the frequency of taking pictures
frame_per_second = 24
num_frames = (60 * film_length_minutes) * frame_per_second
interval_seconds = hours * 3600 / num_frames
interval_minutes = interval_seconds / 60
print(f"Taking pictures every {interval_seconds} seconds (i.e. {interval_minutes} minutes)")
print(f"{num_frames} frames to be taken")

pictures_list = []

# initializing  the camera
pygame.camera.init()

# make the list of all available cameras
cam_list = pygame.camera.list_cameras()

# initializing the cam variable with default camera
cam = pygame.camera.Camera(cam_list[0], (640, 480))

# opening the camera
cam.start()


def take_picture(filename):
    # if camera is detected or not
    if cam_list:

        # capturing the single image
        image = cam.get_image()

        # saving the image
        pygame.image.save_extended(image, filename)

    # if camera is not detected the moving to else part
    else:
        print("No camera on current device")
        quit()


def make_video():
    pictures_list.pop(0)
    clip = ImageSequenceClip(pictures_list, fps=frame_per_second)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    clip.write_videofile(f"saved_videos/{timestamp}.mp4", fps=frame_per_second)


def main():
    picture_count = 1

    # Create folders if it doesn't exist
    if not os.path.exists("saved_pictures"):
        os.makedirs("saved_pictures")
    if not os.path.exists("saved_videos"):
        os.makedirs("saved_videos")

    # Take pictures
    while picture_count <= num_frames:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"saved_pictures/picture_{picture_count}_{timestamp}.jpg"
        take_picture(filename)
        pictures_list.append(filename)
        print(f"{picture_count} pictures taken. Percentage complete: {round(picture_count / num_frames * 100, 2)}%")
        time.sleep(interval_seconds)
        picture_count += 1

    # Make video
    make_video()

    pygame.quit()
    print(f"Generated video at {time.strftime('%Y%m%d-%H%M%S')}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"Detected KeyboardInterrupt. Exiting after the video is generated ...")
        make_video()
        pygame.quit()
        print(f"Generated video at {time.strftime('%Y%m%d-%H%M%S')}")
