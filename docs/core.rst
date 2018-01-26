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

Events can be listened to by either registering them via :meth:`TwitchClient.event`, or by subclassing
:class:`TwitchClient` and overriding the event.

All events must be coroutines.

TODO: WRITE

Data Structures
----------------

Message
~~~~~~~

.. autoclass:: Message
    :members:

User
~~~~~~
.. autoclass:: User
    :members: