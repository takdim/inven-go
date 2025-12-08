from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from app.models.user import User, UserLog
from app import db
from datetime import datetime

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Username atau password salah', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Akun Anda tidak aktif. Hubungi administrator.', 'warning')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # Update last login
        user.last_login = datetime.now()
        db.session.commit()
        
        # Log aktivitas
        UserLog.log_activity(
            user_id=user.id,
            activity='Login',
            description=f'User {user.username} berhasil login',
            ip_address=request.remote_addr
        )
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard.index')
        
        flash(f'Selamat datang, {user.nama_lengkap}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            nama_lengkap=form.nama_lengkap.data,
            role='staff'
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/logout')
@login_required
def logout():
    # Log aktivitas
    UserLog.log_activity(
        user_id=current_user.id,
        activity='Logout',
        description=f'User {current_user.username} logout',
        ip_address=request.remote_addr
    )
    
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('auth.login'))
