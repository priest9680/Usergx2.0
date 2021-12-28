# pylint: disable=missing-module-docstring
#
# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.


class StopConversation(Exception):
    """Raise if conversation has terminated"""


class ProcessCanceled(Exception):
    """Raise if thread has terminated"""


class UsergeBotNotFound(Exception):
    """Raise if userge bot not found"""
