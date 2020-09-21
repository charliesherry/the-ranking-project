from flask import Flask
app = Flask("apironhack")

@app.route('/')
def welcome():
    return 'Welcome to the ApIronhack!'

