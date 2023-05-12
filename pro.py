import multiprocessing
import random
import time

def productor(cola_compartida, p_cargado, p_eliminado, p_realizado):
    for i in range(p_cargado):
        while cola_compartida.full():
            print('productor: la cola está llena.')
            time.sleep(1)
        item = random.randint(0, 99)
        cola_compartida.put(item)
        print('productor: produce item {}'.format(item))
        time.sleep(p_eliminado)
        print('productor: el tamaño de la cola es {}'.format(cola_compartida.qsize()))
    p_realizado.value = 1.0

def consumidor(cola_compartida, c_eliminado, c_realizado):
    time.sleep(1) 
    while True:
        if cola_compartida.empty():
            c_realizado.value = 1.0
            print('consumidor: la cola está vacía')
            time.sleep(1)
        else:
            c_realizado.value = 0.0
            time.sleep(c_eliminado)
            item = cola_compartida.get()
            print('consumidor: procesando item {}'.format(item))

if __name__ == '__main__':
    pf = multiprocessing.Value('d', 0.0)
    cf = multiprocessing.Value('d', 0.0)
    cola_compartida = multiprocessing.Queue(3)
    p = multiprocessing.Process(target=productor, args=(cola_compartida, 5, 1.0, pf))
    c = multiprocessing.Process(target=consumidor, args=(cola_compartida, 0.5, cf))
    p.start()
    c.start()
    while True:
        if int(pf.value + cf.value) == 2:
            print('Procesos terminados')
            p.terminate()
            c.terminate()
            break
        time.sleep(1)
