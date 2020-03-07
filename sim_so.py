import simpy
import random

def OSProcess (nameProcess, env, process,ram):
    global processTime 
    global times
       
    # Crea Proceso
    yield env.timeout(random.expovariate(1.0 / 10))

    # Proceso Nuevo
    initTime = env.now
    stateProcess= "new"
    executeInstructions = random.randint(1, 10) #instrucciones a ejecutar
    requestRam = random.randint(1,10) #memoria solicitada

    print( stateProcess, '->', nameProcess)
    print( nameProcess , ' initTime->', initTime)

    #Ejecucion
    with ram.get(requestRam) as Stack:
        stateProcess = "ready"
        yield Stack 
        while executeInstructions > 1:
            with process.request() as OSProcess:
                yield OSProcess
                stateProcess = "running"
                executeInstructions = executeInstructions - 3
                yield env.timeout(1)
                print(nameProcess, "->", stateProcess, " -> Duration: ", env.now) 
            if executeInstructions < 1:
              yield env.timeout(1)
        
        ram.put(requestRam)


    lapseTime = env.now - initTime
    times.append(lapseTime)
    print('%s total %f' % (nameProcess, lapseTime))
    processTime = processTime + lapseTime


# ----------------------
#Simulacion
env = simpy.Environment() 
process = simpy.Resource(env, capacity = 100)
ram = simpy.Container(env, init=100, capacity = 100)
times = list()
random.seed(10)
processTime = 0

execute = 25 #numero de procesos

for i in range(execute):
    env.process(OSProcess('Proceso %d' % i, env, process,ram))

env.run()

#desviación estandar
avg = processTime / execute
print("\nAVG Process->", avg)
for x in times:
    sd = (x-avg)*(x-avg)

sd = sd /execute
print("Desviación estándar->", sd)
