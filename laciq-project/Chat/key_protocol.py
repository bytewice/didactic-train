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



def create_private_key( g , p, prime_key= False):
    if prime_key:
        a = randprime( 2**16, 2**20)
    else:
        n_bits = int(log2(p))
        a = int.from_bytes(os.urandom(n_bits), 'little')

    return a

def create_keys( g, p, prime_key= False) :
    # INSERT THE REST OF THE CODE HERE
    # must return the private key a and the public key A
    # if prime_key == True, a must be prime.
    
    """
    Gera a chave privada (a) e a chave pública (A) para o algoritmo de Diffie-Hellman.

    :param g: Base (gerador) para o cálculo da chave pública.
    :param p: Número primo que define o grupo modular.
    :param prime_key: Se True, a chave privada (a) deve ser um número primo.
    :return: Tupla contendo a chave privada (a) e a chave pública (A).
    """
    if prime_key:
        # Gera um número primo aleatório menor que p
        a = randprime( 2, p - 1)
    else:
        # Gera um número aleatório menor que p
        a = random.randint( 2, p - 1)

    # Calcula a chave pública A = g^a mod p
    A = pow( g, a, p)

    return a, A


def exchange_keys_server(client_socket, p, g, s, enc_msg, conf_msg):
    # Send p and g to client
    send_json(client_socket, {"p": p, "g": g})
    
    # INSERT THE REST OF THE CODE HERE
    #tem mais alguma coisa pra adicionar aqui? ........


def exchange_keys_client(server_socket):
    """Client side key exchange implementation."""
    # Receive p, g, and server's public key from server
    server_data = recv_json(server_socket)
    p = server_data['p']
    g = server_data['g']
    server_public_key = server_data['public_key']

    # INSERT THE REST OF THE CODE HERE
    client_private_key, client_public_key = create_keys( g, p, prime_key= True)

     # Send client's public key to the server
    send_json(server_socket, {'public_key': client_public_key})

    # Compute the shared secret: server_public_key^client_private_key mod p
    shared_secret = pow( server_public_key, client_private_key, p)

    return shared_secret

    