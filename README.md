# didactic-train
projeto do PS da laciq


Explique como esse protocolo impede que alguém, ao interceptar os pacotes trocados, consiga
obter a chave compartilhada.

O protocolo utilizado no projeto é uma variação do Diffie-Hellman adaptado para um chat com vários participantes, a dificuldade de se obter a chave compartilhada é consequência da dificuldade do problema do logaritmo discreto. 

Pacotes que poderiam ser interceptados: 'Ai' e 'Ai^(s)'

notação: A (chave pública), a(chave privada), i(indice da pessoa q usa o serviço)

Para obter a chave compartilhada a partir de 'Ai^(s)' o atacante deveria ter a chave privada 'ai' e utilizar algumas propriedades de inverso logaritmo para obter a chave compartilhada. Dessa forma, essa dificuldade se sustenta na dificuldade de se obter a 'ai' quando o cliente envia 'Ai' para o servidor.

Para obter a chave pública (ai) a partir da chave privada (Ai) o atacante deveria resolver o problema do logaritmo discreto, que é um problema criptoraficamente seguro contra atacantes clássicos. (dependendo da geração de chaves, tamanho de p e g, etc)

Portanto, a segurança do protocolo é garantida pela dificuldade de se obter as chaves privadas 'ai' e 's' a partir dos valores públicos g, p, Ai e Ai^(s). E essa dificuldade é garantida pelo problema do logaritmo discreto.
