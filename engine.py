'''
Conjunto de classes e funções para melhor uso da inteface gráfica gerada pelo módulo graphics.py que incluem:
Janela
Keys
Mover
'''
from graphics import *
import math
import time


class Janela:

    def __init__(self, title: str, largura: int, altura: int):
        '''Classe que cria uma interface gráfica, recebe como paramêtros o título,a largura e a altura da janela, permite adicionar e remover objetos da tela'''
        self.__title = title
        self.__largura = largura
        self.__altura = altura
        self.__win = GraphWin(title, largura, altura, autoflush=False)

        self.__obj_in_tela = []

    def getObj_in_tela(self):
        '''Método para acessar a lista de objetos na tela'''
        return self.__obj_in_tela

    def getWin(self):
        '''Método para acessar o objeto que representa a tela'''
        return self.__win

    def addObj_in_tela(self, objeto: object):
        '''Método que adiciona um objeto da lista de objetos na tela, parametros: objetos gráficos'''
        self.getObj_in_tela().append(objeto)

    def draw_tela(self,object):
        object.draw(self.getWin())

    def delObj_in_tela(self, objeto: object):
        '''Método que remove um objeto da lista de objetos na tela, parametros: objetos gráficos'''
        self.getObj_in_tela().remove(objeto)
        
        return self.__obj_in_tela

    def del_tela(self,object):
        object.undraw()
        
    def add_mult_objs(self, list: list):
        '''Método que adiciona vários objetos da tela, parametros: lista de objetos gŕaficos'''
        for objeto in list:
            self.addObj_in_tela(objeto)
        return self.getObj_in_tela

    def del_mult_objs(self, list: list):
        '''Método que deleta vários objetos da tela, parametros: lista de objetos gráficos'''
        for objeto in list:
            self.delObj_in_tela(objeto)
        return self.getObj_in_tela


class Keys:
    '''Classe para detectar eventos no teclado, lida com mais de uma tecla ao mesmo tempo.
    Para usar crie um objeto Keys e use a função "bind_all()"
    keys_obj = Keys()
    janela.bind_all("<KeyPress>", keys_obj.pressionar_tecla)
    function_use_key(keys_obj.key)
    janela.bind_all("<KeyRelease>", keys_obj.soltar_tecla)
    '''

    def __init__(self):
        self.keys = []

    def pressionar_tecla(self, event):
        self.keys.append(event.keysym)

    def soltar_tecla(self, event):
        if event.keysym in self.keys:
            self.keys.remove(event.keysym)


