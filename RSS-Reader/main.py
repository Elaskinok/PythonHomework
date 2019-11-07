'''Main module of RssReader which starts program.'''

import logging
from logging import config
import argparse

from rss_parser import RssReader


VERSION = '1.0'

LOGS_FILENAME = "rss_reader.log"

ROOT_LOGGER_NAME = 'RssReader'
MODULE_LOGGER_NAME = ROOT_LOGGER_NAME + '.main'

CORRECT_END_LOG = 'END (correct)'

# LINK = 'https://www.reddit.com/.rss'

LINK = 'https://news.yahoo.com/rss/'
# LINK = 'https://www.newsisfree.com/rss/'


def create_args_parser() -> argparse.ArgumentParser:
    '''Func which creats parser of arguments of command-line.
        Return: argparse.ArgumentParser

    '''
    logger = logging.getLogger(MODULE_LOGGER_NAME + '.create_args_parser')
    logger.info("Create parser of arguments")

    parser = argparse.ArgumentParser(description='Command-line RSS reader.')
    return parser


def init_args(parser: argparse.ArgumentParser) -> None:
    '''Func which takes parser and adds arguments.
       -v, --version
       --json
       -l, --limit
       link
       -V, --verbose 
    '''
    logger = logging.getLogger(MODULE_LOGGER_NAME + '.init_args')
    logger.info('Initialize arguments of command-line')

    parser.add_argument(
        '-v',
        '--version',
        help='Print version info',
        action='version',
        version=('version ' + VERSION)
    )
    parser.add_argument(
        '--json',
        help='Print result as JSON in stdout',
        action='store_true'
    )
    parser.add_argument(
        "-l",
        '--limit',
        type=int,
        help='Limit news topics if this parameter provided'
    )
    parser.add_argument(
        "link",
        type=str,
        nargs='?',
        help='Link on RSS resource'
    )
    parser.add_argument(
        "-V",
        "--verbose",
        help='Print all logs in stdout',
        action='store_true'
    )


if __name__ == "__main__":
    logging.config.fileConfig('logger_config.conf')
    logger = logging.getLogger(MODULE_LOGGER_NAME)
    logger.info('START')

    parser = create_args_parser()
    init_args(parser)
    args = parser.parse_args()

    if args.verbose is True:
        logger.info('Output logs')

        with open(LOGS_FILENAME, 'r') as file:
            print(file.read())

        logger.info(CORRECT_END_LOG)
    elif args.link is not None:
        logger.info('Entrance to get news case')

        rss_reader = RssReader(link=LINK)

        if args.limit is not None:
            limit = args.limit
        else:
            limit = 0

        if args.json is True:
            news = rss_reader.get_news_as_json(limit=limit)
        else:
            news = rss_reader.get_news_as_string(limit=limit)

        print(news)
        logger.info(CORRECT_END_LOG)
    else:
        logger.error('END (no args)')
        parser.parse_args(['-h'])
