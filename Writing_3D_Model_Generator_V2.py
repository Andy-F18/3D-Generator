import datetime
import os


def write_obj(obj, name, app):
    file = open("Models/"+name+".obj", "w+")

    file.write("# {}\t{}\n".format(datetime.date.today(), datetime.datetime.now().strftime("%H:%M:%S")))
    file.write("# 3D Model Generator\n")

    n = 0
    p0 = -1
    t_p = 20
    c = len(obj)
    for o in obj:
        p = round((n/c*100)/t_p)
        if p != p0:
            app.add_log("Saving... {}%".format(p*t_p))
            p0 = p
        write_cube(file, create_cube(o[0], o[2], o[1], n))
        n += 1

    file.close()

    return os.path.getsize("Models/"+name+".obj")


def create_cube(x, y, z, n):
    name = "o Cube_{}\n".format(n)
    v1 = "v {} {} {}\n".format(float(x), float(y), float(z))
    v2 = "v {} {} {}\n".format(float(1+x), float(y), float(z))
    v3 = "v {} {} {}\n".format(float(1+x), float(1+y), float(z))
    v4 = "v {} {} {}\n".format(float(x), float(1+y), float(z))

    v5 = "v {} {} {}\n".format(float(x), float(y), float(1+z))
    v6 = "v {} {} {}\n".format(float(1+x), float(y), float(1+z))
    v7 = "v {} {} {}\n".format(float(1+x), float(1+y), float(1+z))
    v8 = "v {} {} {}\n".format(float(x), float(1+y), float(1+z))

    f1 = "f {} {} {} {}\n".format(1+n*8, 2+n*8, 3+n*8, 4+n*8)
    f2 = "f {} {} {} {}\n".format(1+n*8, 2+n*8, 6+n*8, 5+n*8)
    f3 = "f {} {} {} {}\n".format(2+n*8, 3+n*8, 7+n*8, 6+n*8)
    f4 = "f {} {} {} {}\n".format(3+n*8, 4+n*8, 8+n*8, 7+n*8)
    f5 = "f {} {} {} {}\n".format(4+n*8, 1+n*8, 5+n*8, 8+n*8)
    f6 = "f {} {} {} {}\n".format(5+n*8, 6+n*8, 7+n*8, 8+n*8)

    cube = [name,
            v1, v2, v3, v4, v5, v6, v7, v8,
            f1, f2, f3, f4, f5, f6]

    return cube


def write_cube(file, cube):
    for l in cube:
        file.write(l)