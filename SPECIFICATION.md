# UTHPortal - Server

19 December 2014 - ...

**Version**:  N/A
**Last Updated** : 23 Dec 2014

## Developer Team
**Konstantinos Kanellis**  <<kkanelli@hotmail.com>>
*Electrical & Computer Engineering* undergraduate at *University of Thessaly*

**George T. Gougoudis** << ... >>
*Electrical & Computer Engineering* undergraduate at *University of Thessaly*

## Project Goal
**UTHPortal** is a web-application which is targeted to the *students* currently attending at **University of Thessaly**. It's main goal is to provide easy and direct access to the necessary information and services each student needs in order to be informed about the following:

 - **University**'s and **faculty**'s announcements, news, events & misc informations.
 - **Courses** informations and announcements

In addition, each student can use the following services provided by the university:

 - **Webmail** (Horde mail client)
 - **e-Class** (course management system)
 - Virtual Private Connection (VPN)

**UTHPortal**'s strives to deliver the information above, to each student using a *personalized* profile, which is set up by the student.

## Project Architecture

UTHPortal is written in **Python 2.7+** language. It makes use of the following frameworks/packages:

- **[Flask](http://flask.pocoo.org/)**: Lightweight web application framework
- **[PyMongo](http://api.mongodb.org/python/current/)**: Python library to work with MongoDB
- **[gevent](http://www.gevent.org/)**: Coroutine-based networking library
- **[gunicorn](http://www.gunicorn.org/)**: Python WSGI HTTP Server for UNIX
- **[Requests](http://docs.python-requests.org/)**: HTTP library (used instead of the old *urllib2*)
-  **[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)**: Python library for web-scrapping & DOM parsing
- **[Universal Feed Parser](https://pythonhosted.org/feedparser/)**: Feed parser for RSS & Atom feeds
- **[APScheduler](https://pythonhosted.org/APScheduler/)**: Task/Job scheduling queue
- ...

It consists of three main components:

1. **Gatherer** which is responsible for fetching, filtering and saving data *scrapped* from specific web sources.
2. **Webserver** which provides the **RESTful** interface between the server-side and the client-side (**mobile application**). 
3. **Notifier** which is responsible for **sending push notifications** to the client when *new* data is available, in order to inform the student.

### Structure/Template

The basic project template is designated below. **Note** that it may be subject to often and important changes.

- **data** (contains all data needed for initialization & crosschecking)
- **library** (main modules used)
- **server** (modules for web-server component)
- configure.py (configuration module)
- database.py (database interface & implementation)
- gatherer.py (component)
- start.py (initialize and start  gatherer)
- tasks.py (tasks interfaces & implementations)

**NOTE**: Folders are noted with **bold**.

### Component: Gatherer

#### Overview
Gatherer's job is to make sure that UTHPortal is constantly up-to-date. This is made possible with constant polling to web sources, where the info is located. The majority of the web sources supported are:

- Plain HTML websites
- RSS & ATOM feeds
- Emails (mailing lists)
- Documents (e.g. \*.doc or \*.xls)

Starting the gatherer requires some input known beforehand which is defined in a configuration file:

- A list of web sources info (uri, type, update interval).
- Database connection host, port & credentials.
- Logging configuration file (and? unused loggers)
- Web sources related info (number of parallel connections, polling tries & polling timeout)

By the time gatherer is fired up, it checks the integrity of the database by crosschecking the web source input with the database entries. Then the *task queue* is initialized and all the related tasks are configured and added to the queue. Using this technique all tasks are organized. Finally  the *update* procedure takes place, where all tasks (each one with its own pace) are asynchronously polling the according web sources.

While the *task-queue* is running, it is possible to give commands using a *command-prompt* in order to perform specific tasks like: **start, stop, update-all, refresh** and **exit**. The exact behavior of the commands above, is explained in details in the segment below. 

#### Implementation

Gatherer is a **class** which is initialized in *start.py* module. Gatherer defines a *task-queue scheduler* using **APScheduler**. It is running in the background (using **gevent**) and all the tasks are stored in memory. Then, all tasks are created using appropriate classes from tasks.py using the list of web sources:

- Each list entry has a dictionary with the following entries:
	- **URI**: Unique database path (where info are stored)
	- **Type**: Type of task (to initialize the proper class)
	- **Interval**: Time in secs

When a task is created, all info stored in database are loaded in RAM into a dictionary. Then using a unique id, which depends on the task, the necessary methods of the task (e.g *parse*) are set using methods originated from library folder. Finally the newly created tasks are enqueued to the queue. 

## Control  Flow

- Fetch the data from the web
- Parse/filter/edit the data accordingly
- Compare the saved data with the new data
	- IF they differ **notify** all clients subscribed, **move to history** the old - *saved*- data and **update** the database with the new data.


## Database Model

## Interfaces 


