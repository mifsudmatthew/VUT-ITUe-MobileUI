import sqlite3

class Model:
    
    def __init__(self): # Setting a constructor which makes a connection to the database

        # Making a connection
        self.con = sqlite3.connect("reportsDatabase.db")
        
        # Creating an instance of cursor to use SQLite statements
        self.cursor = self.con.cursor()
        
        # Creating a reports table
        self.createReportsTable()
         
    # Creating a function which creates a reports table
    def createReportsTable(self):
        
        # Creating the table itself and setting the attributes
        self.cursor.execute("CREATE TABLE IF NOT EXISTS reports (id integer PRIMARY KEY AUTOINCREMENT, report varchar(50) NOT NULL, time varchar(50), details varchar(100), marked BOOLEAN NOT NULL CHECK (marked IN (0,1)), longitude REAL, latitude REAL)")
        
        # Committing result to database
        self.con.commit()
        
    # Creating a function which adds a report
    def addReport(self, report, time=None, details=None, longitude=None, latitude=None):
        
        # Adding parameters as a new record into the table
        self.cursor.execute("INSERT INTO reports(report, time, details, marked, longitude, latitude) VALUES(?,?,?,?,?,?)", (report, time, details, 0, longitude, latitude))
        
        # Committing result to database
        self.con.commit()


    # Creating a function to get all the marked and unmarked reports
    def getReports(self):
        
        # Getting all entries which are unchecked
        unmarked_reports = self.cursor.execute("SELECT id, report, time, details, longitude, latitude FROM reports WHERE marked = 0").fetchall()
        
        # Getting all entries which are unchecked
        marked_reports = self.cursor.execute("SELECT id, report, time, details, longitude, latitude FROM reports WHERE marked = 1").fetchall()
        
        return marked_reports, unmarked_reports # Returning the result
    
    # Creating a function to mark a report as selected
    def markSelected(self, reportid):

        # Updating attribute to set as selected
        self.cursor.execute("UPDATE reports SET marked = 1 WHERE id = ? ", (reportid,))
        
        # Committing result to database
        self.con.commit()
        
    # Creating a function to mark a report as unselected
    def markUnselected(self, reportid):

        # Updating attribute to set as unselected
        self.cursor.execute("UPDATE reports SET marked = 0 WHERE id = ? ", (reportid,))
        
        # Committing result to database
        self.con.commit()
        
        # Returning report title
        task_text = self.cursor.execute("SELECT report FROM reports WHERE id = ?", (reportid,)).fetchall()
        return task_text[0][0]

    # Creating a function to obtain the number of selected reports in the table
    def getNumSelectedReports(self):
        
        # Obtaining all results which are selected
        selectedReports = self.cursor.execute("SELECT COUNT(*) FROM reports WHERE marked = 1").fetchone()

        # Returning number of selected reports
        return selectedReports[0]
    
    # Creating a function to obtain the number of pending reports
    def getTotalReports(self):
        
        # Obtaning the amount of report in table
        totalReports = self.cursor.execute("SELECT COUNT(*) FROM reports").fetchone()

        # Returning the total number of reports
        return totalReports[0]
    
    # Creating a function to get the ID of the only selected task
    def getReportID(self):
        
        # Obtaining all reports which are selected
        reports = self.cursor.execute("SELECT id FROM reports WHERE marked = 1").fetchall()

        # Checking if there is only one report obtained
        if (len(reports) == 1):
            
            # If so the primary key of the report is returned
            return reports[0][0]
        

    # Creating a function to get the details of the only selected report    
    def getSelectedDetails(self):
        
        # Obtaining all reports' details which are selected
        reports = self.cursor.execute("SELECT details FROM reports WHERE marked = 1").fetchall()

        # Checking if there is only one report obtained
        if (len(reports) == 1):
            
            # If so the details of the report are returned
            return reports[0][0]

    # Creating a function to return the latitude based on a report id
    def getLatitude(self, reportid):

        # Obtaining the latitude of a report matching the primary key in the parameter
        latitude = self.cursor.execute("SELECT latitude FROM reports WHERE id = ?", (reportid,)).fetchone()

        return latitude[0]

    # Creating a function to return the longitude based on a report id
    def getLongitude(self, reportid):

        # Obtaining the longitude of a report matching the primary key in the parameter
        longitude = self.cursor.execute("SELECT longitude FROM reports WHERE id = ?", (reportid,)).fetchone()

        return longitude[0]

    # Creating a function to apply report details 
    def applyReport(self, reportid, new_details=None, new_time=None):
        
        updateReport = "UPDATE reports SET details = COALESCE(?, details), time = COALESCE(?, time) WHERE id = ?"

        # Updating the entry with the matching id to 'updateReport'
        self.cursor.execute(updateReport, (new_details, new_time, reportid))
        
        # Committing result to database
        self.con.commit()

