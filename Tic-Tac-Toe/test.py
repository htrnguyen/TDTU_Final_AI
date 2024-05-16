from functools import partial
from tkinter import *

import constant

root = Tk()
root.title("Caro by SAM")
Buts = {}
gioitren = range(1, 21)
gioiduoi = range(381, 401)
gioitrai = [
    1,
    21,
    41,
    61,
    81,
    101,
    121,
    141,
    161,
    181,
    201,
    221,
    241,
    261,
    281,
    301,
    321,
    341,
    361,
    381,
]
gioiphai = [
    20,
    40,
    60,
    80,
    100,
    120,
    140,
    160,
    180,
    200,
    220,
    240,
    260,
    280,
    300,
    320,
    340,
    360,
    380,
    400,
]

vitricothedanh = [0] * 400
# vitricothedanh=[10001,11002,12003,10004,12009,13009,10010]
vitrix = [0] * 200
vitrio = [0] * 200
vitritam = [0] * 200
vitrixr = [0] * 200
vitrior = [0] * 200
khoidaudanh = 0
vitria = [0] * 400
index = 0
ratex = 0
rateo = 0
rate = 0
toadocuoi = 0
toadocuoitam = 0
nhay = 14
ketthuc = 0
khoidaudanh = 0
bat = 0
maxthua = 0
maxf = 0

KHOIDONG = 1111
DATCHO = 2222
COCHO = 3333
TIMCHO = 4444
XOA = 5555
TIM = 6666
SAPXEPCONCHAU = 777


