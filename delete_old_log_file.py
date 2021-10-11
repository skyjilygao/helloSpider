import datetime
import os
import shutil
import sys, getopt
from loguru import logger

# definde logs base dir.
log_base_dir = 'logs/delete_old_log'
logger.add(log_base_dir + "/run_log.log", rotation='10MB', enqueue=True, encoding='utf-8', level='INFO', backtrace=True, diagnose=True)
logger.add(log_base_dir + "/error_log.log", rotation='10MB', enqueue=True, encoding='utf-8', level='ERROR', backtrace=True, diagnose=True)

def delete_dir(logDir, days):
    """
    delete method.
    ------
    Parameters
    ------------
    logDir : str
        log der
    days: int
        delete before days

    """
    now = datetime.datetime.now()
    last7d = now - datetime.timedelta(days=days)
    last7dd = datetime.date(last7d.year, last7d.month, last7d.day)
    logger.info('will delete {} dir'.format(last7dd))

    listdir = os.listdir(logDir)
    # logger.info(listdir)
    for d in listdir:
        if d == 'run_log.log' or 'error_log.log' == d or 'warn_log.log' == d:
            continue
        try:
            t = datetime.datetime.strptime(d, '%Y-%m-%d')
            tdd = datetime.date(t.year, t.month, t.day)
            if tdd < last7dd:
                logger.info('deleting {}'.format(logDir + '/' + d))
                shutil.rmtree(logDir + '/' + d)
        except BaseException as e:
            logger.exception(e)
            # logger.exception('process error, dir[{}], error info:{}'.format(d, e), e)

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:f:', ['days=', 'folder='])
        logDir = '/home/skyjilygao/logs/testPorj'
        days = 7
        for opt_name, opt_value in opts:
            if opt_name in ('-d', '--days'):
                days = opt_value
                continue
            if opt_name in ('-f', '--folder'):
                logDir = opt_value
                continue

        logger.info('config info. [folder={}, days={}]'.format(logDir, days))
        logger.info('delete start...')
        delete_dir(logDir, int(days))
    except BaseException as e:
        logger.exception('unknow error',e)
    finally:
        logger.info('delete end...')
