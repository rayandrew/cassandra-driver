from seeds import fake, NUMBER_GENERATOR

from itertools import permutations

list_of_username = [
    "rayandrew",
    "aldrich",
    "nathanchrst",
    "girvandip",
    "kukuhbr",
    "yowinarto"
]

users = [
    dict(username=user,
         password=fake.password())
    for user in list_of_username
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
    conn.empty_batch_statement()


def down(conn):
    conn.truncate("users")
    pass
