def up(conn):
    conn.execute("""
        CREATE TABLE tweets (
          tweet_id uuid PRIMARY KEY,
          username text,
          body text
        );
    """)
    pass


def down(conn):
    conn.drop("tweets")
    pass
