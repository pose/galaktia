# Introduction #

This document describes the current structure based on the ClientArchitectureSketch wiki page, as well as the roles of each file and script. It does not, however, describe the innards of each one. Refer to the corresponding Wiki page for detailed information.


# Files #

As Galaktia Client 0.2 is a web application running HTML5, the delivery package is just an HTML file that serves as the main canvas for javascript files. All the logic is located in the aforementioned scripts.

The files are hosted by a WebServer (which may not be in the same host as the GameServer), and the structure is as follows:

| **Script Name** | **short description** | **svn path** | **webserver path** |
|:----------------|:----------------------|:-------------|:-------------------|
| Main | Main script, initializes logging and main objects | galaktia/trunk/galaktia/web/assets/js/main.js |  |
| Client | Contains the WebSocket and codec | galaktia/trunk/galaktia/web/assets/js/client.js |  |
| Dispatcher | Dispatches the events to controllers | galaktia/trunk/galaktia/web/assets/js/dispatcher.js |  |
| Controler | Controller stub | galaktia/trunk/galaktia/web/assets/js/controller.js |  |
| UI | Registers event handlers to UI, like key-press events | galaktia/trunk/galaktia/web/assets/js/ui.js |  |
| View | Canvas renderer | galaktia/trunk/galaktia/web/assets/js/view.js |  |


## Scripts ##

Javascript scripts use not-yet-standard technologies and may not work other than in Google Chrome. WebSockets in Firefox are expected to be ready for 3.7.


### Main ###
This is the main framework that coordinates and holds the client together. It has to:
  * Validate Mootools;
  * Register the setup in the domready event;
  * Create the main object files;
  * Set up logging.

### Client ###
This script mirrors the server counterpart. It's responsible of
  * Managing the WebSocket that binds to the server;
  * Holding the codec that serializes the messages;
  * Setting up a handler that calls the dispatch controller.

### Dispatcher ###
The dispatcher reacts to events from Client and calls the corresponding controller, which has to process it. This is currently done with a hash that maps a message name to a controller, so if you want to add new controllers you should edit the hash.

### UI ###
This script registers the event handlers in the UI (HTML5 DOM) as callbacks to other components such as View or Client. It also has convenience functions to show some dialog screens (alert, confirm, prompt). Event handlers are triggered by keys E, S, M, H, X (related to the names of the corresponding messages).
Currently, it provides a way to send messages (via the Client script) using the prompt.

### View ###
Renders the map and other graphical objects to the canvas object in the host HTML file. It currently draws simple tiles and a sprite in isometric projection given the coordinates of the object. The lack of a DAO to store and retrieve data about the scene may hamper the development of complex scene managers.