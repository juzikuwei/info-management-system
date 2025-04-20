from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

# 创建应用实例
app = Flask(__name__)
app.config.from_object(Config)

# 初始化登录管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录!'

# 确保数据库目录存在
os.makedirs(os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')), exist_ok=True)

# 用户模型
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 初始化数据库
def init_db():
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    ''')
    
    # 创建信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS information (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # 检查是否有默认管理员账户，如果没有则创建
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    user = cursor.fetchone()
    if not user:
        password_hash = generate_password_hash("admin123")
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("admin", password_hash))
    
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 用户加载回调
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['password_hash'])
    return None

# 路由: 首页
@app.route('/')
def index():
    return redirect(url_for('login'))

# 路由: 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], user_data['username'], user_data['password_hash'])
            login_user(user)
            flash('登录成功!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误!', 'danger')
    
    return render_template('login.html')

# 路由: 仪表板
@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM information WHERE user_id = ? ORDER BY date DESC", (current_user.id,))
    information_list = cursor.fetchall()
    conn.close()
    
    return render_template('dashboard.html', information_list=information_list)

# 路由: 添加信息
@app.route('/add_information', methods=['GET', 'POST'])
@login_required
def add_information():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        date = request.form.get('date')
        
        conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO information (title, content, category, date, user_id) VALUES (?, ?, ?, ?, ?)",
            (title, content, category, date, current_user.id)
        )
        conn.commit()
        conn.close()
        
        flash('信息添加成功!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_information.html')

# 路由: 编辑信息
@app.route('/edit_information/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_information(id):
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        date = request.form.get('date')
        
        cursor.execute(
            "UPDATE information SET title = ?, content = ?, category = ?, date = ? WHERE id = ? AND user_id = ?",
            (title, content, category, date, id, current_user.id)
        )
        conn.commit()
        conn.close()
        
        flash('信息更新成功!', 'success')
        return redirect(url_for('dashboard'))
    
    cursor.execute("SELECT * FROM information WHERE id = ? AND user_id = ?", (id, current_user.id))
    information = cursor.fetchone()
    conn.close()
    
    if not information:
        flash('信息不存在或无权限!', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_information.html', information=information)

# 路由: 删除信息
@app.route('/delete_information/<int:id>')
@login_required
def delete_information(id):
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM information WHERE id = ? AND user_id = ?", (id, current_user.id))
    conn.commit()
    conn.close()
    
    flash('信息删除成功!', 'success')
    return redirect(url_for('dashboard'))

# 路由: 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出!', 'success')
    return redirect(url_for('login'))

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)