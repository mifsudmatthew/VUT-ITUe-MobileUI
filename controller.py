from kivy.config import Config
Config.set('graphics', 'resizable', '0') # Turning off resizability of window, to lock in mobile view

from kivymd.app import MDApp

from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDTimePicker
from datetime import datetime

from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox

from kivy_garden.mapview import MapView

# Importing the model which retrieves data from the database
from model import Model
db = Model() # Creating a Model object to access database methods

# Reports simulating data that would be sent from the control centre, uncomment to add
# db.addReport("Marsa Accident", "", "", 35.8792, 14.4974)
# db.addReport("Sliema Accident", "", "", 35.9120, 14.5017)
# db.addReport("Valletta Accident", "", "", 35.8992, 14.5141)
# db.addReport("Hamrun Accident", "", "", 35.8912, 14.4938)
# db.addReport("Birgu Accident", "", "", 35.8881, 14.5221)
# db.addReport("Citadella Accident", "", "", 36.0465, 14.2398)
# db.addReport("Mdina Accident", "", "", 35.8864, 14.4031)
# db.addReport("Gzira Accident", "", "", 35.9049, 14.4937)
# db.addReport("St. Julians Accident", "", "", 35.9214, 14.4906)

from kivy.properties import BooleanProperty

from kivy.core.window import Window
Window.size = 450, 750 # Setting window size to a mobile resolution

# Creating a class for the dialog box that contains the location of each accident
class MapDialog(MDBoxLayout):
    
    def __init__(self, **kwargs): # Setting up the constructor
        
        super().__init__(**kwargs) # Inherting from super class
        
        # Creating a mapview widget with the corresponding longitude and latitude of the current ticked item
        mapview = MapView(zoom=19, lat=db.getLongitude(app.buttonID), lon=db.getLatitude(app.buttonID))

        self.add_widget(mapview) # Adding the created map to the dialog box

# Creating a class for the dialog box that contains the report details of each accident
class ReportDetailsDialog(MDBoxLayout):
    
    def __init__(self, **kwargs): # Setting up the constructor
        
        super().__init__(**kwargs) # Inherting from super class
        
        # Filling in labels of the dialog box with data from database
        self.ids.reportDetailsLabel.text = "Case/Report ID:   " + str(db.getReportID()) + "\n\nSpecifics:"
        self.ids.reportDetailsLabel2.text = str(db.getSelectedDetails())

# Creating a class for the dialog box that contains the number of pending reports
class ReportNumDialog(MDBoxLayout):
    
    def __init__(self, **kwargs): # Setting up the constructor
        
        super().__init__(**kwargs) # Inherting from super class
        
        self.ids.reportNumLabel.text = str(db.getTotalReports()) # Setting the label to display number of pending reports

# Creating a class for the dialog box that allows submission of report by the authority
class SubmitDialog(MDBoxLayout):
    
    # Initialising isEmpty flag to True so that initially the view details and submission button are disabled 
    isEmpty = BooleanProperty(True)
    
    def __init__(self, **kwargs): # Setting up the constructor
        
        super().__init__(**kwargs) # Inherting from super class
        
        self.ids.time_text.text = datetime.now().strftime("%H:%M") # Obtaining the current time and displaying it/

        self.ids.details_text.bind(text=self.onTyping) # Binding 'onTyping' function to the details text box.
        
    def showTimePicker(self): # Displaying the time picker
        
        timeDialog = MDTimePicker() # Creating a time picker
        timeDialog.bind(on_save = self.on_save) # Binding the save button to the time dialog
        timeDialog.open() # Displaying the picker itself
        
        # Updating dimensions of screen so that picker resizes
        Window.size = 451, 750
        Window.size = 450, 750
    
    def on_save(self, instance, value): # Function to execute when saving
        
        date = value.strftime("%H:%M") # Obtaining the current time
        self.ids.time_text.text = str(date) # Displaying the current time
    
    def onTyping(self, instance, value): # Function to execute when typing

        # Making sure textbox contains between 0 and 100 characters
        if len(self.ids.details_text.text) == 0 or len(self.ids.details_text.text.strip()) > 100:
            self.isEmpty = True # If not between 0 and 100, save button is disabled
        else:
            self.isEmpty = False # If it is between 0 and 100, save button is enabled

        
