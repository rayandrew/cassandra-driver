def up(conn):
    conn.execute("""
        CREATE TABLE followers (
          username text,
          follower text,
          since timestamp,
          PRIMARY KEY (username, follower)
        );
    """)
    pass


def down(conn):
    conn.drop("followers")
    pass
