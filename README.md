# W6 Project - The Meme Ranking

![image](https://res-1.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/ajracsdqu5gmyfl6nai0)

## The main goals of this project are:
- Create an API 
- Store information from github to MongoDB
- Obtain information from MongoDB through endpoints created in our API

All of the previous is done to perform a "Meme Ranking" from the instructors comments to our pull requests. 

## The main tools I used were:
- Flask
- Requests
- Pymongo
- Other python tools (pandas, regex , etc.)

## Introduction to the files in this repo:
- Server.py : This file is used to run the server of our own API.
- src/database.py : This file is created in order to generate our database in MongoDB
- src/functions.py : This file contains the functions used to extract all the information from Github
- src/lab_controllers.py & student_controllers.py: These have the endpoints needed to extract the information from MongoDB through our API.
- Output: Here you can find the json files generated from the requests to Github and then inserted into MongoDB.


Thank you for appreciating the work done here!


![image](https://i.imgflip.com/4g8k1q.jpg)



