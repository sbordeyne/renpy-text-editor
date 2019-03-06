import tkinter as tk
import tkinter.ttk as ttk
import mp3play

class SoundViewer(tk.Frame):
    def __init__(self, master=None, fpath=None):
        super().__init__(master)
        self.pbar = ttk.Progressbar(self)
        self.fpath = fpath
        self.time_elapsed = tk.IntVar()
        self.time_elapsed.set(0)  # seconds
        self.volume = tk.IntVar()
        self.volume.set(80)
        self.clip = mp3play.load(fpath)
        self.paused = True
        self.started = False

        self.pbar.config(orient="horizontal",
                         length=300,
                         variable=self.time_elapsed,
                         mode="determinate",
                         maximum=self.clip.milliseconds())

        self.pbar.grid(row=0, column=0, columnspan=10)
        self.play_pause_btn = tk.Button(self,
                                        bitmap=tk.BitmapImage("@assets/button-play.xbm"),
                                        command=self.toggle_pause)
        self.stop_btn = tk.Button(self,
                                  bitmap=tk.BitmapImage("@assets/button-stop.xbm"),
                                  command=self.stop)
        self.volume_scl = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL,
                                   variable=self.volume,
                                   )
        self.volume_lbl = tk.Label(self, bitmap=tk.BitmapImage("@assets/volume-icon.xbm"))
        self.play_pause_btn.grid(row=1, column=8)
        self.stop_btn.grid(row=1, column=9)
        self.volume_lbl.grid(row=1, column=0)
        self.volume_scl.grid(row=1, column=1)
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.loop()

    def toggle_pause(self):
        if self.paused:
            print("play")
            self.play()
        else:
            print("pause")
            self.pause()

    def play(self, *args):
        self.play_pause_btn.config(bitmap=tk.BitmapImage("@assets/button-pause.xbm"))
        self.paused = False
        self.clip.play(start_ms=self.time_elapsed.get())

    def pause(self, *args):
        self.play_pause_btn.config(bitmap=tk.BitmapImage("@assets/button-play.xbm"))
        self.paused = True
        self.clip.pause()

    def stop(self, *args):
        self.clip.stop()
        self.time_elapsed.set(0)
        self.paused = True
        self.play_pause_btn.config(bitmap=tk.BitmapImage("@assets/button-play.xbm"))

    def set_volume(self, *args):
        return
        vol = 0
        if args:
            vol = args[0]
        else:
            vol = self.volume.get()
        self.clip.volume(vol / 10)

    def quit(self):
        self.stop()
        self.master.destroy()

    def loop(self):
        if not self.paused:
            self.time_elapsed.set(self.time_elapsed.get() + 1)
        self.set_volume()
        self.after(1, self.loop)
