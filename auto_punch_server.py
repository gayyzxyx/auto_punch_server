#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.web, time
tasks = []

def getTask():
    returnList = []
    for line in tasks:
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(line["trigger"])))
        returnList.append("%s\n%s\n%s\n%s" % (line["username"], line["password"], localtime, line["start"]))
    return returnList

def is_exist_task(username, password, trigger):
    for task in tasks:
        if task["username"] == username and task["password"] == password and task["trigger"] == trigger:
            return True
    return False

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print "get"
        if len(tasks) == 0:
            self.render("index.html",tasks = [])
        else:
            self.render("index.html", tasks = getTask())

    def post(self):
        print "post"
        username, password, trigger, start = self.get_argument("username"), self.get_argument("password"), time.mktime(time.strptime(self.get_argument("trigger"), '%Y-%m-%d %H:%M:%S')), self.get_argument("start")
        task = {}
        if username and password and trigger and not is_exist_task(username, password, trigger):
            task["username"], task["password"], task["trigger"], task["start"]  = username, password,  trigger, start
            tasks.append(task)
            self.render("index.html", tasks = getTask())
        else:
            self.write("error")



class task(tornado.web.RequestHandler):
    def get(self):
        print 'get'
        if len(tasks):
            returnTask = '{"username":"%s","password":"%s","trigger":"%s"}' % (tasks[0]["username"], tasks[0]["password"], tasks[0]["trigger"])
            self.write(returnTask)
            tasks.remove(tasks[0])
        else:
            self.write('')

    def post(self):
        print 'post'


application = tornado.web.Application([
    (r"/static/(.*\.(css|js|png|jpg|ico|gif))", tornado.web.StaticFileHandler, dict(path="static")),
    (r"/", MainHandler),
    (r'/task', task),
    (r'/user/add', MainHandler),
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
