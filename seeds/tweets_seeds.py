from seeds import fake
from seeds.users_seeds import users, permutation_users

current_user, *list_followers = users

tweet_id = 1
tweet = fake.sentence()
time = fake.date_time()

timelines = [
    (user, time, tweet_id)
    for user in list_followers
]


def up(conn):
    query_tweet = conn.prepare_statement("""
      INSERT INTO tweets (tweet_id, username, body)
      VALUES (?, ?, ?)
    """)

    query_timeline = conn.prepare_statement("""
      INSERT INTO timeline (username, time, tweet_id)
      VALUES (?, ?, ?)
    """)

    query_userline = conn.prepare_statement("""
      INSERT INTO userline (username, time, tweet_id)
      VALUES (?, ?, ?)
    """)

    print("Inserting tweet")
    conn.execute(query_tweet, (tweet_id, current_user, tweet))

    print("Inserting current_user timeline")
    conn.execute(query_timeline, (tweet_id, time, tweet_id))

    print("Inserting current_user userline")
    conn.execute(query_userline, (tweet_id, time, tweet_id))

    for timeline in timelines:
        conn.prepare_batch_statement(query_timeline, timeline)

    conn.execute(conn.batch_statement)


def down(conn):
    conn.truncate("userline")
    conn.truncate("timeline")
    conn.truncate("tweets")
