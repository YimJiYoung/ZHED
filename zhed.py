import pygame
import random
from pygame.locals import *
import sys

screen=0

class Game:
    def __init__(self):
        self.title = 'Zhed'
        self.width = 400 #window width
        self.height = 600 #window height
        
        self.level= 1
        self.blocks=[] #맵의 블록들에 대한 정보 저장
        self.clicked=False
        self.clickedBlock=(-1,-1)
        self.numBlocks=0 #맵에 있는 숫자 블록의 수
        
        self.win=False
        self.lose=False
        
        self.sound=True
        
        self.run = True
        
        self.finalLevel=9
    
    def play(self):
        global screen
        
        pygame.init()
      
        pygame.display.set_caption(self.title) # title 설정
        size = (self.width, self.height) # 윈도우 크기 설정
        screen = pygame.display.set_mode(size)
        WHITE=(255,255,255)
        screen.fill(WHITE) # 배경화면 white

        pygame.mixer.music.load('sound/bgm.mp3') # bgm 로드
        pygame.mixer.music.play(-1) # bgm 재생

        click_sound= pygame.mixer.Sound('sound/button.wav') # 버튼 클릭 사운드 로드
        win_sound= pygame.mixer.Sound('sound/win.wav') # 승리 사운드 로드
        
        #self.menu=Menu(screen)
        #self.menu.mainloop()

        self.create_blocks()# 초기 블록 설정
        
        while self.run:
            #이벤트 처리하는 부분
            for event in pygame.event.get():
                 if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                 #왼쪽 마우스 버튼이 눌렸을 때
                 if event.type == MOUSEBUTTONDOWN and event.button == 1:
                     x=int(event.pos[0]/50) # x index
                     y=int((event.pos[1]-100)/50) # y index
                     if(y>=0 and y<=7) : # 범위 안
                        pygame.mixer.Sound.play(click_sound)
                        self.clickBlock((x,y))
                     #sound icon 클릭
                     if(event.pos[0]>325 and event.pos[0]<375 and event.pos[1]>25 and event.pos[1]<75):
                         if(self.sound): # 재생 중 
                             pygame.mixer.music.pause() #멈춤
                             self.sound=False
                         else:
                             pygame.mixer.music.unpause() #다시 재생
                             self.sound=True
                     #restart icon 클릭
                     if(event.pos[0]>300 and event.pos[0]<375 and event.pos[1]>510 and event.pos[1]<590):
                         self.create_blocks()
                         self.lose=False
            #게임 상태 업데이트하는 부분
            if(self.win): # 이겼을 때           
                if(self.level<self.finalLevel):                 
                    self.level+=1
                    pygame.mixer.Sound.play(win_sound)
                    self.win=False
                    self.create_blocks()
                    
            elif(self.numBlocks==0): # 이긴 상태가 아닌데 확장가능한 숫자 블록 수 0개 이다
                    self.lose=True
                    
            #게임 상태 화면에 그려주는 부분
            screen.fill(WHITE)
            self.render() 
            pygame.display.update() 

    def render(self):  
        global screen
        for i in range(0,8):
                for j in range(0,8):
                    x,y = j*50,i*50+100
                   # 이미지 로드
                    if(self.blocks[i][j]['num']=='-1'): #destination block인 경우
                        if (self.blocks[i][j]['state']==0):
                            self.image = pygame.image.load('img/dest.png')
                        else :
                            self.image = pygame.image.load('img/b.png')
                    elif(self.blocks[i][j]['num']=='0'): #일반 block인 경우
                        if (self.blocks[i][j]['state']==0):
                            self.image = pygame.image.load('img/gray.png')
                        elif (self.blocks[i][j]['state']==1): 
                            self.image = pygame.image.load('img/b.png')
                        else:
                            self.image = pygame.image.load('img/gray_selected.png')
                    else: #number block인 경우
                        if (self.blocks[i][j]['state']==0 or self.blocks[i][j]['state']==1):
                            self.image = pygame.image.load('img/%s.png'% self.blocks[i][j]['num'])
                        else:
                            self.image = pygame.image.load('img/b.png')
                    screen.blit(self.image,(x,y))
        #레벨 표시
        font = pygame.font.SysFont("comicsansms", 40)
        levelText = font.render("%d"%self.level, True, (0,0,0))
        screen.blit(levelText,(200 - levelText.get_width() // 2, 50 - levelText.get_height() // 2))

        #restart
        restart = pygame.image.load('img/restart.png') #크기 75,80
        screen.blit(restart,(300,510))
        #sound 아이콘
        if(self.sound):
            sound = pygame.image.load('img/sound_1.png') #크기 50,50
        else:
            sound = pygame.image.load('img/sound_0.png')
        screen.blit(sound,(325,25))

        #message box
        if(self.win):
            msg = pygame.image.load('img/msg_win.png') 
        elif(self.lose):
            msg = pygame.image.load('img/msg_lose.png') 
        else:
            msg = pygame.image.load('img/msg_idle.png') 
        screen.blit(msg,(25,510))
        

    def create_blocks(self):
        global screen
        #block 2차원 배열 초기화
        self.blocks = [[0]*8 for i in range(8)]
        
        level1_map = [
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '1',   '-1',  '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
        ]
        level2_map = [
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '2',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '-1',  '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
        ]
        level3_map = [
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '1',   '1',   '0',   '-1',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
        ]
        level4_map = [
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '-1',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',  '0',   '0',   '0',
            '0',   '0',   '2',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '2',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
        ]
        level5_map = [
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '2',   '0',   '0',   '-1',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '2',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '1',   '0',   '2',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
        ]
        level6_map = [
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '-1',   '0',   '0',   '0',   '3',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '2',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '3',   '0',   '0',
            '0',   '0',   '0',   '2',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
        ]
        level7_map = [
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '1',   '0',   '0',   '0',   '0',
            '0',   '-1',   '0',   '0',   '0',   '0',   '1',   '0',
            '0',   '0',   '0',   '0',   '0',   '1',   '0',   '0',
            '0',   '0',   '2',   '0',   '2',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
        ]
        level8_map = [
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '1',   '1',   '0',   '0',
            '0',   '1',   '0',   '0',   '0',   '0',   '-1',   '0',
            '0',   '0',   '0',   '1',   '1',   '0',   '0',   '0',
            '0',   '0',   '1',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
        ]
        level9_map = [
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '1',   '2',   '0',   '0',
            '0',   '0',   '0',   '1',   '0',   '0',   '0',   '0',
            '0',   '0',   '1',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '3',   '0',
            '0',   '0',   '-1',   '0',   '0',   '0',   '0',   '0',
            '0',   '0',   '0',   '0',   '0',   '0',   '0',   '0',
        ]
        
        pos=0
        for i in range(0,8):
                for j in range(0,8):
                    self.blocks[i][j]={}
                    #level에 따른 map 설정
                    if(self.level==1):
                        self.blocks[i][j]['num']= level1_map[pos]
                        self.numBlocks=1 
                    elif(self.level==2):
                        self.blocks[i][j]['num']= level2_map[pos]
                        self.numBlocks=1 
                    elif(self.level==3):
                        self.blocks[i][j]['num']= level3_map[pos]
                        self.numBlocks=2
                    elif(self.level==4):
                        self.blocks[i][j]['num']= level4_map[pos]
                        self.numBlocks=2
                    elif(self.level==5):
                        self.blocks[i][j]['num']= level5_map[pos]
                        self.numBlocks=4
                    elif(self.level==6):
                        self.blocks[i][j]['num']= level6_map[pos]
                        self.numBlocks=4
                    elif(self.level==7):
                        self.blocks[i][j]['num']= level7_map[pos]
                        self.numBlocks=5
                    elif(self.level==8):
                        self.blocks[i][j]['num']= level8_map[pos]
                        self.numBlocks=6
                    elif(self.level==9):
                        self.blocks[i][j]['num']= level9_map[pos]
                        self.numBlocks=5

                    #목적지 블록 : -1 일반 블록: 0 숫자 블록: 1~4
                    #평상시: 0 블록 클릭되었을 때:1 갈 수 있는 표시 뜰 때:2(위) 3(아래) 4(왼) 5(오)
                    #(숫자블록) 선택됨: -1
                    self.blocks[i][j]['state']= 0
                    pos+=1
            

    def clickBlock(self,pos):
        x=pos[0]
        y=pos[1]
        if(self.blocks[y][x]['num']=='-1'): #destination block인 경우
            if(self.blocks[y][x]['state']!=0 and self.blocks[y][x]['state']!=1): #갈 수 있는 표시 뜰 때(평상시, 블록 확장된 상태 x)
                self.goWay(pos,self.blocks[y][x]['state'])
                self.win=True                
        elif(self.blocks[y][x]['num']=='0'): #일반 block인 경우
            if(self.blocks[y][x]['state']!=0 and self.blocks[y][x]['state']!=1): #갈 수 있는 표시 뜰 때(평상시, 블록 확장된 상태 x)
                self.goWay(pos,self.blocks[y][x]['state'])                
        else: #number block인 경우
            if(self.blocks[y][x]['state']==0): #이전에 클릭 안된 경우
                if(self.clicked==True): #이미 클릭된 블록이 있다면
                    self.closeWay(self.clickedBlock)
                    self.blocks[self.clickedBlock[1]][self.clickedBlock[0]]['state']=0
                self.openWay(pos)
                self.blocks[y][x]['state']=1
            elif (self.blocks[y][x]['state']==1): #이전에 클릭된 경우 -> 원상태로
                self.closeWay(pos)
                self.blocks[y][x]['state']=0
                
    def goWay(self,pos,state): #선택한 위치로 확장(이동)
        pos=self.clickedBlock
        self.closeWay(pos)
        x=pos[0]
        y=pos[1]
        i=0
        count=0
        if(state==2): # 위
            while(count<int(self.blocks[y][x]['num'])):
                if(y-i<0): #범위 밖
                    break
                if(self.blocks[y-i][x]['num']=='-1' or self.blocks[y-i][x]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y-i][x]['state']!=1):#열리지 않았을 때
                        self.blocks[y-i][x]['state']=1
                        count+=1                       
                i+=1
        i=0
        count=0              
        if(state==3): # 아래
            while(count<int(self.blocks[y][x]['num'])):
                if(y+i>7): #범위 밖
                    break
                if(self.blocks[y+i][x]['num']=='-1' or self.blocks[y+i][x]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y+i][x]['state']!=1): #열리지 않았을 때
                        self.blocks[y+i][x]['state']=1
                        count+=1
                i+=1
        i=0
        count=0 
        if(state==4): # 왼
            while(count<int(self.blocks[y][x]['num'])):
                if(x-i<0): #범위 밖
                    break
                if(self.blocks[y][x-i]['num']=='-1' or self.blocks[y][x-i]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y][x-i]['state']!=1):#열리지 않았을 때
                        self.blocks[y][x-i]['state']=1
                        count+=1
                i+=1
        i=0
        count=0 
        if(state==5): # 오
            while(count<int(self.blocks[y][x]['num'])): #num만큼 위쪽 방향으로 갈 수 있는 길 표시
                if(x+i>7): #범위 밖
                    break
                if(self.blocks[y][x+i]['num']=='-1' or self.blocks[y][x+i]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y][x+i]['state']!=1):#열리지 않았을 때
                        self.blocks[y][x+i]['state']=1
                        count+=1
                i+=1
                
        self.blocks[y][x]['state']=-1 # 선택됨 다시 못고침
        self.numBlocks-=1 # 숫자 블록 수 --
                
    def openWay(self,pos): #갈 수 있는 길 표시
        x=pos[0]
        y=pos[1]
        i=0
        count=0
        while(count<int(self.blocks[y][x]['num'])): #num만큼 위쪽 방향으로 갈 수 있는 길 표시
            if(y-i<0): #범위 밖
                break
            else:
                if(self.blocks[y-i][x]['num']=='-1' or self.blocks[y-i][x]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y-i][x]['state']!=1):
                        self.blocks[y-i][x]['state']=2
                        count+=1
                i+=1
        i=0
        count=0
        while(count<int(self.blocks[y][x]['num'])): #num만큼 아래쪽 방향으로 갈 수 있는 길 표시
            if(y+i>7): #범위 밖
                break
            else:
                if(self.blocks[y+i][x]['num']=='-1' or self.blocks[y+i][x]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y+i][x]['state']!=1):
                        self.blocks[y+i][x]['state']=3
                        count+=1
                i+=1
        i=0
        count=0
        while(count<int(self.blocks[y][x]['num'])): #num만큼 왼쪽 방향으로 갈 수 있는 길 표시
            if(x-i<0): #범위 밖
                break
            else:
                if(self.blocks[y][x-i]['num']=='-1' or self.blocks[y][x-i]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y][x-i]['state']!=1):
                        self.blocks[y][x-i]['state']=4
                        count+=1
                i+=1
        i=0
        count=0
        while(count<int(self.blocks[y][x]['num'])): #num만큼 오른쪽 방향으로 갈 수 있는 길 표시
            if(x+i>7): #범위 밖
                break
            else:
                if(self.blocks[y][x+i]['num']=='-1' or self.blocks[y][x+i]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y][x+i]['state']!=1):
                        self.blocks[y][x+i]['state']=5
                        count+=1
                i+=1
                
        self.clicked=True
        self.clickedBlock=pos
        
    def closeWay(self,pos): #갈 수 있는 길 표시 해제
        x=pos[0]
        y=pos[1]
        i=0
        count=0
        while(count<int(self.blocks[y][x]['num'])): #num만큼 위쪽 방향으로 갈 수 있는 길 표시 해제
            if(y-i<0): #범위 밖
                break
            else:
                if(self.blocks[y-i][x]['num']=='-1' or self.blocks[y-i][x]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y-i][x]['state']!=1):
                        self.blocks[y-i][x]['state']=0
                        count+=1
                i+=1
        i=0
        count=0
        while(count<int(self.blocks[y][x]['num'])): #num만큼 아래쪽 방향으로 갈 수 있는 길 표시 해제
            if(y+i>7): #범위 밖
                break
            else:
                if(self.blocks[y+i][x]['num']=='-1' or self.blocks[y+i][x]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y+i][x]['state']!=1):
                        self.blocks[y+i][x]['state']=0
                        count+=1
                i+=1
        i=0
        count=0
        while(count<int(self.blocks[y][x]['num'])): #num만큼 왼쪽 방향으로 갈 수 있는 길 표시 해제
            if(x-i<0): #범위 밖
                break
            else:
                if(self.blocks[y][x-i]['num']=='-1' or self.blocks[y][x-i]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y][x-i]['state']!=1):
                        self.blocks[y][x-i]['state']=0
                        count+=1
                i+=1
        i=0
        count=0
        while(count<int(self.blocks[y][x]['num'])): #num만큼 오른쪽 방향으로 갈 수 있는 길 표시 해제
            if(x+i>7): #범위 밖
                break
            else:
                if(self.blocks[y][x+i]['num']=='-1' or self.blocks[y][x+i]['num']=='0') : #일반 or destination block인 경우
                    if(self.blocks[y][x+i]['state']!=1):
                        self.blocks[y][x+i]['state']=0
                        count+=1
                i+=1
                
        self.clicked=False
class Menu:
    def __init__(self,screen):
        self.screen=screen
        
    def mainloop(self):
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.fill((255,255,255))
            pygame.draw.rect (self.screen,(0,0,0), [50, 450, 100, 100])

            pygame.display.update() 

      

                        
if __name__ == '__main__':
    Game = Game()
    Game.play()
