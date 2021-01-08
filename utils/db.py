# Importing dependencies
import requests

# API location
API_URL = "https://designapi.principle105.repl.co/"

# Gets user information
def get_user(username):
  try:
    response = requests.get(API_URL + f"user/get_user/{username}").json()
    return response
  except Exception as e:
    return {"message": "Something went wrong"}

# Gets hospital information
def get_hospital(name):
  try:
    response = requests.get(API_URL + f"hospital/get_hospital/{name}").json()
    return response
  except Exception as e:
    print(e)
    return {"message": "Something went wrong"}

# Deletes a user
def delete_user(username):
  try:
    response = requests.post(API_URL + f"user/delete_user/{username}").json()
    return response
  except Exception as e:
    print(e)
    return {"message": "Something went wrong"}

# Registers a user
def register_user(username, password):
  try:
    if len(username) < 3:
      return {"message": "Your username must be at least 3 characters long"}
    elif len(password) < 3:
      return {"message": "Your password must be at least 3 characters long"}
    elif "/" in password:
      return {"message": "Your password cannot contain /"}
    response = requests.get(API_URL + f"user/register_user/{username}/{password}").json()
    return response
  except Exception as e:
    print(e)
    return {"message": "Something went wrong"}

# Creates a hospital
def create_hospital(name,creator_username):
  try:
    if len(name) < 3:
      return {"message": "The hospital name must be at least 3 characters long"}
    response = requests.get(API_URL + f"hospital/create_hospital/{name}/{creator_username}").json()
    return response
  except Exception as e:
    print(e)
    return {"message": "Something went wrong"}

#Joins a hospital
def join_hospital(name,join_code,creator_username):
  try:
    response = requests.get(API_URL + f"hospital/join_hospital/{name}/{join_code}/{creator_username}").json()
    return response
  except Exception as e:
    print(e)
    return {"message": "Something went wrong"}

# Updates a user's schedule
def update_schedule(hospital,username,value):
  try:
    response = requests.get(API_URL + f"hospital/update_schedule/{hospital}/{username}/{value}").json()
    return response
  except Exception as e:
    return {"message": "Something went wrong"}

# Update hospital schedule
def update_hospital(hospital,stat,value):
  try:
    response = requests.get(API_URL + f"hospital/update_hospital/{hospital}/{stat}/{value}").json()
    return response
  except Exception as e:
    print(e)