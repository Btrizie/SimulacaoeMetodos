# **Simulação e Métodos analíticos**

## M2:
Desenvolver um gerador responsável por fornecer os números pseudoaleatórios normalizados entre 0 e 1.

    início:
        definir parâmetros do método da congruência linear:
            a ← multiplicador
            c ← incremento
            M ← módulo
            seed ← valor inicial

        definir variável global:
            último ← seed

        procedimento NextRandom():
            último ← (a * último + c) mod M
            retornar último / M    # número entre 0 e 1

        programa principal:
            criar lista vazia dados
            para i de 1 até N:
                gerar novo número ← NextRandom()
                adicionar novo
    fim

## M4: 
Implementar um simulador de filas orientado a eventos utilizando números pseudoaleatórios gerados pelo método da congruência linear (LCG).

    início:
        inicializar variáveis globais
        count ← limite de números pseudoaleatórios

        criar escalonador de eventos vazio
        agenda primeira chegada

        enquanto (existirem eventos) e (count > 0) faça:
            evento ← remover próximo evento do escalonador
            atualizar estatísticas (tempo acumulado no estado atual)
            avançar relógio para tempo do evento

            se evento for CHEGADA então
                agenda próxima chegada
                se servidor estiver livre então
                    ocupar servidor
                    agenda SAÍDA
                senão se fila tiver espaço então
                    cliente entra na fila
                fim se
            fim se

            se evento for SAÍDA então
                liberar servidor ou atender próximo da fila
                se fila não estiver vazia então
                    agenda próxima SAÍDA
                fim se
            fim se
        fim enquanto

        calcular distribuição de probabilidade:
            para cada estado k:
                prob[k] ← tempo_estado[k] / tempo_total

        imprimir resultados:
            - tempo acumulado em cada estado
            - distribuição de probabilidades
            - número de clientes atendidos
    fim

## M6: 
Aprimorar o simulador de forma a prepará-lo a aceitar uma rede de filas com topologia genérica (tandem), ou seja, a entrada de uma fila é a saída da "anterior".

    início:
        inicializar variáveis globais
        count ← limite de números pseudoaleatórios
        relógio ← 0
        criar duas filas (Fila1 e Fila2) com:
            - número de servidores
            - capacidade total
            - intervalos de chegada/serviço
            - contadores zerados (clientes, tempos de estado)
    
        criar escalonador de eventos vazio
        agendar primeira chegada externa em Fila1 no tempo 1.5
    
        enquanto (existirem eventos) e (count > 0) faça:
            evento ← remover próximo evento do escalonador
            atualizar estatísticas de cada fila (tempo acumulado no estado atual)
            avançar relógio para tempo do evento
    
            se evento for CHEGADA_EXTERNA em Fila1 então
                decrementar count
                gerar próximo tempo de chegada e agendar
                processar chegada em Fila1:
                    se houver servidor livre então
                        ocupar servidor
                        agendar SAÍDA de Fila1
                    senão se houver espaço na fila então
                        cliente entra na fila
                    senão
                        cliente é perdido
                    fim se
            fim se
    
            se evento for SAÍDA_FILA1 então
                processar saída em Fila1:
                    cliente atendido++
                    se fila não vazia então
                        remover cliente da fila
                        decrementar count
                        agendar próxima SAÍDA
                    senão
                        liberar servidor
                    fim se
                processar chegada em Fila2 (cliente transferido da Fila1)
    
            fim se
    
            se evento for SAÍDA_FILA2 então
                processar saída em Fila2:
                    cliente atendido++
                    se fila não vazia então
                        remover cliente da fila
                        decrementar count
                        agendar próxima SAÍDA
                    senão
                        liberar servidor
                    fim se
            fim se
    
        fim enquanto
    
        calcular distribuição de probabilidade:
            para cada fila i:
                para cada estado k:
                    prob[k] ← tempo_estado[k] / tempo_total
    
        imprimir resultados para cada fila:
            - configuração (G/G/servidores/capacidade)
            - tempo acumulado por estado
            - distribuição de probabilidades
            - número de clientes atendidos
            - número de clientes perdidos
    
        imprimir tempo global da simulação
    fim

