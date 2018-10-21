def up(conn):
    conn.execute("""
        CREATE TABLE followers (
          username text,
          follower text,
          since timestamp,
          PRIMARY KEY (username, follower)
        );
    """)


def down(conn):
    conn.drop("followers")
