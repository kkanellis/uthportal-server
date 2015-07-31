# UTHPortal - Server

19 December 2014 - ...

**Version**:  N/A Draft
**Last Updated** : 31 July 2015

## Developer Team
**Konstantinos Kanellis**  <<kkanelli@hotmail.com>>
*Electrical & Computer Engineer* undergraduate at *University of Thessaly*

**George T. Gougoudis** <<george_gougoudis@hotmail.com>>
*Electrical & Computer Engineer* undergraduate at *University of Thessaly*

## Project Goal
*UTHPortal* is a mobile application (powered by a web-service) which is targeted to *students* currently attending *University of Thessaly*. Its main goal is to provide **easy** and **direct** access to the necessary information and services a student might need in his everyday life, which are scattered around different web-locations. 

The list below summarizes some of the information:

 - **University**'s and **faculty**'s announcements, news, events
 - **Courses** information and announcements
 - **Curriculum** and **exam schedule**

In addition, each student is able to use the following services provided by the university:

 - **Webmail** (Horde mail client)
 - **e-Class** (course management system)
 - **euniversity** (grading system)

**UTHPortal**'s strives to deliver the information above, to each student using a *personalized* profile, which is set up by the student. In this document we describe the structural and operational details of the server-side component.

## Project Architecture

*UTHPortal-Server* is written in **Python 2.7+** language. It makes use of the following *open-source* frameworks/packages:

