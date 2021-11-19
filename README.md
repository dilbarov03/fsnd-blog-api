# Blog API Backend

## About

This is the simple blog API project. Everyone can get posts and users, but to create new posts - authorization and permissions are needed.

https://blog03-api.herokuapp.com

## API

In order to use the API users don't need to be authenticated, but for creating new posts and users - it is indeed crucial. Users can either have a guest, assistant and owner status. An overview of the API can be found below as well as in the provided postman collection.

### Retreiving data (Guests and members)

**GET** `/posts`

Retrieves all posts

```
curl -X GET \
  https://blog03-api.herokuapp.com/posts'
```

Sample response:
```
{
    "all_posts": {
        "Advanced Visual Studio Code for Python Developers": "Visual Studio Code, or VS Code for short, is a free and open source code editor by Microsoft. You can use VS Code as a lightweight code editor to make quick changes, or you can configure it as an integrated development environment (IDE) through the use of third-party extensions. In this tutorial, you’re going to look at how to get the most out of VS Code for Python development.",
        "This is a second post": "This is new body"
    }
}
```

**GET** `/posts/<int:post_id>`

Retrieves a specific post by id

```
curl -X GET \
  https://blog03-api.herokuapp.com/posts/1
```

Sample response:
```
{
    "body": "The fractions module in Python is arguably one of the most underused elements of the standard library. Even though it may not be well-known, it’s a useful tool to have under your belt because it can help address the shortcomings of floating-point arithmetic in binary. That’s essential if you plan to work with financial data or if you require infinite precision for your calculations.",
    "title": "Representing Rational Numbers With Python Fractions"
}
```

**GET** `/users`

Retrieves all existing users

```
curl -X GET \
  https://blog03-api.herokuapp.com/users'
```

Sample response:
```
{
    "all_users": {
        "1": "Thomas Party",
        "2": "Dilbarov Uktamjon",
        "3": "Xondamir Mo'minov",
        "4": "Anthony May"
    }
}
```

**GET** `/users/<int:user_id>`

Retrieves posts of specific users

```
curl -X GET \
  https://blog03-api.herokuapp.com/users/1
```

Sample response:
```
{
    "user_posts": {
        "Advanced Visual Studio Code for Python Developers": "Visual Studio Code, or VS Code for short, is a free and open source code editor by Microsoft. You can use VS Code as a lightweight code editor to make quick changes, or you can configure it as an integrated development environment (IDE) through the use of third-party extensions. In this tutorial, you’re going to look at how to get the most out of VS Code for Python development.",
        "Build a Command-Line To-Do App With Python and Typer": "Building an application to manage your to-do list can be an interesting project when you’re learning a new programming language or trying to take your skills to the next level. In this tutorial, you’ll build a functional to-do application for the command line using Python and Typer, which is a relatively young library for creating powerful command-line interface (CLI) applications in almost no time."
    }
}
```

### Managing data (Members only)

**POST** `/users` (Owner role only)

Create a new user

```
curl -X POST \
  https://blog03-api.herokuapp.com/users \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "full_name": "Komilov Sardor"
}'
```
Sample response:
```
{'success': 'True'}
```

**POST** `/posts` (Owner role only)

Create a new post

```
curl -X POST \
  https://blog03-api.herokuapp.com/posts \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "New Post",
    "body": "Body for new post",
    "author": "3"
}'
```
Sample response:
```
{'success': 'True'}
```

**PATCH** `/posts/<int:post_id>` (Supports both owner and assistant role)

Update post

```
curl -X PATCH \
  https://blog03-api.herokuapp.com/posts/2 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Updated title!"
}'
```
Sample response:
```
{'success': 'True'}
```


**DELETE** `/posts/<int:post_id>` (Owner role only)

Delete a given post

```
curl -X DELETE \
  https://blog03-api.herokuapp.com/posts/4 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN> ' \

```
Sample response:
```
{
  'success': 'True',
  'deleted': '4'
}
```

## Installation

The following section explains how to set up and run the project locally.

### Installing Dependencies

The project requires Python 3.8. Using a virtual environment such as `pipenv` is recommended. Set up the project as follows:

```

pipenv shell
pipenv install

```

### Database Setup


With Postgres running, create a database and import data using the blog_api.psql file provided. In terminal run:
```

sudo -u postgres createdb blog_api
psql blog_api < blog_api.psql
```

### Running the server

To run the server, first set the environment variables, then execute:

```bash
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql:///blog_api"
python manage.py runserver
```

## Testing

To test the API, first create a test database in postgres and then execute the tests as follows:

```
sudo -u postgres createdb api_testing
psql api_testing < test_blog_api.psql
python test_app.py
```
