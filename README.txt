This is the task assigned by TAP, Kuwait

app.py has all the apis
task.py is the cronjob script that will automate the tasks.

To run the application,

Run app.py, using POSTMAN you can access the apis and enter the json
eg: {"task": "payment","time":"2"}

Here the task to be repeated is payment and the time interval is 2min.
I have used minutes as this is a demo code.

Once you have the data in the db, Run task.py and it will do the tasks based
on the intervals by calculating the last updated time and the current time.

Algorithm used:
1. Take entries using the add api
2. view entries using the view all api
3. edit the entries using the replace api
4. update the entries using the update api
5. create a json that looks like: {"task":"","time":"", "last seen":"", "creation time":""}
6. run a script that finds the difference between the last seen and the current time and checks with the time interval and then updates the last seen time to current time.

NEW Task- new_app.py

This the new task, asked to complete.
Run the requirements.txt.
and run new_app.py

the apis are created as mentioned in the task.

-/plan/create
-/feature/create
-/plan/list_all
-/plan/id/update
-/plan/limit

the names of the api are self explainatory.

I hope I have successfully completed the task as expected.
