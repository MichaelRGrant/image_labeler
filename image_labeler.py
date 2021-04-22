import glob
import os
from tkinter import *
from tkinter import ttk
from typing import ClassVar

from PIL import Image, ImageTk


class LabelImages:
    """
    TKInter image labeler. This will show all images within a folder and allow
    the user to quickly label those images in a binary fashion. After labeling is complete,
    the labels get saved as a binary vector.
    """

    def __init__(self, root: ClassVar, path: str):
        """
        root: Tk Inter class object
        path: str
            path to the directory of images to be labeled
        """
        self.root = root
        self.images = []
        self.check_dict = {}
        self.path = path

        self.cols = 15
        for i in range(len(glob.glob(os.path.join(self.path, "*")))):
            self.check_dict[i] = IntVar()

        self.label = ttk.Label(
            self.root,
            text="Click each picture that shows a colony. When complete, click Finished Labeling at bottom.",
            justify="center",
            background="blue",
            foreground="black",
            font=(
                "Times",
                18,
            ),
        )  # child of the master

        self.label.pack(side="top", fill="both", expand=False)

        self.finish = ttk.Button(
            self.root, text="Finished Labeling", command=self.get_response
        )
        self.finish.pack(side="bottom", expand=False)

        self.canvas = Canvas(self.root)
        self.frame = Frame(self.canvas)
        self.vsb = ttk.Scrollbar(
            self.root, orient="vertical", command=self.canvas.yview
        )
        self.hsb = ttk.Scrollbar(
            self.root, orient="horizontal", command=self.canvas.xview
        )
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((10, 10), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    def populate(self):
        image_count = 0
        for i, infile in enumerate(glob.glob(os.path.join(self.path, "*"))):
            self.check_dict[i].set(0)
            image_count += 1
            r, c = divmod(image_count - 1, self.cols)

            self.cb = ttk.Checkbutton(
                self.frame,
            )
            self.cb.grid(row=r, column=c)

            im = Image.open(infile)
            resized = im.resize((64, 64), Image.ANTIALIAS)
            self.tkimage = ImageTk.PhotoImage(resized)
            self.cb.config(
                image=self.tkimage,
                variable=self.check_dict[i],
                onvalue=1,
                offvalue=0,
            )
            self.images.append(self.tkimage)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get_response(self):
        self.response = [
            self.check_dict[i].get()
            for i in range(len(glob.glob(os.path.join(self.path, "*"))))
        ]
        self.root.destroy()


def run_labeler(path) -> list:
    """
    Run the TkInter labeler.

    Parameters:
    -------
    path: str

    Returns:
    -------
    list
        A binary vecotry (list) of image labels.
    """
    root = Tk()
    app = LabelImages(root, path)
    root.title("Image Labeler")
    root.mainloop()
    return app.response
