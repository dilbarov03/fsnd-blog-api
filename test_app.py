import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import Users, Posts, db

#TESTING = True
ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx3d3pHY3pZM0Vnc2YyVUJOXzZuTiJ9.eyJpc3MiOiJodHRwczovL3Byb2dlcjAzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTk1MjUxOTM4ZGFkMTAwNmYyZjI1YmIiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTYzNzIzNTA5MywiZXhwIjoxNjM3MzIxNDkzLCJhenAiOiJaTEY2RXlROTJ0MWlybmdid2xwUXVGcFFPQnFHMzZkRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicGF0Y2g6cG9zdHMiXX0.fLfF8xSlbYVLkwI8g7fjmwIxtODmjjy1nxvdoeN1loSCCtrojSpLLkadZ5dwPTsASTn60bV8PZoi1lZEHPiyzju4cnwBDRSH9ph8D1M7Tpl6LX1eEd6HDDlz3PtSAUtpXlGy8KBA7qPe00IZwnRPBx3sorb4fmliFbAhF9VibtVxZDCmYi4Eadk0O7n_qTTMPxKBp9ETNBoy0QToCmfE7a05x1uVFkKX67ZK8uYORquXtmlAc2EGTEJKm4YIv-z7C25V1yrRmCYyaZtdmmvpH5LrHwbopcEUzrtvh9Sm8STJS5bMiH373APYiWmgRj__LFSlx5u5FRF1qwIj4ctL6Q'
OWNER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx3d3pHY3pZM0Vnc2YyVUJOXzZuTiJ9.eyJpc3MiOiJodHRwczovL3Byb2dlcjAzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTk1MjU5NDgzYTIwZTAwNjkyMjQ2NTUiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTYzNzIzNDY2OCwiZXhwIjoxNjM3MzIxMDY4LCJhenAiOiJaTEY2RXlROTJ0MWlybmdid2xwUXVGcFFPQnFHMzZkRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBvc3RzIiwicGF0Y2g6cG9zdHMiLCJwb3N0OnBvc3RzIiwicG9zdDp1c2VycyJdfQ.DTXnUbimUQVbIhl8tduGO5EHgyY-CV_8374tuHFo1uD8y0D2AR1LoEu-cCdYaOAT9xxKOgGULYPSG6KP0u5_jcvU0G-Fon9yS-3B_LE-8SAuEFNi2uChPBAlsjzPebu40yusxmfVgocI-kQZQBx8ZQrsb_Zqkt41F39MrUv0UOxGMr_BSDH0bgKSHQngqalB62aSz85jQsdtwt0nOgvVnkrPqZ6JxKojbOOQOMzRnS1VGDRne_lJIOIE-BAMXRjsburEwlRQe83vBhPJBmXWMEZYlR28VVd3KbJNsR-wbif4vxuU33mhNUt_36U5j4uUPu3gduzdQzCNvI_MtQol7Q'

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