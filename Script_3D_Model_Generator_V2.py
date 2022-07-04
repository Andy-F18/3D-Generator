import pprint

import numpy as np


def verif_x(imgs):
    img_front = imgs['front']
    img_up = imgs['up']

    Xz = np.zeros(img_front.size[0])
    for x in range(0, img_front.size[0]):
        for z in range(0, img_front.size[1]):
            color = img_front.getpixel((x, img_front.size[1] - 1 - z))

            if color[0] != 0 or color[1] != 0 or color[2] != 0:
                Xz[x] += 1

    Xy = np.zeros(img_up.size[1])
    for x in range(0, img_up.size[0]):
        for y in range(0, img_up.size[1]):
            color = img_up.getpixel((x, img_up.size[1] - 1 - y))

            if color[0] != 0 or color[1] != 0 or color[2] != 0:
                Xy[x] += 1

    X1 = transform_axis(Xz)
    X2 = transform_axis(Xy)

    if equals(X1, X2):
        return True

    return False


def verif_y(imgs):
    img_up = imgs['up']
    img_side = imgs['side']

    Yx = np.zeros(img_up.size[1])
    for y in range(0, img_up.size[1]):
        for x in range(0, img_up.size[0]):
            color = img_up.getpixel((x, img_up.size[1] - 1 - y))

            if color[0] != 0 or color[1] != 0 or color[2] != 0:
                Yx[y] += 1

    Yz = np.zeros(img_side.size[0])
    for y in range(0, img_side.size[0]):
        for z in range(0, img_side.size[1]):
            color = img_side.getpixel((y, img_side.size[1] - 1 - z))

            if color[0] != 0 or color[1] != 0 or color[2] != 0:
                Yz[y] += 1

    Y1 = transform_axis(Yx)
    Y2 = transform_axis(Yz)

    if equals(Y1, Y2):
        return True

    return False


def verif_z(imgs):
    img_side = imgs['side']
    img_front = imgs['front']

    Zy = np.zeros(img_side.size[1])
    for z in range(0, img_side.size[1]):
        for y in range(0, img_side.size[0]):
            color = img_side.getpixel((y, img_side.size[1] - 1 - z))

            if color[0] != 0 or color[1] != 0 or color[2] != 0:
                Zy[z] += 1

    Zx = np.zeros(img_front.size[1])
    for z in range(0, img_front.size[1]):
        for x in range(0, img_front.size[0]):
            color = img_front.getpixel((x, img_front.size[1] - 1 - z))

            if color[0] != 0 or color[1] != 0 or color[2] != 0:
                Zx[z] += 1

    Z1 = transform_axis(Zy)
    Z2 = transform_axis(Zx)

    if equals(Z1, Z2):
        return True

    return False


def equals(tab1, tab2):
    if len(tab1) != len(tab2):
        return False

    l = len(tab1)
    for e in range(0, l):
        if tab1[e] != tab2[e]:
            return False

    return True


def transform_axis(tab):
    axe = []
    for e in tab:
        if e > 0:
            axe.append(True)
        else:
            axe.append(False)

    return axe


