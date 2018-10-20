def up(conn):
    conn.execute("""
        CREATE TABLE friends (
          username text,
          friend text,
          since timestamp,
          PRIMARY KEY (username, friend)
        );
    """)
    pass


def down(conn):
    conn.drop("friends")
    pass
