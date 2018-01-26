"""
Twitch Message Interface Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the TMI (twitch message interface).
:copyright: (c) 2018 Carlos Fernandez
:license: MIT, see LICENSE for more details.
"""

__title__ = 'pytmi'
__author__ = 'Carlos Fernandez'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018 Carlos Fernandez'
__version__ = '0.0.1'


from .client import TwitchClient
from .message import Message
from .user import User, UserType