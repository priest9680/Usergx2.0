import functools
from userge import userge, Filters
from userge.db import Database

WELCOME_TABLE = Database.create_table("welcome")
LEFT_TABLE = Database.create_table("left")

WELCOME_LIST = WELCOME_TABLE.find_all({'on': True}, {'_id': 1})
LEFT_LIST = LEFT_TABLE.find_all({'on': True}, {'_id': 1})

WELCOME_CHATS = Filters.chat([])
LEFT_CHATS = Filters.chat([])

for i in WELCOME_LIST:
    WELCOME_CHATS.add(i.get('_id'))

for i in LEFT_LIST:
    LEFT_CHATS.add(i.get('_id'))


def raw_set(name, table, chats):
    def decorator(func):

        @functools.wraps(func)
        async def wrapper(_, message):

            if message.chat.type in ["private", "bot", "channel"]:
                await message.edit(f'Are you high XO\nSet {name} in a group chat')
                return

            string = message.matches[0].group(1)

            if string is None:
                await message.edit(f"wrong syntax\n`.set{name.lower()} <{name.lower()} message>`")

            else:
                new_entry = {'_id': message.chat.id, 'data': string, 'on': True}

                if table.find_one('_id', message.chat.id):
                    table.update_one({'_id': message.chat.id}, new_entry)

                else:
                    table.insert_one(new_entry)

                chats.add(message.chat.id)
                await message.edit(f"{name} message has been set for the \n`{message.chat.title}`")

        return wrapper

    return decorator


def raw_no(name, table, chats):
    def decorator(func):

        @functools.wraps(func)
        async def wrapper(_, message):

            try:
                chats.remove(message.chat.id)

            except KeyError:
                await message.edit(f"First Set {name} Message!")

            else:
                table.update_one({'_id': message.chat.id}, {'on': False})
                await message.edit(f"{name} Disabled Successfully !")

        return wrapper

    return decorator


def raw_do(name, table, chats):
    def decorator(func):

        @functools.wraps(func)
        async def wrapper(_, message):

            if table.find_one('_id', message.chat.id):
                chats.add(message.chat.id)
                table.update_one({'_id': message.chat.id}, {'on': True})

                await message.edit(f'I will {name} new members XD')

            else:
                await message.edit(f'Please set the {name} message with `.set{name.lower()}`')

        return wrapper

    return decorator


def raw_say(table):
    def decorator(func):

        @functools.wraps(func)
        async def wrapper(_, message):
            message_str = table.find_one('_id', message.chat.id)['data']

            user = message.from_user
            fname = user.first_name if user.first_name else ''
            lname = user.last_name if user.last_name else ''
            fullname = fname + ' ' + lname
            username = user.username if user.username else ''

            kwargs = {
                'fname': fname,
                'lname': lname,
                'fullname': fullname,
                'uname': username,
                'chat': message.chat.title if message.chat.title else "this group",
                'mention': f'<a href="tg://user?id={user.id}">{username or fullname or "user"}</a>',
            }

            await message.reply(message_str.format(**kwargs))

        return wrapper

    return decorator


def raw_ls(name, table):
    def decorator(func):

        @functools.wraps(func)
        async def wrapper(_, message):
            liststr = ""
            list_ = table.find_all({'on': True}, {'_id': 1, 'data': 1})

            for j in list_:
                liststr += f"**{(await userge.get_chat(j.get('_id'))).title}**\n"
                liststr += f"`{j.get('data')}`\n\n"

            await message.edit(liststr or f'`NO {name.upper()}S STARTED`')

        return wrapper

    return decorator


@userge.on_cmd("setwelcome", about="Creates a welcome message in current chat :)")
@raw_set('Welcome', WELCOME_TABLE, WELCOME_CHATS)
def setwel(): pass


@userge.on_cmd("setleft", about="Creates a left message in current chat :)")
@raw_set('Left', LEFT_TABLE, LEFT_CHATS)
def setleft(): pass


@userge.on_cmd("nowelcome", about="Disables welcome message in the current chat :)")
@raw_no('Welcome', WELCOME_TABLE, WELCOME_CHATS)
def nowel(): pass


@userge.on_cmd("noleft", about="Disables left message in the current chat :)")
@raw_no('Left', LEFT_TABLE, LEFT_CHATS)
def noleft(): pass


@userge.on_cmd("dowelcome", about="Turns on welcome message in the current chat :)")
@raw_do('Welcome', WELCOME_TABLE, WELCOME_CHATS)
def dowel(): pass


@userge.on_cmd("doleft", about="Turns on left message in the current chat :)")
@raw_do('Left', LEFT_TABLE, LEFT_CHATS)
def doleft(): pass


@userge.on_cmd("listwelcome", about="Shows the activated chats for welcome")
@raw_ls('Welcome', WELCOME_TABLE)
def lswel(): pass


@userge.on_cmd("listleft", about="Shows the activated chats for left")
@raw_ls('Left', LEFT_TABLE)
def lsleft(): pass


@userge.on_new_member(WELCOME_CHATS)
@raw_say(WELCOME_TABLE)
def saywel(): pass


@userge.on_left_member(LEFT_CHATS)
@raw_say(LEFT_TABLE)
def sayleft(): pass