def generate(app):
    app.add_log("----------------------------- GENERATION -----------------------------")
    app.add_log("Begin generation")

    c = app.imgs['up'].size[0]
    size = (c, c, c)
    app.add_log("Object dimensions : ({}X{}x{})".format(c, c, c))

    obj = [[[False for z in range(0, size[2])] for y in range(0, size[1])] for x in range(0, size[0])]

    masks = {}
    for c in app.colors_list:
        masks[c] = {
            "side": [[]],
            "front": [[]],
            "up": [[]]
        }

        # ret_1 = []
        # ret_2 = []
        # ret_3 = []
        #
        # p_side = mp.Process(target=mask_color, args=(app.imgs['side'], c, app.colors_list, ret_1))
        # p_front = mp.Process(target=mask_color, args=(app.imgs['front'], c, app.colors_list, ret_2))
        # p_up = mp.Process(target=mask_color, args=(app.imgs['up'], c, app.colors_list, ret_3))
        #
        # app.add_log("X {} mask detected".format(c))
        # p_side.start()
        # app.add_log("Y {} mask detected".format(c))
        # p_front.start()
        # app.add_log("Z {} mask detected".format(c))
        # p_up.start()
        #
        # p_side.join()
        # p_front.join()
        # p_up.join()
        #
        # masks[c]["side"] = ret_1
        # app.add_log("X {} mask calculated".format(c))
        # masks[c]["front"] = ret_2
        # app.add_log("Y {} mask calculated".format(c))
        # masks[c]["up"] = ret_3
        # app.add_log("Z {} mask calculated".format(c))
        # app.add_log("----------")

        app.add_log("X {} mask detected".format(c))
        masks[c]["side"] = mask_color(app.imgs['side'], c, app.colors_list)
        app.add_log("X {} mask calculated".format(c))

        app.add_log("Y {} mask detected".format(c))
        masks[c]["front"] = mask_color(app.imgs['front'], c, app.colors_list)
        app.add_log("Y {} mask calculated".format(c))

        app.add_log("Z {} mask detected".format(c))
        masks[c]["up"] = mask_color(app.imgs['up'], c, app.colors_list)
        app.add_log("Z {} mask calculated".format(c))
        app.add_log("----------")

    n = 0
    p0 = -1
    t_p = 20
    app.add_log("Begin object masking")
    obj2 = obj.copy()
    c = size[0]

    for z in range(0, size[2]):
        p = round((n/(c**3)*100)/t_p)
        if p != p0:
            app.add_log("Masking... {}%".format(p*t_p))
            p0 = p

        for y in range(0, size[1]):
            for x in range(0, size[0]):
                for m in masks:
                    if app.colors_list[m]["op"] == "ADD":
                        obj[x][y][z] = obj[x][y][z] or (masks[m]["side"][z][y]
                                                        and masks[m]["front"][z][size[0] - x - 1]
                                                        and masks[m]["up"][y][size[0] - x - 1])
                    else:
                        obj[x][y][z] = obj[x][y][z] and (masks[m]["side"][z][y]
                                                         or masks[m]["front"][z][size[0] - x - 1]
                                                         or masks[m]["up"][y][size[0] - x - 1])

                n += 1

    app.add_log("Object masked")
    app.add_log("----------")

    app.add_log("Begin coordinates calculation")
    coord = calcul_coord(obj2, app, t_p)
    app.add_log("Coordinates calculated : {} cubes".format(len(coord)))

    return coord


def mask_color(img, color, colors, ret=None):
    Xz = []
    c_list = {}

    go = False
    for c in colors:
        if c == color:
            go = True
        if go:
            c_list[c] = True
        else:
            c_list[c] = False

    for z in range(0, img.size[1]):
        Xz.append([])
        for x in range(0, img.size[0]):
            p_color = img.getpixel((x, img.size[0]-1-z))

            c_id = "black"
            for c in colors:
                R = colors[c]["val"][0] - 5 <= p_color[0] <= colors[c]["val"][0] + 5
                G = colors[c]["val"][1] - 5 <= p_color[1] <= colors[c]["val"][1] + 5
                B = colors[c]["val"][2] - 5 <= p_color[2] <= colors[c]["val"][2] + 5

                if R and G and B:
                    c_id = c

            if c_id != "black" and c_list[c_id]:
                if colors[color]["op"] == "ADD":
                    Xz[z].append(True)
                else:
                    Xz[z].append(False)

            else:
                if colors[color]["op"] == "ADD":
                    Xz[z].append(False)
                else:
                    Xz[z].append(True)

    if ret is None:
        return Xz
    else:
        ret = Xz


def calcul_coord(obj, app, t_p):
    c = len(obj)

    coord = []
    n = 0
    p0 = -1
    for z in range(0, c):
        p = round((n/(c**3)*100)/t_p)
        if p != p0:
            app.add_log("Calcule coordinates... {}%".format(p*t_p))
            p0 = p
        for y in range(0, c):
            for x in range(0, c):
                if obj[x][y][z]:
                    coord.append((x, y, z))
                n += 1

    return coord


def print_obj(obj):
    for f in obj:
        pprint.pprint(f)
        print("\n")
