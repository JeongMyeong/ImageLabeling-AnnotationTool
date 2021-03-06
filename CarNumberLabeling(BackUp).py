import time
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
import glob
import tkinter as tk
import math
from tkinter import messagebox
from tkinter import simpledialog

class Labeling(Frame):
    def Create(self):
        self.user_width, self.user_height =1000,750 #1366, 768

        self.dirpath = ''
        self.image_path = ''
        self.x_location = []
        self.y_location = []
        self.canvas =''
        self.xy=[[]]
        self.press =''
        self.test=0
        self.start=0
        self.car_cnt = 0
        self.tag =[]
        ########
        #Widget#
        ########
        select_btn = Button(text='folder', command=self.dirBtn_cmd ).place(x=0, y=0)#, command=self.dirBtn_cmd)  # 폴더선택

        scrollbar = Scrollbar()  # 스크롤바
        self.tree = ttk.Treeview(yscrollcommand=scrollbar.set)  # 파일목록
        scrollbar.config(command=self.tree.yview)
        self.tree.place(x=0, y=100, width=150, height=250)
        scrollbar.place(x=150, y=100, height=250)
        clear_btn = Button(text='clear', command=self.clearBtn_cmd).place(x=50, y=0)
        save_btn = Button(text='save', command = self.saveBtn_cmd).place(x=70, y=50)
        all_btn = Button(text='all', command=self.allBtn_cmd).place(x=0, y=75)
        no_btn = Button(text='no', command=self.noBtn_cmd).place(x=20,y=75)
        add_data = Button( text='AddData', command=self.addDataBtn_cmd).place(x=40,y=75)
        deleteimg_btn = Button( text='deleteIMG', command=self.deleteimg).place(x=0,y=50)
        label_btn = Button(text='label', command=self.modify_label).place(x=0, y=25)
        type_btn = Button(text='type', command=self.modify_type).place(x=35, y=25)
        self.xytext = ttk.Label(text='0')
        self.xytext.place(x=70, y=27)
        self.label_info = Label(text="None")
        self.label_info.place(x=0, y=self.user_height)

        self.tree.bind("<Double-1>", self.OnDoubleClick)  # 트리에서 더블클릭
        self.tree.bind("<Button-1>", self.clickontree)
        self.cropcanvas = Canvas(width=700, height=500)  # 없는파일일때 처리 해야함
        self.cropcanvas.place(x=0, y=self.user_height + 50)

    def __init__(self):
        self.cnt=0
        Frame.__init__(self)
        # self.window = window
        self.pack()
        self.Create()


    def modify_type(self):
        self.car_type_dialog()
        self.xy[self.car_cnt - 1][8]=self.c_type
        self.labelinfo_print()

    def modify_label(self):
        while True:
            self.carnum_label = simpledialog.askstring("input", "Write num-label")
            if(self.carnum_label==''):
                continue
            else:
                break
        self.xy[self.car_cnt-1][9]=self.carnum_label
        self.labelinfo_print()

    def dataLoad(self):
        self.labels = dict()                                    #dic


        for filename in self.images:
            self.labels[filename[len(self.dirpath) + 1:]]=[]
        with open(self.dirpath + self.savefname, 'r') as f:
            data = f.readlines()                                            #txt에 있는 모든 데이터를 data 리스트에 담는다.
        for i in data:
            one_data = i.split()
            for key in self.labels.keys():
                xy_li=[]
                if key == one_data[0]:
                    for xy in range(1,len(one_data)):
                        if xy==9 or xy==10:
                            xy_li.append(one_data[xy])
                            continue
                        if (xy % 2 == 1):
                            one_data[xy]=int(float(one_data[xy])/self.wd*self.user_width)
                        else:
                            one_data[xy]=int(float(one_data[xy])/self.hg*self.user_height)
                        xy_li.append(one_data[xy])
                    self.labels[key].append(xy_li)

    def dirBtn_cmd(self):  # 폴더선택 버튼명령
        select = Tk()
        select.dirName = filedialog.askdirectory()  # 경로 선택
        self.dirpath=select.dirName  # 경로 설정
        directory = self.dirpath.split('/')[-1]
        self.savefname = '/'+directory+'_labels.txt'
        self.images = glob.glob(self.dirpath + '/*.jpg')  # 경로에 있는 .jpg 파일들을 리스트에 담음
        if (os.path.isfile(self.dirpath + self.savefname)==False):
            with open(self.dirpath + self.savefname, 'w') as f:
                pass

        for i in self.tree.get_children():
            self.tree.delete(i)

        for i in range(len(self.images)):
            self.tree.insert("", "end", text=str(self.images[i][len(self.dirpath) + 1:]))  # 이미지의 경로를 따라 이름만 tree에 추가
        select.withdraw()  # tk종료

    def allBtn_cmd(self):                           #파일 전체목록 보여주기
        self.images=self.original_images

        for i in self.tree.get_children():
            self.tree.delete(i)

        for i in range(len(self.images)):
            self.tree.insert("", "end", text=str(self.images[i][len(self.dirpath) + 1:]))  # 이미지의 경로를 따라 이름만 tree에 추가

    def noBtn_cmd(self):                    #라벨링 안된 파일들만 보이기

        for i in self.tree.get_children():
            self.tree.delete(i)

        with open(self.dirpath + self.savefname, 'r') as f:
            all_data = f.read()
            all_data = all_data.split()
        cnt=0
        tmp_images=[]
        self.original_images=self.images
        for i in range(len(self.images)):
            if not str(self.images[i][len(self.dirpath) + 1:]) in all_data:
                tmp = self.dirpath+'/' + str(self.images[i][len(self.dirpath) + 1:])
                tmp_images.append(tmp)
                self.tree.insert("", "end", text=str(self.images[i][len(self.dirpath) + 1:]))  # 이미지의 경로를 따라 이름만 tree에 추가
                cnt+=1
        self.images=tmp_images


    def click2(self,event):
        self.press = 'nonpress'


    def clickontree(self,event):
        item = self.tree.identify('item', event.x, event.y)
        image_name = self.tree.item(item, "text")
        self.image_path = self.dirpath + '/' + image_name
        self.chk = 0
        for i in self.images:
            if i[len(self.dirpath) + 1:] == self.image_path[len(self.dirpath) + 1:]:
                self.select_jpg = self.image_path[len(self.dirpath) + 1:]
                break
            else:
                self.chk = self.chk + 1

    def click(self,event):  # 클릭했을때 커맨드

        self.press = 'press'
        if self.car_cnt==0:
            self.car_cnt+=1
            self.addTag(self.car_cnt)
        if(len(self.xy[self.car_cnt-1])<7):
            self.xy[self.car_cnt-1].append(event.x)
            self.xy[self.car_cnt-1].append(event.y)
            if len(self.xy[self.car_cnt-1]) == 8:

                self.press = 'nonpress'
                self.canvas.create_line(self.xy[self.car_cnt - 1][6], self.xy[self.car_cnt - 1][7],self.xy[self.car_cnt - 1][0], self.xy[self.car_cnt - 1][1], fill="red", width=1,tags=self.tag[self.car_cnt - 1][3])
                self.car_type_dialog()
                self.xy[self.car_cnt-1].append(self.c_type)
                self.carnum_label_dialog()
                self.xy[self.car_cnt-1].append(self.carnum_label)
                self.labelinfo_print()
                self.cropimageView()

    def imageOnDoubleClick(self,event):
        # os.remove(self.dirpath + '/' + self.select_jpg)
        # print(self.dirpath + '/' + self.select_jpg)
        # for car in range(self.car_cnt):
        #     self.carnum_label_dialog()
        #     if(len(self.xy[car]) == 9):
        #         self.xy[car].append(self.carnum_label)
        #     if(len(self.xy[car]) == 10):
        #         self.xy[car][9]=self.carnum_label
        self.labelinfo_print()
        self.saveBtn_cmd()

    def deleteimg(self):
        os.remove(self.dirpath + '/' + self.select_jpg)
        print(self.dirpath + '/' + self.select_jpg)

    def OnDoubleClick(self, event):
        self.xy = [[]]
        item = self.tree.identify('item', event.x, event.y)
        image_name = self.tree.item(item, "text")
        self.image_path = self.dirpath + '/' + image_name
        self.chk = 0
        for i in self.images:
            if i[len(self.dirpath) + 1:] == self.image_path[len(self.dirpath) + 1:]:
                self.select_jpg = self.image_path[len(self.dirpath) + 1:]
                break
            else:
                self.chk = self.chk + 1
        self.clear()
        self.viewImage()

    def addDataBtn_cmd(self):
        if(len(self.xy[self.car_cnt-1])<8):           #만약 추가하고 안 그렸을때 처리
            print('First, draw Line')
        else:
            self.car_cnt += 1
            self.addTag(self.car_cnt)
            self.xy.append([])

    def addTag(self,cnt):
        self.tag=[]
        for i in range(cnt):
            tmptag = []
            for k in range(4):
                tmptag.append('line' + str(i)+str(k))
            self.tag.append(tmptag)

    def clearBtn_cmd(self):
        self.save='yes'
        self.clear()

    def clear(self):

        for i in range(self.car_cnt):
            self.canvas.delete(self.tag[i][0],self.tag[i][1],self.tag[i][2],self.tag[i][3])
        self.tag = []
        self.xy=[[]]
        self.car_cnt = 0


    def saveBtn_cmd(self):
        output_li = []
        origin_xy=[]
        if self.car_cnt == 0 :
            save = 'yes'
        for i in range(len(self.xy)):
            tmp_li = []
            for k in range(len(self.xy[i])):                    #원래 좌표를 따로 빼둠
                tmp_li.append(self.xy[i][k])
            origin_xy.append(tmp_li)

        for i in self.xy:
            for k in range(len(i)):
                if (k==8 or k==9):
                    continue
                if k % 2 == 0:
                    i[k] = int((i[k] * self.wd / self.user_width) +1)           #좌표를 저장할때는 해상도를 다시 원래 해상도로 되돌림
                else:
                    i[k] = int((i[k] * self.hg / self.user_height) +1)

        print(self.car_cnt)
        for i in range(self.car_cnt):
            output_li.append(self.image_path[len(self.dirpath) + 1:])       #txt파일에 저장할 output 문자열을 만듦
            if (len(self.xy[i])==9 or len(self.xy[i])==10):
                self.save = 'yes'
            else:
                self.save = 'no'

            for k in range(len(self.xy[i])):
                output_li.append(' ')
                output_li.append(str(self.xy[i][k]))
            output_li.append('\n')
        output = ''.join(output_li)

        with open(self.dirpath + self.savefname, 'r') as f:
            data = f.readlines()                                            #txt에 있는 모든 데이터를 data 리스트에 담는다.
        index=0
        duplication=0
        index_li=[]

        for i in data:
            one_data = i.split()
            if one_data[0] == self.image_path[len(self.dirpath) + 1:]:
                duplication = 1
                index_li.append(index)
            index += 1
        for i in range(len(index_li)):
            del data[index_li[0]]

        data.append(output)
        data = ''.join(data)

        self.xy = origin_xy
        self.labels[self.select_jpg] = self.xy
        if self.save=='yes':
            self.labelinfo_print()
            self.cropimageView()
            with open(self.dirpath + self.savefname, 'w') as f:
                f.write(data)
            if (duplication == 1):
                messagebox.showinfo("수정", "수정되었습니다.")
            else:
                messagebox.showinfo("저장", "저장되었습니다.")
        else:
            messagebox.showinfo("Error", "Don't Save")

    def MsgMotion(self,event):                  #사진위에서 마우스 올라갔을때 커맨드

        self.xytext.config(text=str(event.x) + ',' + str(event.y))
        self.x = event.x
        self.y = event.y
        self.draw()
        sel_car = -1
        # try:
        if len(self.xy[self.car_cnt-1])>=8:
            if self.press == 'press':
                distmp=[]

                for k in range(self.car_cnt):
                    a = self.xydistance([self.xy[k][0], self.xy[k][1]], [event.x, event.y])
                    b = self.xydistance([self.xy[k][2], self.xy[k][3]], [event.x, event.y])
                    c = self.xydistance([self.xy[k][4], self.xy[k][5]], [event.x, event.y])
                    d = self.xydistance([self.xy[k][6], self.xy[k][7]], [event.x, event.y])
                    distmp.append([a, b, c, d])

                for i in range(len(distmp)):
                    for k in distmp[i]:
                        if k <= 10:
                            sel_car=i
                if(sel_car != -1):
                    a, b, c, d = distmp[sel_car]

                if min(a, b, c, d)<=10:
                    if (min(a, b, c, d) == a):
                        self.canvas.delete(self.tag[sel_car][0])
                        self.canvas.create_line(event.x, event.y, self.xy[sel_car][2], self.xy[sel_car][3],fill="red", width=1,tags=self.tag[sel_car][0])
                        self.canvas.delete(self.tag[sel_car][3])
                        self.canvas.create_line(self.xy[sel_car][6], self.xy[sel_car][7], event.x, event.y,fill="red", width=1,tags=self.tag[sel_car][3])
                        self.xy[sel_car][0], self.xy[sel_car][1] = event.x, event.y
                    if (min(a, b, c, d) == b):
                        self.canvas.delete(self.tag[sel_car][0])
                        self.canvas.create_line(self.xy[sel_car][0], self.xy[sel_car][1], event.x, event.y,fill="red", width=1,tags=self.tag[sel_car][0])
                        self.canvas.delete(self.tag[sel_car][1])
                        self.canvas.create_line(event.x, event.y, self.xy[sel_car][4], self.xy[sel_car][5],fill="red", width=1,tags=self.tag[sel_car][1])
                        self.xy[sel_car][2], self.xy[sel_car][3] = event.x, event.y
                    if (min(a, b, c, d) == c):
                        self.canvas.delete(self.tag[sel_car][1])
                        self.canvas.create_line(self.xy[sel_car][2], self.xy[sel_car][3], event.x, event.y,fill="red", width=1,tags=self.tag[sel_car][1])
                        self.canvas.delete(self.tag[sel_car][2])
                        self.canvas.create_line(self.xy[sel_car][6], self.xy[sel_car][7], event.x, event.y,fill="red", width=1,tags=self.tag[sel_car][2])
                        self.xy[sel_car][4], self.xy[sel_car][5] = event.x, event.y
                    if (min(a, b, c, d) == d):
                        self.canvas.delete(self.tag[sel_car][2])
                        self.canvas.create_line(event.x, event.y, self.xy[sel_car][4], self.xy[sel_car][5],fill="red", width=1,tags=self.tag[sel_car][2])
                        self.canvas.delete(self.tag[sel_car][3])
                        self.canvas.create_line(event.x, event.y, self.xy[sel_car][0], self.xy[sel_car][1],fill="red", width=1,tags=self.tag[sel_car][3])
                        self.xy[sel_car][6], self.xy[sel_car][7] = event.x, event.y
                self.labels[self.select_jpg] = self.xy
                self.cropimageView()
                self.labelinfo_print()


    def draw(self):
        self.cnt=0
        self.cnt = len(self.xy[self.car_cnt-1])
        for i in [2,4,6]:
            if self.cnt==i:
                self.canvas.create_line(self.xy[self.car_cnt - 1][i-2], self.xy[self.car_cnt - 1][i-1], self.x, self.y,fill="red", width=1, tags=self.tag[self.car_cnt - 1][i//2-1])
                self.canvas.delete(self.tag[self.car_cnt - 1][(i // 2) - 1])
                self.canvas.create_line(self.xy[self.car_cnt - 1][i-2], self.xy[self.car_cnt - 1][i-1], self.x, self.y,fill="red", width=1, tags=self.tag[self.car_cnt - 1][i//2-1])

        if self.cnt == 8:
            self.canvas.create_line(self.xy[self.car_cnt-1][6], self.xy[self.car_cnt-1][7], self.xy[self.car_cnt-1][0], self.xy[self.car_cnt-1][1], fill="red", width=1,tags=self.tag[self.car_cnt-1][3])



    def LoadDrawLine(self):
        self.car_cnt = len(self.labels[self.select_jpg])        #선택한 사진의 라벨링된 차 갯수
        loadxy = self.labels[self.select_jpg]
        index_li = [[0, 1, 2, 3, 0], [2, 3, 4, 5, 1], [4, 5, 6, 7, 2], [6, 7, 0, 1, 3]]
        if self.car_cnt > 0:
            for num in range(self.car_cnt):
                self.addTag(self.car_cnt)
                for index in range(len(index_li)):
                    for tagnum in index_li:
                        self.canvas.create_line(loadxy[num][tagnum[0]], loadxy[num][tagnum[1]], loadxy[num][tagnum[2]],loadxy[num][tagnum[3]], fill="red", width=1,tags=self.tag[num][tagnum[4]])
                for i in range(len(loadxy[num])):
                        self.xy[num].append(loadxy[num][i])
                self.xy.append([])

    def viewImage(self):  # 이미지를 띄우는 명령
        self.press = 'nonpress'
        self.test +=1
        self.car_cnt = 0
        # self.clear()
        self.tree.bind("<Key>", self.key)  # 트리에서 더블클릭
        try:
            self.canvas.delete("main_image")
        except: pass
        self.wd, self.hg = Image.open(self.image_path).size                                                            #사진 해상도
        self.dataLoad()
        self.canvas = Canvas(width=self.user_width,height=self.user_height)                                             #없는파일일때 처리 해야함

        self.photo = ImageTk.PhotoImage(Image.open(self.image_path).resize((int(self.user_width*self.wd/self.wd),int(self.user_height*self.hg/self.hg))))

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo, tags="main_image")
        self.canvas.place(x=180,y=0)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind('<ButtonRelease-1>', self.click2)
        self.canvas.bind("<Motion>", self.MsgMotion)
        self.canvas.bind("<Double-1>", self.imageOnDoubleClick)

        self.LoadDrawLine()
        self.cropimageView()

        self.labelinfo_print()



    def cropimageView(self):
        self.labels[self.select_jpg] = self.xy
        self.cropimgli = []
        start_x = 0                                                                         # CROP 된 사진들 이어붙이기 위해서 시작부분 조절
        # self.canvas.delete('carcrop')
        # print(self.labels)
        for car in range(self.car_cnt):
            crop_beforeimg = Image.open(self.image_path)
            li = self.labels[self.select_jpg][car]
            x = (li[0] * self.wd / self.user_width, li[2] * self.wd / self.user_width, li[4] * self.wd / self.user_width, li[6] * self.wd / self.user_width)
            y = (li[1] * self.hg / self.user_height, li[3] * self.hg / self.user_height, li[5] * self.hg / self.user_height, li[7] * self.hg / self.user_height)
            cropxy = (min(x), min(y), max(x), max(y))  # x와 y값의 최소 최대값으로 CROP
            crop_img = ImageTk.PhotoImage(crop_beforeimg.crop(cropxy))
            self.cropimgli.append(crop_img)
            self.cropcanvas.create_image(start_x, 0, anchor=tk.NW, image=self.cropimgli[car], tags='carcrop')
            start_x += max(x) - min(x)
    #트리 위에서 키보드 제어
    def key(self,event):
        if event.keysym == 'Down':          # 키보드 아래키
            self.chk = self.chk + 1
            self.image_path = self.dirpath + '/' + self.images[self.chk][len(self.dirpath)+1:]
        if event.keysym == 'Up':            # 키보드 윗키
            self.chk = self.chk - 1
            self.image_path = self.dirpath + '/' + self.images[self.chk][len(self.dirpath) + 1:]
        self.select_jpg = self.images[self.chk][len(self.dirpath) + 1:]
        if event.keysym == 'Return':        # 엔터 키
            self.xy=[[]]
            self.car_cnt = 0
            self.viewImage()

    #점과 점사이 거리
    def xydistance(self,x,y):
        distance = math.sqrt(pow(int(x[0])-int(y[0]),2)+pow((int(x[1])-int(y[1])),2))
        return distance

    # 자동차 타입적는 dialog
    def car_type_dialog(self):
        while True:
            self.c_type = simpledialog.askstring("Input", "Input Type")
            if(self.c_type ==''):
                continue
            else:
                break
    def carnum_label_dialog(self):
        while True:
            self.carnum_label = simpledialog.askstring("input", "Write num-label")
            if(self.carnum_label==''):
                continue
            else:
                break



    #라벨정보를 하단에 출력
    def labelinfo_print(self):
        print(self.xy)
        self.labels[self.select_jpg] = self.xy
        info = self.labels[self.select_jpg]
        self.infostr=''
        for car in info:
            for index in range(len(car)):
                if index == 8:
                    self.infostr+='type ' + str(car[index])
                if index == 9:
                    self.infostr+=' num: '+str(car[index])
                else:
                    if index!=8:
                        self.infostr+=str(car[index])+' '
            self.infostr+='\n'
        self.label_info.config(text=self.infostr)

root = Tk()
root.geometry("1300x1000")
app = Labeling()
app.mainloop()