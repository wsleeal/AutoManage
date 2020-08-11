import datetime
import psutil
import time
import re
import os
import logging
import json

class AutoManutencao:

    '''
    * Busca uso do processador
    * Busca uso da memoria
    * Busca todos os processos em um array
    * Busca Horario atual

    * Finaliza processo de acordo com TTL
    * Inicia processo
    * Reinicia computador se a memoria estiver alta
    * Reinicia computador em horario determinado 
    '''

    def __init__(self):
        try:
            # Busca informacoes da memoria em um array
            self.memoria = dict(psutil.virtual_memory()._asdict())

            # Busca media de uso do processador no intervalo definido
            self.proc_use = psutil.cpu_percent(interval=1)

            # Retorna todos as taks em um dict
            self.tasks = [task for task in psutil.process_iter(['pid', 'name', 'username', 'status'])]

            # Retorna hora atual
            self.hora = time.strftime("%H:%M:%S", time.localtime())
        except Exception as e:
            self.logger('Console').critical('Erro: {}'.format(e))
    
    def killProcTTL(self, proc: str, ttl: int):
        '''
        * Verifica processo ativo 
        * Mata o processo de acordo com o TTL em segundos
        '''
        proc_hora = str
        for task in self.tasks:
            if task.info['name'] == proc:
                # Retorna hora de start e limpa string
                proc_hora = str(task)
                proc_hora = str(re.findall("\\d{2}\\:\\d{2}\\:\\d{2}", proc_hora)[0])

                # Calculo da hora
                d = datetime.datetime
                formater = '%H:%M:%S'
                proc_ttl = d.strptime(self.hora, formater) - d.strptime(proc_hora, formater)
                proc_ttl = proc_ttl.total_seconds()
                
                # Mata processo de acordo com TTL
                if proc_ttl >= ttl:
                    task.kill()
                    self.logger('Console').debug('Processo: {} - Finalizado'.format(
                        task.info['name']))

    def iniciarProc(self, proc_name: str, proc_path: str):
        '''
        * Inicia processo caso nao exista
        '''
        existe = False
        for p in self.tasks:
            if p.info['name'] == proc_name:
                existe = True

        if existe == False:
            os.startfile(proc_path)
            self.logger('Console').debug('Processo: {} - Iniciado'.format(
                proc_name))
    
    def reiniciaPc(self, horario,memoria_percent):
        '''
        * Reinicia PC no horario definido: '%H:%M:%S'
        * Reinicia PC por uso execivo de memoria
        '''
        # Por Horario
        d = datetime.datetime
        formater = '%H:%M:%S'

        hora_atual = d.strptime(self.hora, formater)
        hora_atual = str(re.findall("\\d{2}\\:\\d{2}", str(hora_atual))[0])

        hora_desligar = d.strptime(horario, formater)
        hora_desligar = str(re.findall("\\d{2}\\:\\d{2}", str(hora_desligar))[0])

        if hora_atual == hora_desligar:
            self.logger('Console').debug('Servidor Reiniciado por Horario Definido')
            os.system('shutdown -r -f -t 1')
            time.sleep(60)

        # Por memoria
        if self.memoria['percent'] > memoria_percent:
            self.logger('Console').critical('Servidor Reiniciado Memoria Insuficiente')
            os.system('shutdown -r -f -t 1')
            time.sleep(60)

            
    def logger(self,name):
    
        formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            filename='console.log',
            format=formatter,
            level=logging.DEBUG)
        logger = logging.getLogger(name)

        return logger

    def start(self):


        with open('processos.json', 'r') as json_file: 
            processos = json.load(json_file)
        
        for p in processos:
            self.killProcTTL(proc=processos[p]['name'],ttl=3600)
            self.iniciarProc(processos[p]['name'],processos[p]['path'])

        self.reiniciaPc('23:30:00',90)

if __name__ == '__main__':

    try:
        app = AutoManutencao()
        app.logger('Console').info('App Started')
        print('App Started')
        while True:
            app.__init__()
            app.start()
            time.sleep(10)
    except Exception as e:
        AutoManutencao().logger('Console').critical('Erro: {}'.format(e))