# Creating a class for the list of reports      
class ListItemWithCheckBox(TwoLineAvatarIconListItem):
    
    def __init__(self, primaryKey=None, **kwargs): # Setting up the constructor
        
        super().__init__(**kwargs) # Inherting from super class
        
        self.primaryKey = primaryKey # Obtaining the primary key of the item in list
    
    # Selecting the report in list
    def mark(self, check, reportEntry):
        
        if check.active == True: # If entry is currently selected
            
            reportEntry.text = '[i]' +  reportEntry.text + '[/i]' # Text is formatted in italics
            
            db.markSelected(reportEntry.primaryKey) # Report in list is marked as selected
            
            # Checking how many selected reports there are
            if(db.getNumSelectedReports()==1):
                app.isDisabled = False # Enabling submit and view details
            else:
                app.isDisabled = True # Disabling submit and view details buttons
                
        else:
            
            # Report in list is marked as unselected
            reportEntry.text = str(db.markUnselected(reportEntry.primaryKey))
            
            # Checking how many selected reports there are
            if(db.getNumSelectedReports()==1):
                app.isDisabled = False # Enabling submit and view details
            else:
                app.isDisabled = True # Disabling submit and view details buttons
    
    # Obtaining the primary key of the list item   
    def getID(self,reportEntry):

        app.buttonID = reportEntry.primaryKey # Storing key in app variable buttonID

# Creating a class for the checkboxes
class LeftCheckBox(ILeftBody, MDCheckbox):
    pass

# Main App Class
class ControllerApp(MDApp):
    
    isDisabled = BooleanProperty(True) # Creating a global flag to disabling and enabling buttons
    buttonID = 0 # Creating a global variable to store the ID of each entry in the list

    # Setting the theme
    def build(self):
        
        self.title = 'Report System by Matthew Mifsud' # Setting window title
        self.theme_cls.theme_style = "Dark" # Setting a dark theme
        self.theme_cls.primary_palette = ("Blue") # Setting a primary color
        
        # Checking how many selected reports there are
        if(db.getNumSelectedReports()==1):
            app.isDisabled = False # Enabling submit and view details buttons
        else:
            app.isDisabled = True # Disabling submit and view details buttons

    # Creating a function which will make the map dialog box appear
    def showMapDialog(self):
        
        # Creating a dialog box which runs the function MapDialog() created prior
        self.task_list_dialog = MDDialog(title = "Location", type="custom", content_cls = MapDialog())  
        
        # Opening dialog
        self.task_list_dialog.open()
        
    # Creating a function which will make the submit dialog box appear
    def showSubmitDialog(self):
        
        # Creating a dialog box which runs the function SubmitDialog() created prior
        self.task_list_dialog = MDDialog(title = "Submit report", type="custom", content_cls = SubmitDialog())  
        
        # Opening dialog
        self.task_list_dialog.open()
        
    # Creating a function which will make the pending reports dialog box appear    
    def showReportNumDialog(self):
        
        # Creating a dialog box which runs the function ReportNumDialog() created prior
        self.task_list_dialog = MDDialog(title = "Pending cases/reports", type="custom", content_cls= ReportNumDialog())  
        
        # Opening dialog
        self.task_list_dialog.open()
    
    
    # Creating a function which will make the report details dialog box appear     
    def showReportDetailsDialog(self):
        
        # Creating a dialog box which runs the function ReportNumDialog() created prior
        self.task_list_dialog = MDDialog(title = "Details", type="custom", content_cls= ReportDetailsDialog()) 
        
        # Opening dialog 
        self.task_list_dialog.open()
    
    # Creating a function which fills a report   
    def fillReport(self,task_details,task_time):
        
        reportID = db.getReportID() # Obtaining the report ID

        # Looping through all list children to find one report the matching primary key
        for child in self.root.ids['container'].children:
            
            # If report matches primary key
            if child.primaryKey == reportID:
                
                # Set the secondary_text of the report, with the time
                child.secondary_text =  "At: "+ task_time + " and filled"
                
        
        db.applyReport(db.getReportID(),task_details,"At: "+ task_time + " and filled") # Sending details to database
        
    # Creating a function which closes any dialog box    
    def closeDialog(self, *args):
        self.task_list_dialog.dismiss()
    
    # Creating to load report and display them in list
    def on_start(self):
        
        markedReports, unmarkedReports = db.getReports()  # Obtaining both marked and unmarked reports
        
        # Listing marked report first so that they appear at the top
        if(markedReports!=[]): # If list is not empty
            
            for report in markedReports: # Looping through every report
                
                # Creating a new list item (report)
                tempReport = ListItemWithCheckBox(primaryKey=report[0], text = "[i]" + report[1] + "[/i]", secondary_text = report[2])
                
                # Setting the check as active
                tempReport.ids.check.active = True
                
                # Display report in list
                self.root.ids.container.add_widget(tempReport)
        
        # Unmarked reports will appear below marked ones
        if(unmarkedReports!=[]):
            
            for report in unmarkedReports: # Looping through every report
                
                # Creating a new list item (report)
                tempReport = ListItemWithCheckBox(primaryKey=report[0], text=report[1], secondary_text = report[2])
                
                # Display report in list
                self.root.ids.container.add_widget(tempReport)
            
        
# Running the app
app = ControllerApp()
app.run()
