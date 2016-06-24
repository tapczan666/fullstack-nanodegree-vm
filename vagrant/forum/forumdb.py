#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    ## Database connection
    DB = psycopg2.connect("dbname=forum")
    cur = DB.cursor()

    QUERY = "SELECT * FROM posts ORDER BY time DESC;"
    cur.execute(QUERY)
    data = cur.fetchall()
    posts = [{'content': str(row[0]), 'time': str(row[1])} for row in data]
    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.

    '''
    ## Sanitize input
    content = bleach.clean(content)

    ## Database connection
    DB = psycopg2.connect("dbname=forum")
    cur = DB.cursor()

    t = time.strftime('%c', time.localtime())
    QUERY = "INSERT INTO posts (content, time) VALUES (%s, %s);"
    cur.execute(QUERY, (content, t))
    DB.commit()
    DB.close()
