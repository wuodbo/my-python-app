import tkinter as tk
from tkinter import messagebox, ttk
import pymysql
import random
from datetime import datetime, timedelta

class UnifiedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie DataBase")
        self.root.geometry("1100x700")
        
        # Настройки подключения к БД
        self.DB_CONFIG = {
            'host': 'pma.protokovich.net',
            'user': 'root',
            'password': '123',
            'database': 'films',
            'charset': 'utf8mb4'
        }
        
        # Глобальные переменные
        self.current_frame = None
        self.current_mode = "database" 
        
        # Данные пользователя для Dashboard
        self.user_data = {
            'name': 'Ксюша',
            'username': '@wuodbo',
            'new_users_today': [85, 43],
            'search_history': [
                "как настроить профиль",
                "новые фильмы 2024",
                "топ сериалы комедии",
                "настройки приватности"
            ],
            'chat_messages': [
                {'user': 'Panda123', 'message': 'Какие фильмы сегодня вы смотрели?'},
                {'user': 'wuodbo', 'message': 'Как настроить профиль?'}
            ]
        }
        
        # Создание главного меню переключения
        self.create_mode_switcher()
        
        # Инициализация базы данных
        self.init_database()
        
        self.show_database_mode()

    def create_mode_switcher(self):
        switcher_frame = tk.Frame(self.root, bg="#ACACAC", height=50)
        switcher_frame.pack(fill=tk.X, side=tk.TOP)
        switcher_frame.pack_propagate(False)
        
        # Кнопки переключения
        dashboard_btn = tk.Button(switcher_frame, text="📊 Перейти в Dashboard", 
                                 font=('Arial', 12), bg="#7E7D7D", fg="#000000",
                                 bd=1, relief="solid", padx=20, pady=8, 
                                 command=self.show_dashboard_mode)
        dashboard_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        database_btn = tk.Button(switcher_frame, text="🗄️ Перейти в Меню БД", 
                                font=('Arial', 12), bg="#7E7D7D", fg="#000000",
                                bd=1, relief="solid", padx=20, pady=8, 
                                command=self.show_database_mode)
        database_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Индикатор текущего режима
        self.mode_label = tk.Label(switcher_frame, text="Текущий режим: Меню БД", 
                                  font=('Arial', 11, 'bold'), bg="#ACACAC", fg="#000000")
        self.mode_label.pack(side=tk.RIGHT, padx=20, pady=10)

    def show_dashboard_mode(self):
        self.current_mode = "dashboard"
        self.mode_label.config(text="Текущий режим: Dashboard")
        self.clear_current_interface()
        self.create_dashboard_interface()

    def show_database_mode(self):
        self.current_mode = "database"
        self.mode_label.config(text="Текущий режим: Меню БД")
        self.clear_current_interface()
        self.create_database_interface()

    def clear_current_interface(self):
        if hasattr(self, 'main_container') and self.main_container:
            self.main_container.destroy()

    def create_dashboard_interface(self):
        self.main_container = tk.Frame(self.root, bg='#f8f9fa')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_dashboard_navigation_panel(self.main_container)
        self.create_dashboard_content_panel(self.main_container)

    def create_dashboard_navigation_panel(self, parent):
        nav_frame = tk.Frame(parent, bg='#495057', width=250)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        nav_frame.pack_propagate(False)
        
        # Информация о пользователе
        user_info_frame = tk.Frame(nav_frame, bg='#495057')
        user_info_frame.pack(fill=tk.X, pady=20, padx=15)
        
        tk.Label(user_info_frame, text="Вы вошли под:",  bg='#495057', fg='#e9ecef', font=('Arial', 10)).pack(anchor='w')
        tk.Label(user_info_frame, text=self.user_data['name'], bg='#495057', fg='#ffffff', font=('Arial', 12, 'bold')).pack(anchor='w')
        tk.Label(user_info_frame, text=self.user_data['username'], bg='#495057', fg='#adb5bd', font=('Arial', 10)).pack(anchor='w')
        
        # Разделитель
        tk.Frame(nav_frame, height=1, bg='#6c757d').pack(fill=tk.X, padx=10, pady=10)
        
        # Пункты меню
        menu_items = [
            "Личный профиль",
            "Друзья", 
            "Карта просмотров",
            "История просмотров",
            "Расширенный поиск"
        ]
        
        for item in menu_items:
            menu_btn = tk.Button(nav_frame, text=item, font=('Arial', 11), bg='#495057', fg='#e9ecef', bd=0, anchor='w', padx=15, pady=12,
                                command=lambda i=item: self.dashboard_menu_click(i))
            menu_btn.pack(fill=tk.X)
            menu_btn.bind("<Enter>", lambda e: e.widget.configure(bg='#6c757d'))
            menu_btn.bind("<Leave>", lambda e: e.widget.configure(bg='#495057'))
        
        tk.Frame(nav_frame, height=1, bg='#6c757d').pack(fill=tk.X, padx=10, pady=10)
        
        # Кнопка выхода
        exit_btn = tk.Button(nav_frame, text="Выйти из аккаунта →", font=('Arial', 11, 'bold'),
                            bg='#495057', fg='white', bd=0, padx=15, pady=12, command=self.dashboard_logout)
        exit_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        exit_btn.bind("<Enter>", lambda e: e.widget.configure(bg='#5a6268'))
        exit_btn.bind("<Leave>", lambda e: e.widget.configure(bg='#6c757d'))

    def create_dashboard_content_panel(self, parent):
        content_frame = tk.Frame(parent, bg='#f8f9fa')
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
        first_row = tk.Frame(content_frame, bg='#f8f9fa')
        first_row.pack(fill=tk.X, pady=(0, 20))
        
        # Новые пользователи
        self.create_dashboard_new_users_widget(first_row)
        
        # Поисковая строка
        self.create_dashboard_search_widget(first_row)
        
        second_row = tk.Frame(content_frame, bg='#f8f9fa')
        second_row.pack(fill=tk.BOTH, expand=True)
        
        # Суточная активность
        self.create_dashboard_activity_widget(second_row)
        
        # Чат
        self.create_dashboard_chat_widget(second_row)

    def create_dashboard_new_users_widget(self, parent):
        users_frame = tk.LabelFrame(parent, text="Новых пользователей за сегодня:  Ваши минуты просмотра за сутки:", 
                                   font=('Arial', 11, 'bold'), bg='#ffffff', bd=1, relief='solid', padx=15, pady=15)
        users_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        users_frame.grid_propagate(False)
        users_frame.columnconfigure(0, weight=1)
        
        numbers_frame = tk.Frame(users_frame, bg='#ffffff')
        numbers_frame.pack(expand=True)
        
        for i, number in enumerate(self.user_data['new_users_today']):
            number_frame = tk.Frame(numbers_frame, bg='#ffffff')
            number_frame.grid(row=0, column=i, padx=30)
            
            tk.Label(number_frame, text=str(number), font=('Arial', 32, 'bold'), bg='#ffffff', fg='#495057').pack()
            
            label_text = "Пользователи" if i == 0 else "Минуты"
            tk.Label(number_frame, text=label_text, font=('Arial', 10), bg='#ffffff', fg='#6c757d').pack()

    def create_dashboard_search_widget(self, parent):
        search_frame = tk.LabelFrame(parent, text="Поиск", font=('Arial', 11, 'bold'), 
                                    bg='#ffffff', bd=1, relief='solid', padx=15, pady=15)
        search_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        search_frame.columnconfigure(0, weight=1)
        
        # Поисковая строка
        search_container = tk.Frame(search_frame, bg='#ffffff')
        search_container.pack(fill=tk.BOTH, expand=True)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_container, textvariable=self.search_var, font=('Arial', 10), 
                               bd=1, relief='solid', bg='#f8f9fa', fg='#495057')
        search_entry.pack(fill=tk.X, pady=10, padx=10)
        search_entry.insert(0, "Напишите что-нибудь...")
        search_entry.bind('<FocusIn>', lambda e: self.clear_search_placeholder(search_entry))
        search_entry.bind('<FocusOut>', lambda e: self.restore_search_placeholder(search_entry))
        search_entry.bind('<Return>', self.perform_search)
        
        # Кнопка поиска
        search_btn = tk.Button(search_container, text="Найти", font=('Arial', 11), 
                              bg='#6c757d', fg='white', bd=0, pady=8, command=lambda: self.perform_search())
        search_btn.pack(fill=tk.X, padx=10)

    def clear_search_placeholder(self, entry):
        if entry.get() == "Напишите что-нибудь...":
            entry.delete(0, tk.END)
            entry.configure(fg='#495057')

    def restore_search_placeholder(self, entry):
        if not entry.get().strip():
            entry.insert(0, "Напишите что-нибудь...")
            entry.configure(fg='#6c757d')

    def perform_search(self, event=None):
        query = self.search_var.get().strip()
        if query and query != "Напишите что-нибудь...":
            messagebox.showinfo("Поиск", f"Выполняется поиск: '{query}'")
        else:
            messagebox.showwarning("Поиск", "Введите поисковый запрос")

    def create_dashboard_activity_widget(self, parent):
        activity_frame = tk.LabelFrame(parent, text="Суточная активность", font=('Arial', 11, 'bold'), 
                                      bg='#ffffff', bd=1, relief='solid', padx=15, pady=15)
        activity_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        activity_frame.columnconfigure(0, weight=1)
        
        # График активности
        chart_frame = tk.Frame(activity_frame, bg='#ffffff', height=200)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        canvas = tk.Canvas(chart_frame, bg='#ffffff', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        hours = list(range(24))
        activities = [random.randint(10, 100) for _ in hours]
        
        chart_width = 400
        chart_height = 150
        bar_width = chart_width / len(hours) - 2
        
        for i, activity in enumerate(activities):
            x1 = i * (chart_width / len(hours)) + 1
            x2 = x1 + bar_width
            y1 = chart_height - (activity * chart_height / 100)
            y2 = chart_height
            
            canvas.create_rectangle(x1, y1, x2, y2, fill='#6c757d', outline='')
            
            # Подписи часов
            if i % 3 == 0:
                canvas.create_text(x1 + bar_width/2, chart_height + 10, text=f"{i:02d}:00", font=('Arial', 7), fill='#495057')
        
        period_frame = tk.Frame(activity_frame, bg='#ffffff')
        period_frame.pack(fill=tk.X)
        period_frame.columnconfigure(0, weight=1)
        
        period_inner_frame = tk.Frame(period_frame, bg='#ffffff')
        period_inner_frame.pack(anchor='center')
        
        tk.Label(period_inner_frame, text="Показать данные за:", font=('Arial', 10), bg='#ffffff', fg='#495057').pack(side=tk.LEFT)
        
        # Выпадающий список
        self.period_var = tk.StringVar(value="Сегодня")
        from tkinter import ttk
        period_dropdown = ttk.Combobox(period_inner_frame, textvariable=self.period_var,
                                      values=["Сегодня", "Вчера", "Неделя", "Месяц"], state="readonly", width=12)
        period_dropdown.pack(side=tk.LEFT, padx=(10, 0))
        
        # Кнопка "Применить"
        apply_btn = tk.Button(period_inner_frame, text="Применить", font=('Arial', 9), 
                             bg='#6c757d', fg='white', bd=0, padx=10, command=self.apply_period)
        apply_btn.pack(side=tk.LEFT, padx=(10, 0))

    def apply_period(self):
        selected_period = self.period_var.get()
        messagebox.showinfo("Период", f"Применен период: {selected_period}")

    def create_dashboard_chat_widget(self, parent):
        chat_frame = tk.LabelFrame(parent, text="Чат пользователей", font=('Arial', 11, 'bold'), 
                                  bg='#ffffff', bd=1, relief='solid')
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        chat_frame.columnconfigure(0, weight=1)
        
        # Сообщения чата
        chat_messages_frame = tk.Frame(chat_frame, bg='#ffffff')
        chat_messages_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        messages_container = tk.Frame(chat_messages_frame, bg='#ffffff')
        messages_container.pack(expand=True, fill=tk.BOTH)
        messages_container.columnconfigure(0, weight=1)

        for i, msg in enumerate(self.user_data['chat_messages']):
            message_frame = tk.Frame(messages_container, bg='#ffffff')
            message_frame.grid(row=i, column=0, sticky='ew', pady=5)
            message_frame.columnconfigure(0, weight=1)
            
            username_color = '#495057' if msg['user'] == 'wuodbo' else '#6c757d'
            
            msg_inner_frame = tk.Frame(message_frame, bg='#ffffff')
            msg_inner_frame.pack(anchor='w')
            
            tk.Label(msg_inner_frame, text=f"{msg['user']}:", font=('Arial', 9, 'bold'), 
                    bg='#ffffff', fg=username_color).pack(side=tk.LEFT)
            
            tk.Label(msg_inner_frame, text=msg['message'], font=('Arial', 9), 
                    bg='#ffffff', fg='#495057').pack(side=tk.LEFT, padx=(5, 0))
        
        # Поле ввода сообщения
        input_frame = tk.Frame(chat_frame, bg='#e9ecef')
        input_frame.pack(fill=tk.X, padx=15, pady=15)
        
        entry = tk.Entry(input_frame, font=('Arial', 10), bd=0, bg='#ffffff', relief='solid', fg='#495057')
        entry.insert(0, "Напишите что-нибудь...")
        entry.pack(fill=tk.X, padx=10, pady=10)
        entry.bind('<FocusIn>', lambda e: entry.delete(0, tk.END) if entry.get() == "Напишите что-нибудь..." else None)
        entry.bind('<Return>', lambda e: self.send_message(entry))

    def dashboard_menu_click(self, item):
        messagebox.showinfo("Навигация", f"Переход к: {item}")

    def dashboard_logout(self):
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            messagebox.showinfo("Выход", "Перенаправление на страницу выхода...")

    def send_message(self, entry):
        message = entry.get().strip()
        if message and message != "Напишите что-нибудь...":
            messagebox.showinfo("Чат", f"Сообщение отправлено: {message}")
            entry.delete(0, tk.END)

    def create_database_interface(self):
        self.main_container = tk.Frame(self.root, bg="#7E7D7D")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Создание главного меню БД
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # Текстовые переменные для БД интерфейса
        self.title_text = tk.StringVar()
        self.info_text = tk.StringVar()
        self.title_text.set("🏠 Главное меню Базы Данных")
        self.info_text.set("""Для работы с меню используйте выпадающие списки выше

👥 Управление данными - работа с записями базы данных
🔍 Поиск и фильтрация - поиск и фильтрация информации  
📈 Отчеты и аналитика - создание отчетов и графиков
🤖 Администрирование - настройки системы
🆘 Справка - документация и поддержка""")
        
        # Основной фрейм (главный экран)
        self.db_main_frame = tk.Frame(self.main_container, padx=20, pady=20, bg="#7E7D7D")
        self.db_main_frame.pack(fill=tk.BOTH, expand=True)
                
        # Заголовок
        title_label = tk.Label(self.db_main_frame, textvariable=self.title_text, 
                              font=("Arial", 16, "bold"), bg="#ACACAC", fg="#000000", 
                              padx=15, pady=15)
        title_label.pack(pady=10)
                        
        # Информационный текст
        info_label = tk.Label(self.db_main_frame, textvariable=self.info_text, justify=tk.LEFT, 
                             font=("Arial", 12), bg="#7E7D7D", fg="#000000", padx=15, pady=15)
        info_label.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Создание меню БД
        self.create_database_menus()

    def create_database_menus(self):
        # Меню "Главная"  
        main_menu = tk.Menu(self.menubar, tearoff=0, bg="#ACACAC", fg="#000000")
        main_menu.add_command(label="Обновить", command=self.refresh, activebackground="#7E7D7D")
        main_menu.add_separator()
        main_menu.add_command(label="Сброс", command=self.reset_to_default, activebackground="#7E7D7D")
        main_menu.add_separator()
        main_menu.add_command(label="Выход", command=self.root.quit, activebackground="#7E7D7D")
        self.menubar.add_cascade(label="🏠 Главная", menu=main_menu)

        # Меню "Управление данными"  
        data_menu = tk.Menu(self.menubar, tearoff=0, bg="#7E7D7D", fg="#000000")
        data_menu.add_command(label="Фильмы", command=self.show_films_list, activebackground="#ACACAC")
        data_menu.add_separator()
        data_menu.add_command(label="Сцены", command=self.show_scenes_list, activebackground="#ACACAC")
        data_menu.add_separator()
        data_menu.add_command(label="Решения", command=self.show_solutions_list, activebackground="#ACACAC")
        data_menu.add_separator()
        data_menu.add_command(label="Зрители", command=self.show_viewers_list, activebackground="#ACACAC")
        data_menu.add_separator()
        data_menu.add_command(label="Карты просмотров", command=self.show_views_maps_list, activebackground="#ACACAC")
        data_menu.add_separator()
        data_menu.add_command(label="Сюжеты", command=self.show_stories_list, activebackground="#ACACAC")
        data_menu.add_separator()
        data_menu.add_command(label="Сценарии", command=self.show_scenarios_list, activebackground="#ACACAC")
        self.menubar.add_cascade(label="👥 Управление данными", menu=data_menu)

        # Меню "Поиск и фильтрация"  
        search_menu = tk.Menu(self.menubar, tearoff=0, bg="#ACACAC", fg="#000000")
        search_menu.add_command(label="Быстрый поиск", command=self.quick_search, activebackground="#7E7D7D")
        search_menu.add_separator()
        search_menu.add_command(label="Расширенный поиск", command=self.advanced_search, activebackground="#7E7D7D")
        search_menu.add_separator()
        search_menu.add_command(label="Фильтры по категориям", command=self.category_filters, activebackground="#7E7D7D")
        self.menubar.add_cascade(label="🔍 Поиск и фильтрация", menu=search_menu)

        # Меню "Отчеты и аналитика"  
        reports_menu = tk.Menu(self.menubar, tearoff=0, bg="#7E7D7D", fg="#000000")
        reports_menu.add_command(label="Статистические отчеты", command=self.stat_reports, activebackground="#ACACAC")
        reports_menu.add_separator()
        reports_menu.add_command(label="Графики и диаграммы", command=self.charts, activebackground="#ACACAC")
        reports_menu.add_separator()
        reports_menu.add_command(label="Экспорт отчетов", command=self.export_reports, activebackground="#ACACAC")
        self.menubar.add_cascade(label="📈 Отчеты и аналитика", menu=reports_menu)

        # Меню "Администрирование"  
        admin_menu = tk.Menu(self.menubar, tearoff=0, bg="#ACACAC", fg="#000000")
        admin_menu.add_command(label="Управление пользователями", command=self.user_management, activebackground="#7E7D7D")
        admin_menu.add_separator()
        admin_menu.add_command(label="Права доступа", command=self.access_rights, activebackground="#7E7D7D")
        admin_menu.add_separator()
        admin_menu.add_command(label="Резервное копирование", command=self.backup, activebackground="#7E7D7D")
        admin_menu.add_separator()
        admin_menu.add_command(label="Журнал операций", command=self.operation_log, activebackground="#7E7D7D")
        self.menubar.add_cascade(label="🤖 Администрирование", menu=admin_menu)

        # Меню "Справка и поддержка"  
        help_menu = tk.Menu(self.menubar, tearoff=0, bg="#7E7D7D", fg="#000000")
        help_menu.add_command(label="Руководство пользователя", command=self.user_manual, activebackground="#ACACAC")
        help_menu.add_separator()
        help_menu.add_command(label="О программе", command=self.about, activebackground="#ACACAC")
        help_menu.add_separator()
        help_menu.add_command(label="Проверка обновлений", command=self.check_updates, activebackground="#ACACAC")
        self.menubar.add_cascade(label="🆘 Справка и поддержка", menu=help_menu)

    # Функции для работы с БД
    def create_connection(self):
        try:
            connection = pymysql.connect(**self.DB_CONFIG)
            return connection
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Не удалось подключиться к базе данных:\n{e}")
            return None

    def init_database(self):
        try:
            connection = self.create_connection()
            if connection:
                cursor = connection.cursor()
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS movie (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        description VARCHAR(1000) NOT NULL,
                        director VARCHAR(100) NOT NULL,
                        year_of_creation INT(4) NOT NULL,
                        status ENUM('Опубликован','Архив','Черновик','Премьера') NOT NULL
                    )
                """)
                
                connection.commit()
                cursor.close()
                connection.close()
                print("База данных проверена успешно")
        except pymysql.Error as e:
            messagebox.showerror("Ошибка инициализации БД", f"Ошибка при проверке базы данных:\n{e}")

    # Функции для работы с таблицей movie
    def get_all_films(self):
        connection = self.create_connection()
        if not connection:
            return []
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM movie ORDER BY id DESC")
                films = cursor.fetchall()
                
                result = []
                for film in films:
                    result.append({
                        'id': film[0],
                        'name': film[1],
                        'description': film[2],
                        'director': film[3],
                        'year_of_creation': film[4],
                        'status': film[5]
                    })
                return result
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при получении данных:\n{e}")
            return []
        finally:
            connection.close()

    def add_film_to_db(self, name, description, director, year_of_creation, status):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO movie (name, description, director, year_of_creation, status) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, description, director, year_of_creation, status))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при добавлении фильма:\n{e}")
            return False
        finally:
            connection.close()

    def update_film_in_db(self, film_id, name, description, director, year_of_creation, status):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE movie SET name=%s, description=%s, director=%s, year_of_creation=%s, status=%s WHERE id=%s"
                cursor.execute(sql, (name, description, director, year_of_creation, status, film_id))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при обновлении фильма:\n{e}")
            return False
        finally:
            connection.close()

    def delete_film_from_db(self, film_id):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM movie WHERE id = %s", (film_id,))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при удалении фильма:\n{e}")
            return False
        finally:
            connection.close()

    # Функции для работы с таблицей scene
    def get_all_scenes(self):
        connection = self.create_connection()
        if not connection:
            return []
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM scene ORDER BY id DESC")
                scenes = cursor.fetchall()
                
                result = []
                for scene in scenes:
                    result.append({
                        'id': scene[0],
                        'name': scene[1],
                        'type': scene[2],
                        'time_of_scene': scene[3],
                        'change_scene': scene[4]
                    })
                return result
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при получении сцен:\n{e}")
            return []
        finally:
            connection.close()

    def add_scene_to_db(self, name, scene_type, time_of_scene, change_scene):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO scene (name, type, time_of_scene, change_scene) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, scene_type, time_of_scene, change_scene))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при добавлении сцены:\n{e}")
            return False
        finally:
            connection.close()

    def update_scene_in_db(self, scene_id, name, scene_type, time_of_scene, change_scene):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE scene SET name=%s, type=%s, time_of_scene=%s, change_scene=%s WHERE id=%s"
                cursor.execute(sql, (name, scene_type, time_of_scene, change_scene, scene_id))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при обновлении сцены:\n{e}")
            return False
        finally:
            connection.close()

    def delete_scene_from_db(self, scene_id):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM scene WHERE id = %s", (scene_id,))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при удалении сцены:\n{e}")
            return False
        finally:
            connection.close()

    # Функции для работы с таблицей solutions
    def get_all_solutions(self):
        connection = self.create_connection()
        if not connection:
            return []
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM solutions ORDER BY id DESC")
                solutions = cursor.fetchall()
                
                result = []
                for solution in solutions:
                    result.append({
                        'id': solution[0],
                        'point_of_time': solution[1],
                        'action': solution[2]
                    })
                return result
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при получении решений:\n{e}")
            return []
        finally:
            connection.close()

    def add_solution_to_db(self, point_of_time, action):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO solutions (point_of_time, action) VALUES (%s, %s)"
                cursor.execute(sql, (point_of_time, action))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при добавлении решения:\n{e}")
            return False
        finally:
            connection.close()

    def update_solution_in_db(self, solution_id, point_of_time, action):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE solutions SET point_of_time=%s, action=%s WHERE id=%s"
                cursor.execute(sql, (point_of_time, action, solution_id))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при обновлении решения:\n{e}")
            return False
        finally:
            connection.close()

    def delete_solution_from_db(self, solution_id):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM solutions WHERE id = %s", (solution_id,))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при удалении решения:\n{e}")
            return False
        finally:
            connection.close()

    # Функции для работы с таблицей viewer
    def get_all_viewers(self):
        connection = self.create_connection()
        if not connection:
            return []
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM viewer ORDER BY id DESC")
                viewers = cursor.fetchall()
                
                result = []
                for viewer in viewers:
                    result.append({
                        'id': viewer[0],
                        'email': viewer[1],
                        'nick': viewer[2]
                    })
                return result
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при получении зрителей:\n{e}")
            return []
        finally:
            connection.close()

    def add_viewer_to_db(self, email, nick):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO viewer (email, nick) VALUES (%s, %s)"
                cursor.execute(sql, (email, nick))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при добавлении зрителя:\n{e}")
            return False
        finally:
            connection.close()

    def update_viewer_in_db(self, viewer_id, email, nick):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE viewer SET email=%s, nick=%s WHERE id=%s"
                cursor.execute(sql, (email, nick, viewer_id))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при обновлении зрителя:\n{e}")
            return False
        finally:
            connection.close()

    def delete_viewer_from_db(self, viewer_id):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM viewer WHERE id = %s", (viewer_id,))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при удалении зрителя:\n{e}")
            return False
        finally:
            connection.close()

    # Функции для работы с таблицей views_map (исправлено название)
    def get_all_views_maps(self):
        connection = self.create_connection()
        if not connection:
            return []
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM views_map ORDER BY id DESC")
                views_maps = cursor.fetchall()
                
                result = []
                for views_map in views_maps:
                    result.append({
                        'id': views_map[0],
                        'latest_update': views_map[1],
                        'number_of_perfect_solutions': views_map[2],
                        'number_of_films_watched': views_map[3]
                    })
                return result
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при получении карт просмотров:\n{e}")
            return []
        finally:
            connection.close()

    def add_views_map_to_db(self, latest_update, number_of_perfect_solutions, number_of_films_watched):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO views_map (latest_update, number_of_perfect_solutions, number_of_films_watched) VALUES (%s, %s, %s)"
                cursor.execute(sql, (latest_update, number_of_perfect_solutions, number_of_films_watched))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при добавлении карты просмотра:\n{e}")
            return False
        finally:
            connection.close()

    def update_views_map_in_db(self, views_map_id, latest_update, number_of_perfect_solutions, number_of_films_watched):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE views_map SET latest_update=%s, number_of_perfect_solutions=%s, number_of_films_watched=%s WHERE id=%s"
                cursor.execute(sql, (latest_update, number_of_perfect_solutions, number_of_films_watched, views_map_id))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при обновлении карты просмотра:\n{e}")
            return False
        finally:
            connection.close()

    def delete_views_map_from_db(self, views_map_id):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM views_map WHERE id = %s", (views_map_id,))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при удалении карты просмотра:\n{e}")
            return False
        finally:
            connection.close()

    # Функции для работы с таблицей story
    def get_all_stories(self):
        connection = self.create_connection()
        if not connection:
            return []
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM story ORDER BY id DESC")
                stories = cursor.fetchall()
                
                result = []
                for story in stories:
                    result.append({
                        'id': story[0],
                        'genre': story[1],
                        'type': story[2]
                    })
                return result
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при получении сюжетов:\n{e}")
            return []
        finally:
            connection.close()

    def add_story_to_db(self, genre, story_type):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO story (genre, type) VALUES (%s, %s)"
                cursor.execute(sql, (genre, story_type))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при добавлении сюжета:\n{e}")
            return False
        finally:
            connection.close()

    def update_story_in_db(self, story_id, genre, story_type):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE story SET genre=%s, type=%s WHERE id=%s"
                cursor.execute(sql, (genre, story_type, story_id))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при обновлении сюжета:\n{e}")
            return False
        finally:
            connection.close()

    def delete_story_from_db(self, story_id):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM story WHERE id = %s", (story_id,))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при удалении сюжета:\n{e}")
            return False
        finally:
            connection.close()

    # Функции для работы с таблицей scenario
    def get_all_scenarios(self):
        connection = self.create_connection()
        if not connection:
            return []
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM scenario ORDER BY id DESC")
                scenarios = cursor.fetchall()
                
                result = []
                for scenario in scenarios:
                    result.append({
                        'id': scenario[0],
                        'author': scenario[1],
                        'last_update': scenario[2]
                    })
                return result
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при получении сценариев:\n{e}")
            return []
        finally:
            connection.close()

    def add_scenario_to_db(self, author, last_update):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO scenario (author, last_update) VALUES (%s, %s)"
                cursor.execute(sql, (author, last_update))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при добавлении сценария:\n{e}")
            return False
        finally:
            connection.close()

    def update_scenario_in_db(self, scenario_id, author, last_update):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE scenario SET author=%s, last_update=%s WHERE id=%s"
                cursor.execute(sql, (author, last_update, scenario_id))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при обновлении сценария:\n{e}")
            return False
        finally:
            connection.close()

    def delete_scenario_from_db(self, scenario_id):
        connection = self.create_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM scenario WHERE id = %s", (scenario_id,))
                connection.commit()
                return True
        except pymysql.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при удалении сценария:\n{e}")
            return False
        finally:
            connection.close()

    # Функции отображения списков
    def show_films_list(self):
        self.clear_current_frame()
        self.title_text.set("🎬 Управление фильмами")
        self.info_text.set("")
        
        films = self.get_all_films()
        
        # Создание фрейма для списка фильмов
        list_frame = tk.Frame(self.db_main_frame, bg="#7E7D7D")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Кнопка добавления
        add_btn = tk.Button(list_frame, text="➕ Добавить фильм", font=("Arial", 12, "bold"),
                           bg="#ACACAC", fg="#000000", padx=20, pady=10,
                           command=self.show_add_film_form)
        add_btn.pack(pady=10)
        
        # Таблица фильмов
        columns = ("ID", "Название", "Описание", "Режиссер", "Год", "Статус")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.column("Название", width=150)
        tree.column("Описание", width=200)
        
        # Заполнение данными
        for film in films:
            tree.insert("", "end", values=(
                film['id'],
                film['name'],
                film['description'][:50] + "..." if len(film['description']) > 50 else film['description'],
                film['director'],
                film['year_of_creation'],
                film['status']
            ))
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки действий
        actions_frame = tk.Frame(list_frame, bg="#7E7D7D")
        actions_frame.pack(pady=10)
        
        edit_btn = tk.Button(actions_frame, text="✏️ Редактировать", font=("Arial", 10),
                            bg="#ACACAC", fg="#000000", padx=15, pady=5,
                            command=lambda: self.edit_film(tree))
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(actions_frame, text="🗑️ Удалить", font=("Arial", 10),
                             bg="#ACACAC", fg="#000000", padx=15, pady=5,
                             command=lambda: self.delete_film(tree))
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(actions_frame, text="🔄 Обновить", font=("Arial", 10),
                              bg="#ACACAC", fg="#000000", padx=15, pady=5,
                              command=self.show_films_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)

    def show_scenes_list(self):
        self.clear_current_frame()
        self.title_text.set("🎭 Управление сценами")
        self.info_text.set("")
        
        scenes = self.get_all_scenes()
        
        list_frame = tk.Frame(self.db_main_frame, bg="#7E7D7D")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        add_btn = tk.Button(list_frame, text="➕ Добавить сцену", font=("Arial", 12, "bold"),
                           bg="#ACACAC", fg="#000000", padx=20, pady=10,
                           command=self.show_add_scene_form)
        add_btn.pack(pady=10)
        
        columns = ("ID", "Название", "Тип", "Время сцены", "Смена сцены")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for scene in scenes:
            tree.insert("", "end", values=(
                scene['id'],
                scene['name'],
                scene['type'],
                scene['time_of_scene'],
                scene['change_scene']
            ))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        actions_frame = tk.Frame(list_frame, bg="#7E7D7D")
        actions_frame.pack(pady=10)
        
        edit_btn = tk.Button(actions_frame, text="✏️ Редактировать", font=("Arial", 10),
                            bg="#ACACAC", fg="#000000", padx=15, pady=5,
                            command=lambda: self.edit_scene(tree))
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(actions_frame, text="🗑️ Удалить", font=("Arial", 10),
                             bg="#ACACAC", fg="#000000", padx=15, pady=5,
                             command=lambda: self.delete_scene(tree))
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(actions_frame, text="🔄 Обновить", font=("Arial", 10),
                              bg="#ACACAC", fg="#000000", padx=15, pady=5,
                              command=self.show_scenes_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)

    def show_solutions_list(self):
        self.clear_current_frame()
        self.title_text.set("🎯 Управление решениями")
        self.info_text.set("")
        
        solutions = self.get_all_solutions()
        
        list_frame = tk.Frame(self.db_main_frame, bg="#7E7D7D")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        add_btn = tk.Button(list_frame, text="➕ Добавить решение", font=("Arial", 12, "bold"),
                           bg="#ACACAC", fg="#000000", padx=20, pady=10,
                           command=self.show_add_solution_form)
        add_btn.pack(pady=10)
        
        columns = ("ID", "Точка времени", "Действие")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        for solution in solutions:
            tree.insert("", "end", values=(
                solution['id'],
                solution['point_of_time'],
                solution['action']
            ))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        actions_frame = tk.Frame(list_frame, bg="#7E7D7D")
        actions_frame.pack(pady=10)
        
        edit_btn = tk.Button(actions_frame, text="✏️ Редактировать", font=("Arial", 10),
                            bg="#ACACAC", fg="#000000", padx=15, pady=5,
                            command=lambda: self.edit_solution(tree))
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(actions_frame, text="🗑️ Удалить", font=("Arial", 10),
                             bg="#ACACAC", fg="#000000", padx=15, pady=5,
                             command=lambda: self.delete_solution(tree))
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(actions_frame, text="🔄 Обновить", font=("Arial", 10),
                              bg="#ACACAC", fg="#000000", padx=15, pady=5,
                              command=self.show_solutions_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)

    def show_viewers_list(self):
        self.clear_current_frame()
        self.title_text.set("👥 Управление зрителями")
        self.info_text.set("")
        
        viewers = self.get_all_viewers()
        
        list_frame = tk.Frame(self.db_main_frame, bg="#7E7D7D")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        add_btn = tk.Button(list_frame, text="➕ Добавить зрителя", font=("Arial", 12, "bold"),
                           bg="#ACACAC", fg="#000000", padx=20, pady=10,
                           command=self.show_add_viewer_form)
        add_btn.pack(pady=10)
        
        columns = ("ID", "Email", "Ник")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        for viewer in viewers:
            tree.insert("", "end", values=(
                viewer['id'],
                viewer['email'],
                viewer['nick']
            ))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        actions_frame = tk.Frame(list_frame, bg="#7E7D7D")
        actions_frame.pack(pady=10)
        
        edit_btn = tk.Button(actions_frame, text="✏️ Редактировать", font=("Arial", 10),
                            bg="#ACACAC", fg="#000000", padx=15, pady=5,
                            command=lambda: self.edit_viewer(tree))
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(actions_frame, text="🗑️ Удалить", font=("Arial", 10),
                             bg="#ACACAC", fg="#000000", padx=15, pady=5,
                             command=lambda: self.delete_viewer(tree))
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(actions_frame, text="🔄 Обновить", font=("Arial", 10),
                              bg="#ACACAC", fg="#000000", padx=15, pady=5,
                              command=self.show_viewers_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)

    def show_views_maps_list(self):
        self.clear_current_frame()
        self.title_text.set("🗺️ Управление картами просмотров")
        self.info_text.set("")
        
        views_maps = self.get_all_views_maps()
        
        list_frame = tk.Frame(self.db_main_frame, bg="#7E7D7D")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        add_btn = tk.Button(list_frame, text="➕ Добавить карту просмотра", font=("Arial", 12, "bold"),
                           bg="#ACACAC", fg="#000000", padx=20, pady=10,
                           command=self.show_add_views_map_form)
        add_btn.pack(pady=10)
        
        columns = ("ID", "Последнее обновление", "Принятые решения", "Просмотренные фильмы")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for views_map in views_maps:
            tree.insert("", "end", values=(
                views_map['id'],
                views_map['latest_update'],
                views_map['number_of_perfect_solutions'],
                views_map['number_of_films_watched']
            ))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        actions_frame = tk.Frame(list_frame, bg="#7E7D7D")
        actions_frame.pack(pady=10)
        
        edit_btn = tk.Button(actions_frame, text="✏️ Редактировать", font=("Arial", 10),
                            bg="#ACACAC", fg="#000000", padx=15, pady=5,
                            command=lambda: self.edit_views_map(tree))
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(actions_frame, text="🗑️ Удалить", font=("Arial", 10),
                             bg="#ACACAC", fg="#000000", padx=15, pady=5,
                             command=lambda: self.delete_views_map(tree))
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(actions_frame, text="🔄 Обновить", font=("Arial", 10),
                              bg="#ACACAC", fg="#000000", padx=15, pady=5,
                              command=self.show_views_maps_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)

    def show_stories_list(self):
        self.clear_current_frame()
        self.title_text.set("📖 Управление сюжетами")
        self.info_text.set("")
        
        stories = self.get_all_stories()
        
        list_frame = tk.Frame(self.db_main_frame, bg="#7E7D7D")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        add_btn = tk.Button(list_frame, text="➕ Добавить сюжет", font=("Arial", 12, "bold"),
                           bg="#ACACAC", fg="#000000", padx=20, pady=10,
                           command=self.show_add_story_form)
        add_btn.pack(pady=10)
        
        columns = ("ID", "Жанр", "Тип")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        for story in stories:
            tree.insert("", "end", values=(
                story['id'],
                story['genre'],
                story['type']
            ))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        actions_frame = tk.Frame(list_frame, bg="#7E7D7D")
        actions_frame.pack(pady=10)
        
        edit_btn = tk.Button(actions_frame, text="✏️ Редактировать", font=("Arial", 10),
                            bg="#ACACAC", fg="#000000", padx=15, pady=5,
                            command=lambda: self.edit_story(tree))
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(actions_frame, text="🗑️ Удалить", font=("Arial", 10),
                             bg="#ACACAC", fg="#000000", padx=15, pady=5,
                             command=lambda: self.delete_story(tree))
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(actions_frame, text="🔄 Обновить", font=("Arial", 10),
                              bg="#ACACAC", fg="#000000", padx=15, pady=5,
                              command=self.show_stories_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)

    def show_scenarios_list(self):
        self.clear_current_frame()
        self.title_text.set("🎭 Управление сценариями")
        self.info_text.set("")
        
        scenarios = self.get_all_scenarios()
        
        list_frame = tk.Frame(self.db_main_frame, bg="#7E7D7D")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        add_btn = tk.Button(list_frame, text="➕ Добавить сценарий", font=("Arial", 12, "bold"),
                           bg="#ACACAC", fg="#000000", padx=20, pady=10,
                           command=self.show_add_scenario_form)
        add_btn.pack(pady=10)
        
        columns = ("ID", "Автор", "Последнее обновление")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        for scenario in scenarios:
            tree.insert("", "end", values=(
                scenario['id'],
                scenario['author'],
                scenario['last_update']
            ))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        actions_frame = tk.Frame(list_frame, bg="#7E7D7D")
        actions_frame.pack(pady=10)
        
        edit_btn = tk.Button(actions_frame, text="✏️ Редактировать", font=("Arial", 10),
                            bg="#ACACAC", fg="#000000", padx=15, pady=5,
                            command=lambda: self.edit_scenario(tree))
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(actions_frame, text="🗑️ Удалить", font=("Arial", 10),
                             bg="#ACACAC", fg="#000000", padx=15, pady=5,
                             command=lambda: self.delete_scenario(tree))
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(actions_frame, text="🔄 Обновить", font=("Arial", 10),
                              bg="#ACACAC", fg="#000000", padx=15, pady=5,
                              command=self.show_scenarios_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)

    # Формы добавления
    def show_add_film_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Добавить фильм")
        form_window.geometry("500x400")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Добавить новый фильм", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Название:", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(form_frame, width=40)
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Описание:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        description_text = tk.Text(form_frame, width=40, height=4)
        description_text.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Режиссер:", bg="#7E7D7D", fg="#000000").grid(row=2, column=0, sticky="w", pady=5)
        director_entry = tk.Entry(form_frame, width=40)
        director_entry.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Год создания:", bg="#7E7D7D", fg="#000000").grid(row=3, column=0, sticky="w", pady=5)
        year_entry = tk.Entry(form_frame, width=40)
        year_entry.grid(row=3, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Статус:", bg="#7E7D7D", fg="#000000").grid(row=4, column=0, sticky="w", pady=5)
        status_var = tk.StringVar(value="Опубликован")
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, 
                                   values=["Опубликован", "Архив", "Черновик", "Премьера"], state="readonly")
        status_combo.grid(row=4, column=1, pady=5, padx=5)
        
        def save_film():
            name = name_entry.get().strip()
            description = description_text.get("1.0", tk.END).strip()
            director = director_entry.get().strip()
            year = year_entry.get().strip()
            status = status_var.get()
            
            if not all([name, description, director, year, status]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            try:
                year = int(year)
            except ValueError:
                messagebox.showerror("Ошибка", "Год должен быть числом")
                return
            
            if self.add_film_to_db(name, description, director, year, status):
                messagebox.showinfo("Успех", "Фильм успешно добавлен")
                form_window.destroy()
                self.show_films_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить фильм")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_film).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def show_add_scene_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Добавить сцену")
        form_window.geometry("500x300")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Добавить новую сцену", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Название:", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(form_frame, width=40)
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Тип:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        type_var = tk.StringVar(value="Видеофайл")
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, 
                                 values=["Видеофайл", "Текст", "Изображение"], state="readonly")
        type_combo.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Время сцены (HH:MM:SS):", bg="#7E7D7D", fg="#000000").grid(row=2, column=0, sticky="w", pady=5)
        time_entry = tk.Entry(form_frame, width=40)
        time_entry.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Смена сцены:", bg="#7E7D7D", fg="#000000").grid(row=3, column=0, sticky="w", pady=5)
        change_var = tk.StringVar(value="Нет")
        change_combo = ttk.Combobox(form_frame, textvariable=change_var, 
                                   values=["Да", "Нет"], state="readonly")
        change_combo.grid(row=3, column=1, pady=5, padx=5)
        
        def save_scene():
            name = name_entry.get().strip()
            scene_type = type_var.get()
            time_of_scene = time_entry.get().strip()
            change_scene = change_var.get()
            
            if not all([name, scene_type, time_of_scene, change_scene]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if self.add_scene_to_db(name, scene_type, time_of_scene, change_scene):
                messagebox.showinfo("Успех", "Сцена успешно добавлена")
                form_window.destroy()
                self.show_scenes_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить сцену")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_scene).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def show_add_solution_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Добавить решение")
        form_window.geometry("500x250")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Добавить новое решение", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Точка времени (HH:MM:SS):", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        time_entry = tk.Entry(form_frame, width=40)
        time_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Действие:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        action_var = tk.StringVar(value="Не изменять")
        action_combo = ttk.Combobox(form_frame, textvariable=action_var, 
                                   values=["Словестные", "Психические", "Физческие", "Материальные", "Не изменять"], state="readonly")
        action_combo.grid(row=1, column=1, pady=5, padx=5)
        
        def save_solution():
            point_of_time = time_entry.get().strip()
            action = action_var.get()
            
            if not all([point_of_time, action]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if self.add_solution_to_db(point_of_time, action):
                messagebox.showinfo("Успех", "Решение успешно добавлено")
                form_window.destroy()
                self.show_solutions_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить решение")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_solution).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def show_add_viewer_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Добавить зрителя")
        form_window.geometry("500x200")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Добавить нового зрителя", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Email:", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(form_frame, width=40)
        email_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Ник:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        nick_entry = tk.Entry(form_frame, width=40)
        nick_entry.grid(row=1, column=1, pady=5, padx=5)
        
        def save_viewer():
            email = email_entry.get().strip()
            nick = nick_entry.get().strip()
            
            if not all([email, nick]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if self.add_viewer_to_db(email, nick):
                messagebox.showinfo("Успех", "Зритель успешно добавлен")
                form_window.destroy()
                self.show_viewers_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить зрителя")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_viewer).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def show_add_views_map_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Добавить карту просмотра")
        form_window.geometry("500x300")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Добавить новую карту просмотра", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Последнее обновление (YYYY-MM-DD HH:MM:SS):", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        latest_update_entry = tk.Entry(form_frame, width=40)
        latest_update_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Кол-во принятых решений:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        solutions_entry = tk.Entry(form_frame, width=40)
        solutions_entry.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Кол-во просмотренных фильмов:", bg="#7E7D7D", fg="#000000").grid(row=2, column=0, sticky="w", pady=5)
        films_entry = tk.Entry(form_frame, width=40)
        films_entry.grid(row=2, column=1, pady=5, padx=5)
        
        def save_views_map():
            latest_update = latest_update_entry.get().strip()
            number_of_perfect_solutions = solutions_entry.get().strip()
            number_of_films_watched = films_entry.get().strip()
            
            if not all([latest_update, number_of_perfect_solutions, number_of_films_watched]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            try:
                number_of_perfect_solutions = int(number_of_perfect_solutions)
                number_of_films_watched = int(number_of_films_watched)
            except ValueError:
                messagebox.showerror("Ошибка", "Количества должны быть числами")
                return
            
            if self.add_views_map_to_db(latest_update, number_of_perfect_solutions, number_of_films_watched):
                messagebox.showinfo("Успех", "Карта просмотра успешно добавлена")
                form_window.destroy()
                self.show_views_maps_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить карту просмотра")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_views_map).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def show_add_story_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Добавить сюжет")
        form_window.geometry("500x200")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Добавить новый сюжет", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Жанр:", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        genre_var = tk.StringVar(value="Фантастика")
        genre_combo = ttk.Combobox(form_frame, textvariable=genre_var, 
                                  values=["Фантастика", "Боевик", "Фентези", "Приключения", "Комедия", "Триллер", "Ужасы", "Драма"], state="readonly")
        genre_combo.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Тип:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        type_var = tk.StringVar(value="Линейный")
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, 
                                 values=["Линейный", "Концентрический", "Многолинейный", "Динамический", "Адинамический"], state="readonly")
        type_combo.grid(row=1, column=1, pady=5, padx=5)
        
        def save_story():
            genre = genre_var.get()
            story_type = type_var.get()
            
            if not all([genre, story_type]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if self.add_story_to_db(genre, story_type):
                messagebox.showinfo("Успех", "Сюжет успешно добавлен")
                form_window.destroy()
                self.show_stories_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить сюжет")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_story).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def show_add_scenario_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Добавить сценарий")
        form_window.geometry("500x200")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Добавить новый сценарий", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Автор:", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        author_entry = tk.Entry(form_frame, width=40)
        author_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Последнее обновление (YYYY-MM-DD):", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        last_update_entry = tk.Entry(form_frame, width=40)
        last_update_entry.grid(row=1, column=1, pady=5, padx=5)
        
        def save_scenario():
            author = author_entry.get().strip()
            last_update = last_update_entry.get().strip()
            
            if not all([author, last_update]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if self.add_scenario_to_db(author, last_update):
                messagebox.showinfo("Успех", "Сценарий успешно добавлен")
                form_window.destroy()
                self.show_scenarios_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить сценарий")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_scenario).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def edit_film(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для редактирования")
            return
        
        item = tree.item(selected[0])
        film_id = item['values'][0]
        
        # Получаем полные данные о фильме
        films = self.get_all_films()
        film_data = None
        for film in films:
            if film['id'] == film_id:
                film_data = film
                break
        
        if not film_data:
            messagebox.showerror("Ошибка", "Не удалось найти данные фильма")
            return
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Редактировать фильм")
        form_window.geometry("500x400")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Редактировать фильм", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Название:", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(form_frame, width=40)
        name_entry.insert(0, film_data['name'])
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Описание:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        description_text = tk.Text(form_frame, width=40, height=4)
        description_text.insert("1.0", film_data['description'])
        description_text.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Режиссер:", bg="#7E7D7D", fg="#000000").grid(row=2, column=0, sticky="w", pady=5)
        director_entry = tk.Entry(form_frame, width=40)
        director_entry.insert(0, film_data['director'])
        director_entry.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Год создания:", bg="#7E7D7D", fg="#000000").grid(row=3, column=0, sticky="w", pady=5)
        year_entry = tk.Entry(form_frame, width=40)
        year_entry.insert(0, str(film_data['year_of_creation']))
        year_entry.grid(row=3, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Статус:", bg="#7E7D7D", fg="#000000").grid(row=4, column=0, sticky="w", pady=5)
        status_var = tk.StringVar(value=film_data['status'])
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, 
                                   values=["Опубликован", "Архив", "Черновик", "Премьера"], state="readonly")
        status_combo.grid(row=4, column=1, pady=5, padx=5)
        
        def save_film():
            name = name_entry.get().strip()
            description = description_text.get("1.0", tk.END).strip()
            director = director_entry.get().strip()
            year = year_entry.get().strip()
            status = status_var.get()
            
            if not all([name, description, director, year, status]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            try:
                year = int(year)
            except ValueError:
                messagebox.showerror("Ошибка", "Год должен быть числом")
                return
            
            if self.update_film_in_db(film_id, name, description, director, year, status):
                messagebox.showinfo("Успех", "Фильм успешно обновлен")
                form_window.destroy()
                self.show_films_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить фильм")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_film).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def edit_scene(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сцену для редактирования")
            return
        
        item = tree.item(selected[0])
        scene_id = item['values'][0]
        
        scenes = self.get_all_scenes()
        scene_data = None
        for scene in scenes:
            if scene['id'] == scene_id:
                scene_data = scene
                break
        
        if not scene_data:
            messagebox.showerror("Ошибка", "Не удалось найти данные сцены")
            return
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Редактировать сцену")
        form_window.geometry("500x300")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Редактировать сцену", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Название:", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(form_frame, width=40)
        name_entry.insert(0, scene_data['name'])
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Тип:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        type_var = tk.StringVar(value=scene_data['type'])
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, 
                                 values=["Видеофайл", "Текст", "Изображение"], state="readonly")
        type_combo.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Время сцены (HH:MM:SS):", bg="#7E7D7D", fg="#000000").grid(row=2, column=0, sticky="w", pady=5)
        time_entry = tk.Entry(form_frame, width=40)
        time_entry.insert(0, scene_data['time_of_scene'])
        time_entry.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Смена сцены:", bg="#7E7D7D", fg="#000000").grid(row=3, column=0, sticky="w", pady=5)
        change_var = tk.StringVar(value=scene_data['change_scene'])
        change_combo = ttk.Combobox(form_frame, textvariable=change_var, 
                                   values=["Да", "Нет"], state="readonly")
        change_combo.grid(row=3, column=1, pady=5, padx=5)
        
        def save_scene():
            name = name_entry.get().strip()
            scene_type = type_var.get()
            time_of_scene = time_entry.get().strip()
            change_scene = change_var.get()
            
            if not all([name, scene_type, time_of_scene, change_scene]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if self.update_scene_in_db(scene_id, name, scene_type, time_of_scene, change_scene):
                messagebox.showinfo("Успех", "Сцена успешно обновлена")
                form_window.destroy()
                self.show_scenes_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить сцену")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_scene).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def edit_solution(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите решение для редактирования")
            return
        
        item = tree.item(selected[0])
        solution_id = item['values'][0]
        
        solutions = self.get_all_solutions()
        solution_data = None
        for solution in solutions:
            if solution['id'] == solution_id:
                solution_data = solution
                break
        
        if not solution_data:
            messagebox.showerror("Ошибка", "Не удалось найти данные решения")
            return
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Редактировать решение")
        form_window.geometry("500x200")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Редактировать решение", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Точка времени (HH:MM:SS):", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        time_entry = tk.Entry(form_frame, width=40)
        time_entry.insert(0, solution_data['point_of_time'])
        time_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Действие:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        action_var = tk.StringVar(value=solution_data['action'])
        action_combo = ttk.Combobox(form_frame, textvariable=action_var, 
                                   values=["Словестные", "Психические", "Физческие", "Материальные", "Не изменять"], state="readonly")
        action_combo.grid(row=1, column=1, pady=5, padx=5)
        
        def save_solution():
            point_of_time = time_entry.get().strip()
            action = action_var.get()
            
            if not all([point_of_time, action]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if self.update_solution_in_db(solution_id, point_of_time, action):
                messagebox.showinfo("Успех", "Решение успешно обновлено")
                form_window.destroy()
                self.show_solutions_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить решение")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_solution).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def edit_viewer(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите зрителя для редактирования")
            return
        
        item = tree.item(selected[0])
        viewer_id = item['values'][0]
        
        viewers = self.get_all_viewers()
        viewer_data = None
        for viewer in viewers:
            if viewer['id'] == viewer_id:
                viewer_data = viewer
                break
        
        if not viewer_data:
            messagebox.showerror("Ошибка", "Не удалось найти данные зрителя")
            return
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Редактировать зрителя")
        form_window.geometry("500x200")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Редактировать зрителя", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Email:", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(form_frame, width=40)
        email_entry.insert(0, viewer_data['email'])
        email_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Ник:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        nick_entry = tk.Entry(form_frame, width=40)
        nick_entry.insert(0, viewer_data['nick'])
        nick_entry.grid(row=1, column=1, pady=5, padx=5)
        
        def save_viewer():
            email = email_entry.get().strip()
            nick = nick_entry.get().strip()
            
            if not all([email, nick]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if self.update_viewer_in_db(viewer_id, email, nick):
                messagebox.showinfo("Успех", "Зритель успешно обновлен")
                form_window.destroy()
                self.show_viewers_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить зрителя")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_viewer).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def edit_views_map(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите карту просмотра для редактирования")
            return
        
        item = tree.item(selected[0])
        views_map_id = item['values'][0]
        
        views_maps = self.get_all_views_maps()
        views_map_data = None
        for views_map in views_maps:
            if views_map['id'] == views_map_id:
                views_map_data = views_map
                break
        
        if not views_map_data:
            messagebox.showerror("Ошибка", "Не удалось найти данные карты просмотра")
            return
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Редактировать карту просмотра")
        form_window.geometry("500x300")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Редактировать карту просмотра", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Последнее обновление (YYYY-MM-DD HH:MM:SS):", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        latest_update_entry = tk.Entry(form_frame, width=40)
        latest_update_entry.insert(0, str(views_map_data['latest_update']))
        latest_update_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Кол-во принятых решений:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        solutions_entry = tk.Entry(form_frame, width=40)
        solutions_entry.insert(0, str(views_map_data['number_of_perfect_solutions']))
        solutions_entry.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Кол-во просмотренных фильмов:", bg="#7E7D7D", fg="#000000").grid(row=2, column=0, sticky="w", pady=5)
        films_entry = tk.Entry(form_frame, width=40)
        films_entry.insert(0, str(views_map_data['number_of_films_watched']))
        films_entry.grid(row=2, column=1, pady=5, padx=5)
        
        def save_views_map():
            latest_update = latest_update_entry.get().strip()
            number_of_perfect_solutions = solutions_entry.get().strip()
            number_of_films_watched = films_entry.get().strip()
            
            if not all([latest_update, number_of_perfect_solutions, number_of_films_watched]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            try:
                number_of_perfect_solutions = int(number_of_perfect_solutions)
                number_of_films_watched = int(number_of_films_watched)
            except ValueError:
                messagebox.showerror("Ошибка", "Количества должны быть числами")
                return
            
            if self.update_views_map_in_db(views_map_id, latest_update, number_of_perfect_solutions, number_of_films_watched):
                messagebox.showinfo("Успех", "Карта просмотра успешно обновлена")
                form_window.destroy()
                self.show_views_maps_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить карту просмотра")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_views_map).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def edit_story(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сюжет для редактирования")
            return
        
        item = tree.item(selected[0])
        story_id = item['values'][0]
        
        stories = self.get_all_stories()
        story_data = None
        for story in stories:
            if story['id'] == story_id:
                story_data = story
                break
        
        if not story_data:
            messagebox.showerror("Ошибка", "Не удалось найти данные сюжета")
            return
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Редактировать сюжет")
        form_window.geometry("500x200")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Редактировать сюжет", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Жанр:", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        genre_var = tk.StringVar(value=story_data['genre'])
        genre_combo = ttk.Combobox(form_frame, textvariable=genre_var, 
                                  values=["Фантастика", "Боевик", "Фентези", "Приключения", "Комедия", "Триллер", "Ужасы", "Драма"], state="readonly")
        genre_combo.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Тип:", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        type_var = tk.StringVar(value=story_data['type'])
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, 
                                 values=["Линейный", "Концентрический", "Многолинейный", "Динамический", "Адинамический"], state="readonly")
        type_combo.grid(row=1, column=1, pady=5, padx=5)
        
        def save_story():
            genre = genre_var.get()
            story_type = type_var.get()
            
            if not all([genre, story_type]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if self.update_story_in_db(story_id, genre, story_type):
                messagebox.showinfo("Успех", "Сюжет успешно обновлен")
                form_window.destroy()
                self.show_stories_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить сюжет")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_story).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def edit_scenario(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сценарий для редактирования")
            return
        
        item = tree.item(selected[0])
        scenario_id = item['values'][0]
        
        scenarios = self.get_all_scenarios()
        scenario_data = None
        for scenario in scenarios:
            if scenario['id'] == scenario_id:
                scenario_data = scenario
                break
        
        if not scenario_data:
            messagebox.showerror("Ошибка", "Не удалось найти данные сценария")
            return
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Редактировать сценарий")
        form_window.geometry("500x200")
        form_window.configure(bg="#7E7D7D")
        
        tk.Label(form_window, text="Редактировать сценарий", font=("Arial", 14, "bold"), 
                bg="#7E7D7D", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(form_window, bg="#7E7D7D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Поля формы
        tk.Label(form_frame, text="Автор:", bg="#7E7D7D", fg="#000000").grid(row=0, column=0, sticky="w", pady=5)
        author_entry = tk.Entry(form_frame, width=40)
        author_entry.insert(0, scenario_data['author'])
        author_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Последнее обновление (YYYY-MM-DD):", bg="#7E7D7D", fg="#000000").grid(row=1, column=0, sticky="w", pady=5)
        last_update_entry = tk.Entry(form_frame, width=40)
        last_update_entry.insert(0, str(scenario_data['last_update']))
        last_update_entry.grid(row=1, column=1, pady=5, padx=5)
        
        def save_scenario():
            author = author_entry.get().strip()
            last_update = last_update_entry.get().strip()
            
            if not all([author, last_update]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if self.update_scenario_in_db(scenario_id, author, last_update):
                messagebox.showinfo("Успех", "Сценарий успешно обновлен")
                form_window.destroy()
                self.show_scenarios_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить сценарий")
        
        # Кнопки
        button_frame = tk.Frame(form_window, bg="#7E7D7D")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=save_scenario).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", font=("Arial", 10), bg="#ACACAC", fg="#000000",
                 padx=15, pady=5, command=form_window.destroy).pack(side=tk.LEFT, padx=5)

    def delete_film(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления")
            return
        
        item = tree.item(selected[0])
        film_id = item['values'][0]
        film_name = item['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить фильм '{film_name}'?"):
            if self.delete_film_from_db(film_id):
                messagebox.showinfo("Успех", "Фильм успешно удален")
                self.show_films_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить фильм")

    def delete_scene(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сцену для удаления")
            return
        
        item = tree.item(selected[0])
        scene_id = item['values'][0]
        scene_name = item['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить сцену '{scene_name}'?"):
            if self.delete_scene_from_db(scene_id):
                messagebox.showinfo("Успех", "Сцена успешно удалена")
                self.show_scenes_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить сцену")

    def delete_solution(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите решение для удаления")
            return
        
        item = tree.item(selected[0])
        solution_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить это решение?"):
            if self.delete_solution_from_db(solution_id):
                messagebox.showinfo("Успех", "Решение успешно удалено")
                self.show_solutions_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить решение")

    def delete_viewer(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите зрителя для удаления")
            return
        
        item = tree.item(selected[0])
        viewer_id = item['values'][0]
        viewer_nick = item['values'][2]
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить зрителя '{viewer_nick}'?"):
            if self.delete_viewer_from_db(viewer_id):
                messagebox.showinfo("Успех", "Зритель успешно удален")
                self.show_viewers_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить зрителя")

    def delete_views_map(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите карту просмотра для удаления")
            return
        
        item = tree.item(selected[0])
        views_map_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту карту просмотра?"):
            if self.delete_views_map_from_db(views_map_id):
                messagebox.showinfo("Успех", "Карта просмотра успешно удалена")
                self.show_views_maps_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить карту просмотра")

    def delete_story(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сюжет для удаления")
            return
        
        item = tree.item(selected[0])
        story_id = item['values'][0]
        story_genre = item['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить сюжет '{story_genre}'?"):
            if self.delete_story_from_db(story_id):
                messagebox.showinfo("Успех", "Сюжет успешно удален")
                self.show_stories_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить сюжет")

    def delete_scenario(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сценарий для удаления")
            return
        
        item = tree.item(selected[0])
        scenario_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот сценарий?"):
            if self.delete_scenario_from_db(scenario_id):
                messagebox.showinfo("Успех", "Сценарий успешно удален")
                self.show_scenarios_list()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить сценарий")

    # Вспомогательные функции
    def clear_current_frame(self):
        for widget in self.db_main_frame.winfo_children():
            widget.destroy()

    # Функции меню
    def refresh(self):
        messagebox.showinfo("Обновление", "Данные обновлены")

    def reset_to_default(self):
        messagebox.showinfo("Сброс", "Настройки сброшены к значениям по умолчанию")

    def quick_search(self):
        messagebox.showinfo("Быстрый поиск", "Функция быстрого поиска")

    def advanced_search(self):
        messagebox.showinfo("Расширенный поиск", "Функция расширенного поиска")

    def category_filters(self):
        messagebox.showinfo("Фильтры", "Функция фильтров по категориям")

    def stat_reports(self):
        messagebox.showinfo("Отчеты", "Функция статистических отчетов")

    def charts(self):
        messagebox.showinfo("Графики", "Функция графиков и диаграмм")

    def export_reports(self):
        messagebox.showinfo("Экспорт", "Функция экспорта отчетов")

    def user_management(self):
        messagebox.showinfo("Пользователи", "Функция управления пользователями")

    def access_rights(self):
        messagebox.showinfo("Права доступа", "Функция управления правами доступа")

    def backup(self):
        messagebox.showinfo("Резервное копирование", "Функция резервного копирования")

    def operation_log(self):
        messagebox.showinfo("Журнал операций", "Функция журнала операций")

    def user_manual(self):
        messagebox.showinfo("Руководство", "Функция руководства пользователя")

    def about(self):
        messagebox.showinfo("О программе", "Интерактивная система управления фильмами\nВерсия 1.0")

    def check_updates(self):
        messagebox.showinfo("Обновления", "Проверка обновлений")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedApp(root)
    root.mainloop()