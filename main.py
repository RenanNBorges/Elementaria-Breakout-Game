from graphics import *
from engine import *

import math
import time

class Menu:
    def __init__(self, options,win, win_width=800, win_height=800):
        self.options = options
        self.win = win
        self.selected_option = 0
        self.selected = options[self.selected_option]
        self.banner = Image(Point(win_width/2,200),"img/name.gif")
        self.image = Image(Point(win_width/2,win_height/2),"img/menus/inicial-menu.gif")
        self.image.draw(self.win)
        self.banner.draw(self.win)
        
        
        
        
    def draw_menu(self):
        for i in range(len(self.options)):
            option = Text(Point(400, 425 + i * 50), self.options[i])
            if i == self.selected_option:
                option.setFill("red")
            option.draw(self.win)

    def get_selected(self):
        return self.selected

    def run_menu(self):
        self.draw_menu()
        
        while True:
            key = self.win.getKey()
            if key == "Up":
                if self.selected_option > 0:
                    self.selected_option -= 1
                    self.selected = self.options[self.selected_option]
            elif key == "Down":
                if self.selected_option < len(self.options) - 1:
                    self.selected_option += 1
                    self.selected = self.options[self.selected_option]
            elif key == "Return": #verificação se a tecla pressionada é enter
                if self.get_selected() == "Sair":
                    exit()
                break #interrompe o loop e volta para o código que chamou a função run()
            for option in self.win.items[:]:
                if isinstance(option,Text):
                    option.undraw()
            self.draw_menu()
            update(30)

class ObjetoGame:
    def __init__(self,object,img,window):
        self.item = object
        self.win = window
        self.__centerPoint = self.item.getCenter()
        self.image = Image(self.get_centerPoint(),img)
        self.collide = True

    def undraw(self):
        self.image.undraw()
        self.item.undraw()
    
    def move_on(self,x,y):
        self.image.move(x,y)
        self.item.move(x,y)
        self.__centerPoint = self.item.getCenter()
    
    def set_image(self,image:str):
        self.image.img = image
    
    def get_object(self):
        return self.item 
    
    def get_centerPoint(self):
        return self.__centerPoint


    
    
        
class Bola(ObjetoGame):
    def __init__(self, x, y, angulo, janela):
        super().__init__(Circle(Point(x, y), 10),'img/ball.gif',janela)
        self.angulo = angulo
        self.mode = 1
        self.collide = False
        self.velocidade = 5

    def movimentar(self):
        self.move_on(self.velocidade * math.cos(math.radians(self.angulo)),
                       self.velocidade * math.sin(math.radians(self.angulo)))

        x = self.item.getCenter().getX()
        y = self.item.getCenter().getY()
        r = self.item.getRadius()
        
        if self.mode == 1:
            if x - r <= 0 or x + r >= self.win.width:
                self.angulo = 180 - self.angulo
                return True
            if y - r <= 50:
                self.angulo = - self.angulo
                return True
        
        elif self.mode == 2:
            if x - r <= 0 or x + r >= self.win.width:
                self.angulo = 180 - self.angulo
                return True
            if y - r <= 100 or y + r >= self.win.height:
                self.angulo = - self.angulo
                return True

        
    def set_velocidade(self, velocidade):
        self.velocidade = velocidade
        return self.velocidade

    @staticmethod
    def nearst_point(min, max, unit_coord):
        if unit_coord < min:
            return min
        elif unit_coord > max:
            return max
        else:
            return unit_coord

    def colisao(self, retangulo):
        retangulo = retangulo
        x = self.nearst_point(retangulo.getP1().getX(),
                           retangulo.getP2().getX(),
                           self.item.getCenter().getX())
        y = self.nearst_point(retangulo.getP1().getY(),
                           retangulo.getP2().getY(),
                           self.item.getCenter().getY())

        distancia_entre = math.sqrt((self.item.getCenter().getX() - x)**2 +
                                    (self.item.getCenter().getY() - y)**2)
        if distancia_entre - self.item.getRadius() <= 3:
            self.angulo = self.reacao_colisao(retangulo.getCenter())
            self.velocidade += 0.001
            return True

    def reacao_colisao(self,coords):
        # Calcular o ângulo de reflexão
        angulo_incidente = math.degrees(math.atan2(
            self.item.getCenter().getY() -
            coords.getY(),
            self.item.getCenter().getX() -
            coords.getX()))
        angulo_normal = math.degrees(math.atan2(
            self.item.getCenter().getY() -
            coords.getY(),
            self.item.getCenter().getX() -
            coords.getX()))
        angulo_refletido = 2 * angulo_normal - angulo_incidente
        return angulo_refletido

    def set_mode(self,mode:int):
        self.mode = mode
        return self.mode


