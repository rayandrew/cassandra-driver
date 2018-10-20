def up(conn):
    conn.execute("""
        CREATE TABLE userline (
          username text,
          time timeuuid,
          tweet_id uuid,
          PRIMARY KEY (username, time)
        ) WITH CLUSTERING ORDER BY (time DESC);
    """)
    pass


def down(conn):
    conn.drop("userline")
    pass
