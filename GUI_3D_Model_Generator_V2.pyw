import os
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

import Script_3D_Model_Generator_V2 as Gene
import Writing_3D_Model_Generator_V2 as Write


class App:
    def __init__(self):
        try:
            os.mkdir("Models")
        except FileExistsError:
            pass

        self.bg = "#ccc"
        self.bg_butt = "#eee"
        self.bg_not_ok = "#f55"
        self.bg_ok = "#4b4"

        self.root = tk.Tk()
        self.root.title("3D Model Generator")

        # ##################### dimension + window position ######################
        w = 1225
        h = 750
        self.root.configure(background=self.bg)
        p_r = int(self.root.winfo_screenwidth() / 2 - w / 2)
        p_d = int(self.root.winfo_screenheight() / 2 - h / 2 - 50)
        self.root.geometry("{}x{}+{}+{}".format(w, h, p_r, p_d))

        # ##################### presentation ######################
        l_titre = tk.Label(self.root, text="3D Model Generator", font=("Calibri", 30), bg=self.bg)
        l_titre.pack(padx=10, pady=20)

        # ##################### widgets import ######################
        f_control = tk.Frame(self.root, bg=self.bg)
        self.f_plan = tk.LabelFrame(f_control, bg=self.bg, text="Plan")

        # disposition
        #   0X
        #   00
        self.files = {
            'up': "",
            'front': "",
            'side': ""
        }

        self.imgs = {
            'up': Image.Image(),
            'front': Image.Image(),
            'side': Image.Image()
        }

        c = 200
        self.can_up = tk.Canvas(self.f_plan, width=c, height=c, bg="black")
        self.can_up.bind("<Button-1>", self.pos_can)
        self.can_up.grid(row=0, column=0, padx=5, pady=5)

        self.can_front = tk.Canvas(self.f_plan, width=c, height=c, bg="black")
        self.can_front.bind("<Button-1>", self.pos_can)
        self.can_front.grid(row=1, column=0, padx=5, pady=5)

        self.can_side = tk.Canvas(self.f_plan, width=c, height=c, bg="black")
        self.can_side.bind("<Button-1>", self.pos_can)
        self.can_side.grid(row=1, column=1, padx=5, pady=5)

        self.f_plan.pack()

        # ##################### widgets control ######################
        self.b_verif = tk.Button(f_control, text="Verify", state=tk.DISABLED, command=self.verify, font=("Bold", 15),
                                 bg=self.bg_butt)
        self.b_verif.pack(pady=10)

        self.b_generate = tk.Button(f_control, text="Generate", state=tk.DISABLED, font=("Bold", 15),
                                    command=self.generate, bg=self.bg_butt)
        self.b_generate.pack()

        f_control.pack(side=tk.LEFT, padx=10)

        # ##################### widgets colors order ######################
        self.colors_list = {
            "white": {
                "val": (255, 255, 255),
                "op": "ADD",
                "ch": False,
                "frame": tk.Frame
            }
        }

        f_colors = tk.LabelFrame(self.root, text="Colors order", bg=self.bg)
        self.f_list = tk.Frame(f_colors, bg="#eee")

        f_order = tk.Frame(f_colors, bg=self.bg)
        tk.Button(f_order, text="\u21E7", command=lambda: self.change_order("up"), bg=self.bg_butt,
                  width=3).pack()  # up
        tk.Button(f_order, text="\u21E9", command=lambda: self.change_order("down"), bg=self.bg_butt,
                  width=3).pack()  # down

        tk.Button(f_order, text="ADD", command=lambda: self.change_order("ADD"), bg=self.bg_butt, width=3).pack()  # ADD
        tk.Button(f_order, text="SUB", command=lambda: self.change_order("SUB"), bg=self.bg_butt, width=3).pack()  # SUB

        f_colors.pack(side=tk.LEFT, padx=10)
        self.f_list.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.NW)
        f_order.pack(side=tk.LEFT, pady=5, padx=5)

        for c in self.colors_list:
            self.colors_list[c]["frame"] = tk.LabelFrame(self.f_list, bg=self.bg)

            tk.Canvas(self.colors_list[c]["frame"], width=10, height=10,
                      bg=self.col_to_hex(self.colors_list[c]["val"]),
                      highlightbackground="black", highlightthickness=1).pack(side=tk.LEFT, padx=2)

            tk.Label(self.colors_list[c]["frame"], text=self.colors_list[c]["op"],
                     bg=self.bg, width=4).pack(side=tk.LEFT)
            self.colors_list[c]["frame"].pack()

        self.selec = None

        # ##################### widgets logs ######################
        f_logs = tk.LabelFrame(self.root, text="Logs", bg=self.bg)

        self.logs = tk.Text(f_logs, width=70, height=25, wrap="none", state=tk.DISABLED)
        screen_yscroll = tk.Scrollbar(f_logs)
        screen_yscroll.configure(command=self.logs.yview)

        self.logs.pack(side=tk.LEFT, padx=5, pady=5)
        screen_yscroll.pack(side=tk.LEFT, fill=tk.Y)
        self.logs.configure(state=tk.DISABLED, yscrollcommand=screen_yscroll.set)

        f_logs.pack(side=tk.LEFT, padx=10)

        self.root.mainloop()

    @staticmethod
    def col_to_hex(col):
        r = hex(col[0]).replace("0x", "")
        if len(r) == 1:
            r = "0" + r
        g = hex(col[1]).replace("0x", "")
        if len(g) == 1:
            g = "0" + g
        b = hex(col[2]).replace("0x", "")
        if len(b) == 1:
            b = "0" + b

        return "#" + r + g + b

    def add_color(self, col):
        n = len(self.colors_list)
        c = "color" + str(n)
        if n % 2 == 1:
            op = "SUB"
        else:
            op = "ADD"

        self.colors_list[c] = {
            "val": col,
            "op": op,
            "ch": True,
            "frame": {
                "frame": tk.Frame,
                "text": tk.Label
            }
        }

        self.colors_list[c]["frame"]["frame"] = tk.LabelFrame(self.f_list, bg=self.bg)

        can = tk.Canvas(self.colors_list[c]["frame"]["frame"], width=10, height=10,
                        bg=self.col_to_hex(self.colors_list[c]["val"]),
                        highlightbackground="black", highlightthickness=1)
        can.pack(side=tk.LEFT, padx=2)
        can.bind("<Button-1>", lambda eff: self.selec_color(c))

        self.colors_list[c]["frame"]["text"] = tk.Label(self.colors_list[c]["frame"]["frame"],
                                                        text=self.colors_list[c]["op"], bg=self.bg, width=4)
        self.colors_list[c]["frame"]["text"].pack(side=tk.LEFT)
        self.colors_list[c]["frame"]["text"].bind("<Button-1>", lambda eff: self.selec_color(c))

        self.colors_list[c]["frame"]["frame"].pack()
        self.colors_list[c]["frame"]["frame"].bind("<Button-1>", lambda eff: self.selec_color(c))

    def selec_color(self, col):
        if self.selec is None:
            self.colors_list[col]["frame"]["frame"].config(bg="#59f")
            self.colors_list[col]["frame"]["text"].config(bg="#59f")
            self.selec = col

        else:
            if self.selec == col:
                self.colors_list[col]["frame"]["frame"].config(bg=self.bg)
                self.colors_list[col]["frame"]["text"].config(bg=self.bg)
                self.selec = None

            else:

                self.colors_list[self.selec]["frame"]["frame"].config(bg=self.bg)
                self.colors_list[self.selec]["frame"]["text"].config(bg=self.bg)

                self.colors_list[col]["frame"]["frame"].config(bg="#59f")
                self.colors_list[col]["frame"]["text"].config(bg="#59f")
                self.selec = col

    def change_order(self, sens):
        if self.selec is None:
            return

        co = []
        for c in self.colors_list:
            co.append(c)
        i = co.index(self.selec)
        co.pop(i)

        if sens == "up":
            if i == 1:
                return
            else:
                co.insert(i - 1, self.selec)
                n_color = {}
                for c in co:
                    n_color[c] = self.colors_list[c]

                self.colors_list = n_color.copy()

        elif sens == "down":
            if i > len(co):
                return
            else:
                co.insert(i + 1, self.selec)
                n_color = {}
                for c in co:
                    n_color[c] = self.colors_list[c]

                self.colors_list = n_color.copy()

        elif sens == "ADD" or sens == "SUB":
            self.colors_list[self.selec]["op"] = sens
            self.colors_list[self.selec]["frame"]["text"].config(text=sens)

        for c in self.colors_list:
            if c == "white":
                self.colors_list[c]["frame"].pack_forget()
            else:
                self.colors_list[c]["frame"]["frame"].pack_forget()

        n = 0
        for c in self.colors_list:
            if c == "white":
                self.colors_list[c]["frame"].pack()
            else:
                self.colors_list[c]["frame"]["frame"].pack()
            n += 1

    def verify(self):
        self.add_log("--------------------------- VERIFICATIONS ----------------------------")
        up_size = self.imgs['up'].size
        front_size = self.imgs['front'].size
        side_size = self.imgs['side'].size

        if up_size == front_size == side_size:
            self.add_log("Images dimensions : OK")
        else:
            self.add_log("Images dimensions : NOT OK")
            return False

        x_ok = Gene.verif_x(self.imgs)
        if x_ok:
            self.add_log("Axe X : OK")
        else:
            self.add_log("Axe X : NOT OK")

        y_ok = Gene.verif_y(self.imgs)
        if y_ok:
            self.add_log("Axe Y : OK")
        else:
            self.add_log("Axe Y : NOT OK")

        z_ok = Gene.verif_z(self.imgs)
        if z_ok:
            self.add_log("Axe Z : OK")
        else:
            self.add_log("Axe Z : NOT OK")

        if x_ok and y_ok and z_ok:
            self.add_log("Axis checked : OK")
            self.b_verif.config(bg=self.bg_ok, state=tk.DISABLED)
            self.b_generate.config(state=tk.NORMAL)
        else:
            self.add_log("Axis checked : NOT OK")

        for y in range(0, self.imgs["up"].size[1]):
            for x in range(0, self.imgs["up"].size[0]):
                col = self.imgs["up"].getpixel((x, y))
                col = (col[0], col[1], col[2])
                if not (col[0] <= 5 and col[1] <= 5 and col[2] <= 5):
                    if not self.col_exist(col):
                        self.add_color(col)

    def col_exist(self, col):
        for c in self.colors_list:
            R = self.colors_list[c]["val"][0] - 5 <= col[0] <= self.colors_list[c]["val"][0] + 5
            G = self.colors_list[c]["val"][1] - 5 <= col[1] <= self.colors_list[c]["val"][1] + 5
            B = self.colors_list[c]["val"][2] - 5 <= col[2] <= self.colors_list[c]["val"][2] + 5

            if R and G and B:
                return True

        return False

    def generate(self):
        obj = Gene.generate(self)
        self.add_log("Generation complet")
        self.add_log("------------------------------- SAVING -------------------------------")

        pop_name = tk.Toplevel(self.root, bg=self.bg)
        pop_name.title("Name object")
        w = 300
        h = 100
        pR = int(pop_name.winfo_screenwidth() / 2 - w / 2)
        pD = int(pop_name.winfo_screenheight() / 2 - h / 2 - 50)
        pop_name.geometry("{}x{}+{}+{}".format(w, h, pR, pD))

        f_name = tk.LabelFrame(pop_name, text="Choose a name", bg=self.bg)

        name = tk.StringVar()
        e_name = tk.Entry(f_name, textvariable=name, width=20)
        e_name.pack(side=tk.LEFT, padx=5, pady=5)

        b_name = tk.Button(f_name, text="Valid", command=self.out)
        b_name.pack(side=tk.LEFT, padx=5, pady=5)

        f_name.pack(padx=10, pady=10)

        pop_name.grab_set()
        self.root.wait_window(pop_name)

        if name.get() != "":
            self.add_log("Object name : {}".format(name.get()))

            self.add_log("Begin saving")
            size = Write.write_obj(obj, name.get(), self)
            self.add_log("Object {}.obj saved [{}Ko]".format(name.get(), int(size / 1000)))
        else:
            self.add_log("Object not saved")

    def out(self):
        k = list(self.root.children.keys())
        s = self.root.children.get(k[len(k) - 1])
        s.destroy()

    def pos_can(self, event):
        file = self.__browseFiles()
        self.b_verif.config(bg=self.bg_butt)

        if file == "":
            return

        img = Image.open(file)
        re_img = self.resize(img)

        photo = ImageTk.PhotoImage(re_img)
        event.widget.config(width=re_img.size[0], height=re_img.size[1])
        event.widget.image = photo
        event.widget.create_image(0, 0, anchor=tk.NW, image=event.widget.image)

        if event.widget.winfo_id() == self.can_up.winfo_id():
            self.files['up'] = file
            self.imgs['up'] = img
            self.add_log("Up image added:     {}  ({}X{})".format(file.split("/")[len(file.split("/")) - 1],
                                                                  img.size[0], img.size[1]))

        elif event.widget.winfo_id() == self.can_front.winfo_id():
            self.files['front'] = file
            self.imgs['front'] = img
            self.add_log("Front image added:  {}  ({}X{})".format(file.split("/")[len(file.split("/")) - 1],
                                                                  img.size[0], img.size[1]))

        elif event.widget.winfo_id() == self.can_side.winfo_id():
            self.files['side'] = file
            self.imgs['side'] = img
            self.add_log("Side image added:   {}  ({}X{})".format(file.split("/")[len(file.split("/")) - 1],
                                                                  img.size[0], img.size[1]))

        if self.files["up"] != "" and self.files['front'] != "" and self.files['side'] != "":
            self.b_verif.config(state=tk.NORMAL)
        else:
            self.b_verif.config(state=tk.DISABLED)

        # print(self.files)

    def add_log(self, txt):
        self.logs.config(state=tk.NORMAL)

        self.logs.insert(tk.END, txt + "\n")

        self.logs.config(state=tk.DISABLED)
        self.logs.update()
        self.logs.see(tk.END)

    @staticmethod
    def resize(img):
        c = 200
        re_img = Image.new(mode="RGB", size=(c, c))
        re_pix = re_img.load()

        rx = img.size[0] / c
        ry = img.size[1] / c

        for x in range(0, c):
            for y in range(0, c):
                re_pix[x, y] = img.getpixel((int(x * rx), int(y * ry)))

        return re_img

    @staticmethod
    def __browseFiles():
        file = ""

        rep = os.path.abspath(os.getcwd())
        filename_s = filedialog.askopenfilename(initialdir=rep,
                                                title="Select a File",
                                                filetypes=(("PNG files", "*.png"),
                                                           ("all files", "*.*")))
        if filename_s != "":
            filename = filename_s
        else:
            filename = file
        # Change label contents
        file = filename

        return file


if __name__ == '__main__':
    win = App()
