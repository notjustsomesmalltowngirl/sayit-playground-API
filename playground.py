import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from sayit_playground_api.models import db, Playground, DidYouKnow, Hypotheticals, HotTakes, NeverHaveIEver
from sayit_playground_api.models import WouldYouRather, StoryBuilder, Riddle, TwoTruthsAndALie
from sayit_playground_api.models import User
import smtplib
import logging
from email.message import EmailMessage
from sqlalchemy.sql.expression import func
from utils.helpers import (get_game_by_type, return_error_for_wrong_params,
                           get_game_to_type_mapping, get_api_key, require_api_key)
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.context_processor
def inject_globals():
    return dict(current_year=datetime.now().year)


# with app.app_context():
#     db.create_all()
#     game = Playground.query.filter_by(type='did you know').scalar()
#     query = getattr(game, game_type)
#     print(query.order_by(func.random()).limit(1).one().to_dict())


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/v1/all-game-types', methods=['GET'])
@require_api_key
def get_all_game_types():
    all_games = Playground.query.all()
    return jsonify(
        {
            'all_games': [g.type for g in all_games]
        }
    ), 200


@app.route('/api/v1/get-random', methods=['GET'])
@require_api_key
def get_random_game():
    game_type = request.args.get('game_type')
    error_response = return_error_for_wrong_params(game_type)
    if error_response:
        error, status_code = error_response
        return jsonify(error), status_code
    type_ = get_game_to_type_mapping(game_type)
    game = Playground.query.filter_by(type=game_type.lower()).scalar()
    query = getattr(game, type_)  # get query based on game type
    return jsonify(
        {
            game_type: query.order_by(func.random()).limit(1).one().to_dict()
        }
    )


@app.route('/api/v1/get-by-type', methods=['GET'])
@require_api_key
def get_by_type():
    game_type = request.args.get('game_type')
    limit = request.args.get('limit')
    category = request.args.get('category')
    error_response = return_error_for_wrong_params(game_type, limit)
    if error_response:
        error, status_code = error_response
        return jsonify(error), status_code
    game = Playground.query.filter_by(type=game_type.lower()).scalar()
    match game_type.lower():
        case 'did you know':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), DidYouKnow,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'hypotheticals':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), Hypotheticals,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'hot takes':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), HotTakes,
                                                   category=category, limit=limit)
            return jsonify(result), status_code
        case 'never have i ever':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), NeverHaveIEver,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'would you rather':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), WouldYouRather,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'story builder':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), StoryBuilder,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'riddles':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), Riddle, category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'two truths and a lie':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), TwoTruthsAndALie,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        # default's been handled


@app.route('/suggest', methods=['GET', 'POST'])
@login_required
def suggest():
    admin_users = User.query.filter_by(role='admin').all()
    admin_emails = [admin.email for admin in admin_users]
    sender_email = os.getenv('ADMIN_EMAIL_1')
    sender_password = os.getenv('SENDER_APP_PASSWORD')

    if request.method == 'POST':
        suggestion_title = request.form.get('title')
        suggestion_description = request.form.get('description')
        suggestion_type = request.form.get("feature-category")
        suggestion_use_case_example = request.form.get('use_case_example')
        use_case_text = (
            f"{suggestion_use_case_example}"
            if suggestion_use_case_example
            else "No use case example provided."
        )
        msg = EmailMessage()
        msg['Subject'] = 'Suggestion For Playground API'
        msg['From'] = sender_email
        msg['To'] = ', '.join(admin_emails)  # multiple recipients
        msg.set_content(
            f"""Suggestion title: {suggestion_title}
            Description: {suggestion_description}
            Type: {suggestion_type}
            Use case example: {use_case_text}
            """
        )
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                flash("✅ Suggestion sent successfully!", )

        except smtplib.SMTPException as e:
            logging.exception(f"Failed to send suggestion email, {e}")
            print(f"Failed to send suggestion email, {e}")
            flash("❌ Failed to send suggestion. Please try again later.", )
        else:
            return redirect(url_for('home'))
    return render_template('suggestions.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 🔹 Check if the email is already registered
        existing_user = User.query.filter_by(email=request.form['email']).first()
        if existing_user:
            flash('You are registered login instead')
            return redirect(url_for('login'))
        # 🔹 Create new user
        new_user = User(email=request.form['email'],
                        password=generate_password_hash(request.form['password']),
                        username=request.form['username'])
        # 🔹 Give an admin role to specific emails
        if new_user.email in [os.getenv('ADMIN_EMAIL_1'), os.getenv('ADMIN_EMAIL_2'),
                              os.getenv('ADMIN_EMAIL_3'), ]:
            new_user.role = 'admin'
            flash('Welcome admin')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/sign-in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        elif not user:
            flash('That email is not registered, please try again with a registered email', )
        elif not check_password_hash(user.password, request.form['password']):
            flash('Incorrect Password')
    return render_template('login.html')


@app.route('/profile')
@login_required
def profile():
    if not current_user.api_key:
        for _ in range(3):
            try:
                current_user.api_key = get_api_key()
                db.session.commit()
                break
            # except get_api_key() returns one it has returned before, since that is marked as unique
            except IntegrityError:
                db.session.rollback()
                with open('error_log.txt', 'a') as f:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] Failed to create user {current_user.id}'s api key "
                          f"'cause of Integrity errors", file=f)
        else:
            print('Integrity error')
    return render_template('profile.html')


@app.route('/update_email', methods=['POST'])
@login_required
def update_profile():
    new_email = request.form.get('new_email')  # retrieve the email the user entered
    new_password = request.form.get('new_password')
    if 'update_email' in request.form:
        if new_email:  # check that new_email is not None
            # check to see if the email user is trying to change to is already registered
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user:  # if that email already registered
                if new_email == current_user.email:  # check if it's for the current user
                    flash('Same as current email')
                else:
                    flash('That email address is already in use.')
            else:  # if the new email doesn't already exist, change the email
                current_user.email = new_email
                db.session.commit()
                flash('Email updated successfully!')
    elif 'update_password' in request.form:
        if not check_password_hash(current_user.password, new_password):
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('password changed successfully')
        else:
            flash('Same as previous password.')
    return redirect(url_for('profile'))


@app.route('/docs')
def docs_page():
    if current_user.is_authenticated and current_user.api_key:
        api_key = current_user.api_key
    else:
        api_key = 'API_KEY'
    return render_template('documentation.html', api_key=api_key,
                           valid_types=['did you know, ', 'hypotheticals, ', 'hot takes, ', 'never have i ever, ',
                                        'would you rather, ',
                                        'story builder, ', 'riddles, ', 'two truths and a lie'])


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