class Tijolo(ObjetoGame):
    def __init__(self,x,y,hits):
        super().__init__(Rectangle(Point(x-35,y-15),Point(x+15,y+15)),'img/enemy.gif',None)
        self.hits = hits
        
    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            self.undraw()
        return self.hits

class Paddle(ObjetoGame):
    def __init__(self,x,y, window):
        super().__init__(Rectangle(Point(x-50,y-20),Point(x+50,y+20)),'img/player.gif',window)
        self.moves = Mover(self.item)
        self.moves_rotation = Rotation(self.item,Point(400,400),100,7)
        self.moves.config_keys(right= True,left=True)
        self.left = "Left"
        self.right = "Right"
        self.speed = 15
        self.mode = 1
        
        

    def move(self,key):
        self.image.undraw()
        if self.mode == 1 :
            if key == self.left and self.item.getP1().getX() > 0:
                self.move_on(-self.speed,0)
            elif key == self.right and self.item.getP2().getX() < 800:
                self.move_on(self.speed,0)
                
        elif self.mode == 2 or self.mode == 3:
            self.moves_rotation.move_girar(key)

        self.image = Image(self.item.getCenter(),'img/player.gif')
        self.image.draw(self.win)
        
        

    def set_mode(self,mode:int):
        self.mode = mode
        return self.mode

    def config_keymap(self,config):
        if config == 1:
            self.left = "Left"
            self.right = "Right"
            return 'Configuração Atualizada!'
        
        elif config == 2:
            self.left = "a"
            self.right = "d"
            return 'Configuração Atualizada!'

        else:
            return 'Configuração Não Atualizada'

class Lifes:
    def __init__(self,life,window):
        self.lifes_count = life
        self.win = window
        self.lifes_list = []
        x, y = 50, 25
        for life in range(self.lifes_count):
            self.life = ObjetoGame(Circle(Point(x,y),10),"img/life.gif",self.win)
            self.lifes_list.append(self.life)
            x += 45
            
    def del_life(self):
        if len(self.lifes_list) > 0:
            self.lifes_list[-1].undraw()
            del self.lifes_list[-1]
            return len(self.lifes_list)
        else:
            return 0
    
    def reset_life(self):
        for i in enumerate(self.lifes_count):
            self.del_life()
        x, y = 50, 25
        for life in range(self.lifes_count):
            self.life = ObjetoGame(Circle(Point(x,y),10),"img/life.gif",self.win)
            self.lifes_list.append(self.life)
            x += 45
            
    def set_lifes(self,lifes):
        self.lifes_count = lifes
        return self.lifes_count
   
