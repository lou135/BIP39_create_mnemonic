from random import randint
from time import sleep
import hashlib
def dice():
    return randint(0,7)

def binary(n):
    return format(n, '03b')

#Safe bit
def bit_transformer(bit):
    bit=''.join(bit).replace('11','').replace('00','') #junta os bits resultantes dos numeros gerados e remove os bits 00 e 11
    bit=bit.replace('01','0').replace('10','1') #substitui 01>0 e 10>1
    return bit

def safe_bit(l):
    bit=[]
    bit2=[]
    while len(bit2)!=l:
        bit.append(binary(dice()))
        bit2=bit_transformer(bit)
        if len(bit2)>l:
            bit=[]
            bit2=[]
    return bit2

#128 bit
def bit128():
    return safe_bit(128)

def divide_bit128(n):
    bits11=[]
    bit7=[]
    #chop 128bit into 11bit
    inicio=0
    for _ in range(12):
        if inicio!=121:
            bits11.append(n[inicio:inicio+11])
            inicio += 11
        else:
            bit7.append(n[inicio:inicio+11])
    return [bits11,bit7]

def bit11_into_decimal(n):
    valorT=[]
    for c,v in enumerate(n):          #Para cada bit11 na lista
        valorTbit=0
        for i,bit in enumerate(n[c]): #Para cada numero no bit11
            expoente = 11 - i - 1
            valor = int(bit) * (2 ** expoente)
            valorTbit=valorTbit+valor  #valor total do bit11
        valorT.append(valorTbit)
    return valorT

def decimal_to_word(n):
    words=[]
    with open('Blockchain/BIP39.txt', 'r') as arquivo:
        linhas = arquivo.readlines()
        for i in n:
            words.append(linhas[i].replace('\n',''))
    return words

#Bits de segurança
def bit128_to_hash(n):
    numero = int(n, 2)
    num_bytes = (len(n) + 7) // 8 
    byte_array = numero.to_bytes(num_bytes, byteorder='big')
    hash=hashlib.sha256(byte_array).hexdigest()
    return hash

def hash_to_bit(n):
    valor=n[0]
    bits=['0000','0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011','1100','1101','1110','1111']
    letras=['a','b','c','d','e','f']
    for i,h in enumerate(letras):
        if valor==h:
            valor=10+i
    for i,h in enumerate(bits):
        if int(valor)==i:
            return h


def word12(bit7,bitcheck):
    bit=[bit7[0]+bitcheck]
    decimal=bit11_into_decimal(bit)
    word=decimal_to_word(decimal)
    return word[0]


bit=bit128()  #cria o bit seguro
bit11e7=divide_bit128(bit) #divide o bit128 em 11 bits11(v[0]) e 1 bit7(v[1])
decimal_bit11=bit11_into_decimal(bit11e7[0]) #recebe o valor decimal de cada bit11
words=decimal_to_word(decimal_bit11) #transforma o valor decimal de cada bit11 numa palavra da lista BIP39
hash=bit128_to_hash(bit) #cria o hash(sha256) do bit 128
bitcheck=hash_to_bit(hash) #cira o bit de verificação
mnemonic=words.append(word12(bit11e7[1],bitcheck)) #junta a palavra de verificação

words=' '.join(words)
print(f'''
{words}
''')
