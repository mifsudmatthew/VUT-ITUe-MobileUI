Author: Matthew Mifsud , xmifsum00

Required Python Version: IMPORTANT Python 3.10.8 not newer.

Required packages:  pip install Kivy[full]
			  pip install KivyMD
			  pip install mapview
			  pip install kivy-garden

How to run program: 1. Make sure you are in the directory containing 'controller.py'.
                    2. Enter "python controller.py" in terminal or run controller.py in IDE.
                    3. Automatically the program will open and a mobile user interface is visible.

Content Distribution: 1. controller.py - This is the actual controller file, which bridges the view and the model.
			    2. model.py - This the model file, that is handling the backend.
			    3. controller.kv - This is the view, which displays the UI content. It is called controller only due to a Kivy naming convention.