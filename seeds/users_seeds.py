from seeds import fake

from itertools import permutations

users = [
    dict(username=fake.user_name(),
         password=fake.password())
    for _ in range(10)
]

permutation_users = permutations([user["username"] for user in users], 2)
relations = [(com_user[0], com_user[1], fake.date_time())
             for com_user in permutation_users]


def up(conn):
    query = conn.prepare_simple_statement("""
        INSERT INTO users (username, password)
        VALUES (%(username)s, %(password)s)
        """)

    for user in users:
        conn.prepare_batch_statement(query, user)

    conn.execute(conn.batch_statement)


def down(conn):
    conn.truncate("users")
    pass
