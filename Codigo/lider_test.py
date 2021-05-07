import asyncio
import time
import msvcrt


com = msvcrt.getch()
print("valor recebido: ", ord(com))
#print("com ASCII: " com & 0xFF)
'''
if ord(comando) == 119:
    print("Correto")
else:
    print("tecla: ", comando, "ASCII: ", ord(comando))
'''