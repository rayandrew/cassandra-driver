from seeds import fake
from seeds.users_seeds import relations


# followers_relations = [{"username": com_user[0], "follower": com_user[
#     1], "since": fake.date_time()} for com_user in permutation_users]


def up(conn):

    # query = conn.prepare_simple_statement("""
    #     INSERT INTO followers (username, follower, since)
    #     VALUES (%(username)s, %(follower)s, %(since)s)
    #     """)

    query = conn.prepare_statement("""
    INSERT INTO followers (username, follower, since)
    VALUES (?, ?, ?)
  """)

    for relation in relations:
        conn.prepare_batch_statement(query, relation)
        # conn.execute(query, (relation["username"],
        #                      relation["follower"], relation["since"]))

    conn.execute(conn.batch_statement)


def down(conn):
    conn.truncate("followers")
