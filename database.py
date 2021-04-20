from sqlite3 import connect

connection = connect('user.db', check_same_thread=False)
curs = connection.cursor()
CREATE_USERS_TABLE = """Create table if not Exists Users
                    (id Integer primary key,
                    first_name Text,
                    last_name Text,
                    email Text,
                    password Text,
                    country Text,
                    State_Province Text,
                    _id Integer,
                    date Date,
                    image_tag Text,
                    CONSTRAINT email_unique UNIQUE(email)
                    );"""

CREATE_BLOG_TABLE = """Create table if not Exists Blog
                    (id Integer primary key, 
                    blog_id int,
                    author Text, 
                    title Text,
                    content Text, 
                    create_date Date,
                    blog_image_tag Text);"""

CREATE_USER = """INSERT INTO Users(first_name,last_name,email,password,country,State_Province,_id, date, 
image_tag) Values(?,?,?, ?,?,?,?, ?,?); """

CREATE_BLOG = """INSERT INTO Blog(blog_id, author, title,content,create_date, blog_image_tag) Values (?,?,?,?,?,?);"""

CHECK_USER = """SELECT email,password,first_name,State_Province,image_tag from Users where email=?; """

UPDATE_USER_IMAGE = """UPDATE Users SET image_tag=? WHERE  email=? """

SELECT_POST="""SELECT * FROM Blog"""




def create_table():
    with connection:
        curs.execute(CREATE_USERS_TABLE)
        curs.execute(CREATE_BLOG_TABLE)


def insert_into_user_table(first_name, last_name, email, password, country, state_province, _id, date, image_tag):
    with connection:
        curs.execute(CREATE_USER,
                     (first_name, last_name, email, password, country, state_province, _id, date, image_tag))


def insert_into_blog_table(blog_id, author, title, content, create_date, blog_image_tag):
    with connection:
        curs.execute(CREATE_BLOG, (blog_id, author, title, content, create_date, blog_image_tag))


def get_user(email):
    with connection:
        curs.execute(CHECK_USER, (email,))
        return curs.fetchone()


def update_image(image, email):
    with connection:
        curs.execute(UPDATE_USER_IMAGE, (image, email))


def get_blog():
    with connection:
        curs.execute(SELECT_POST)
        return curs.fetchall()