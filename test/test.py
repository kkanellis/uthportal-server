from uthportal.database import *

def test_db():
    db = MongoDatabaseManager( port = "27017",host = "127.0.0.1" )
    if db.connect( ) :
        print ("Succes!")
        db.disconnect()
    else :
        print("Test failed!")



def main():
    test_db()


if __name__ == "__main__":
    main()




