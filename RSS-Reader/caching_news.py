import logging
import sqlite3

from rss_reader_consts import *


ROOT_LOGGER_NAME = 'RssReader'
MODULE_LOGGER_NAME = ROOT_LOGGER_NAME + '.caching_news'


DB_NAME = 'news.db'

HEADER_TABLE_NAME = 'date_'


class DataBaseConn:
    """Context Manager, which work with sqlite3."""

    def __init__(self, db_name):
        self._db_name = db_name

    def __enter__(self):
        self._conn = sqlite3.connect(self._db_name)
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()
        self._conn.close()
        if exc_val:
            raise


def table_create(TABLE_NAME) -> None:
	logger = logging.getLogger(MODULE_LOGGER_NAME + '.table_create')
	logger.info(f'Create table in database: {DB_NAME} if it doesn\'t exist with name: {TABLE_NAME}')	

	command = '''CREATE TABLE if not exists 
							{}
							(title text,
							 link text,
							 short_content text)
							'''.format(TABLE_NAME)

	with DataBaseConn(DB_NAME) as connection:
		cursor = connection.cursor()
		cursor.execute(command)



def db_write(date: str, title: str, link: str, short_content: str) -> None:
	logger = logging.getLogger(MODULE_LOGGER_NAME + '.db_write')
	logger.info(f'Write to table "{date}" in database "{DB_NAME}"')

	table_create(HEADER_TABLE_NAME + date)

	# command = f'''INSERT INTO {date} VALUES ('{title}','{link}','345')'''

	with DataBaseConn(DB_NAME) as connection:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO {} VALUES (?,?,?)".format(HEADER_TABLE_NAME + date), (title, link, short_content))
	 

def get_list_of_tables() -> str:
	logger = logging.getLogger(MODULE_LOGGER_NAME + '.get_list_of_tables')
	logger.info('Getting list of names of tables in database')

	with DataBaseConn(DB_NAME) as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM sqlite_master where type='table'")

		tables = cursor.fetchall()
		
	tables_names = ''
	for table in tables:
		tables_names += '\n' + table[2][5:]

	return tables_names


def db_read(date: str) -> str:
	logger = logging.getLogger(MODULE_LOGGER_NAME + '.db_read')
	logger.info(f'Read cached news with date: {date}')

	with DataBaseConn(DB_NAME) as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM {}".format(HEADER_TABLE_NAME + date))

		rows = cursor.fetchall()
		news = ''
		for row in rows:
			news += KEYWORD_TITLE + row[0] + EN
			news += KEYWORD_LINK + row[1] + EN
			news += KEYWORD_CONTENT + row[2] + EN
			news += NEWS_SEPARATOR + DEN

	return news