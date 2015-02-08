fields:

DatabaseManager, NotifierManager
tasks
settings

server_thread

functions:

__init__: Call function to read configuration files. Call functions to create tree from tasks. Instantiate the databasemanager, notifiermanager, scheduler.

read_settings()

create_task_tree(tasks_dir)

start_server()

stop_server()

restart()
