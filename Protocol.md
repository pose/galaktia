# Introduction #

Overview of every type of message in the game protocol, describing its parameters and use.
This based on the source code and [this](http://www.rolear.com.ar/foro/viewtopic.php?f=4&t=92) forum post.

**Update**: Brought up to date to [revision 121](https://code.google.com/p/galaktia/source/detail?r=121).

Optional parameters are marked with italic. I've made some additional comments also in italics, but maybe this is not the place.

# Messages #

## Action ##
**Source**: http://code.google.com/p/galaktia/source/browse/trunk/galaktia/galaktia/server/protocol/operations/action.py

The action messages are an abstract type used as base for user in-game actions. These are only meant to be extended onto new types, and not be used directly.

### ActionRequest ###
Client-side message, sent to server to inform of an user action.

**Parameters**:
  * subject - The id or username of the user perfoming the action. _Right now this is set to session\_id, which is sent already in every message, so its kinda redundant and could be removed to avoid data duplication._
  * action -  An action identifier. _This isnt being currently used, maybe it should be removed, and can be obtained from the already sent message type._
  * _object_ - Either the position of the object that the action is done upon or the id said object.

### ActionResponse ###
Server-side response to an ActionCommand message. Informs the client that the action was authorized by the server.

### ActionUpdate ###
Server-side message to inform players of another player's action, in their Line of Sight. This is sent after the corresponding ActionResponse message was sent. It's an exact replica of the matching ActionRequest.

**Parameters**:
  * subject - The id or username of the user perfoming the action.
  * action - An action identifier.
  * _object_ - Either the position of the object that the action is done upon or the id said object.


## Talk ##
**Source**: http://code.google.com/p/galaktia/source/browse/trunk/galaktia/galaktia/server/protocol/operations/talk.py

These are the in-game chat messages. They implement the Action types, but not completly.
_I'm not sure whether this should be a subset of Action, since it seems kinda wierd to implement it halfway through_

### SayThis (ActionRequest) ###
Client-side message sent to let the server know the player said something on chat. This cand either be a whisper or global chat message.

**Parameters**:
  * _whisper`_`to_ (int) or (string): The id or username of the user being whispered. Maps to ActionUpdate object. _Since I'm not sure the client will know the id's of other users, the option to send the username is available_

### SomeoneSaid (ActionUpdate) ###
Server-side message to inform other clients of a SayThis message.

**Parameters**:
  * username (string): The username of the user that sent the chat message. Maps to ActionUpdate subject.
  * message (string): The message being sent. Maps to ActionUpdate action.

## Move ##
**Source**: http://code.google.com/p/galaktia/source/browse/trunk/galaktia/galaktia/server/protocol/operations/move.py

These are the movement messages. They are of course a subset of Action.

### MoveDxDy (ActionRequest) ###
Client-side message sent when a player moves to a new position.

**Parameters**:
  * delta tuple(int, int): The relative movement of the player in the map as a tuple(x, y). Maps to ActionRequest action.

### PlayerMoved (ActionUpdate) ###
Served-side response to MoveDxDy. Informs players that are able to see the player that moved it's new position.

**Parameters**:
  * session\_id (int): The session id of the player that moved. Maps to ActionUpdate subject.
  * position tuple(int, int): The new player's position as tuple(x, y). Maps to ActionUpdate object.
  * delta tuple(int, int): The player's relative movement as tuple(x, y). Maps to ActionUpdate action.

### PlayerEnteredLOS (ActionUpdate) ###
Server-side message sent to inform a player that another player entered it's Line Of Sight.

**Parameters**:
  * session\_id (int): The session id of the player that moved. Maps to ActionUpdate subject.
  * position tuple(int, int): The position where the new player is. Maps to ActionUpdate object.
  * description : This is undefined as of now. It's supposed to carry info about the player that enters the LOS, but it still not defined how.

## Join ##
**Source**: http://code.google.com/p/galaktia/source/browse/trunk/galaktia/galaktia/server/protocol/operations/join.py

Series of messages sent in the login process.

### StartConnection ###
Client-side message sent to begin the login process.

### CheckProtocolVersion ###
Server-side response to StartConnection. Sent to check the client is up to date.

**Parameters**:
  * version (string): The current client version that server is working with.
  * url (string): An url pointing to the latest client version, in case the client is old.

### RequestUserJoin ###
Client-side message sent once the version is validated. This is the actual login message.

**Parameters**:
  * username (string): The name of the user loggin in.

### UserAccepted ###
Server-side response to RequestUserJoin, signaling that the user was accepted or rejected. When accepted, it also carries extra information about the session. _I have the feeling that this should be two different messages, one for accept, another for reject._

**Parameters**:
  * accepted (bool): Whether the player was accepted (true) or rejected (false).
  * _username_ (string): The player's username, only senf if it was accepted.
  * _session`_`id_ (int): The player's corresponding session id, only sent if it was accepted.
  * _player`_`initial`_`state_ : This has to be defined, but right now its a tuple(int, int) with the player's position in the map.

### UserJoined ###
Server-side annoucement, informing that a player logged in. This is, obviously, sent to all players.

**Parameters**:
  * username (string): The name of the user that logged in.

## Exit ##
**Source**: http://code.google.com/p/galaktia/source/browse/trunk/galaktia/galaktia/server/protocol/operations/exit.py

These are the logout messages. These implement Action, to some degree.

### LogoutRequest (ActionRequest) ###
Client-side message informing that player is logging out.

This seems to have no paremeters, but it's not the definitive version yet.

### LogoutResponse (Message) ###
Server-side response confirming the logout to the client.

_Shouldnt this implement AcionResponse?_

### UserExited (ActionUpdate) ###
Server-side annoucement, informing that player logged out.

**Parameters**:
  * username (string): The name of the user that logged out. This maps to ActionUpdate object.
  * session\_id (integer): The session id of the user that logged out. This maps to ActionUpdate subject.





