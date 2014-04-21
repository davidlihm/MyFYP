__author__ = 'User'

import tornado.ioloop
import tornado.web
import tornado.template
import test_web
import database
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class EditorHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("editor.html")
    def post(self):
        #content = self.get_arguments()
        subject = self.get_argument('subject')
        payload = self.get_argument('payload')
        #print(content)
        prob, isHam, risk_set = test_web.doPost(subject, payload)
        print('dopost~')
        self.render("result.html",
                    subject=subject,
                    payload=payload,
                    prob=prob,
                    isHam=int(isHam),
                    risk_set = risk_set)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/editor", EditorHandler)

],static_path='./static')

if __name__ == "__main__":
    application.listen(8811)
    tornado.ioloop.IOLoop.instance().start()