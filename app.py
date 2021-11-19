import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Posts, Users
from auth import AuthError, requires_auth

def create_app(test_config=False):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route("/")
  def index():
    return "Hello World"

  @app.route("/posts")
  def get_all_posts():
    all_posts = Posts.query.order_by(Posts.id).all()
    return jsonify({
      "all_posts": {a.title: a.body for a in all_posts}
      })

  @app.route("/posts/<int:post_id>")
  def get_post_by_id(post_id):
    post = Posts.query.filter(Posts.id==post_id).all()
    if post:
      return jsonify({
        "title": post[0].title,
        "body": post[0].body
        })
    else:
      abort(404)

  @app.route("/users")
  def get_all_users():
    users = Users.query.order_by(Users.id).all()
    return jsonify({
      "all_users": {a.id: a.full_name for a in users}
      })

  @app.route("/users/<int:user_id>")
  def get_user_posts(user_id):
    user_posts = Posts.query.filter(Posts.author==user_id).all()
    if user_posts:
      return jsonify({
        "user_posts": {a.title: a.body for a in user_posts}
        })
    else:
      abort(404)

  @app.route("/users", methods=["POST"])
  @requires_auth('post:users')
  def create_user(jwt):
    body_json = request.get_json()
    if body_json:
      if not ("full_name" in body_json):
        abort(422)

      full_name = body_json.get('full_name')

      try:
        user = Users(full_name=full_name)
        user.insert()

        return jsonify({
            "success": True
            })
      except:
        abort(422)
    else:
      abort(422)

  @app.route("/posts", methods=["POST"])
  @requires_auth('post:posts')
  def create_post(jwt):
    body_json = request.get_json()
    if not ("title" in body_json and "body" in body_json and "author" in body_json):
      abort(422)

    title = body_json.get('title')
    body = body_json.get('body')
    author = body_json.get('author')

    #try:
    post = Posts(title=title, body=body, author=author)
    post.insert()

    return jsonify({
        "success": True
          })
    #except:
      #abort(422)

  @app.route("/posts/<int:post_id>", methods=["PATCH"])
  @requires_auth('patch:posts')
  def update_post(jwt, post_id):
    post = Posts.query.get(post_id)

    if post!=None:
      try:
        body_json = request.get_json()


        title = body_json.get('title')
        body = body_json.get('body')
        author = body_json.get('author')

        if title:
          post.title = title
        if body:
          post.body = body
        if author:
          post.author = author
        
        post.update()

        return jsonify({
            "success": True
            })
      except:
        abort(422)

    else:
      abort(404)

  @app.route("/posts/<int:post_id>", methods=["DELETE"])
  @requires_auth('delete:posts')
  def delete_post(jwt, post_id):
    post = Posts.query.get(post_id)

    if post!=None:
      try:
        post.delete()

        return jsonify({
            'success': True,
            'deleted': post_id
        })
      except:
          abort(422)
    else:
        abort(404)

  return app

app = create_app()
# Error Handling

@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
  }), 422

@app.errorhandler(404)
def not_found(error):
  return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
      }), 404

@app.errorhandler(401)
def auth_error(error):
  return jsonify({
      "success": False,
      "error": 401,
      "message": "Not authorized"
      }), 401

@app.errorhandler(500)
def internal_error(error):
  return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal server error"
      }), 500

@app.errorhandler(AuthError)
def auth_error_handler(AuthError):
  return (jsonify(
      {
          "error": AuthError.status_code,
          "message": AuthError.error["description"],
          "success": False,
      }
  ), AuthError.status_code,) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)