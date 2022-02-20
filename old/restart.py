from datetime import datetime
import logging
import os

def logger(name):
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        filename='console.log',
        format=formatter,
        level=logging.DEBUG)
    logger = logging.getLogger(name)
    return logger

def timer(horario_do_restart):
    while True:
        a = datetime.now()
        if a.hour==horario_do_restart:
            logger('Console').info('Reiniciado')
            os.system('shutdown -r -f -t 1')
            break

if __name__ == "__main__":
    try:
        print('Rodando...')
        logger('Console').info('Iniciado')
        timer(11)
    except Exception as e:
        logger('Console').error(str(e))
