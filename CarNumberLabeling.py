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
        self.user_width, self.user_height =1000,700 #1366, 768

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

        scrollbar = Scrollbar()                                                      # 스크롤바
        self.tree = ttk.Treeview(yscrollcommand=scrollbar.set)                       # 파일목록
        scrollbar.config(command=self.tree.yview)                                    #스크롤바 config
        self.tree.place(x=0, y=100, width=150, height=250)                           # 파일목록 위치설정
        scrollbar.place(x=150, y=100, height=250)                                    # 스크롤바 위치설정
        clear_btn = Button(text='clear', command=self.clearBtn_cmd).place(x=50, y=0) # Labeling 정보들 모두 초기화버튼
        save_btn = Button(text='save', command = self.saveBtn_cmd).place(x=70, y=50) # 저장 버튼
        all_btn = Button(text='all', command=self.allBtn_cmd).place(x=0, y=75)       # 모든 파일 리스트 목록 보기 버튼
        no_btn = Button(text='no', command=self.noBtn_cmd).place(x=20,y=75)          # 아직 Labeling 되지 않은 파일 리스트 목록 보기 버튼
        add_data = Button( text='AddData', command=self.addDataBtn_cmd).place(x=40,y=75) # 번호판이 두개일 때 Labeling 데이터 하나 더 추가하기 버튼
        deleteimg_btn = Button( text='deleteIMG', command=self.deleteimg).place(x=0,y=50) # 쓸모없는 데이터일때 이미지 제거 버튼
        label_btn = Button(text='label', command=self.modify_label).place(x=0, y=25)    # 번호판 문자Label 수정 버튼
        type_btn = Button(text='type', command=self.modify_type).place(x=35, y=25)      # 번호판 Type 수정 버튼

        lu_up_btn = Button(text='▲',command=self.lu_upBtn_cmd).place(x=22, y=500)      # Labeling 좌표 1픽셀 수정 (왼쪽 위 좌표에서 위로)
        lu_down_btn = Button(text='▼',command=self.lu_downBtn_cmd).place(x=22, y=552)  # Labeling 좌표 1픽셀 수정 (왼쪽 위 좌표에서 아래로)
        lu_left_btn = Button(text='◀',command=self.lu_leftBtn_cmd).place(x=0, y=526)   # Labeling 좌표 1픽셀 수정 (왼쪽 위 좌표에서 왼쪽으로)
        lu_right_btn = Button(text='▶',command=self.lu_rightBtn_cmd).place(x=45, y=526)# Labeling 좌표 1픽셀 수정 (왼쪽 위 좌표에서 오른쪽으로)

        ru_up_btn = Button(text='▲', command=self.ru_upBtn_cmd).place(x=91, y=500)         #위와 동일.
        ru_down_btn = Button(text='▼', command=self.ru_downBtn_cmd).place(x=91, y=552)
        ru_left_btn = Button(text='◀', command=self.ru_leftBtn_cmd).place(x=68, y=526)
        ru_right_btn = Button(text='▶', command=self.ru_rightBtn_cmd).place(x=114, y=526)

        rd_up_btn = Button(text='▲', command=self.rd_upBtn_cmd).place(x=91, y=578)
        rd_down_btn = Button(text='▼', command=self.rd_downBtn_cmd).place(x=91, y=630)
        rd_left_btn = Button(text='◀', command=self.rd_leftBtn_cmd).place(x=68, y=604)
        rd_right_btn = Button(text='▶', command=self.rd_rightBtn_cmd).place(x=114, y=604)

        ld_up_btn = Button(text='▲', command=self.ld_upBtn_cmd).place(x=22, y=578)
        ld_down_btn = Button(text='▼', command=self.ld_downBtn_cmd).place(x=22, y=630)
        ld_left_btn = Button(text='◀', command=self.ld_leftBtn_cmd).place(x=0, y=604)
        ld_right_btn = Button(text='▶', command=self.ld_rightBtn_cmd).place(x=45, y=604)

        self.xytext = ttk.Label(text='0')                                                    # Canvas 위의 좌표 초기값.
        self.xytext.place(x=70, y=27)                                                        # Canvas 위의 좌표 위치설정.
        self.label_info = Label(text="None")                                                 # Labeliong 정보 초기값
        self.label_info.place(x=0, y=self.user_height+15)                                    # Labeling 정보 위치 설정.

        self.tree.bind("<Double-1>", self.OnDoubleClick)                                     # 트리에서 더블클릭
        self.tree.bind("<Button-1>", self.clickontree)                                       # 트리에서 한 번 클릭.
        self.cropcanvas = Canvas(width=700, height=500)                                      # 없는파일일때 처리 해야함
        self.cropcanvas.place(x=180+self.user_width+20, y=0)

    def __init__(self):                                                     # 클래스 처음
        self.cnt=0
        Frame.__init__(self)
        # self.window = window
        self.pack()
        self.Create()

    def lu_upBtn_cmd(self):                                                             # Labeling 좌표 1픽셀씩 수정 버튼

        car_idx=self.car_cnt-1
        self.xy[car_idx][1] -= 1
        self.canvas.delete(self.tag[car_idx][0])
        self.canvas.delete(self.tag[car_idx][3])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                fill="red", width=1, tags=self.tag[car_idx][0])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][3])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()
    def lu_downBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼

        car_idx=self.car_cnt-1
        self.xy[car_idx][1] += 1
        self.canvas.delete(self.tag[car_idx][0])
        self.canvas.delete(self.tag[car_idx][3])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                fill="red", width=1, tags=self.tag[car_idx][0])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][3])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def lu_leftBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][0] -= 1
        self.canvas.delete(self.tag[car_idx][0])
        self.canvas.delete(self.tag[car_idx][3])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                fill="red", width=1, tags=self.tag[car_idx][0])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][3])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def lu_rightBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][0] += 1
        self.canvas.delete(self.tag[car_idx][0])
        self.canvas.delete(self.tag[car_idx][3])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                fill="red", width=1, tags=self.tag[car_idx][0])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][3])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def ru_upBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][3] -= 1
        self.canvas.delete(self.tag[car_idx][0])
        self.canvas.delete(self.tag[car_idx][1])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                fill="red", width=1, tags=self.tag[car_idx][0])
        self.canvas.create_line(self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                fill="red", width=1, tags=self.tag[car_idx][1])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def ru_downBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx = self.car_cnt - 1
        self.xy[car_idx][3] += 1
        self.canvas.delete(self.tag[car_idx][0])
        self.canvas.delete(self.tag[car_idx][1])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                fill="red", width=1, tags=self.tag[car_idx][0])
        self.canvas.create_line(self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                fill="red", width=1, tags=self.tag[car_idx][1])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()
        self.cropimageView()
        self.labelinfo_print()

    def ru_rightBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][2] += 1
        self.canvas.delete(self.tag[car_idx][0])
        self.canvas.delete(self.tag[car_idx][1])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                fill="red", width=1, tags=self.tag[car_idx][0])
        self.canvas.create_line(self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                fill="red", width=1, tags=self.tag[car_idx][1])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def ru_leftBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][2] -= 1
        self.canvas.delete(self.tag[car_idx][0])
        self.canvas.delete(self.tag[car_idx][1])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                fill="red", width=1, tags=self.tag[car_idx][0])
        self.canvas.create_line(self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                fill="red", width=1, tags=self.tag[car_idx][1])
        self.labels[self.select_jpg] = self.xy

    def rd_downBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][5] += 1
        self.canvas.delete(self.tag[car_idx][1])
        self.canvas.delete(self.tag[car_idx][2])
        self.canvas.create_line(self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                fill="red", width=1, tags=self.tag[car_idx][1])
        self.canvas.create_line(self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][2])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def rd_upBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][5] -= 1
        self.canvas.delete(self.tag[car_idx][1])
        self.canvas.delete(self.tag[car_idx][2])
        self.canvas.create_line(self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                fill="red", width=1, tags=self.tag[car_idx][1])
        self.canvas.create_line(self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][2])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def rd_rightBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][4] += 1
        self.canvas.delete(self.tag[car_idx][1])
        self.canvas.delete(self.tag[car_idx][2])
        self.canvas.create_line(self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                fill="red", width=1, tags=self.tag[car_idx][1])
        self.canvas.create_line(self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][2])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def rd_leftBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][4] -= 1
        self.canvas.delete(self.tag[car_idx][1])
        self.canvas.delete(self.tag[car_idx][2])
        self.canvas.create_line(self.xy[car_idx][2],
                                self.xy[car_idx][3],
                                self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                fill="red", width=1, tags=self.tag[car_idx][1])
        self.canvas.create_line(self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][2])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def ld_downBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][7] += 1
        self.canvas.delete(self.tag[car_idx][2])
        self.canvas.delete(self.tag[car_idx][3])
        self.canvas.create_line(self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][2])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][3])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def ld_upBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][7] -= 1
        self.canvas.delete(self.tag[car_idx][2])
        self.canvas.delete(self.tag[car_idx][3])
        self.canvas.create_line(self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][2])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][3])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def ld_leftBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][6] -= 1
        self.canvas.delete(self.tag[car_idx][2])
        self.canvas.delete(self.tag[car_idx][3])
        self.canvas.create_line(self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][2])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][3])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    def ld_rightBtn_cmd(self):                                                            # Labeling 좌표 1픽셀씩 수정 버튼
        car_idx=self.car_cnt-1
        self.xy[car_idx][6] += 1
        self.canvas.delete(self.tag[car_idx][2])
        self.canvas.delete(self.tag[car_idx][3])
        self.canvas.create_line(self.xy[car_idx][4],
                                self.xy[car_idx][5],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][2])
        self.canvas.create_line(self.xy[car_idx][0],
                                self.xy[car_idx][1],
                                self.xy[car_idx][6],
                                self.xy[car_idx][7],
                                fill="red", width=1, tags=self.tag[car_idx][3])
        self.labels[self.select_jpg] = self.xy
        self.cropimageView()
        self.labelinfo_print()

    # Labeling 타입 수정 버튼
    def modify_type(self):
        self.car_type_dialog()
        self.xy[self.car_cnt - 1][8]=self.c_type                                        # Labeling 타입을 수정해준다.
        self.labelinfo_print()                                                          # Labeling 정보를 업데이트해준다,

    # 번호판 문구 labeling 정보를 수정 버튼.
    def modify_label(self):
        while True:                                                                     # Labeling 타입의 올바른 정보가 들어올때까지 반복.
            self.carnum_label = simpledialog.askstring("input", "Write num-label")
            if(self.carnum_label==''):
                continue
            else:
                break
        self.xy[self.car_cnt-1][9]=self.carnum_label                                      # Labeling 번호판 문구를 수정해준다.
        self.labelinfo_print()                                                          # Labeling 정보를 업데이트해준다,

    # 데이터를 로드하는 함수.
    def dataLoad(self):
        self.labels = dict()                                    # dictionary


        for filename in self.images:
            self.labels[filename[len(self.dirpath) + 1:]]=[]    # key 값을 file 명으로 한다.
        with open(self.dirpath + self.savefname, 'r') as f:
            data = f.readlines()                                            # txt에 있는 모든 데이터를 data 리스트에 담는다.
        for i in data:
            one_data = i.split()
            for key in self.labels.keys():
                xy_li=[]
                if key == one_data[0]:                                      # 이미 데이터가 있을 때
                    for xy in range(1,len(one_data)):
                        if xy==9 or xy==10:
                            xy_li.append(one_data[xy])
                            continue
                        if (xy % 2 == 1):
                            one_data[xy]=int(float(one_data[xy]))
                        else:
                            one_data[xy]=int(float(one_data[xy]))
                        xy_li.append(one_data[xy])
                    self.labels[key].append(xy_li)

    # 폴더선택 버튼명령
    def dirBtn_cmd(self):
        select = Tk()
        select.dirName = filedialog.askdirectory()  # 경로 선택
        self.dirpath=select.dirName                 # 경로 설정
        directory = self.dirpath.split('/')[-1]
        self.savefname = '/'+directory+'_labels.txt'
        self.images = glob.glob(self.dirpath + '/*.jpg')            # 경로에 있는 .jpg 파일들을 리스트에 담음
        if (os.path.isfile(self.dirpath + self.savefname)==False):
            with open(self.dirpath + self.savefname, 'w') as f:
                pass

        for i in self.tree.get_children():
            self.tree.delete(i)

        for i in range(len(self.images)):
            self.tree.insert("", "end", text=str(self.images[i][len(self.dirpath) + 1:]))               # 이미지의 경로를 따라 이름만 tree에 추가
        select.withdraw()                                                                               # tk종료

    # 파일 전체목록 보여주기
    def allBtn_cmd(self):
        self.images=self.original_images
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i in range(len(self.images)):
            self.tree.insert("", "end", text=str(self.images[i][len(self.dirpath) + 1:]))  # 이미지의 경로를 따라 이름만 tree에 추가

    # 라벨링 안된 파일들만 보이기
    def noBtn_cmd(self):
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

    # 파일목록에서 한번만 클릭했을 때
    def clickontree(self,event):
        item = self.tree.identify('item', event.x, event.y)
        image_name = self.tree.item(item, "text")
        self.image_path = self.dirpath + '/' + image_name
        self.chk = 0
        for i in self.images:                                                                           # 선택한 파일의 이름을 변수에 담아둔다.
            if i[len(self.dirpath) + 1:] == self.image_path[len(self.dirpath) + 1:]:
                self.select_jpg = self.image_path[len(self.dirpath) + 1:]
                break
            else:
                self.chk = self.chk + 1

    # Canvas 위에서 클릭했을때 커맨드
    def click(self,event):
        self.press = 'press'
        if self.car_cnt == 0:               # 만약 차량의 개수가 0개이면
            self.car_cnt += 1               # 차량 개수를 +1
            self.addTag(self.car_cnt)

        if(len(self.xy[self.car_cnt-1])<7):                                         # Labeling이 안되어있으면 좌표를 저장.
            self.xy[self.car_cnt-1].append(int(self.canvas.canvasx(event.x)))
            self.xy[self.car_cnt-1].append(int(self.canvas.canvasy(event.y)))
            if len(self.xy[self.car_cnt-1]) == 8:
                self.press = 'nonpress'
                self.canvas.create_line(self.xy[self.car_cnt - 1][6], self.xy[self.car_cnt - 1][7],self.xy[self.car_cnt - 1][0], self.xy[self.car_cnt - 1][1], fill="red", width=1,tags=self.tag[self.car_cnt - 1][3])
                self.car_type_dialog()
                self.xy[self.car_cnt-1].append(self.c_type)
                self.carnum_label_dialog()
                self.xy[self.car_cnt-1].append(self.carnum_label)
                self.labelinfo_print()
                self.cropimageView()

    # Canvas 이미지에서 더블클리개 했을 때
    def imageOnDoubleClick(self,event):
        self.labelinfo_print()                                  # Labeling 정보를 업데이트.
        self.saveBtn_cmd()                                      # 저장.


    # 이미지 파일을 삭제하는 버튼 명령
    def deleteimg(self):
        os.remove(self.dirpath + '/' + self.select_jpg)
        print(self.dirpath + '/' + self.select_jpg)

    # 트리뷰에서 더블클릭했을 때
    def OnDoubleClick(self, event):
        self.xy = [[]]
        item = self.tree.identify('item', event.x, event.y)                             # 선택한 파일의 경로를 저장하고
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
        self.viewImage()                                                                # 선택한 파일의 결로대로 이미지를 띄워준다.

    # 차량이 두개 있을때 Labeling 데이터 추가 버튼.
    def addDataBtn_cmd(self):
        if(len(self.xy[self.car_cnt-1])<8):           #만약 추가하고 안 그렸을때 처리
            print('First, draw Line')
        else:
            self.car_cnt += 1
            self.addTag(self.car_cnt)
            self.xy.append([])


    # Canvas를 그리기위한 Tag 생성 함수.
    def addTag(self,cnt):
        self.tag=[]
        for i in range(cnt):
            tmptag = []
            for k in range(4):
                tmptag.append('line' + str(i)+str(k))
            self.tag.append(tmptag)


    # 정보들을 초기화.
    def clearBtn_cmd(self):
        self.save='yes'
        self.clear()



    # 정보들 초기화 하는 함수,
    def clear(self):

        for i in range(self.car_cnt):
            self.canvas.delete(self.tag[i][0],self.tag[i][1],self.tag[i][2],self.tag[i][3])
        self.tag = []
        self.xy=[[]]
        self.car_cnt = 0

    # 저장 버튼.
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

    # 사진위에서 마우스 올라갔을때 커맨드
    def MsgMotion(self,event):
        self.x, self.y = int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y))  # 스크롤 했을때 상대적인 값.
        self.xytext.config(text=str(self.x) + ',' + str(self.y))                      # 위치값 수정
        self.draw()
        sel_car = -1
        if len(self.xy[self.car_cnt-1])>=8:                                           # 라벨위치값이 온전히 다 존재할 때
            if self.press == 'press':                                                 # 마우스를 누른 상태라면
                distance_tmp=[]
                for k in range(self.car_cnt):
                    a = self.xydistance([self.xy[k][0], self.xy[k][1]], [self.x, self.y])
                    b = self.xydistance([self.xy[k][2], self.xy[k][3]], [self.x, self.y])
                    c = self.xydistance([self.xy[k][4], self.xy[k][5]], [self.x, self.y])
                    d = self.xydistance([self.xy[k][6], self.xy[k][7]], [self.x,self.y])
                    distance_tmp.append([a, b, c, d])

                for i in range(len(distance_tmp)):
                    for k in distance_tmp[i]:
                        if k <= 10:
                            sel_car=i
                if(sel_car != -1):
                    a, b, c, d = distance_tmp[sel_car]

                if min(a, b, c, d)<=10:                                                 # 마우스에서 제일 가까운 부분을 연산.
                    if (min(a, b, c, d) == a):
                        self.canvas.delete(self.tag[sel_car][0])
                        self.canvas.create_line(self.x, self.y, self.xy[sel_car][2], self.xy[sel_car][3],fill="red", width=1,tags=self.tag[sel_car][0])
                        self.canvas.delete(self.tag[sel_car][3])
                        self.canvas.create_line(self.xy[sel_car][6], self.xy[sel_car][7], self.x, self.y,fill="red", width=1,tags=self.tag[sel_car][3])
                        self.xy[sel_car][0], self.xy[sel_car][1] = self.x, self.y
                    elif (min(a, b, c, d) == b):
                        self.canvas.delete(self.tag[sel_car][0])
                        self.canvas.create_line(self.xy[sel_car][0], self.xy[sel_car][1], self.x, self.y,fill="red", width=1,tags=self.tag[sel_car][0])
                        self.canvas.delete(self.tag[sel_car][1])
                        self.canvas.create_line(self.x, self.y, self.xy[sel_car][4], self.xy[sel_car][5],fill="red", width=1,tags=self.tag[sel_car][1])
                        self.xy[sel_car][2], self.xy[sel_car][3] = self.x, self.y
                    elif (min(a, b, c, d) == c):
                        self.canvas.delete(self.tag[sel_car][1])
                        self.canvas.create_line(self.xy[sel_car][2], self.xy[sel_car][3], self.x, self.y,fill="red", width=1,tags=self.tag[sel_car][1])
                        self.canvas.delete(self.tag[sel_car][2])
                        self.canvas.create_line(self.xy[sel_car][6], self.xy[sel_car][7], self.x, self.y,fill="red", width=1,tags=self.tag[sel_car][2])
                        self.xy[sel_car][4], self.xy[sel_car][5] = self.x, self.y
                    elif (min(a, b, c, d) == d):
                        self.canvas.delete(self.tag[sel_car][2])
                        self.canvas.create_line(self.x, self.y, self.xy[sel_car][4], self.xy[sel_car][5],fill="red", width=1,tags=self.tag[sel_car][2])
                        self.canvas.delete(self.tag[sel_car][3])
                        self.canvas.create_line(self.x, self.y, self.xy[sel_car][0], self.xy[sel_car][1],fill="red", width=1,tags=self.tag[sel_car][3])
                        self.xy[sel_car][6], self.xy[sel_car][7] = self.x, self.y
                self.labels[self.select_jpg] = self.xy
                self.cropimageView()
                self.labelinfo_print()

    # Canvas 위에 labeling 할 정보를 선으로 출력.
    def draw(self):
        self.cnt=0
        car_idx=self.car_cnt-1
        self.cnt = len(self.xy[car_idx])
        for i in [2,4,6]:
            if self.cnt==i:
                self.canvas.create_line(self.xy[car_idx][i-2],
                                        self.xy[car_idx][i-1],
                                        self.x, self.y,
                                        fill="red", width=1, tags=self.tag[car_idx][i//2-1])
                self.canvas.delete(self.tag[car_idx][(i // 2) - 1])
                self.canvas.create_line(self.xy[car_idx][i-2],
                                        self.xy[car_idx][i-1],
                                        self.x, self.y,
                                        fill="red", width=1, tags=self.tag[car_idx][i//2-1])

        if self.cnt == 8:
            self.canvas.create_line(self.xy[car_idx][6],
                                    self.xy[car_idx][7],
                                    self.xy[car_idx][0],
                                    self.xy[car_idx][1],
                                    fill="red", width=1,tags=self.tag[car_idx][3])

    # 이미 Labeling 된 정보가 있을때 그 정보를 로드하여 Canvas에 좌표대로 그려줌.
    def LoadDrawLine(self):
        self.car_cnt = len(self.labels[self.select_jpg])        # 선택한 사진의 라벨링된 차 갯수
        loadxy = self.labels[self.select_jpg]
        index_li = [[0, 1, 2, 3, 0], [2, 3, 4, 5, 1], [4, 5, 6, 7, 2], [6, 7, 0, 1, 3]]
        if self.car_cnt > 0:
            for num in range(self.car_cnt):
                self.addTag(self.car_cnt)
                for _ in range(len(index_li)):
                    for tagnum in index_li:
                        self.canvas.create_line(loadxy[num][tagnum[0]], loadxy[num][tagnum[1]], loadxy[num][tagnum[2]],loadxy[num][tagnum[3]], fill="red", width=1,tags=self.tag[num][tagnum[4]])
                for i in range(len(loadxy[num])):
                        self.xy[num].append(loadxy[num][i])
                self.xy.append([])

    # 이미지를 띄우는 명령
    def viewImage(self):
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
        self.canvas = Canvas(width=self.user_width,height=self.user_height,scrollregion=(0, 0, self.wd, self.hg))                   # Canvas에 파일의 정보들을 준다.
        self.photo = ImageTk.PhotoImage(Image.open(self.image_path))
        self.thumbnail_photo = ImageTk.PhotoImage(Image.open(self.image_path).resize((700,500)))                                    # Thumnail.
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo, tags="main_image")                                           # 파일의 정보대로 Canvas에 그린다.
        self.canvas.place(x=180,y=0)                                                                                                # Canvas 위치 설정.
        self.thumbnailcanvas = Canvas(width=700, height=500)
        self.thumbnailcanvas.place(x=180+self.user_width+20, y=400)                                                                 # Thumnail 위치 설정.
        self.thumbnailcanvas.create_image(0, 0, anchor=tk.NW, image=self.thumbnail_photo, tags='main_image')                        # Thumnail 정보를 Canvas에 그린다.


        hs = Scrollbar(root, orient=HORIZONTAL, command=self.canvas.xview)                                                          # Canvas에 스크롤 기능
        hs.place(x=180, y=self.user_height, width= self.user_width)                                                                 # Canvas에 스크롤 기능
        vs = Scrollbar(root, orient=VERTICAL, command=self.canvas.yview)                                                            # Canvas에 스크롤 기능
        vs.place(x=180+self.user_width,y=0,height=self.user_height)                                                                 # Canvas에 스크롤 기능
        self.canvas.configure(xscrollcommand=hs.set, yscrollcommand=vs.set)                                                         # Canvas에 스크롤 기능

        self.canvas.bind("<Button-1>", self.click)                                                                                  # Canvas 위에서 사용될 마우스 옵션들을 부여.
        self.canvas.bind('<ButtonRelease-1>', self.click2)                                                                          # Canvas 위에서 사용될 마우스 옵션들을 부여.
        self.canvas.bind("<Motion>", self.MsgMotion)                                                                                # Canvas 위에서 사용될 마우스 옵션들을 부여.
        self.canvas.bind("<Double-1>", self.imageOnDoubleClick)                                                                     # Canvas 위에서 사용될 마우스 옵션들을 부여.

        self.LoadDrawLine()
        self.cropimageView()

        self.labelinfo_print()


    # Labeling 된 좌표쪽 정보만 보여주는 CropImageView.
    def cropimageView(self):
        self.labels[self.select_jpg] = self.xy
        self.cropimgli = []
        start_y = 0                                                                         # CROP 된 사진들 이어붙이기 위해서 시작부분 조절
        for car in range(self.car_cnt):
            crop_beforeimg = Image.open(self.image_path)
            li = self.labels[self.select_jpg][car]
            x = (li[0], li[2], li[4], li[6])
            y = (li[1], li[3], li[5], li[7])
            cropxy = (min(x), min(y), max(x), max(y))  # x와 y값의 최소 최대값으로 CROP
            crop_img = ImageTk.PhotoImage(crop_beforeimg.crop(cropxy))
            self.cropimgli.append(crop_img)
            self.cropcanvas.create_image(0, start_y, anchor=tk.NW, image=self.cropimgli[car], tags='carcrop')
            start_y += max(y) - min(y)

    # 트리 위에서 키보드 제어
    def key(self,event):
        if event.keysym == 'Down':               # 키보드 아래키
            self.chk = self.chk + 1
            self.image_path = self.dirpath + '/' + self.images[self.chk][len(self.dirpath)+1:]
        if event.keysym == 'Up':                  # 키보드 윗키
            self.chk = self.chk - 1
            self.image_path = self.dirpath + '/' + self.images[self.chk][len(self.dirpath) + 1:]
        self.select_jpg = self.images[self.chk][len(self.dirpath) + 1:]
        if event.keysym == 'Return':               # 엔터 키
            self.xy=[[]]
            self.car_cnt = 0
            self.viewImage()

    # 점과 점사이 거리 계산 함수
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


    # 자동차 Type을 적는 Dialog
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