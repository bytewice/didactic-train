import os
from utils import get_key
from utils import decrypt_message, recv_json, send_json
from sympy import randprime
from math import log2
import random

"""
As funcoes recv_json e send_json sao usadas para enviar e receber dicionarios

recv_json tem:
    * input: socket 
    * output: dicionario
send_json tem:
    * input: socket e o dicionario
    * output: None

Quando o servidor inicia, ele ja escolhe uma mensagem de confirmacao (conf_msg) para os clients e ja cifra (obtendo enc_msg).
Por isso nao precisa usar o algoritmo de encriptacao, pois o cifrotexto ja vem no argumento da funcao.

A funcao decrypt_message inverte a funcao de encriptacao usada pelo servidor se for usada com a mesma chave.
    * input: cifrotexto (use str) e chave
    * output: mensagem decriptada

    ATENCAO, A chave DEVE SER OBTIDA USANDO A FUNCAO get_key.
    Nao passe o valor da chave compartilhada obtida diretamente para decrypt_message.
    Faca:
    chave = get_key(chave_compatilhada) # chave_compartilhada tem tipo int
    decrypt_message(cifrotexto, chave)

"""



def create_private_key(g, p, prime_key= False): 
    if prime_key:         
        a = randprime(2**16, 2**20)
    else:
        n_bits = int(log2(p)/3) 
        a = int.from_bytes(os.urandom(n_bits), 'little') #---------#  gerar números grandes criptograficamente #---------# 
        #---------#  em tese esse .urandom(n) vai gerar n bytes #----------------------------------------# 
        #---------#  por isso q eu dividi por 3 pra ter o log8 e gerar os bytes mais certinhos #---------#     
    return a

def create_keys( g, p, prime_key= False) :
    # INSERT THE REST OF THE CODE HERE
    # must return the private key a and the public key A
    # if prime_key == True, a must be prime.

    a = create_private_key(g, p,prime_key=True) #---------# acho prime_key=True que tanto faz ser primo ou não no #---------------#
    #---------#                                 #---------# contexto q to usando ent vai assim msm #---------------#
    A = pow( g, a)                              #---------#       A = g^a                          #---------------#

    return a, A


def exchange_keys_server(client_socket, p, g, s, enc_msg, conf_msg):
    # Send p and g to client
    send_json(client_socket, {"p": p, "g": g})
    
    # INSERT THE REST OF THE CODE HERE

    #---------# Para cada i = 0, 1, ..., N calcula Ai^s      #---------#
    #---------# Para isso precisa receber Ai                 #---------#
    client_data = recv_json(client_socket)                   #---------# confirmar se isso aq tá certo p receber o Ai!!!
    public_key = client_data['public']                       #---------# Isso aqui é o Ai ???? meti essa de maluco
    
    xd = pow(public_key, s)                                  #---------# xd = (g^a)^s = g^as
    send_json(client_socket, {"c": enc_msg, "Shared_s": xd}) #---------# Faz o envio para Pi

    #          ...                                           #
    #       Aguarda a mensagem decryptada                    #
    #          ...                                           #

    client_data = recv_json(client_socket)
    msg_dot = client_data['decrypted_msg']
    #---------# O servidor compara m' com m, e retorna ok se tiver igual e nao ok caso contrário
    if(msg_dot == conf_msg): return("ok")
    else: return("not ok")



def exchange_keys_client(server_socket):
    """Client side key exchange implementation."""
    # Receive p, g, and server's public key from server
    server_data = recv_json(server_socket)
    p = server_data['p']
    g = server_data['g']

    # INSERT THE REST OF THE CODE HERE
    private, public = create_keys( p, g, prime_key=True)
    send_json(server_socket, {"public_key": public})    #---------# enviou a chave pública do cliente
    
    #                ...                                                #
    #           espera para receber de volta a info                     #
    #                ...                                                #
    
    server_data2 = recv_json(server_socket)             #---------# recebeu Shared_s e a cifra
    shared = server_data2['Shared_s']
    c = server_data2['c']
    
    #---------# calcula (Ai^s)^1/p para este passo é recomendável que p seja um primo
    server_public = shared ** 1/private                 #---------# server_public = g^s
    #---------# calcula mi' = D(g^s, c) e envia m' para o servidor    #---------#
    msg = decrypt_message(c, get_key(server_public))
    send_json(server_socket, {"decrypted_msg": msg})   

    


    
    
    