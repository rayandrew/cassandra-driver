from seeds import fake
from datetime import datetime
from cassandra.util import uuid, uuid_from_time
from seeds.users_seeds import users


def make_tweet(conn, username):
    tweet_id = uuid.uuid1()
    timeuuid = uuid_from_time(datetime.now())
    content = fake.sentence()
    conn.prepare_batch_statement(
        """
    INSERT INTO tweets (tweet_id, username, body)
    VALUES (%s, %s, %s)
    """,
        (tweet_id, username, content)
    )
    conn.prepare_batch_statement(
        """
    INSERT INTO userline (username, time, tweet_id)
    VALUES (%s, %s, %s)
    """,
        (username, timeuuid, tweet_id)
    )
    conn.prepare_batch_statement(
        """
    INSERT INTO timeline (username, time, tweet_id)
    VALUES (%s, %s, %s)
    """,
        (username, timeuuid, tweet_id)
    )
    # Insert tweets to followers' timeline
    followers = conn.execute("""
      SELECT follower
      FROM followers
      WHERE username=%s
    """, (username,))

    for follower in followers:
        conn.prepare_batch_statement("""
          INSERT INTO timeline (username, time, tweet_id)
          VALUES (%s, %s, %s)
        """, (follower.follower, timeuuid, tweet_id))


def up(conn):
    for user in users:
        print("Inserting tweets for user: ", user["username"])
        for _ in range(10):
            make_tweet(conn, user["username"])

    conn.execute(conn.batch_statement)
    conn.empty_batch_statement()


def down(conn):
    conn.truncate("userline")
    conn.truncate("timeline")
    conn.truncate("tweets")
