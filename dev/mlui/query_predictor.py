from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT * FROM predictions")
rows = cursor.fetchall()
for row in rows:
    print(row)