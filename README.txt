# Optimate
JSON data structure in a Pyramid server read by an AngularJS client.

Current instructions:
  Ensure you have the neccesary modules installed.
  The project uses Pyramid, ZODB and AngularJS.
  AngularTreeview and NgModal modules are in the client/js folder
  If you have not, run
	$VENV/bin/easy_install docutils pyramid_tm pyramid_zodbconn pyramid_debugtoolbar nose coverage
  in your virtual environment.
  You need to have Node installed on your system to run the client dependancies.
	You can get the installer from http://nodejs.org/download/

  Install the server dependances by runnning 
	$ python setup.py develop
  in the optimate directory.

  Install the tool dependancies by running 
	$ npm install
  in the client directory.
  Add the client dependancies by running 
	$ bower install
  in the client directory
	
  To start the server:
    In the optimate directory run 
        $ pserve development.ini --reload
  To start the client:
    In the client directory open index.html
  To run the server tests, in the server directory:
	nosetests
    
  Visit http://localhost:8000/app/index.html to see the JSON data displayed.
  Click on the label of an item to see it's children.
