# didactic-train
projeto do PS da laciq

---

## 1) Explique como esse protocolo impede que alguém, ao interceptar os pacotes trocados, consiga obter a chave compartilhada.

O protocolo utilizado no projeto é uma variação do protocolo de troca de chaves de Diffie-Hellman, adaptado para um ambiente de comunicação em grupo. A segurança da chave compartilhada é garantida pela dificuldade computacional do problema do logaritmo discreto, que impede que um atacante, mesmo interceptando os pacotes trocados, consiga obter a chave privada dos participantes ou reconstruir a chave compartilhada.  

Os valores que podem ser capturados por um atacante durante a troca de chaves incluem  A_i = g^{a_i} mod p  , que representa a chave pública do participante \(i\), e  A_i^s mod p , um valor intermediário enviado ao servidor. Nessa equação, \(g\) é a base pública do grupo cíclico escolhido, \(p\) é um número primo grande utilizado como módulo, \(a_i\) é a chave privada do participante, \(A_i\) é a chave pública correspondente e \(s\) representa um valor secreto adicional eventualmente utilizado pelo servidor para compor a chave final.  

Para obter a chave compartilhada, um atacante precisaria recuperar a chave privada \(a_i\) a partir do valor público \(A_i\). No entanto, essa operação requer resolver a equação \(a_i = log_g A_i mod p\), conhecida como o problema do logaritmo discreto (DLP - Discrete Logarithm Problem). Esse problema é considerado computacionalmente intratável para números suficientemente grandes, especialmente quando os parâmetros do sistema, como \(p\) e \(g\), são escolhidos de forma segura.  

Além disso, mesmo que um atacante intercepte \(A_i^s\), ele não conseguirá calcular a chave compartilhada sem conhecimento de \(s\) ou de \(a_i\), pois a operação necessária seria \((A_i^s)^{a_i^{-1}} mod p\). Isso exigiria a recuperação de \(a_i\), o que, como demonstrado anteriormente, requer a resolução do problema do logaritmo discreto. Caso \(s\) seja desconhecido, a chave compartilhada permanece oculta.  

Dessa forma, a segurança do protocolo baseia-se na dificuldade computacional de resolver o problema do logaritmo discreto, impedindo que um atacante obtenha a chave privada \(a_i\) a partir da chave pública \(A_i\) ou derive a chave compartilhada a partir dos valores interceptados. Desde que os parâmetros \(p\) e \(g\) sejam escolhidos de forma adequada, como um primo suficientemente grande e um gerador seguro, a chave compartilhada entre os participantes permanecerá protegida contra ataques de força bruta ou algoritmos conhecidos para resolver o DLP.

---

## 2) Explicar como um atacante com um computador quântico (com um número suficiente de  qubits confiáveis) poderia descobrir a chave compartilhada utilizando um algoritmo que determina o período de uma função.

O algoritmo de shor é um modelo matemático que se propõe a resolver problemas matemáticos difíceis, como é o caso da fatoração de números grandes e o logaritmo discreto, utilizando características da computação quântica como o paralelismo e a transformada de fourier quântica discreta. Tal resolução representa uma ameaça para modelos criptográficos cuja segurança é fundamentada na dificuldade desses problemas, como é o caso do RSA e o Diffie-Hellman.

Ao aplicar o Algoritmo de Shor, que resolve problemas de fatoração e logaritmo discreto encontrando o período de uma função matemática específica de forma eficiente, o atacante pode comprometer a segurança dos protocolos. No caso do Diffie-Hellman, por exemplo, a equação g^x mod p = k representa um problema de logaritmo discreto, que pode ser reduzido à busca pelo período da função f(x) = g^x mod p. Com um computador quântico, esse período pode ser determinado rapidamente, permitindo que o atacante calcule a chave secreta compartilhada e, assim, quebre o sistema de criptografia.

Dessa forma, se um atacante tiver acesso a um computador quântico suficientemente poderoso, ele poderá usar o Algoritmo de Shor para calcular o período da função correspondente ao problema matemático subjacente e descobrir a chave privada de sistemas criptográficos baseados em RSA, Diffie-Hellman e ECC. Isso demonstra a vulnerabilidade dessas técnicas na era quântica e reforça a necessidade de desenvolver novas formas de criptografia pós-quântica.