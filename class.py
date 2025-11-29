from curses.ascii import EM


class SMSNotifire:
    def notify(self, msg):
        return f"SMS : {msg} send to contancts."


class EmailNotifire:
    def notify(self, msg):
        return f"Email : {msg} send to users."


class PushNotifire:
    def notify(self, msg):
        return f"Push : {msg} send to browswers."


class NotificationManager:
    def __init__(self, notifires=[]):
        self.notifires = notifires

    def send(self, msg):
        if not self.notifires:
            return False

        for notifire in self.notifires:
            print(notifire.notify(msg))


n1 = NotificationManager([SMSNotifire(), EmailNotifire(), PushNotifire()])
n1.send("Hello world")