def danhgia():

    global vitrix
    global vitrio
    global rate
    sox1, sox2, sox3, sox4, sox5 = 0, 0, 0, 0, 0
    listmap = [
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
        "ssssssssssssssssssss",
    ]

    listcheotrenphai = [""] * 20
    listcheotraiduoi = [""] * 20
    listcheotraitren = [""] * 20
    listcheoduoiphai = [""] * 20
    listmapdoc = [""] * 20
    for x in vitrix:
        hang = (x - 1) // 20
        cot = (x - 1) % 20
        listmap[hang] = listmap[hang][:cot] + "x" + listmap[hang][cot + 1 :]
    for y in vitrio:
        hang = (y - 1) // 20
        cot = (y - 1) % 20
        listmap[hang] = listmap[hang][:cot] + "o" + listmap[hang][cot + 1 :]

    for cot in range(20):
        for hang in range(20 - cot):
            listcheotrenphai[cot] = (
                listcheotrenphai[cot] + listmap[hang][hang + cot : hang + cot + 1]
            )

    for cheo in range(1, 20):
        for hang in range(20 - cheo):
            listcheotraiduoi[cheo] = (
                listcheotraiduoi[cheo] + listmap[hang + cheo][hang : hang + 1]
            )

    for cot in range(20):
        for hang in range(cot + 1):
            listcheotraitren[cot] = (
                listcheotraitren[cot] + listmap[cot - hang][hang : hang + 1]
            )

    for cheo in range(19):
        for hang in range(cheo + 1):
            listcheoduoiphai[cheo] = (
                listcheoduoiphai[cheo]
                + listmap[19 - hang][19 + hang - cheo : 20 + hang - cheo]
            )

    for cot in range(20):
        for hang in range(20):
            listmapdoc[cot] = listmapdoc[cot] + listmap[hang][cot : cot + 1]

    for kiemt in range(20):

        sox2 = listmap[kiemt].count("ssxxs") + sox2
        sox2 = listmap[kiemt].count("sxxss") + sox2
        sox2 = listmap[kiemt].count("sxsxs") + sox2
        sox3 = listmap[kiemt].count("sxxxs") + sox3
        sox3 = listmap[kiemt].count("sxsxxs") + sox3
        sox3 = listmap[kiemt].count("sxxsxs") + sox3
        sox4 = listmap[kiemt].count("xxxxs") + sox4
        sox4 = listmap[kiemt].count("sxxxx") + sox4
        sox4 = listmap[kiemt].count("xsxxx") + sox4
        sox4 = listmap[kiemt].count("xxxsx") + sox4
        sox4 = listmap[kiemt].count("xxsxx") + sox4
        sox5 = listmap[kiemt].count("xxxxx") + sox5

        sox2 = listcheotrenphai[kiemt].count("ssxxs") + sox2
        sox2 = listcheotrenphai[kiemt].count("sxxss") + sox2
        sox2 = listcheotrenphai[kiemt].count("sxsxs") + sox2
        sox3 = listcheotrenphai[kiemt].count("sxxxs") + sox3
        sox3 = listcheotrenphai[kiemt].count("sxsxxs") + sox3
        sox3 = listcheotrenphai[kiemt].count("sxxsxs") + sox3
        sox4 = listcheotrenphai[kiemt].count("xxxxs") + sox4
        sox4 = listcheotrenphai[kiemt].count("sxxxx") + sox4
        sox4 = listcheotrenphai[kiemt].count("xsxxx") + sox4
        sox4 = listcheotrenphai[kiemt].count("xxxsx") + sox4
        sox4 = listcheotrenphai[kiemt].count("xxsxx") + sox4
        sox5 = listcheotrenphai[kiemt].count("xxxxx") + sox5

        sox2 = listcheotraiduoi[kiemt].count("ssxxs") + sox2
        sox2 = listcheotraiduoi[kiemt].count("sxxss") + sox2
        sox2 = listcheotraiduoi[kiemt].count("sxsxs") + sox2
        sox3 = listcheotraiduoi[kiemt].count("sxxxs") + sox3
        sox3 = listcheotraiduoi[kiemt].count("sxsxxs") + sox3
        sox3 = listcheotraiduoi[kiemt].count("sxxsxs") + sox3
        sox4 = listcheotraiduoi[kiemt].count("xxxxs") + sox4
        sox4 = listcheotraiduoi[kiemt].count("sxxxx") + sox4
        sox4 = listcheotraiduoi[kiemt].count("xsxxx") + sox4
        sox4 = listcheotraiduoi[kiemt].count("xxxsx") + sox4
        sox4 = listcheotraiduoi[kiemt].count("xxsxx") + sox4
        sox5 = listcheotraiduoi[kiemt].count("xxxxx") + sox5

        sox2 = listcheotraitren[kiemt].count("ssxxs") + sox2
        sox2 = listcheotraitren[kiemt].count("sxxss") + sox2
        sox2 = listcheotraitren[kiemt].count("sxsxs") + sox2
        sox3 = listcheotraitren[kiemt].count("sxxxs") + sox3
        sox3 = listcheotraitren[kiemt].count("sxsxxs") + sox3
        sox3 = listcheotraitren[kiemt].count("sxxsxs") + sox3
        sox4 = listcheotraitren[kiemt].count("xxxxs") + sox4
        sox4 = listcheotraitren[kiemt].count("sxxxx") + sox4
        sox4 = listcheotraitren[kiemt].count("xsxxx") + sox4
        sox4 = listcheotraitren[kiemt].count("xxxsx") + sox4
        sox4 = listcheotraitren[kiemt].count("xxsxx") + sox4
        sox5 = listcheotraitren[kiemt].count("xxxxx") + sox5

        sox2 = listcheoduoiphai[kiemt].count("ssxxs") + sox2
        sox2 = listcheoduoiphai[kiemt].count("sxxss") + sox2
        sox2 = listcheoduoiphai[kiemt].count("sxsxs") + sox2
        sox3 = listcheoduoiphai[kiemt].count("sxxxs") + sox3
        sox3 = listcheoduoiphai[kiemt].count("sxsxxs") + sox3
        sox3 = listcheoduoiphai[kiemt].count("sxxsxs") + sox3
        sox4 = listcheoduoiphai[kiemt].count("xxxxs") + sox4
        sox4 = listcheoduoiphai[kiemt].count("sxxxx") + sox4
        sox4 = listcheoduoiphai[kiemt].count("xsxxx") + sox4
        sox4 = listcheoduoiphai[kiemt].count("xxxsx") + sox4
        sox4 = listcheoduoiphai[kiemt].count("xxsxx") + sox4
        sox5 = listcheoduoiphai[kiemt].count("xxxxx") + sox5

        sox2 = listmapdoc[kiemt].count("ssxxs") + sox2
        sox2 = listmapdoc[kiemt].count("sxxss") + sox2
        sox2 = listmapdoc[kiemt].count("sxsxs") + sox2
        sox3 = listmapdoc[kiemt].count("sxxxs") + sox3
        sox3 = listmapdoc[kiemt].count("sxsxxs") + sox3
        sox3 = listmapdoc[kiemt].count("sxxsxs") + sox3
        sox4 = listmapdoc[kiemt].count("xxxxs") + sox4
        sox4 = listmapdoc[kiemt].count("sxxxx") + sox4
        sox4 = listmapdoc[kiemt].count("xsxxx") + sox4
        sox4 = listmapdoc[kiemt].count("xxxsx") + sox4
        sox4 = listmapdoc[kiemt].count("xxsxx") + sox4
        sox5 = listmapdoc[kiemt].count("xxxxx") + sox5

    rate = 0
    if sox5 > 3:
        rate = 20
    elif sox5 > 2:
        rate = 19
    elif sox5 > 1:
        rate = 18
    elif sox5 > 0:
        rate = 17
    elif sox4 > 3:
        rate = 16
    elif sox4 > 2:
        rate = 15
    elif sox4 > 1:
        rate = 14
    elif sox4 > 0:
        rate = 13
    elif sox3 > 3:
        rate = 12
    elif sox3 > 2:
        rate = 11
    elif sox3 > 1:
        rate = 10
    elif sox3 > 0:
        rate = 9
    elif sox2 > 5:
        rate = 8
    elif sox2 > 4:
        rate = 7
    elif sox2 > 3:
        rate = 6
    elif sox2 > 2:
        rate = 5
    elif sox2 > 1:
        rate = 4
    elif sox2 > 0:
        rate = 3
    else:
        rate = 2


