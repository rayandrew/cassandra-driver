def up(conn):
    conn.execute("""
        CREATE TABLE timeline (
          username text,
          time timeuuid,
          tweet_id uuid,
          PRIMARY KEY (username, time)
        ) WITH CLUSTERING ORDER BY (time DESC);
    """)


def down(conn):
    conn.drop("timeline")
