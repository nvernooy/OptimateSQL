# Optimate
JSON data structure in a Pyramid server read by an AngularJS client.

Current instructions:
  Ensure you have the neccesary modules installed.
  The project uses Pyramid, ZODB, AngularJS, AngularTreeview, among others

  Install the server dependances by runnning 
	$ python setup.py develop
  in the optimate directory.

  Install the client dependancies by running 
	$ npm install
  in the client directory.
	
  To start the server:
    In the optimate directory run 
                                  $ pserve development.ini --reload
  To start the client:
    In the client directory open index.html
    
  Visit http://localhost:8000/app/index.html to see the JSON data displayed.
  Click on the label of an item to see it's children.