def vitridanh():
    global vitria
    global vitricothedanh
    vitricothedanh = [0] * 400
    for th in vitria:
        if th > 0:
            if th not in gioitren:
                vitricothedanh.append(th - 20)
            if th not in gioiduoi:
                vitricothedanh.append(th + 20)

            if th not in gioiphai:
                vitricothedanh.append(th + 1)
            if th not in gioitrai:
                vitricothedanh.append(th - 1)

            if th not in gioiphai and th not in gioitren:
                vitricothedanh.append(th - 19)
            if th not in gioitrai and th not in gioiduoi:
                vitricothedanh.append(th + 19)

            if th not in gioiphai and th not in gioiduoi:
                vitricothedanh.append(th + 21)
            if th not in gioitrai and th not in gioitren:
                vitricothedanh.append(th - 21)
            vitricothedanh = list(set(vitricothedanh) - set(vitria))
    for j, item in enumerate(vitricothedanh):
        vitricothedanh[j] = 10 * 1000 + item
    for i in vitricothedanh:
        print("vi tri co the danh=", i, " do dai =", len(vitricothedanh))


def xulynut(x, y):
    global index
    global vitritam
    global vitrio
    global vitrix
    global vitrior
    global vitrixr
    global vitria
    global rate
    global ratex
    global rateo
    global khoidaudanh
    global toadocuoi
    global toadocuoitam
    global nhay
    global ketthuc
    global bat
    global maxf
    global maxthua
    if Buts[x, y]["text"] is "":
        a11 = 0
        b12 = 1000
        toadocuoi = 0
        toadocuoitam = 0
        del vitria[:]
        del vitrix[:]
        del vitrio[:]
        Buts[x, y]["text"] = "O"
        vitrior.append(x * 20 + y + 1)

        if khoidaudanh == 0:
            vitrixr.append(x * 20 + y + 2)
            Buts[x, y + 1]["text"] = "X"
            khoidaudanh = 10
            dem = 10
        else:
            dem = 0
        print("khoi dau danh la ", khoidaudanh)
        vitria.extend(vitrior)
        vitria.extend(vitrixr)
        vitrio.extend(vitrior)
        vitrix.extend(vitrixr)
        vitridanh()

        num_base = 12
        rs = 11
        reset = num_base
        ketthuc = 0
        battim = KHOIDONG
        nhay = 0
        print("gia tri cuoi ", (vitricothedanh[-1] // 1000) % 100)

        while dem < 10:

            if (vitricothedanh[-1] // 1000) % 100 == 11 and (
                vitricothedanh[-2] // 1000
            ) % 100 == 12:
                print("baodongjdfgjkdjkdgjgldfljgkljlk")
                ketthuc = ketthuc + 1
            if ketthuc > 0:
                Buts[(toadocuoi - 1) // 20, (toadocuoi - 1) % 20]["text"] = "X"
                vitrixr.append(toadocuoi)
                dem = 10
                break
            if a11 > b12:
                print(
                    "nhaynhaynhaynahynhaynhaynhaynahynhaynhaynhaynahynhaynhaynhaynahynhaynhaynhaynahynhaynhaynhaynahynhaynhaynhaynahynhaynhaynhaynahynhaynhaynhaynahy"
                )
                reset = 11
                maxthua = 0
                b12 = 1000
                if (vitricothedanh[-1] // 1000) % 100 == 11:
                    Buts[(toadocuoi - 1) // 20, (toadocuoi - 1) % 20]["text"] = "X"
                    vitrixr.append(toadocuoi)
                    dem = 10
                    break
            else:
                reset = num_base

            while reset < num_base + 1:
                for j, item in enumerate(vitricothedanh):
                    haidiemdau = (item // 1000) // 100
                    hailevel = (item // 1000) % 100
                    bavitri = item % 1000
                    if battim == KHOIDONG:
                        if j < num_base - 10:
                            hailevel = rs
                            vitricothedanh[j] = (
                                haidiemdau * 100000 + hailevel * 1000 + bavitri
                            )
                        else:
                            hailevel = 10
                            vitricothedanh[j] = (
                                haidiemdau * 100000 + hailevel * 1000 + bavitri
                            )
                        rs = rs + 1
                        if j == len(vitricothedanh) - 1:
                            reset = num_base + 1
                            battim = TIM
                    elif battim == TIM:
                        if hailevel == reset and j == len(vitricothedanh) - 1:
                            if reset > 11:
                                reset = reset - 1
                                nhay = reset
                                battim == TIM
                                break
                            else:
                                reset = num_base + 1
                                break
                        elif hailevel == reset:
                            battim = TIMCHO
                            continue
                    elif battim == TIMCHO:
                        if hailevel == 10 or hailevel > reset:
                            battim = COCHO
                            break
                        elif j == len(vitricothedanh) - 1:
                            if nhay == 11:
                                nhay = 1000
                            if reset > 11:
                                battim = TIM
                                reset = reset - 1
                                break
                            else:
                                reset = num_base + 1
                                break
                    elif battim == COCHO:
                        if hailevel == reset:
                            hailevel = 10
                            vitricothedanh[j] = (
                                haidiemdau * 100000 + hailevel * 1000 + bavitri
                            )
                            battim = DATCHO
                            continue
                    elif battim == DATCHO:
                        if hailevel == 10 or hailevel > reset:
                            hailevel = reset
                            vitricothedanh[j] = (
                                haidiemdau * 100000 + hailevel * 1000 + bavitri
                            )
                            battim = XOA
                            break
                    elif battim == XOA:
                        if hailevel > reset:
                            hailevel = 10
                            vitricothedanh[j] = (
                                haidiemdau * 100000 + hailevel * 1000 + bavitri
                            )
                        if j == len(vitricothedanh) - 1:
                            battim = SAPXEPCONCHAU
                            break
                    elif battim == SAPXEPCONCHAU:
                        if reset >= num_base:
                            reset = num_base + 1
                            break
                        elif hailevel == 10 and reset < num_base:
                            hailevel = reset + 1
                            reset = reset + 1
                            vitricothedanh[j] = (
                                haidiemdau * 100000 + hailevel * 1000 + bavitri
                            )
            # cungcotwhiletrong

            del vitrix[:]
            del vitrio[:]
            vitrix.extend(vitrixr)
            vitrio.extend(vitrior)
            for i in vitricothedanh:
                level = (i // 1000) % 100
                bavi = i % 1000
                if level == 11:
                    vitrix.append(bavi)
                    toadocuoitam = i
                elif level == 12:
                    vitrio.append(bavi)
                # print('i la ',i)
            danhgia()
            ratex = rate
            del vitritam[:]
            vitritam.extend(vitrio)
            del vitrio[:]
            vitrio.extend(vitrix)
            del vitrix[:]
            vitrix.extend(vitritam)
            danhgia()
            rateo = rate
            # print('rate x',ratex,'rate o ',rateo)
            if ratex >= rateo:
                if ratex + 19 < b12:
                    b12 = ratex + 19
                    # print('xxxxxxxxxxxxx',ratex+19,'toado la',toadocuoitam)
            else:
                if 22 - rateo < b12:
                    b12 = 22 - rateo
                    # print('oooooooooooooo',22-rateo,'toado la',toadocuoitam)
            if maxthua < ratex:
                maxthua = ratex

            for dex, thing in enumerate(vitricothedanh):
                if ((thing // 1000) % 100 == 12 and dex == len(vitricothedanh) - 1) or (
                    (vitricothedanh[-1] // 1000) % 100 == 11
                    and (vitricothedanh[-2] // 1000) % 100 == 12
                ):

                    if b12 > a11 and b12 < 40:
                        toadocuoi = toadocuoitam % 1000
                        print("vi lon nhat", toadocuoitam)
                        maxf = maxthua
                        a11 = b12
                    elif b12 == a11 and b12 < 40:
                        if maxf < maxthua:
                            toadocuoi = toadocuoitam % 1000
                            maxf = maxthua
                    maxthua = 0
                    b12 = 1000

            battim = TIM


for r in range(20):
    for c in range(20):
        Buts[r, c] = Button(
            root,
            command=partial(xulynut, x=r, y=c),
            font=("arial", 10, "bold"),
            bd=1,
            height=2,
            width=4,
            borderwidth=2,
        )
        Buts[r, c].grid(row=r, column=c)

root.mainloop()
