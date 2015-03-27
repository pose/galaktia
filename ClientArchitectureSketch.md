# Introduction #

For Galaktia 0.2 (and further versions), it is critical that we have a good, reliable architecture of the client. This page summarizes some ideas and guidelines for the implementation of the client.


# Window Handlers #

Client representation on screen as a window is provided through the use of Window Handlers (handlers from now on). Some classes that will be implemented as handlers following:
  * **Login**: Show a simple form to log in with the user account
  * **SpecialHandler**: From here we'll inherit to make up a Options screens, Select world, server, character creation, etcetera.
  * **GameHandler**: The most important one, were all the game will take place.


# ResourceManager #

This object will be in charge of loading resources and give them to other objects so they are ready to be used on demand. This should be a singleton.

To get a image, the sintax will be something like "resources\_manager.getImage('world.tiles.workshoptile2')" or "resources\_manager.getAnimation('humans.male.dressed.suit.walking'). The string should be a path, like importing python modules. **TODO**: review this, there should be a better way or more elegant solution. This screams METADATA.

Some ideas on resources organization: (TODO: translate from spanish)
  * Imágenes de escenario
    * Criaturas (Un subgrupo muy importante)
      * Personajes
      * Monstruos
  * Imágenes de inventario
    * Imágenes de diálogos, boxes, botones, etc
  * Sonidos
    * Del juego
    * Del programa (meta-game)


# ConfigurationManager #
Loads information about the game, the user configuration, and other things.

This should create a instance of ResourcesManager.

Important things this object should cover:
  * Servers
  * Screen resolution
  * Images and sounds that each class should take from ResourcesManager
  * Remember password (?)

**Do not work extensively on this one: wait for investigation on some API**

# GameHandler #
This is the most important handler. Is the active handler when in game mode.

GameHandler is in charge of taking messages from the server and communicate with the Widgets (just resends the messages to them).

User interaction: takes messages from the user, also through Widgets. The changes can alter things locally or remotely (in this case, it has to communicate with the server).


# Widgets #
Everything that can interact with the user, showing him information and taking instructions from him.

You can think about Widgets as "sub-handlers", but it's not a handler because it can be the case that a lot of widgets need to reacto to a certain message, so there are a lot of active handlers (that can not be the case with window handlers). There may be a order relation between them ('this is the most active widget') so for example, when the user press ESC, the widget 'active on front' gets closed.

Example of two widgets needing to handle the same message: map/radar and position system.

Scenario is the most important widget. It represents the game view.

Other Widgets:
  * Dialog Boxes
  * Chat
    * It would be nice if one can also throw commands via text.
  * User information
  * Map
  * Item container (backpack)
    * Subcontainers?
  * Etc.


# Scenario #
The basic idea is: what the user sees at all times is a 'Scenario', with objects and actors. Objects are motionless things: objects on the floor or dead bodies, and actors are things that can move: creatures (characters, monsters, NPCs), ships, and others.

Separately, we handle the tiles.

  * Actors:
    * Creatures:
      * Characters
        * Own Char! <---- Too low in the class tree.
        * NPCs
        * Monsters
      * Naves
      * Intelligent objects
  * Objects:
    * Architectural objects:
      * Walls
      * Doors
      * Furniture
    * Fallen objects:
      * money, weapons, clothes, your wallet (?)
  * Tiles


# Web/AccountManager Interface #
Create/Modify accounts. You should be able to do these things where you choose: via web or via client.
  * Create account
  * Create character
    * Choose race, profession, starting skills?