- **[Flask](http://flask.pocoo.org/)**: Lightweight web application framework
- **[pushd](http://github.com/rs/pushd)**: Universal Mobile Push Daemon
- **[APScheduler](https://pythonhosted.org/APScheduler/)**: Task/Job scheduling queue
- **[Pymongo](http://api.mongodb.org/python/current/)**: Python library to work with MongoDB
- **[gevent](http://www.gevent.org/)**: Coroutine-based networking library
- **[gunicorn](http://www.gunicorn.org/)**: Python WSGI HTTP Server for UNIX
- **[Requests](http://docs.python-requests.org/)**: HTTP library (used instead of the old *urllib2*)
-  **[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)**: Python library for web-scrapping & DOM parsing
- **[Universal Feed Parser](https://pythonhosted.org/feedparser/)**: Parser for RSS & Atom feeds
- ...

It consists of three main components:

1. **Starter** (currently located at *uth-portal.py*), which provides a way to configure & manage *UTHPortal-Server* at runtime using an interactive shell
2. **Scheduler**, which is responsible for keeping the information fresh, by polling to the web-sources needed
3. **Web-server**, which  provides the **RESTful** interface between the server-side and the client-side (**mobile application**)


### Component: Starter
*Starter* is used to fill the gap between the standalone *UthPortal* class and the user, who wishes to configure and manage this app at run time, performing simple yet important jobs (e.g. adding a new task in the queue, check the status of a running task, run a specific test etc). Currently performing all the above using the interactive shell is limited to local access, but in the future remote control will be added.

So, In order to launch *UTHPortal-Server* we must first execute *starter.py*. Starter will create an instance of *UthPortal* class, which contains the rest of the components. The steps that follow initialization are: loading the **configuration file** (or create one if it doesn't exist) and configure the *loggers* and the *database driver* used accordingly.

The *configuration file* contains fields that specify the following:

- Database daemon host and port - database name - user credentials 
- Logging files path - logging levels
- Task intervals - task authentication info - task update timeout
- Server host and port 
- Tasks location (*library_path*) - temp path 

When the necessary classes are initialized it is time to import the **tasks** and feed them to the *scheduler*.

### Component: Scheduler

Scheduler's goal is to make sure that *UTHPortal* is constantly up-to-date. It maintains a **queue** of tasks (powered by *APScheduler*) and supports all basic queue operations such as enqueuing, dequeuing and modifying a single task.

All tasks are stored in memory (since no persistence is required) and they are executed at specific time intervals (defined at *configuration file*). Queue itself is running in the background, currently using a single thread, but it is planned to be non-blocking and each task will be running in its own greenlet (using *gevent*).

### Tasks
The majority of information provided by *UTHPortal* require constant polling web-sources, so that we are sure that the data we keep are up-to-date. Because of the plethora of different web-sources used by the university and the different faculties, it is very common to extract content from different formats/locations, such as:

- Plain HTML websites
- RSS & ATOM feeds
- Emails (mailing lists)
- Documents (e.g. \*.doc or \*.xls)

For this purpose we use **tasks** and we define different type of tasks for different jobs. All tasks are located in the *tasks* folder and must inherit from the *BaseTask*. The existing tasks are listed below and are self-explanatory:

- **CourseTask**
- **AnnouncementTask** and **RssAnnouncementTask**
- **FoodMenuTask**

Each **task class** must declare two class fields: *update_fields* and *db_query* which are used to determine which fields in the document are subject to change and how query is formatted to distinguish different entries (or in other words which is the **unique key** for this task class). You can skip to *document_prototype* dictionary discussion below, to gain some more insight about these two.

In addition it must override *update* method (from the *BaseTask*) and provide the logic required. Although there might not be many similarities among the different tasks, the standard sequence of steps is the following:

- Fetch the content from the web
- Parse/Filter/Edit the content accordingly
- Compare the saved data (in the database) with the new data
- If they differ:
	- **move to history** the old - *saved*- data
	- **update** the database with the new data.
	- **notify** all users subscribed to this task

Along with each **task**, a dictionary *document_prototype* must be defined, which is the document saved in database if the task has never been executed before. It must contain basic info about the task (e.g. task name, link(s) of the polling web-source(s) etc). It is also necessary to specify a **unique key** for later database retrieval (e.g *code* for *CourseTask*, *type* for *AnnouncementTask* etc).

### Component: Web Server

**To be defined**

## Database Model

UTHPortal uses **[MongoDB](http://www.mongodb.org/)**, which is a *document-oriented database*. Thus, the database is organized with a plethora of *collections* each one containing a number of *documents*. Each document is saved in a format similar to *BSON*, with some extra support (e.g *datetime* objects). 

### Web Sources

The data gathered from the web, are classified according to their origin (web-sources) and there is an **one-to-one relation** between a collection and the according web-source. The majority of the collections follow the schema below:

	[prefix].[department].[info_type]

In the schema above, *info_type* may take the following values for each department:

- **announce**: announcements
	-  **announce.academic**: academic news
	- **announce.events**: department events
	- **announce.general**: general announcements
	- **announce.scholarships**: scholarships news
	- **announce.undergraduate**: announcements for undergraduates
- **courses**: department courses
	- **courses.*course_id***, which depends on the department
- **curriculum**: weekly course schedule (for undergraduates)
- **exams**: exam schedule (for undergraduates)

There is one exception for the schema above, for **uth** - which is the university - and has **no** *courses* collections. Although it contains the following collections besides *announce*:

- **foodmenu**: which is the food menu provided to students
- ...

**NOTE:** each of the sublist items, share the same *BSON* schema respectively (i.e. *announce.academic* & *announce.general*).
 
For example the collection that holds the course information from the *informatics* (inf) department for course *ce120* is named:

	[prefix].inf.courses

Notice that the prefix thing is still there. This is used to distinguish the purpose of these collections and can take the following values:

- **curr**: latest data/info available
- **hist**: history of all changes
- **push**: holds the *clients* who are subscribed to this web-source
- **web**: client-ready document to be served - data which are useless to client have been removed -

Note that the **curr** and **web** collections hold one document each ((??))

### Push notifications

**To be defined**

## Interfaces

The interfaces defined in UTHPortal are:

- **IDatabaseManager**: responsible for database operations
- **INoficationManager**: responsible for *client* (user) notification
- ...

### IDatabaseManager

**IDatabaseManager** is the databse interface . This interface along with its implementations is stored in *database.py* module.

When initializing an IDatabaseManager instance, it is necessary to provide a dictionary, named *info*, with the specific keys:

- **host**: string which contains the connection string
- **port**: integer which specifies the connection port
- **db_name**: string which specifies the database name
- **user** (optional)
- **password** (optional)

Required methods for IDatabaseManager are the following:

-  **connect**
- **disconnect**
- **insert_document**
- **remove_document**
- **find_document**
- **update_document**

The main implementation of this interface is the **MongoDatabaseManager**, which is used throughout the application. Although **MemoryDatabaseMemory** is also used mainly for testing purposes.

Because each implementation may require more arguments than the ones defined in the methods above, we provide a way to pass an arbitrary number of arguments (using \*args and \*\*kwargs).


### INotificationManager

**To be defined**
