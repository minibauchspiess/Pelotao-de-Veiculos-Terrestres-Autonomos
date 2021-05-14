'''import asyncio
import time

t1Time = time.time()
t2Time = time.time()

t1RespTime = []
t2RespTime = []


async def soma(x1, x2):
    #print("x1 vale ",x1)
    await asyncio.sleep(0.000001)
    #print("x2 vale ",x2)
    await asyncio.sleep(0.000001)
    x = x1+x2
    await asyncio.sleep(2)
    #print("x vale",x)
    await asyncio.sleep(0.000001)
    
    return x




async def t1(start):
    await asyncio.sleep(3)
    t1RespTime.append(time.time()-start)


async def t2(start):
    await asyncio.sleep(1)
    t2RespTime.append(time.time()-start)



async def CallTask1(task, period, start):
    global t1Time
    if((time.time()-t1Time)>period)and(task.done()):
        t1Time = start
        task = asyncio.create_task(t1(start))
    else:
        await asyncio.sleep(0.000001)

async def CallTask2(task, period, start):
    global t2Time
    if((time.time()-t2Time)>period)and(task.done()):
        t2Time = start
        task = asyncio.create_task(t2(start))
    else:
        await asyncio.sleep(0.000001)



async def main():
    #await asyncio.gather(task1(time.time()),task2(time.time()))
    start = time.time()
    print("Loop")
    task1 = asyncio.create_task(t1(start))
    task2 = asyncio.create_task(t2(start))
    #await asyncio.gather(t1(start), t2(start))
    await asyncio.sleep(0.000001)
    while (time.time()-start) < 60:

        
        await CallTask1(task1, 10, tempoDeSimulacaoAgora)
        await CallTask2(task2, 18, time.time())
        
        await asyncio.sleep(0.000001)
        #await task1
        #await task2
        #await asyncio.gather(task1(time.time()))
        #await asyncio.gather(task2(time.time()))
    #print("t1RespTime: ", t1RespTime, "  t2RespTime: ", t2RespTime)
    


asyncio.run(main())'''

import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

# Plot Histogram on x
x = np.random.normal(size = 1000)
plt.hist(x, bins=50)
plt.gca().set(title='Frequency Histogram', ylabel='Frequency')