class Stage:
    def __init__(self,window):
        self.scenerys = ['img/scenery/scenery-1.gif','img/scenery/scenery-2.gif','img/scenery/scenery-1.gif']
        self.objects = []
        self.win = window
        self.ball_move = False
        self.actual_stage = 0
        self.mode = 1
        self.points = 0
        self.lifes_init = Lifes(5,self.win)
        self.stage_txt = Text(Point(self.win.width - 150,25),f"Fase {self.actual_stage+1}")
        self.stage_txt.setSize(32)
        self.stage_txt.setFill("white")
        self.add_object(self.stage_txt)
        self.player = Paddle(self.win.width/2,self.win.height-50,self.win)
        self.ball = Bola(self.player.item.getCenter().getX(),
                        self.player.item.getCenter().getY(),
                        -90,self.win)
         
    def add_object(self,object):
        self.objects.append(object)

    def del_object(self,object):
        self.objects.remove(object)
        
    def add_ball(self):
        self.ball = Bola(self.player.item.getCenter().getX(),
                        self.player.item.getCenter().getY() - 50,
                        -90,self.win)
        self.add_object(self.ball)
        self.ball.set_mode(self.mode)
    
    def add_paddle(self):
        self.player = Paddle(self.win.width/2,self.win.height-50,self.win)
        self.player.set_mode(self.mode)
        self.add_object(self.player)
        
    def add_enemys(self,x,y,columm = 10, row = 8):
        self.enemys_table = []
        p1_x = x
        p1_y = y
        for i in range(columm):
            for j in range(row):
                self.enemys_table.append(Tijolo(p1_x, p1_y, 1))
                self.add_object(self.enemys_table[-1])
                self.points += 2
                p1_x += 85
            p1_x = x
            p1_y += 30
    
    def set_scenery(self,scenery_atual:int):
        self.scenery = Image(Point(self.win.width/2, (self.win.height/2)+55),self.scenerys[scenery_atual])
    
    def set_stage(self):
        if self.actual_stage <= 1 and self.actual_stage < 3:
            self.mode = 1
            for life in self.lifes_init.lifes_list:
                self.add_object(life)
            self.set_scenery(0)
            self.scenery.draw(self.win)
            self.add_enemys(100,125)
            return 'Configured'
        elif self.actual_stage >= 4 and self.actual_stage <= 6:
            self.mode = 2
            self.lifes_init = Lifes(3,self.win)
            self.set_scenery(1)
            self.add_enemys(100,300)
            return 'Configured'
        elif self.actual_stage > 6:
            self.mode = 2
            self.lifes_init = Lifes(2,self.win)
            self.set_scenery(2)
            self.add_enemys(100,300)
            return 'Configured'
        
    def draw_objects(self):
        for i, object in enumerate(self.objects):
            try:
                object.image.draw(self.win)
            except AttributeError:
                object.draw(self.win)
        
    def init_stage(self):
        self.reset_tela()
        self.set_stage()
        self.add_paddle()
        self.add_ball()
        self.draw_objects()
        self.wait_ball()
        
    def wait_ball(self):
        while True:
            key = self.win.checkKey()
            self.player.move(key)
            self.ball.move_on(self.player.get_centerPoint().getX() - self.ball.get_centerPoint().getX(),(self.player.get_centerPoint().getY() - self.ball.get_centerPoint().getY())-60)
            if key == "space":
                return 0
    
    def reset_tela(self):
        for itens in self.win.items[:]:
            itens.undraw()
        print(self.win.items)
    
    def check_stage(self):
        if self.ball.get_centerPoint().getY() > 800 or self.ball.get_centerPoint().getY() < 0 or self.ball.get_centerPoint().getX() < 0 or self.ball.get_centerPoint().getX() > self.win.height:
            self.ball.angulo = -90
            self.wait_ball()
            if self.lifes_init.del_life() == 0:
                for itens in self.win.items[:]:
                    itens.undraw()
                game_over = Text(Point(400,450),"GAME OVER!!!")
                game_over.setSize(32)
                game_over.setFill("white")
                game_over.draw(self.win)
                self.actual_stage = 1
        elif len(self.enemys_table) == 0:
            self.actual_stage += 1
            self.reset_tela()
            self.init_stage()
        



class Jogo(Stage):
    def __init__(self):
        self.win_open = Janela("Breakout Adventure",800,800)
        self.win = self.win_open.getWin()
        self.win.setBackground(color_rgb(19, 37, 23))
        super().__init__(self.win)
        self.menu = Menu(["Jogar", "Sair"],self.win,800,800)
        
    def run(self):
        self.init_stage()
        while True:
            key = self.win.checkKey()
            self.ball.movimentar()
            self.check_collison()
            self.player.move(key)
            self.check_stage()
            update(60)
    
        

    def check_collison(self):
        for object in self.enemys_table:
            if self.ball.colisao(object.item):
                if object.hit() == 0:
                    self.enemys_table.remove(object)
                    
        self.ball.colisao(self.player.item)
        
        


def main():
    game = Jogo()
    game.menu.run_menu()
    game.run()

main()