# speck_weg
# Stefan Hochuli, 30.09.2021,
# Folder: server/speck_weg_backend/routes File: __init__.py
#

from typing import Union, TYPE_CHECKING
from flask import Blueprint

from .heroes import HeroAPI

if TYPE_CHECKING:
    from flask.views import MethodViewType, MethodView


def register_view(bp: 'Blueprint', method_view: Union['MethodView', 'MethodViewType'],
                  endpoint: str, url: str, pk: any, pk_type: str):
    """

    :param bp: blueprint to register the view to
    :param method_view: MethodView for registering
    :param endpoint: Name of the endpoint, e.g. hero_api
    :param url: Url of the endpoint, e.g. /heroes/
    :param pk: Identifier in the url, e.g. 'hero_id'
    :param pk_type: Type of the identifier, e.g. 'int'
    :return: -
    """
    view_func = method_view.as_view(endpoint)
    # POST -> without trailing slash
    bp.add_url_rule(url[:-1], view_func=view_func, methods=['POST', ])
    # GET collection
    bp.add_url_rule(url, defaults={pk: None},
                    view_func=view_func, methods=['GET', ])
    # GET / PUT / DELETE single
    bp.add_url_rule(f'{url}<{pk_type}:{pk}>', view_func=view_func,
                    methods=['GET', 'PUT', 'DELETE'])


auth_bp = Blueprint('auth', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')
hero_bp = Blueprint('heroes', __name__, url_prefix='/heroes')

# Registering the blueprints
api_bp.register_blueprint(hero_bp)

# Registering the views
# Usually, the url would be longer, this bp only has one view
register_view(hero_bp, HeroAPI, 'hero_api', '/', 'hero_id', 'int')
