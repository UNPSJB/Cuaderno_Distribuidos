# encoding: utf-8
from subprocess import Popen, check_call
from time import sleep
import atexit
from contextlib import contextmanager
from multiprocessing import Process


comandos = []


def terminar():
    for proc in comandos:
        print("Terminado %s %s" % (proc, proc.pid))
        proc.terminate()


def lanzar_backgounrd(comando, a_menos_que=None, autokill=True):
    """"
    Lanza un proceso en segundo plano. A menos que `a_menos_que` retorne 0.
    Auto-termina el comando al final del proceso.
    """
    global comandos
    if a_menos_que:
        try:
            check_call(a_menos_que.split())
        except:
            pass
        else:
            # Si el valor de retorno es 0, el comando `a_menos_que`
            # retornó OK.
            return (False, a_menos_que)
    sleep(.5)
    proc = Popen(comando)
    print("Lanzando %s con pid %s" % (comando, proc.pid))
    if not comandos:
        atexit.register(terminar)
    if autokill:
        comandos.append(proc)
    return (True, proc.pid)


@contextmanager
def lanzar_como_proceso(func, args=None, kwargs=None, warm_up_time=0):
    assert 0 <= warm_up_time <= 10, (
        "El calentamiento es de 0 a 10 sgunods: %s" % warm_up_time
    )
    subproc = Process(target=func, args=args or (), kwargs=kwargs or {})
    subproc.start()
    print("Lanzando %s con el pid %d." % (func, subproc.pid or None))
    sleep(warm_up_time)
    yield subproc
    if subproc.is_alive():
        subproc.terminate()
