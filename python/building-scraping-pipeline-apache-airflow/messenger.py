import atexit

import psycopg2.extras

STATUS_PENDING = 'pending'
STATUS_COMPLETE = 'complete'
STATUS_DELETED = 'deleted'


class Queue:
    def __init__(self, connection):
        self.connection = connection

        atexit.register(self.cleanup)

    def setup(self):
        cursor = self.connection.cursor()

        cursor.execute('''
            select table_name
              from information_schema.tables
            where table_schema='public'
              and table_type='BASE TABLE'
        ''')
        for cursor_result in cursor:
            if cursor_result[0] == 'queue':
                print('Table already exists')
                return False

        cursor.execute('''
            create sequence queue_seq;

            create table queue (
              id int check (id > 0) primary key default nextval ('queue_seq'),
              created_at timestamp(0) not null DEFAULT CURRENT_TIMESTAMP,
              updated_at timestamp(0) not null DEFAULT CURRENT_TIMESTAMP,
              status varchar(255) not null DEFAULT 'pending',
              job_id varchar(255)
            )
        ''')

        return True

    def push(self, job_id):
        self.__execute_and_commit(
            'insert into queue (job_id) values (%s)',
            [job_id]
        )

    def pull(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute('start transaction')
        cursor.execute(
            '''
            select * from queue where status = %s and
            updated_at < now() - interval '10 second'
            order by random()
            limit 1
            for update
            ''',
            [STATUS_PENDING]
        )
        return cursor.fetchone()

    def delete(self, job_id):
        self.__change_status(job_id, STATUS_DELETED)

    def complete(self, job_id):
        self.__change_status(job_id, STATUS_COMPLETE)

    def touch(self, job_id):
        self.__execute_and_commit(
            'update queue set updated_at = now() where job_id = %s',
            [job_id]
        )

    def __change_status(self, job_id, status):
        self.__execute_and_commit(
            'update queue set status = %s where job_id = %s',
            [status, job_id]
        )

    def __execute_and_commit(self, sql, val):
        cursor = self.connection.cursor()
        cursor.execute(sql, val)

        self.connection.commit()

    def cleanup(self):
        self.connection.commit()