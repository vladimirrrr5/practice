import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QPushButton, QMessageBox, QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush

class MillionaireGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кто хочет стать миллионером")
        self.setMinimumSize(1200, 700)
        
        # Данные игры
        self.PRIZES = [
            500, 1_000, 2_000, 3_000, 5_000, 10_000, 20_000, 40_000, 80_000,
            160_000, 320_000, 640_000, 1_250_000, 2_500_000, 5_000_000
        ]
        
        self.QUESTIONS = [
            {"question": "Какое самое большое животное на Земле?", "options": ["Слон", "Синий кит", "Акула", "Крокодил"], 
             "answer": "Синий кит", "illustration": "🐋"},
            {"question": "Какой газ мы вдыхаем, чтобы жить?", "options": ["Азот", "Углекислый газ", "Кислород", "Водород"], 
             "answer": "Кислород", "illustration": "🌬️"},
            {"question": "Сколько планет в Солнечной системе?", "options": ["7", "8", "9", "10"], 
             "answer": "8", "illustration": "🪐"},
            {"question": "Какой континент самый большой?", "options": ["Африка", "Азия", "Европа", "Антарктида"], 
             "answer": "Азия", "illustration": "🌏"},
            {"question": "Какое государство самое маленькое в мире?", "options": ["Монако", "Науру", "Ватикан", "Сан-Марино"], 
             "answer": "Ватикан", "illustration": "🏛️"},
            {"question": "Какой металл самый легкий?", "options": ["Железо", "Алюминий", "Литий", "Медь"], 
            "answer": "Литий", "illustration": "⚛️"},
            {"question": "Столица Австралии?", "options": ["Сидней", "Мельбурн", "Канберра", "Брисбен"], 
            "answer": "Канберра", "illustration": "🇦🇺"},
            {"question": "Кто написал 'Война и мир'?", "options": ["Толстой", "Достоевский", "Пушкин", "Гоголь"], 
            "answer": "Толстой", "illustration": "📚"},
            {"question": "Сколько океанов на Земле?", "options": ["4", "5", "6", "7"], 
            "answer": "5", "illustration": "🌊"},
            {"question": "Сколько хромосом у человека?", "options": ["42", "44", "46", "48"], 
            "answer": "46", "illustration": "🧬"},
            {"question": "Какой химический элемент обозначается символом Au?", "options": ["Серебро", "Алюминий", "Золото", "Уран"], 
            "answer": "Золото", "illustration": "🥇"},
            {"question": "Где находятся пирамиды Гизы?", "options": ["Мексика", "Египет", "Индия", "Ирак"], 
            "answer": "Египет", "illustration": "🏜️"},
            {"question": "Какой язык самый распространенный в мире?", "options": ["Английский", "Испанский", "Китайский", "Арабский"], 
            "answer": "Китайский", "illustration": "🌐"},
            {"question": "Какой цвет получается при смешивании синего и жёлтого?", "options": ["Зелёный", "Оранжевый", "Фиолетовый", "Коричневый"], 
            "answer": "Зелёный", "illustration": "🎨"},
            {"question": "Кто первый полетел в космос?", "options": ["Нейл Армстронг", "Гагарин", "Королёв", "Титов"], 
            "answer": "Гагарин", "illustration": "🚀"},
        ]
        
        # Состояние игры
        self.current_question_index = 0
        self.used_5050 = False
        self.used_call = False
        self.seconds_left = 30
        self.timer = QTimer()
        
        self.init_ui()
        
    def init_ui(self):
        # Основной стек виджетов
        self.stack = QWidget()
        self.stack_layout = QVBoxLayout(self.stack)
        self.stack_layout.setContentsMargins(0, 0, 0, 0)
        
        # Главное меню
        self.main_menu = self.create_main_menu()
        self.stack_layout.addWidget(self.main_menu)
        
        # Экран правил
        self.rules_screen = self.create_rules_screen()
        self.stack_layout.addWidget(self.rules_screen)
        
        # Экран рейтинга
        self.rating_screen = self.create_rating_screen()
        self.stack_layout.addWidget(self.rating_screen)
        
        # Игровой экран
        self.game_screen = self.create_game_screen()
        self.stack_layout.addWidget(self.game_screen)
        
        # Показываем главное меню
        self.show_screen(self.main_menu)
        
        self.setCentralWidget(self.stack)
        
        # Настройка стилей
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00008B, stop:1 #000000);
                color: white;
                font-family: Arial;
            }
            
            QPushButton {
                background-color: gold;
                color: black;
                border: none;
                padding: 15px 30px;
                font-size: 20px;
                border-radius: 10px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #FFD700;
            }
            
            QPushButton#small_btn {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #4682B4;
                color: white;
            }
            
            QPushButton#exit_btn {
                background-color: #8B0000;
                color: white;
                border-radius: 30px;
                width: 60px;
                height: 60px;
                font-size: 24px;
            }
            
            QLabel#logo {
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 30px;
            }
            
            QLabel#question {
                font-size: 24px;
                background-color: #4169E1;
                padding: 20px;
                border-radius: 10px;
            }
            
            QLabel#timer {
                font-size: 24px;
                background-color: #1E90FF;
                padding: 10px;
                border-radius: 20px;
                qproperty-alignment: AlignCenter;
            }
            
            QLabel#illustration {
                font-size: 72px;
                background-color: #00008B;
                padding: 20px;
                border-radius: 10px;
                qproperty-alignment: AlignCenter;
            }
            
            QFrame#panel {
                background-color: rgba(0, 0, 139, 0.7);
                border-radius: 10px;
            }
            
            QLabel#prize_item {
                padding: 8px;
                margin: 5px 0;
                border-radius: 5px;
            }
            
            QPushButton#hint_btn {
                background-color: #32CD32;
                color: white;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                font-weight: bold;
            }
            
            QPushButton#hint_btn:disabled {
                background-color: gray;
            }
            
            QPushButton#option_btn {
                background-color: #1E3F66;
                color: white;
                padding: 15px;
                border-radius: 10px;
                font-size: 18px;
                border: 2px solid #2A4D7F;
                min-width: 280px;
                min-height: 70px;
                max-width: 280px;
                max-height: 70px;
                margin: 10px;
            }
            
            QPushButton#option_btn:hover {
                background-color: #2A4D7F;
            }
            
            QPushButton#option_btn:disabled {
                background-color: #333333;
                color: #888888;
            }
            
            QPushButton#option_btn_correct {
                background-color: #2E8B57;
                color: white;
            }
                QPushButton#exit_btn {
            background-color: #FF0000;
            color: white;
            border-radius: 30px;
            min-width: 60px;
            max-width: 60px;
            min-height: 60px;
            max-height: 60px;
            font-size: 24px;
            padding: 0;
            margin: 0;
            }
            
            QPushButton#exit_btn:hover {
                background-color: #CC0000;
        """)
    
    def create_main_menu(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Логотип
        logo = QLabel("Кто хочет стать миллионером")
        logo.setObjectName("logo")
        layout.addWidget(logo)
        
        # Кнопка начала игры
        start_btn = QPushButton("Начать игру")
        start_btn.clicked.connect(self.init_game)
        layout.addWidget(start_btn)
        
        # Кнопки правил и рейтинга
        btn_layout = QHBoxLayout()
        rules_btn = QPushButton("Правила")
        rules_btn.setObjectName("small_btn")
        rules_btn.clicked.connect(lambda: self.show_screen(self.rules_screen))
        btn_layout.addWidget(rules_btn)
        
        rating_btn = QPushButton("Рейтинг")
        rating_btn.setObjectName("small_btn")
        rating_btn.clicked.connect(lambda: self.show_screen(self.rating_screen))
        btn_layout.addWidget(rating_btn)
        
        layout.addLayout(btn_layout)
        
        # Кнопка выхода
        exit_btn = QPushButton("✖")
        exit_btn.setObjectName("exit_btn")
        exit_btn.clicked.connect(self.close)
        exit_btn.setFixedSize(60, 60)
        exit_btn.move(self.width() - 80, self.height() - 80)
        exit_btn = QPushButton("Выход")
        exit_btn.setObjectName("small_btn")
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)
        
        return widget
    
    def create_rules_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Контент правил
        rules_content = QLabel()
        rules_content.setObjectName("panel")
        rules_content.setWordWrap(True)
        rules_content.setText("""
            <h2>Правила игры</h2>
            <p>1. Вам будут заданы 15 вопросов с 4 вариантами ответа.</p>
            <p>2. Каждый правильный ответ увеличивает ваш выигрыш.</p>
            <p>3. Вопросы 5 и 9 — несгораемые суммы (5,000 ₽ и 80,000 ₽).</p>
            <p>4. Можно использовать подсказки:</p>
            <ul>
                <li>50/50: убирает два неверных ответа</li>
                <li>Звонок другу: друг подсказывает ответ</li>
            </ul>
            <p>5. На каждый вопрос даётся 30 секунд.</p>
            <p>Цель: выиграть 5,000,000 ₽!</p>
        """)
        rules_content.setFixedWidth(800)
        layout.addWidget(rules_content)
        
        # Кнопка назад
        back_btn = QPushButton("Назад в меню")
        back_btn.clicked.connect(lambda: self.show_screen(self.main_menu))
        layout.addWidget(back_btn)
        
        return widget
    
    def create_rating_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Контент рейтинга
        rating_content = QLabel()
        rating_content.setObjectName("panel")
        rating_content.setText("""
            <h2>Топ игроков</h2>
            <p>1. Иван Петров — 5,000,000 ₽</p>
            <p>2. Анна Смирнова — 1,250,000 ₽</p>
            <p>3. Алексей Иванов — 80,000 ₽</p>
            <p>4. Мария Соколова — 5,000 ₽</p>
            <p>5. Дмитрий Кузнецов — 3,000 ₽</p>
        """)
        rating_content.setFixedWidth(800)
        layout.addWidget(rating_content)
        
        # Кнопка назад
        back_btn = QPushButton("Назад в меню")
        back_btn.clicked.connect(lambda: self.show_screen(self.main_menu))
        layout.addWidget(back_btn)
        
        return widget
    
    def create_game_screen(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Левая панель (подсказки и таймер)
        left_panel = QFrame()
        left_panel.setObjectName("panel")
        left_panel.setFixedWidth(250)
        left_layout = QVBoxLayout(left_panel)
        
        self.call_friend_btn = QPushButton("📞 Звонок другу")
        self.call_friend_btn.setObjectName("hint_btn")
        self.call_friend_btn.clicked.connect(self.call_friend)
        left_layout.addWidget(self.call_friend_btn)
        
        self.fifty_fifty_btn = QPushButton("50/50")
        self.fifty_fifty_btn.setObjectName("hint_btn")
        self.fifty_fifty_btn.clicked.connect(self.fifty_fifty)
        left_layout.addWidget(self.fifty_fifty_btn)
        
        self.timer_label = QLabel("30")
        self.timer_label.setObjectName("timer")
        self.timer_label.setFixedSize(60, 60)
        left_layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
        
        left_layout.addStretch()
        layout.addWidget(left_panel)
        
        # Центральная панель (вопрос и варианты)
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setAlignment(Qt.AlignCenter)
        
        self.question_image = QLabel("🐋")
        self.question_image.setObjectName("illustration")
        center_layout.addWidget(self.question_image)
        
        self.question_text = QLabel("Текст вопроса")
        self.question_text.setObjectName("question")
        self.question_text.setWordWrap(True)
        self.question_text.setFixedWidth(800)
        center_layout.addWidget(self.question_text)
        
        # Контейнер для вариантов ответов с сеткой 2x2
        self.options_container = QWidget()
        self.options_layout = QGridLayout(self.options_container)
        self.options_layout.setSpacing(15)
        self.options_layout.setContentsMargins(20, 20, 20, 20)
        center_layout.addWidget(self.options_container)
        
        layout.addWidget(center_panel)
        
        # Правая панель (призы)
        right_panel = QFrame()
        right_panel.setObjectName("panel")
        right_panel.setFixedWidth(250)
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel("<h3>Вопросы:</h3>"))
        