class Mover:

    def __init__(self, objeto):
        '''Classe para mover um objeto'''
        self.objeto = objeto
        self.direcao = [1, 1]
        self.to_up = True
        self.to_down = True
        self.to_left = True
        self.to_right = True
        self.move_to_up = "Up"
        self.move_to_down = "Down"
        self.move_to_left = "Left"
        self.move_to_right = "Right"

    def move_click(self, event):
        self.x = (event.x) - self.objeto.getCenter().getX()
        self.y = (event.y) - self.objeto.getCenter().getY()
        self.objeto.move(self.x, self.y)

    def move_key(self,
                 keys,
                 velocidade=1):
        self.move_type = "one"
        self.keys = keys
        self.speed = velocidade

        if len(self.keys) == 1 and self.move_type == "one":
            if self.move_to_up in self.keys:
                self.__move_up()
                return 90

            elif self.move_to_down in self.keys:
                self.__move_down()
                return -90

            elif self.move_to_right in self.keys:
                self.__move_right()
                return 0

            elif self.move_to_left in self.keys:
                self.__move_left()
                return 180

        elif len(self.keys) == 2:
            if ( self.move_to_right == self.keys[-1]
                    or self.move_to_right == self.keys[-2]) and ( self.move_to_up == self.keys[-1]
                                                    or self.move_to_up == self.keys[-2]):
                if self.to_right and self.to_up:
                    self.x = self.speed * math.cos(math.radians(-45))
                    self.y = self.speed * math.sin(math.radians(-45))
                    self.objeto.move(self.x, self.y)

            elif ( self.move_to_right == self.keys[-1]
                  or self.move_to_right == self.keys[-2]) and ( self.move_to_down == self.keys[-1]
                                                  or self.move_to_down == self.keys[-2]):
                self.__move_right()
                self.__move_down()

            elif ( self.move_to_left == self.keys[-1]
                  or self.move_to_left == self.keys[-2]) and ( self.move_to_up == self.keys[-1]
                                                 or self.move_to_up == self.keys[-2]):
                self.__move_left()
                self.__move_up()

            elif (self.move_to_left == self.keys[-1]
                  or self.move_to_left == self.keys[-2]) and (self.move_to_down == self.keys[-1]
                                                 or self.move_to_down == self.keys[-2]):
                self.__move_left()
                self.__move_down()

        else:
            return 0

    def __move_right(self):
        if self.to_right:
            self.x = self.speed * math.cos(math.radians(0))
            self.y = self.speed * math.sin(math.radians(0))
            self.objeto.move(self.x, self.y)

    def __move_left(self):
        if self.to_left:
            self.x = self.speed * math.cos(math.radians(180))
            self.y = self.speed * math.sin(math.radians(180))
            self.objeto.move(self.x, self.y)

    def __move_up(self):
        if self.to_up:
            self.x = self.speed * math.cos(math.radians(-90))
            self.y = self.speed * math.sin(math.radians(-90))
            self.objeto.move(self.x, self.y)

    def __move_down(self):
        if self.to_down:
            self.x = self.speed * math.cos(math.radians(90))
            self.y = self.speed * math.sin(math.radians(90))
            self.objeto.move(self.x, self.y)

    def config_keys(self, up=False, down=False, right=False, left=False):
        self.to_up = up
        self.to_down = down
        self.to_left = left
        self.to_right = right

    def set_keys(self, up="UP", down="Down", right="Right", left="Left"):
        self.to_up = up
        self.to_down = down
        self.to_left = left
        self.to_right = right

    def set_velocidade(self, velocidade):
        self.speed = velocidade

    def set_move_type(self,mode):
        self.move_type = mode
        return self.move_type


class Rotation:

    def __init__(self, central_point, objeto_girando, distancia, velocidade,angulo=0):
        self.central_point = central_point
        self.objeto_girando = objeto_girando
        self.distancia = distancia
        self.velocidade = velocidade
        self.angulo = angulo
        self.left = "Left"
        self.right = "Right"

    def girar(self, angulo):

        x = self.central_point.getX() + self.distancia * math.cos(
            math.radians(angulo))
        y = self.central_point.getY() + self.distancia * math.sin(
            math.radians(angulo))
        self.objeto_girando.move(x - self.objeto_girando.getCenter().getX(),
                                 y - self.objeto_girando.getCenter().getY())

    def orbitar(self, sentido="+"):
        if sentido == "+":
            self.angulo += self.velocidade
        elif sentido == "-":
            self.angulo -= self.velocidade
        self.angulo %= 360
        self.girar(self.angulo)

    def move_girar(self, key):
        self.key = key
        if self.key == self.right:
            self.angulo += self.velocidade
            self.angulo %= 360
            self.girar(self.angulo)
        elif self.key == self.left:
            self.angulo -= self.velocidade
            self.angulo %= 360
            self.girar(self.angulo)
        update()

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

class Vetor:
    def __init__(self,objeto):
        self.objeto = objeto
        self.x_init, self.y_init = objeto.getCenter().getX(),objeto.getCenter().getY()
        self.vector = Line(Point(self.x_init, self.y_init),Point(0,0))
        self.angulo = 0
        
    def show_vetor(self):
        self.x_new, self.y_new = self.objeto.getCenter().getX(),self.objeto.getCenter().getY()
        if self.x_init != self.x_new or self.y_init != self.y_new:
            
            self.angulo = math.degrees(math.atan2(self.y_new - self.y_init, self.x_new - self.x_init))
            
            self.vector_x = (self.objeto.getCenter().getX() + (self.objeto.getRadius() * 2) * math.cos(math.radians(-self.angulo)))
            self.vector_y = (self.objeto.getCenter().getY() + (self.objeto.getRadius() * 2) * math.sin(math.radians(self.angulo))) 
            
            
            self.x_init, self.y_init = self.x_new, self.y_new
            self.vector.undraw()
            self.vector = Line(Point(self.x_init, self.y_init),Point(self.vector_x,self.vector_y))
            self.vector.setArrow("last")
            self.vector.setFill("white")
            return True