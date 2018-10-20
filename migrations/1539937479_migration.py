def up(conn):
    conn.execute("""
        CREATE TABLE users (
          username text PRIMARY KEY,
          password text
        );
    """)
    pass


def down(conn):
    conn.drop("users")
    pass
