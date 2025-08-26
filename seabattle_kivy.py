# -*- coding: utf-8 -*-
"""
Seabattle - спрощена версія для компіляції в APK через Kivy
"""
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock

# Конфігурація гри
GRID_SIZE = 10
FLEET_COUNTS = {4:1, 3:2, 2:3, 1:4}

class SeabattleGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid = [['empty' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []
        self.game_over = False
        
        # Створюємо випадковий флот
        self.create_random_fleet()
        
        # Прив'язуємо події
        self.bind(on_touch_down=self.on_touch_down)
        
    def create_random_fleet(self):
        """Створює випадковий флот на полі"""
        for ship_size, count in FLEET_COUNTS.items():
            for _ in range(count):
                placed = False
                attempts = 0
                while not placed and attempts < 100:
                    attempts += 1
                    x = random.randint(0, GRID_SIZE - 1)
                    y = random.randint(0, GRID_SIZE - 1)
                    horizontal = random.choice([True, False])
                    
                    if self.can_place_ship(x, y, ship_size, horizontal):
                        self.place_ship(x, y, ship_size, horizontal)
                        placed = True
    
    def can_place_ship(self, x, y, size, horizontal):
        """Перевіряє чи можна розмістити корабель"""
        if horizontal:
            if x + size > GRID_SIZE:
                return False
            for i in range(size):
                if self.grid[y][x + i] != 'empty':
                    return False
        else:
            if y + size > GRID_SIZE:
                return False
            for i in range(size):
                if self.grid[y + i][x] != 'empty':
                    return False
        return True
    
    def place_ship(self, x, y, size, horizontal):
        """Розміщує корабель на полі"""
        ship_cells = []
        if horizontal:
            for i in range(size):
                self.grid[y][x + i] = 'ship'
                ship_cells.append((x + i, y))
        else:
            for i in range(size):
                self.grid[y + i][x] = 'ship'
                ship_cells.append((x, y + i))
        self.ships.append(ship_cells)
    
    def on_touch_down(self, touch):
        """Обробка дотиків до екрану"""
        if self.game_over:
            return
            
        # Перетворюємо координати дотику в координати сітки
        cell_width = self.width / GRID_SIZE
        cell_height = self.height / GRID_SIZE
        
        grid_x = int(touch.x / cell_width)
        grid_y = int((self.height - touch.y) / cell_height)
        
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            self.shoot(grid_x, grid_y)
        
        return True
    
    def shoot(self, x, y):
        """Стріляє по координатах"""
        if self.grid[y][x] == 'ship':
            self.grid[y][x] = 'hit'
            self.check_win()
        elif self.grid[y][x] == 'empty':
            self.grid[y][x] = 'miss'
        
        # Перемальовуємо поле
        self.canvas.clear()
        self.draw_grid()
    
    def check_win(self):
        """Перевіряє чи гра закінчена"""
        for row in self.grid:
            if 'ship' in row:
                return
        self.game_over = True
        print("Перемога! Всі кораблі потоплено!")
    
    def draw_grid(self):
        """Малює ігрове поле"""
        with self.canvas:
            cell_width = self.width / GRID_SIZE
            cell_height = self.height / GRID_SIZE
            
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    cell_x = x * cell_width
                    cell_y = (GRID_SIZE - 1 - y) * cell_height
                    
                    # Вибираємо колір залежно від стану клітинки
                    if self.grid[y][x] == 'hit':
                        Color(1, 0, 0, 1)  # Червоний для влучань
                    elif self.grid[y][x] == 'miss':
                        Color(0, 0, 1, 0.5)  # Синій для промахів
                    elif self.grid[y][x] == 'ship':
                        Color(0.5, 0.5, 0.5, 1)  # Сірий для кораблів (показуємо для тестування)
                    else:
                        Color(0, 0.5, 1, 0.3)  # Світло-синій для води
                    
                    Rectangle(pos=(cell_x, cell_y), size=(cell_width-2, cell_height-2))
            
            # Малюємо сітку
            Color(1, 1, 1, 1)  # Білий для ліній
            for i in range(GRID_SIZE + 1):
                # Вертикальні лінії
                x = i * cell_width
                Rectangle(pos=(x, 0), size=(1, self.height))
                # Горизонтальні лінії
                y = i * cell_height
                Rectangle(pos=(0, y), size=(self.width, 1))

class SeabattleApp(App):
    def build(self):
        # Головний контейнер
        root = BoxLayout(orientation='vertical')
        
        # Заголовок
        title = Label(text='Seabattle - Морський Бій', size_hint_y=0.1, font_size=24)
        root.add_widget(title)
        
        # Ігрове поле
        game = SeabattleGame()
        root.add_widget(game)
        
        # Кнопки управління
        controls = BoxLayout(size_hint_y=0.1, orientation='horizontal')
        
        new_game_btn = Button(text='Нова гра')
        new_game_btn.bind(on_press=lambda x: self.new_game(game))
        controls.add_widget(new_game_btn)
        
        exit_btn = Button(text='Вихід')
        exit_btn.bind(on_press=lambda x: self.stop())
        controls.add_widget(exit_btn)
        
        root.add_widget(controls)
        
        # Запускаємо малювання після створення віджету
        Clock.schedule_once(lambda dt: game.draw_grid(), 0.1)
        
        return root
    
    def new_game(self, game_widget):
        """Починає нову гру"""
        game_widget.grid = [['empty' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        game_widget.ships = []
        game_widget.game_over = False
        game_widget.create_random_fleet()
        game_widget.canvas.clear()
        game_widget.draw_grid()

if __name__ == '__main__':
    SeabattleApp().run()
