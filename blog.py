import datetime
import database
import uuid


class Blog():
    def __init__(self, author, title, image, body, date=datetime.datetime.now(), post_id=uuid.uuid4().hex):
        self.postid = post_id
        self.author = author
        self.title = title
        self.body = body
        self.create_date = date
        self.image = image

    def create_blog(self):
        database.create_table()
        database.insert_into_blog_table(self.postid, self.title, self.author, self.image, self.create_date, self.body)
        return True

    @staticmethod
    def get_all_blogs():
        return database.get_blog()

    @staticmethod
    def get_a_post(data):
        xp=database.get_blog()
        for i in xp:
            if i[3]==data:
                return i



# Blog.get_a_post()


