from seeds import fake
from seeds.users_seeds import relations


def up(conn):
    query = conn.prepare_statement("""
    INSERT INTO followers (username, follower, since)
    VALUES (?, ?, ?)
  """)

    for relation in relations:
        conn.prepare_batch_statement(query, relation)

    conn.execute(conn.batch_statement)
    conn.empty_batch_statement()


def down(conn):
    conn.truncate("followers")
