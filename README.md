
ADMIN:
user: admin
pass: admin


SETUP PROJECT:
- change mysql user and password in setting.py file
- create taskmanager table in mysql database
- pipenv install => to install environment and requirements
- pipenv shell => activate environment
- cd taskmanager
- python manage.py migrate
- python manage.py createsuperuser => create super user
- python manage.py runserver
- python manage.py test tasks.tests => to run tests

ABOUT THE WEBAPPLICATION:
I considered that the user should insert just the title and description to create the task and all the tasks have the same status after creation. Users just can change the title, description, and status of his/her own task.

Because it was noticed we should have 2 API endpoints, I considered that I should have just 2 classes in my views.py to handle requests.
For creating a task I thought about 3 ways. I decided to have 2 different HTML files but show them on one page; So, if my work is not right, I can change it easily. 
For delete and edit, I found this problem too and used js and same above way to solve this problem, but it didn't work. At last, I had to create new routes.

I used Bootstrap but a little, if the design of pages is important I can change them.

I found more than one way to implement different parts of this project, so I commented some of them in the code. 
First, I wrote views.py and classes with Serilizaer and checked them all, then for adding templates to the code I had to change the code and almost the project was distanced from the structure it should follow(Django restful). 
I started to use generic views and mixin but I found this way may cause challenges and didn't continue.

 
