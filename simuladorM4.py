import heapq
import numpy as np
from collections import deque

class Fila:
    def __init__(self, servidores=1, capacidade=5, tempo_atendimento=(3,5)):
        self.servidores = servidores
        self.capacidade = capacidade
        self.tempo_atendimento = tempo_atendimento
        self.servidores_ocupados = 0
        self.fila = deque()
        self.tempo_por_estado = [0.0] * (capacidade + 1)
        self.tempo_anterior = 0.0
        self.clientes_atendidos = 0
        self.clientes_perdidos = 0

    def estado_atual(self):
        return self.servidores_ocupados + len(self.fila)

    def atualizar_estatisticas(self, novo_tempo):
        delta = novo_tempo - self.tempo_anterior
        estado = self.estado_atual()
        self.tempo_por_estado[estado] += delta
        self.tempo_anterior = novo_tempo

    def gerar_tempo_atendimento(self):
        return np.random.uniform(*self.tempo_atendimento)


class SimuladorTandem:
    def __init__(self, intervalo_chegada=(2,5), limite_randoms=100000):
        self.intervalo_chegada = intervalo_chegada
        self.limite_randoms = limite_randoms
        self.randoms_usados = 0

        self.fila1 = Fila(servidores=1, capacidade=5, tempo_atendimento=(3,5))
        self.fila2 = Fila(servidores=1, capacidade=5, tempo_atendimento=(4,6))

        self.eventos = []
        self.relogio = 0.0

    def agendar_evento(self, tempo, tipo, fila_num):
        heapq.heappush(self.eventos, (tempo, tipo, fila_num))

    def gerar_tempo_chegada(self):
        return np.random.uniform(*self.intervalo_chegada)

    def chegada(self, fila, fila_num):
        # agenda próxima chegada só na primeira fila
        if fila_num == 1:
            tempo_prox = self.relogio + self.gerar_tempo_chegada()
            if self.randoms_usados < self.limite_randoms:
                self.agendar_evento(tempo_prox, "chegada", 1)
                self.randoms_usados += 1

        # atendimento imediato se servidor livre
        if fila.servidores_ocupados < fila.servidores:
            fila.servidores_ocupados += 1
            tempo_saida = self.relogio + fila.gerar_tempo_atendimento()
            self.agendar_evento(tempo_saida, "saida", fila_num)
        else:
            if len(fila.fila) < fila.capacidade - fila.servidores:
                fila.fila.append(self.relogio)
            else:
                fila.clientes_perdidos += 1

    def saida(self, fila, fila_num):
        fila.clientes_atendidos += 1

        # se for saída da primeira fila, entra na segunda
        if fila_num == 1:
            self.chegada(self.fila2, 2)

        # próxima pessoa da fila atual
        if fila.fila:
            fila.fila.popleft()
            tempo_saida = self.relogio + fila.gerar_tempo_atendimento()
            self.agendar_evento(tempo_saida, "saida", fila_num)
        else:
            fila.servidores_ocupados -= 1

    def rodar(self, tempo_inicial=0.0):
        self.relogio = tempo_inicial
        self.agendar_evento(self.relogio, "chegada", 1)  # chegada inicial na primeira fila

        while self.eventos and self.randoms_usados < self.limite_randoms:
            tempo, tipo, fila_num = heapq.heappop(self.eventos)
            self.relogio = tempo

            # atualizar estatísticas
            self.fila1.atualizar_estatisticas(tempo)
            self.fila2.atualizar_estatisticas(tempo)

            if tipo == "chegada":
                fila = self.fila1 if fila_num == 1 else self.fila2
                self.chegada(fila, fila_num)
            elif tipo == "saida":
                fila = self.fila1 if fila_num == 1 else self.fila2
                self.saida(fila, fila_num)

        # resultados
        for i, fila in enumerate([self.fila1, self.fila2], 1):
            tempo_total = sum(fila.tempo_por_estado)
            print(f"\nFila {i}: Servidores={fila.servidores}, Capacidade={fila.capacidade}")
            print("Distribuição de probabilidade dos estados da fila:")
            for j, t in enumerate(fila.tempo_por_estado):
                prob = t / tempo_total if tempo_total > 0 else 0
                print(f"Estado {j}: tempo acumulado = {t:.2f}, probabilidade = {prob:.4f}")
            print(f"Clientes atendidos: {fila.clientes_atendidos}, Clientes perdidos: {fila.clientes_perdidos}")


if __name__ == "__main__":
    sim = SimuladorTandem()
    sim.rodar()
