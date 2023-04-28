from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from info import USERNAME,PASSWORD
import sys
# logged_data: Global for storing strings to print
# for debugging
# append strings to logged_data to add log statements
#
# args: Dictionary that stores all of the variables to be
# passed into the html. Provide args=args in every
# Render template call and manage what is in args
#
# addArgs(input_data): add multiple variables to the 
# args dictionary
#
#
# addArg(data_piece): add one variable to args
# where you pass the variables name as the key and the 
# content as the value
# I.E addArg({"census_data":census})
# adds census object to args with key "census_data" for 
# reference in html




#TODO: We still have a lot of data inconsistencies
#I still need to get city specific data 
#Gennaro -> Your city names are inconsistent to what we are looking for
# I.E For Washington the CITY is District of Columbia but we use DC as the 
# query.
#Ava -> Nothing Yet
#Tim -> Still need to re-organize the stops_data because I need a concrete
# city name in order to pull the data.
#===========Helper Functions================
def addArgs(input_data):
    global args,logged_data
    for data in input_data:
        for name in data:
            args[name] = data[name]


def addArg(data_piece):
    global args,logged_data
    for name in data_piece:
        args[name] = data_piece[name]
    #args = {"logged_data":logged_data}


def cleanDocument(document,excluded_fields,toExclude):
    if toExclude:
        cleaned_doc  = {key: val for key,
            val in document.items() if not excluded_fields.__contains__(key)}
    else:
        cleaned_doc  = {key: val for key,
            val in document.items() if excluded_fields.__contains__(key)}
    return cleaned_doc


def packData(city):
    all_data = []
    census_data = []
    weather_data = []
    jobs_data = []
    stops_data = []
    # Handle census data
    census_excluded = ['_id','state','city','place', 'NAME']
    for document in mongo.db.census_data.find({"city":{"$regex":f"{city.lower()}"}}):
        census_data.append(document)

    
    for i, doc in enumerate(census_data):
        cleaned_doc = cleanDocument(doc,census_excluded,True)
        census_data[i] = cleaned_doc

    all_data.append(census_data)

    # Handle weather_data
    weather_excluded = ['_id','Station','Annual average temperature', 'State', 'City']
    for document in mongo.db.weather_data.find({"City":{"$regex":city.lower()}}):
        weather_data.append(document)

    for i, doc in enumerate(weather_data):
        cleaned_doc = cleanDocument(doc,weather_excluded,True)
        weather_data[i] = cleaned_doc

    all_data.append(weather_data)

    #Handle jobs_data
    jobs_excluded = ['_id',"__v"]
    for document in mongo.db.jobs_data.find({"Position_Location":{"$regex":city.lower()}}):
        jobs_data.append(document)

    for i,doc in enumerate(jobs_data):
        cleaned_doc = cleanDocument(doc,jobs_excluded,True)
        jobs_data[i] = cleaned_doc

    all_data.append(jobs_data)




    stops_excluded = ["stops"]
    #Handle stops_data
    for document in mongo.db.stops_data.find({}):
        stops_data.append(document)
    
    for i,doc in enumerate(stops_data):
        cleaned_doc = cleanDocument(doc,stops_excluded,False)
        stops_data[i] = cleaned_doc 
    
    all_data.append(stops_data)
    return all_data
    



#=============Global Variables=============
app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.8f9qd4d.mongodb.net/test?retryWrites=true&w=majority"
mongo=PyMongo(app)

logged_data = []
args = {}
debug=False
#==========Serving Functions================

@app.route('/')
def index():
    global logged_data
    logged_data = []
    return render_template("index.html",logged_data=logged_data,args=args)
    

@app.route('/data')
def data():
    global logged_data
    logged_data =[]
    if len(request.args) < 1:
        # Do normal homepage stuff
        logged_data.append("No url arguments passed")
        pass
    else:
        # Do stuff with url arguments
        logged_data.append("Url arguments passed")
        requested_city = request.args['city']
        pass

    all_data = packData(requested_city)
    addArg({"all_data":all_data})
    if not debug:
        logged_data = ""
    return render_template("data.html",logged_data=logged_data,args=args)


@app.route('/test')
def test():
    global logged_data
    logged_data = []
    jobs_packed = []
    jobs_cleaned = []
    for document in mongo.db.jobs_data.find({"PositionLocation":{"$regex":"[A,a]tlanta"}}):
        jobs_packed.append(document)
    
    
    #logged_data.append(jobs_packed['PositionLocation'])
    addArg({"jobs_packed":jobs_packed})
    #addArg({"census_packed":census})
    #addArg({"logged_data":logged_data})
    return render_template('test.html',debug=logged_data,args=args)

