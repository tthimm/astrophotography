from argparse import ArgumentParser
from tkinter import *
from io import BytesIO
from time import sleep
import time
from pathlib import Path
import os
from fractions import Fraction
import tkinter
from PIL import Image, ImageTk
import config as conf

is_raspberry_pi = False 

parser = ArgumentParser()
parser.add_argument("--dev", help="Use if not running on a Raspberry Pi.",
                    action="store_true")
args= parser.parse_args()
if not args.dev:
    from picamera import PiCamera
    is_raspberry_pi = True


class App:
    def __init__(self, master):
        self.master = master
        master.bind("<Escape>", self.live_preview_stop)

        ### setup frames
        self.frame = Frame(master)
        self.frame.place(x = 0, y = 0, width =  1200, height = 732)

        self.keep_video_running = False

        ### setup button size and padding
        self.button_ipady = 31
        self.button_ipadx = 25

        # read config file
        self.config, self.config_parser = conf.read_config()
        self.stream = BytesIO()
        self.video_resolution = self.config['Video']['VideoResolution']
        self.resolution = self.config['Video']['ImageResolution']
        self.preview_resolution = self.config['Video']['PreviewResolution']
        self.video_timer = self.config['Video']['VideoTimer']
        self.iso_value = 100
        self.hflip_var = BooleanVar()
        self.hflip_var.set(False)
        self.vflip_var = BooleanVar()
        self.vflip_var.set(False)
        self.ftp_host = self.config['FTP']['Host']
        self.ftp_user = self.config['FTP']['User']
        self.ftp_password = self.config['FTP']['Password']

        # icons
        busy_icon = str(os.getcwd()) + '/ap/busy.png'
        self.busy_icon = ImageTk.PhotoImage(Image.open(busy_icon),
            Image.ANTIALIAS)
        idle_icon = str(os.getcwd()) + '/ap/idle.png'
        self.idle_icon = ImageTk.PhotoImage(Image.open(idle_icon),
            Image.ANTIALIAS)

        ### load preview image
        preview_img =  str(os.getcwd()) + '/ap/preview.png'
        self.img = ImageTk.PhotoImage(
            Image.open(preview_img).resize(self.preview_resolution),
            Image.ANTIALIAS)
        #self.photo_ref = self.img


        ### preview picture
        self.label = Label(self.frame, image = self.img)
        self.label.place(x = 0,y = 0)
        print("loaded")

        ### buttons
        self.update_preview_image_btn = Button(self.frame,
            text="update preview image",
            font=("Arial", 16),
            command = self.update_preview_image)
        self.update_preview_image_btn.place(x = 801, y = 0, width = 400, height = 100)

        self.new_preview_btn = Button(self.frame,
            font=("Arial", 16),
            text="live preview (esc)",
            command = self.live_preview)
        self.new_preview_btn.place(x = 801, y = 101, width = 400, height = 100)

        self.save_image_btn = Button(self.frame,
            font=("Arial", 16),
            text="save new image",
            command = self.save_image)
        self.save_image_btn.place(x = 801, y = 201, width = 400, height = 100)

        self.save_low_light_image_btn = Button(self.frame,
            text="save new low light image (30s exposure)",
            font=("Arial", 16),
            command = self.save_low_light_image)
        self.save_low_light_image_btn.place(x = 801, y = 301, width = 400, height = 100)

        self.record_video_btn = Button(self.frame,
            text="record video (" + str(self.video_timer) + "s)",
            font=("Arial", 16),
            command = self.record_video)
        self.record_video_btn.place(x = 801, y = 401, width = 400, height = 100)

        self.settings_btn = Button(self.frame,
            text = "settings",
            font=("Arial", 16),
            command = self.open_settings_window)
        self.settings_btn.place(x = 801, y = 501, width = 400, height = 100)

        self.quit_btn = Button(self.frame,
            text = "quit",
            font=("Arial", 16),
            command = self.frame.quit)
        self.quit_btn.place(x = 801, y = 601, width = 400, height = 100)

        ### options
        self.label_iso = Label(self.frame,
            text = "ISO " + str(self.iso_value),
            font = ("Arial", 16),
            padx = 5)
        self.label_iso.place(x = 132, y = 601, width = 131, height = 131)

        self.increase_iso_btn = Button(self.frame,
            font = ("Arial", 16),
            text = "+",
            command = self.camera_iso_inc)
        self.increase_iso_btn.place(x = 263, y = 601, width = 131, height = 131)

        self.decrease_iso_btn = Button(self.frame,
            font = ("Arial", 16),
            text = "-",
            command = self.camera_iso_dec)
        self.decrease_iso_btn.place(x = 0, y = 601, width = 131, height = 131)

        self.hflip_option = Checkbutton(self.frame,
            text="flip horizontal",
            font=("Arial", 16),
            variable=self.hflip_var)
        self.hflip_option.place(x = 394, y = 601, width = 200, height = 131)

        self.vflip_option = Checkbutton(self.frame,
            text="flip vertical",
            font=("Arial", 16),
            variable=self.vflip_var)
        self.vflip_option.place(x = 594, y = 601, width = 200, height = 131)

        self.icon_label = Label(self.frame, image = self.idle_icon)
        self.icon_label.place(x = 1184, y = 716, width = 16, height = 16)

    # open new Window. let user enter config settings.
    # save, then return to main window
    def open_settings_window(self):
        self.settings_window = Toplevel(self.master)
        self.settings_window.grab_set() # no input in main window
        self.settings_window.attributes('-topmost', True) # stay on top of main window
        self.settings_window.title('settings')
        self.settings_window.geometry('280x255')
        
        self.video_label = Label(self.settings_window, text = 'Video resolution', font=("Arial", 10))
        self.video_label.place(x = 5, y = 5)
        self.video_resolution_entry = Entry(self.settings_window)
        self.video_resolution_string = tkinter.StringVar()
        self.video_resolution_string.set(str(self.video_resolution[0]) + "x" + str(self.video_resolution[1]))
        self.video_resolution_entry["textvariable"] = self.video_resolution_string
        self.video_resolution_entry.place(x = 120, y = 5)
        
        self.image_label = Label(self.settings_window, text = 'Image resolution', font=("Arial", 10))
        self.image_label.place(x = 5, y = 35)
        self.image_resolution_entry = Entry(self.settings_window)
        self.image_resolution_string = tkinter.StringVar()
        self.image_resolution_string.set(str(self.resolution[0]) + "x" + str(self.resolution[1]))
        self.image_resolution_entry["textvariable"] = self.image_resolution_string
        self.image_resolution_entry.place(x = 120, y = 35)

        self.preview_label = Label(self.settings_window, text = 'Preview resolution', font=("Arial", 10))
        self.preview_label.place(x = 5, y = 65)
        self.preview_resolution_entry = Entry(self.settings_window)
        self.preview_resolution_string = tkinter.StringVar()
        self.preview_resolution_string.set(str(self.preview_resolution[0]) + "x" + str(self.preview_resolution[1]))
        self.preview_resolution_entry["textvariable"] = self.preview_resolution_string
        self.preview_resolution_entry.place(x = 120, y = 65)

        self.video_timer_label = Label(self.settings_window, text = 'Video timer', font=("Arial", 10))
        self.video_timer_label.place(x = 5, y = 95)
        self.video_timer_entry = Entry(self.settings_window)
        self.video_timer_string = tkinter.StringVar()
        self.video_timer_string.set(str(self.video_timer))
        self.video_timer_entry["textvariable"] = self.video_timer_string
        self.video_timer_entry.place(x = 120, y = 95)

        self.ftp_host_label = Label(self.settings_window, text = 'FTP Host', font=("Arial", 10))
        self.ftp_host_label.place(x = 5, y = 125)
        self.ftp_host_entry = Entry(self.settings_window)
        self.ftp_host_string = tkinter.StringVar()
        self.ftp_host_string.set(self.ftp_host)
        self.ftp_host_entry["textvariable"] = self.ftp_host_string
        self.ftp_host_entry.place(x = 120, y = 125)
        
        self.ftp_user_label = Label(self.settings_window, text = 'FTP User', font=("Arial", 10))
        self.ftp_user_label.place(x = 5, y = 155)
        self.ftp_user_entry = Entry(self.settings_window)
        self.ftp_user_string = tkinter.StringVar()
        self.ftp_user_string.set(self.ftp_user)
        self.ftp_user_entry["textvariable"] = self.ftp_user_string
        self.ftp_user_entry.place(x = 120, y = 155)

        self.ftp_password_label = Label(self.settings_window, text = 'FTP Password', font=("Arial", 10))
        self.ftp_password_label.place(x = 5, y = 185)
        self.ftp_password_entry = Entry(self.settings_window)
        self.ftp_password_entry = Entry(self.settings_window)
        self.ftp_password_string = tkinter.StringVar()
        self.ftp_password_string.set(self.ftp_password)
        self.ftp_password_entry["textvariable"] = self.ftp_password_string
        self.ftp_password_entry.place(x = 120, y = 185)

        self.save_settings_btn = Button(self.settings_window,
            text = "speichern",
            font=("Arial", 10),
            command = lambda: conf.save_config(self))
        self.save_settings_btn.place(x = 5, y = 215, width = 100, height = 30)

        self.close_settings_btn = Button(self.settings_window,
            text = "schliessen",
            font=("Arial", 10),
            command = self.settings_window.destroy)
        self.close_settings_btn.place(x = 120, y = 215, width = 100, height = 30)

    def update_icon(self, busy):
        self.icon_label.configure(
            image = (self.busy_icon if busy == True else self.idle_icon))
        self.master.update_idletasks()
        self.master.update()

    def camera_iso_inc(self):
        allowed = (100, 200, 300, 400, 800)
        current_iso = self.iso_value
        for i in allowed:
            if (i == current_iso and i != max(allowed)) or i < current_iso:
                pass
            else:
                self.label_iso.configure(text = "ISO " + str(i))
                self.iso_value = i
                break

    def camera_iso_dec(self):
        allowed = (800, 400, 300, 200, 100)
        current_iso = self.iso_value
        for i in allowed:
            if (i == current_iso and i != min(allowed)) or i > current_iso:
                pass
            else:
                self.label_iso.configure(text = "ISO " + str(i))
                self.iso_value = i
                break

    def setup_camera(self, resolution):
        camera = PiCamera()
        camera.resolution = resolution
        camera.vflip = self.vflip_var.get()
        camera.hflip = self.hflip_var.get()
        camera.iso = self.iso_value
        sleep(2)
        self.stream.seek(0)
        return camera

    def update_preview_image(self):
        self.update_icon(True)
        if (is_raspberry_pi): 
            camera = self.setup_camera(self.preview_resolution)
            camera.capture(self.stream, format='jpeg')

            self.stream.seek(0)
            self.img = ImageTk.PhotoImage(Image.open(self.stream),
                Image.ANTIALIAS)
            self.label.configure(image = self.img)
            self.photo_ref = self.img

            camera.close()
        self.update_icon(False)
        print("preview updated")

    def get_filename(self):
        homestr = str(Path.home())
        timestr = time.strftime("%Y%m%d-%H%M%S")
        return homestr + '/Pictures/' + timestr + '.jpg'

    def get_video_filename(self):
        homestr = str(Path.home())
        timestr = time.strftime("%Y%m%d-%H%M%S")
        return homestr + '/Videos/' + timestr + '.h264'

    def save_image(self):
        self.update_icon(True)
        if (is_raspberry_pi): 
            filename = self.get_filename()
            camera = self.setup_camera(self.resolution)
            camera.capture(filename)

            self.img = ImageTk.PhotoImage(Image.open(filename).resize(
                self.preview_resolution), Image.ANTIALIAS)
            self.label.configure(image = self.img)
            self.photo_ref = self.img

            camera.close()
        self.update_icon(False)
        print("image saved")


    def save_low_light_image(self):
        self.update_icon(True)
        if (is_raspberry_pi): 
            filename = self.get_filename()

            camera = self.setup_camera(self.resolution)
            camera.framerate = Fraction(1, 6)
            camera.sensor_mode = 3
            camera.shutter_speed = 6000000
            camera.exposure_mode = 'off'

            """camera = PiCamera(
                resolution = self.resolution,
                framerate = Fraction(1, 6),
                sensor_mode = 3)
            camera.shutter_speed = 6000000

            camera.iso = self.iso_value
            camera.vflip = self.vflip_var.get()
            camera.hflip = self.hflip_var.get()"""

            # setup_camera sleeps 2 seconds, we want 30
            sleep(28)

            camera.capture(filename)

            self.img = ImageTk.PhotoImage(
                Image.open(filename).resize(self.preview_resolution),
                Image.ANTIALIAS)
            self.label.configure(image = self.img)
            self.photo_ref = self.img

            camera.close()
        self.update_icon(False)
        print("low light image saved")

    def live_preview(self):
        self.update_icon(True)
        if (is_raspberry_pi): 
            camera = self.setup_camera(self.preview_resolution)
            self.keep_video_running = True
            with camera:
                for foo in camera.capture_continuous(self.stream,
                        format='jpeg', use_video_port = True):
                    self.img = ImageTk.PhotoImage(
                        Image.open(self.stream), Image.ANTIALIAS)
                    self.label.configure(image = self.img)
                    self.photo_ref = self.img
                    self.stream.seek(0)
                    self.master.update_idletasks()
                    self.master.update()
                    if self.keep_video_running == False:
                        break
            camera.close()
        self.update_icon(False)
        print("preview stopped")

    def live_preview_stop(self, event):
        self.keep_video_running = False

    def record_video(self):
        self.update_icon(True)
        if (is_raspberry_pi): 
            camera = self.setup_camera(self.video_resolution)
            camera.framerate = 25
            camera.start_recording(self.get_video_filename())
            camera.wait_recording(self.video_timer)
            camera.stop_recording()

            camera.close()
            self.update_icon(False)
        print("video saved")
        

root = Tk()
root.geometry("1200x732+0+0")
root.title("Astrophotography")
app = App(root)
root.mainloop()
