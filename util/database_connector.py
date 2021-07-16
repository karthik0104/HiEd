from mysql.connector import connect, Error, OperationalError
from config.argsparser import ArgumentsParser

configs = ArgumentsParser()

def execute_test_script():
    try:
        with connect(
                host=configs.db_host,
                user=configs.db_user,
                password=configs.db_password
        ) as connection:
            c = connection.cursor()

            fd = open('sql/test_sql.sql', 'r')
            sqlFile = fd.read()
            fd.close()

            sqlCommands = sqlFile.split(';')

            for command in sqlCommands:
                try:
                    print(command)
                    c.execute(command)
                except OperationalError as oe:
                    print(oe)
            print(connection)
    except Error as e:
        print(e)

