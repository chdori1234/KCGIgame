'''
----------------------------------------------------
Pythonゲーム開発
作成者：Chongmyung park
作成日：2019/12/01
説明：Pygameを利用、簡単なアナコンダゲームを実装
----------------------------------------------------
'''

#game制作ライブラリ
import pygame
#ゲームシステム画面ライブラリ
import sys
#時間関連ライブラリ
import time
#ランダムライブラリ
import random

from pygame.locals import *

#変数宣言

#画面の大きさ
CONSOLE_WIDTH = 800;
CONSOLE_HEIGTH = 600;
#画面の背景
WHITE = (255, 255, 255)
#アナコンダの色
GREEN = (0, 50, 0)
#エサの色
BLACK = (0, 0, 0)
#Play情報の色
RED = (150, 0, 0)

#アナコンダのサイズ
#Pixelを使用する場合サイズが小さいなので使用する
SHELL_SIZE = 20
SHELL_WIDTH = CONSOLE_WIDTH / SHELL_SIZE
SHELL_HEIGTH = CONSOLE_HEIGTH / SHELL_SIZE

#キー操作変数
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#アナコンダのスピード
FPS = 10

#アナコンダの動作を定義するクラス
class Python(object):
    #Main
    def __init__(self):
        self.create()
        self.color = GREEN
    #最初のアナコンダを作る
    def create(self):
        #開始のアナコンダサイズ
        self.length = 2
        #開始位置(画面の中央)
        self.positions = [((CONSOLE_WIDTH / 2), (CONSOLE_HEIGTH / 2))]
        #開始の頭の位置を定義（Random）
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    
    #アナコンダんも動作監視
    def control(self, xy):
        #反対側には動かないように座標値をチェック
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else :
            self.direction = xy
    #アナコンダの動きをチェック
    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        #アナコンダのbodyを作成(画面を超えた場合には反対側の画面で現れる)
        new = (((cur[0] + (x * SHELL_SIZE)) % CONSOLE_WIDTH), (cur[1] + (y * SHELL_SIZE)) % CONSOLE_HEIGTH)
        #アナコンダが自身のBodyと会った場合には最初から再開する
        if new in self.positions[2:]:
            self.create()
        #それ以外の場合には動く
        else : 
            self.positions.insert(0, new)
            #動きを表現する為、長さを調整する
            if len(self.positions) > self.length:
                self.positions.pop()
    #エサを食べたら長さを１増やす
    def eat(self):
        self.length += 1

    #アナコンダを実際に出力する関数
    def draw(self, surface):
        for p in self.positions:
            draw_object(surface, self.color, p)

#エサを出力する            
class Feed(object):
    #Main
    def __init__(self):
        self.position = (0, 0)
        self.color = BLACK
        self.create()
    
    #エサを出力    
    def create(self):
        self.position = (random.randint(0, SHELL_WIDTH - 1) * SHELL_SIZE, random.randint(0, SHELL_HEIGTH - 1) * SHELL_SIZE)
    
    #エサを実際に出力
    def draw(self, surface):
        draw_object(surface, self.color, self.position)

#出力処置の定義
def draw_object(surface, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (SHELL_SIZE, SHELL_SIZE))
    pygame.draw.rect(surface, color, r)

#エサを食べる動作をチェック
def check_eat(pythong, feed):
    if pythong.positions[0] == feed.position:
        python.eat()
        feed.create()

#スピード、長さを出力
def game_info(length, speed, surface):
    font = pygame.font.Font(None, 34)
    text = font.render("Length: " + str(length) + "       Speed " + str(round(speed, 2)), 1, RED)
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text, pos)

#メインメソッド開始
if __name__== '__main__':
    python = Python()
    feed = Feed()

    #pygame初期化
    pygame.init()
    #画面の大きさを設定
    window = pygame.display.set_mode((CONSOLE_WIDTH, CONSOLE_HEIGTH),0, 32)
    #ゲーム名を上段バーに出力
    pygame.display.set_caption('Anaconda GAME')
    #画面設定
    surface = pygame.Surface(window.get_size())
    surface = surface.convert()
    surface.fill(WHITE)
    #時刻設定
    clock = pygame.time.Clock()
    #キー反応設定
    pygame.key.set_repeat(1, 40)
    #画面開始
    window.blit(surface, (0, 0))

    #蛇の動作をチェック
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    python.control(UP)
                elif event.key == K_DOWN:
                    python.control(DOWN)
                elif event.key == K_LEFT:
                    python.control(LEFT)
                elif event.key == K_RIGHT:
                    python.control(RIGHT)
        
        #背景出力
        surface.fill(WHITE)
        #動作呼び出し
        python.move()
        #エサチェック
        check_eat(python, feed)
        #エサを食べることで速度増加
        speed = (FPS + python.length) / 2
        #ゲームの情報を出力
        game_info(python.length, speed, surface)
        #再出力処理
        python.draw(surface)
        #エサを再出力
        feed.draw(surface)

        window.blit(surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(speed)