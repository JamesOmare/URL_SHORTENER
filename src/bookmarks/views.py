from flask import Blueprint, request, jsonify, redirect
from http import HTTPStatus
from ..models.bookmark import Bookmark,db
import validators
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasgger import Swagger, swag_from

bookmarks = Blueprint('bookmarks', __name__, url_prefix='/api/v1/bookmarks')

@bookmarks.route('/', methods = ['POST', 'GET'])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()
    if request.method == 'POST':

        #1:21:30
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({

                'error': 'Enter a valid url'

            }), HTTPStatus.BAD_REQUEST

        if Bookmark.query.filter_by(url=url).first():
            return jsonify({

                'error': 'URL already exists'

            }), HTTPStatus.CONFLICT

        bookmark = Bookmark(

            url = url,
            body = body,
            user_id = current_user

        )

        db.session.add(bookmark)
        db.session.commit()

        return jsonify({

            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visits': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at

        }), HTTPStatus.CREATED


    #default page is the first page
    page = request.args.get('page', 1, type=int)
    #5 items assigned per page
    per_page = request.args.get('per_page', 5, type=int)

    bookmarks = Bookmark.query.filter_by(
        user_id = current_user).paginate(page=page, per_page=per_page)

    data = []

    for item in bookmarks.items:
        data.append({

            'id': item.id,
            'url': item.url,
            'short_url': item.short_url,
            'visits': item.visits,
            'body': item.body,
            'created_at': item.created_at,
            'updated_at': item.updated_at


        })

    meta = {

        'page': bookmarks.page,
        'pages': bookmarks.pages,
        'total_count': bookmarks.total,
        'previous_page': bookmarks.prev_num,
        'next_page': bookmarks.next_num,
        'has_next': bookmarks.has_next,
        'has_previous': bookmarks.has_prev

    }
    
    return jsonify({

        'data': data,
        'meta': meta

    }), HTTPStatus.OK


@bookmarks.route('/get_bookmark/<int:id>')
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id = current_user, id = id).first()

    if not bookmark:
        return jsonify({'message': 'item not found'})

    return jsonify({

        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visits': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at

    }), HTTPStatus.OK


@bookmarks.route('/update_url/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
def editbookmark(id):
    current_user = get_jwt_identity()

    bookmark  = Bookmark.query.filter_by(user_id = current_user, id = id).first()

    if not bookmark:
        return jsonify({'message': "item not found"}), HTTPStatus.NOT_FOUND

    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')

    if not validators.url(url):
        return jsonify({

            'error': 'Enter a valid url'

        }), HTTPStatus.BAD_REQUEST

    
    bookmark.url = url
    bookmark.body = body

    db.session.commit()

    return jsonify({

        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visits': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at

    }), HTTPStatus.OK


@bookmarks.delete('/delete/<int:id>')
@jwt_required()
def delete_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id = current_user, id = id).first()

    if not bookmark:
        return jsonify({'message': 'Item to be deleted not found!'}), HTTPStatus.NOT_FOUND
    
    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({}), HTTPStatus.NO_CONTENT 


@bookmarks.get('/<short_url>')
@swag_from('../docs/short_url.yaml')
def redirect_to_url(short_url):
    bookmark = Bookmark.get_short_url(short_url)

    if bookmark:
        bookmark.visits = bookmark.visits+1
        db.session.commit()

        return redirect(bookmark.url)


@bookmarks.get('/stats')
@jwt_required()
def get_status():
    current_user = get_jwt_identity()

    data = []

    items = Bookmark.query.filter_by(user_id = current_user).all()

    for item in items:
        new_link = {

            'visits': item.visits,
            'url': item.url,
            'id': item.id,
            'short_url': item.short_url

        }

        data.append(new_link)

    return jsonify({
        'data': data
    }), HTTPStatus.OK


