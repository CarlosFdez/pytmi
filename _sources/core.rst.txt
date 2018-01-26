.. currentmodule:: pytmi

Core API Reference
==================

This section outlines the core classes of pytmi.

TwitchClient
-------------

.. autoclass:: TwitchClient
    :members:

Event Reference
---------------

This is a list of all possible events that can be propogated by :class:`TwitchClient`.

Events can be listened to by either registering them via the 
:meth:`TwitchClient.event` decorator, or by subclassing
:class:`TwitchClient` and overriding the event.

All events must be coroutines.

.. function:: on_ping()

    Triggered when the client receives a ping from the server.
    The library already handles sending `PONG` back to the server internally.

.. function:: on_raw_message(raw_message)

    Triggered when the client retrieves *any* message from the server,
    but before it is parsed. 
    This includes such messages such as `PING` or `PRIVMSG`.

    :param raw_message: A :class:`str` containing the raw message.

.. function:: on_message(message)

    Triggered when the client receives a chat channel message from a user.

    :param message: A :class:`Message` representing the received message.


Data Structures
----------------

The following classes have minimal behavior on their own,
and are used to encapsulate data supplied by the :class:`TwitchClient`.

Message
~~~~~~~

.. autoclass:: Message()
    :members:

User
~~~~~~
.. autoclass:: UserType
    :members:

.. autoclass:: User()
    :members: