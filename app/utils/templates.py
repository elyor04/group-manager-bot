admin_template = """
📣 <b>Message has been sent to the group admins</b> 📣

👥 <b>Group</b>: <a href="https://t.me/c/{0}">{1}</a>
👱 <b>User</b>: <a href="tg://user?id={2}">{3}</a>
🔗 <b>Message link</b>: <a href="https://t.me/c/{0}/{4}">here</a>

💬 <b>Message</b> 💬

{5}
"""

info_template = """
🆔 <b>ID</b>: <code>{0}</code>
👱 <b>Name</b>: <a href="tg://user?id={0}">{1}</a>
🌐 <b>Username</b>: {2}
👀 <b>Status</b>: {3}
💬 <b>Messages</b>: {4}
❕ <b>Warns</b>: {5}/5
🔇 <b>Muted</b>: {6}
🚷 <b>Banned</b>: {7}
📅 <b>Joined</b>: {8}
"""

welcome_template = """\
Hello <a href="tg://user?id={0}">{1}</a>, \
welcome to <a href="https://t.me/c/{2}">{3}</a>\
"""
