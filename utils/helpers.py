from sqlalchemy.sql import func
import secrets
from functools import wraps
from flask import request, jsonify
from models import User
from flask_mail import Message
from flask import current_app
from extensions import mail

def is_positive_int(s):
    try:
        return int(s) > 0
    except ValueError:
        return False


def get_game_to_type_mapping(game_type):
    """Returns the internal attribute name for a given game type string.

    This function maps a human-readable game type (e.g., "Would You Rather")
    to its corresponding attribute name used in the Playground model
    (e.g., "would_you_rather_questions").

    Parameters:
        game_type (str): The display name of the game type.

    Returns:
        str: The internal attribute name corresponding to the game type."""
    mapping = {
        'did you know': 'did_you_knows',
        'hypotheticals': 'hypotheticals',
        'hot takes': 'hot_takes',
        'never have i ever': 'never_have_i_evers',
        'would you rather': 'would_you_rather_questions',
        'story builder': 'story_builders',
        'riddles': 'riddles',
        'two truths and a lie': 'two_truths_and_a_lie'
    }
    key = game_type.lower()
    return mapping[key]


def return_error_for_wrong_params(game_type, limit=None):
    """    Returns an appropriate error response for invalid or missing game type.

    This function checks whether the provided game_type is missing or not among the
    supported types. If invalid, it returns a dictionary describing the error along
    with the appropriate HTTP status code.

    Parameters:
        limit: (int): the maximum number of responses to be returned
        game_type (str | None): The value of the 'game_type' query parameter.

    Returns:
        tuple[dict, int] | None: A tuple containing the error message dictionary and status code (400 or 422),
                                 or None if the game_type is valid."""
    if limit:
        if not is_positive_int(limit):
            return {
                'status': 'error',
                'code': 'invalid_param_type',
                'message': {
                    'detail': "The 'limit' parameter must be a positive integer or a string that can be converted to a "
                              "positive integer."
                }
            }, 422

    if not game_type:
        return {'status': 'error', 'code': 'missing_params',
                'message': {
                    'Bad Request': "Required parameter 'game_type' is missing. Please set it and try again."
                }
                }, 400
    valid_types = ['did you know', 'hypotheticals', 'hot takes', 'never have i ever', 'would you rather',
                   'story builder', 'riddles', 'two truths and a lie']
    if game_type.lower() not in valid_types:
        return {'status': 'error', 'code': 'invalid_param_value',
                'message': {
                    'Unprocessable Entity': f"{game_type} is not a valid game type . Valid options are: "
                                            f"{', '.join([t for t in valid_types])}"

                }
                }, 422


def get_game_by_type(game, game_type, model_class, category=None, limit=None):
    """Fetches game entries of a specified type, optionally filtered by category or limited in number.

    This helper function dynamically accesses a relationship on the game object using game_type.
    It applies optional filtering by category and random ordering with a result limit.
    The results are returned as a dictionary and a success status code.

    Parameters:
        game (Playground): The Playground model instance containing the relationships.
        game_type (str): The name of the relationship attribute (e.g., 'did_you_knows').
        model_class (db.Model): The SQLAlchemy model class corresponding to the game type.
        category (str, optional): Category to filter results by.
        limit (int, optional): Maximum number of results to return.

    Returns:
        tuple[dict, int]: A tuple containing the queried game data and HTTP status code 200."""
    query = getattr(game, game_type)
    if not category and not limit:  # if user doesn't specify category or limit,
        result = query.order_by(func.random()).all()  # return all games of that type
    elif category:  # if they specify category
        query = query.filter(model_class.category == category)
        result = query.order_by(func.random()).all() if not limit else query.order_by(func.random()).limit(limit).all()
        # check if they specify limit as well
    else:
        result = query.order_by(func.random()).limit(limit).all()  # if no category just limits,
        # pick at random from any category
    return {
        game_type: [
            q.to_dict() for q in result
        ]
    }, 200


def get_api_key():
    api_key = secrets.token_urlsafe(20)
    return api_key


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.args.get('api_key')
        if not api_key:
            return jsonify({'status': 'error',
                            'code': 'api_key_missing',
                            'message': 'Your API key is missing. Append this to the URL with the api_key param.'}
                           ), 401
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            return jsonify({'status': 'error',
                            'code': 'api_key_invalid',
                            'message': f'Your API key is invalid or incorrect. Check your key, '
                                       'or go to https://sayit-playground-api.onrender.com/ to create a free API key.'}
                           ), 401
        return f(*args, **kwargs)

    return decorated


def send_api_key(user_email, api_key):
    subject = "🎉 Your Playground API Key"
    body = f"""Hey there!

    Thanks for registering for the Playground API.
    You are receiving this email to confirm the creation of an 
    API key. If you did not request this, please disregard this email.
    Here is your personal API key for {user_email}:
    {api_key}

    Please keep it secure. You'll need it for every request.

    – The Playground Team
    """

    msg = Message(subject=subject, recipients=[user_email], body=body)
    with current_app.app_context():
        mail.send(msg)
