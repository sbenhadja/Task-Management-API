# Task-Management-API

This mini project aime to solve the Exercise: Building a Simple Task Management API

Developement envirenement: python 3.11.8 , Postgresql 14

**<u>How to execute the project:</u>**

```
1. Clone the project 
2. Open vs code on the cloned project path 
3. Create virtuel env 'cmd' : python -m venv myenv 
4. Activate the venv 'cmd' : .myenv\Scripts\activate 
5. Install the requirement framework 'cmd' : pip install -r requirements.txt 
6. Take some coffee  - optional :)
7. Create Postgresql DB { name: task -- user: Postgres -- PW: admin } 
                     OR change the DATABASES parameter in settings.py with your proper BD parameter
8. Run 'cmd' : python manage.py migrate
     TO migrate the models to DB
9. To run test 'cmd' : python manage.py test task
10. Run the application 'cmd' : python manage.py runserver 
```

**NB:** use Postman for testing all API in this project, you can find a collection of API requests for testing in this project.
 This collection is available in a file format that can be imported into Postman, making it easy for you to test the APIs.

*To test all API, you need at least one user for complete all CRUD test 'see the attached collection'*

```
A. POST: {dns}/user/register 
B. POST: {dns}/user/login ---> {"refresh": "...", "access":"...", ... }
C. Use the access token with all task CRUD API as Authorisation --> Bearer Token
```
