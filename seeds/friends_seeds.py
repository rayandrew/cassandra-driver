from seeds import fake
from seeds.users_seeds import relations


# friend_relations = [{"username": com_user[0], "friend": com_user[
#     1], "since": fake.date_time()} for com_user in permutation_users]


def up(conn):
    # query = conn.prepare_simple_statement("""
    #     INSERT INTO friends (username, friend, since)
    #     VALUES (%(username)s, %(friend)s, %(since)s)
    #     """)

    query = conn.prepare_statement("""
    INSERT INTO friends (username, friend, since)
    VALUES (?, ?, ?)
  """)

    for relation in relations:
        conn.prepare_batch_statement(query, relation)

    conn.execute(conn.batch_statement)


def down(conn):
    conn.truncate("friends")
