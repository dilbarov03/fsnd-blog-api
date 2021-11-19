import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import Users, Posts, db

#TESTING = True
ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx3d3pHY3pZM0Vnc2YyVUJOXzZuTiJ9.eyJpc3MiOiJodHRwczovL3Byb2dlcjAzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTk1MjUxOTM4ZGFkMTAwNmYyZjI1YmIiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTYzNzMyMzE0NCwiZXhwIjoxNjM3NDA5NTQ0LCJhenAiOiJaTEY2RXlROTJ0MWlybmdid2xwUXVGcFFPQnFHMzZkRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicGF0Y2g6cG9zdHMiXX0.wblOV5qg5784_sBeDMGpgafO_yMvrXT-cEkY6ziIgVdUoi498y7sYsTZqevURTtgzGdL3Ld4jFXtZbQ9MrRDP8qBULSsVzz6RYmJ5tuVYKxhP0yk6S_qKgK6bSKE-gGWPZ3GXHzItU81Jah_4_rKsjuoQXItzyPnVLdr7cQl9CRg1vTM4_yLMg-6SnY-W8uh0bx7pCZe849W0rhKsqW-iGfF3m6hLVNVqh_RTq8Ozs6QOA90uV-c6T7WrXB5aXABNIB18DXaVUCHTw80ayB-LU3mSw_40a9vMtgdo4tX6BKzakrf8YZb89T3FSDb4gB_tXytt8d7CoWDDjZjhVL7fQ'
OWNER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx3d3pHY3pZM0Vnc2YyVUJOXzZuTiJ9.eyJpc3MiOiJodHRwczovL3Byb2dlcjAzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTk1MjU5NDgzYTIwZTAwNjkyMjQ2NTUiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTYzNzMyMTk5NiwiZXhwIjoxNjM3NDA4Mzk2LCJhenAiOiJaTEY2RXlROTJ0MWlybmdid2xwUXVGcFFPQnFHMzZkRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBvc3RzIiwicGF0Y2g6cG9zdHMiLCJwb3N0OnBvc3RzIiwicG9zdDp1c2VycyJdfQ.IGr_ki0zxXsstSiGUXB7RwrHcHGebcWQ4U9SWWFesA6C8R-sBIu8uMj3zI4VdCWWleQ6m7VowVqCWIpI9HqhifeNjxJZ-Q9NmD_KOkR_LYHgEDCrAdbeFnYxHmEkj-0RBIquSn0lIYdb3WfhE9UAtStcras20WoLHU6HHkjljt2OJG2Jp2T6UKj3dSFn2WlJq--RnBR9975BfsqwEMzMGuzjwW1xrF4OvUPYL_TzT_b7aZ0bbnOf3x5XrET5dS7W9ZU0vfhpmnpo88hrj5AoM2B6bAC6oA8DzpVuMwu5SIdif9Gqj29V-aQM5o4eTyXTCr0Oy5zCBGX-XfDs95SKLw'

class BasicTest(unittest.TestCase):
	def setUp(self):

		#app.config.from_object('config.TestingConfig')
		app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///api_testing"
		app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		
		self.client = app.test_client()
		self.headers = {'Content-Type': 'application/json'}

		
		#db.create_all()
 
	# executed after each test
	def tearDown(self):
		pass

	
	#Users
	
	def test_create_user(self):
		new_user = {
			"full_name": "Muminov Xondamir"
		}
		self.headers.update({'Authorization': 'Bearer ' + OWNER_TOKEN})

		res = self.client.post('/users', json=new_user, headers=self.headers)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)

	def test_create_user_error(self):
		new_user = {
			"full_name": "Anthony Mall"
		}
		self.headers.update({'Authorization': 'Bearer ' + ASSISTANT_TOKEN})

		res = self.client.post('/users', json=new_user, headers=self.headers)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 403) #assistant role does not have permission to create new users
	

	def test_get_users(self):
		res = self.client.get('/users')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
	#As /users are aviable for everyone, there is no error test for this endpoint

	def test_get_posts_by_specific_user(self):
		res = self.client.get('/users/1')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)

	def test_get_posts_by_specific_user_error(self):
		res = self.client.get('/users/1000')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 404) #user does not exist



	
	#Posts
	
	def test_create_post(self):
		new_post = {
			"title": "This is a new title",
			"body": "This is body",
			"author": "1"
		}
		self.headers.update({'Authorization': 'Bearer ' + OWNER_TOKEN})

		res = self.client.post('/posts', json=new_post, headers=self.headers)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)

	def test_create_post_error(self):
		new_post = {
			"title": "This is a new title",
			"body": "This is body",
			"author": "1"
		}
		
		res = self.client.post('/posts', json=new_post)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 401)

	def test_get_posts(self):
		res = self.client.get('/posts')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
	#As /posts are aviable for everyone, there is no error test for this endpoint

	def test_get_post_by_id(self):
		res = self.client.get('/posts/1')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)

	def test_get_post_by_id_error(self):
		res = self.client.get('/posts/1000')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 404)



	def test_update_post(self):
		updated_post = {
			"title": "Updated title"
		}

		self.headers.update({'Authorization': 'Bearer ' + ASSISTANT_TOKEN})

		res = self.client.patch(f'/posts/1', json=updated_post, headers=self.headers)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)

	def test_update_post_error(self):
		updated_post = {
			"title": "Updated title"
		}

		res = self.client.patch(f'/posts/1', json=updated_post)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 401)

	def test_delete_post(self):
		post = Posts(title='New title 2', body='New body 2',
							author='1')
		post.insert()
		post_id = post.id

		self.headers.update({'Authorization': 'Bearer ' + OWNER_TOKEN})

		res = self.client.delete(f'/posts/{post_id}', headers=self.headers)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)

	def test_delete_post_error(self):
		post = Posts(title='New title 2', body='New body 2',
							author='1')
		post.insert()
		post_id = post.id

		self.headers.update({'Authorization': 'Bearer ' + ASSISTANT_TOKEN})

		res = self.client.delete(f'/posts/{post_id}', headers=self.headers)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 403) #Assistant does not have permission to delete



# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()