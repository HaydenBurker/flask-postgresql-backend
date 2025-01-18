from db import connection, cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS "Users" (
    user_id UUID NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    active BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    UNIQUE (email),
    PRIMARY KEY (user_id)
)""")

connection.commit()

def base_user_object(user):
    [user_id, first_name, last_name, email, active, created_at, updated_at] = user
    return {
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "active": active,
        "created_at": str(created_at),
        "updated_at": str(updated_at)
    }
