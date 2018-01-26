.. pytmi documentation master file, created by
   sphinx-quickstart on Tue Jan 23 20:50:46 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pytmi's documentation!
=================================

PyTMI is a python library for communicating in the Twitch Messaging Interface (`docs <https://dev.twitch.tv/docs/v5/guides/irc/>`_).

This library supports core communication via the :class:`pytmi.TwitchClient` class,
and bot command parsing via the :class:`pytmi.bot.TwitchBot` subclass.
Understanding `asyncio <https://docs.python.org/3/library/asyncio.html>`_ is crucial to using
this library, as bot events and commands are implemented as coroutines. This allows concurrency without
the need for multiple threads.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   core
   bot

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
