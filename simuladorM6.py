import heapq
import numpy as np
from collections import deque

class FilaGG:
    def __init__(self, servidores, capacidade, intervalo_chegada=None, intervalo_servico=(2, 3), limite_randoms=100000):
        self.servidores = servidores
        self.capacidade = capacidade
        self.intervalo_chegada = intervalo_chegada  # só Fila1 tem
        self.intervalo_servico = intervalo_servico
        self.limite_randoms = limite_randoms

        self.relogio = 0.0
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
        self.tempo_por_estado[self.estado_atual()] += delta
        self.tempo_anterior = novo_tempo

    def gerar_tempo_chegada(self, rng):
        if self.intervalo_chegada is None:
            return None
        return rng.uniform(*self.intervalo_chegada)

    def gerar_tempo_atendimento(self, rng):
        return rng.uniform(*self.intervalo_servico)


class SimuladorTandem:
    def __init__(self, limite_randoms=100000):
        self.limite_randoms = limite_randoms
        self.randoms_usados = 0
        self.eventos = []
        self.relogio = 0.0

        self.fila1 = FilaGG(servidores=2, capacidade=3, intervalo_chegada=(1, 4), intervalo_servico=(3, 4), limite_randoms=limite_randoms)
        self.fila2 = FilaGG(servidores=1, capacidade=5, intervalo_chegada=None, intervalo_servico=(2, 3), limite_randoms=limite_randoms)

    def agendar_evento(self, tempo, tipo, fila=None):
        heapq.heappush(self.eventos, (tempo, tipo, fila))

    def usar_random(self):
        self.randoms_usados += 1
        return self.randoms_usados <= self.limite_randoms

    def rodar(self):
        rng = np.random.default_rng()

        # Primeiro cliente chega em 1.5
        self.relogio = 1.5
        self.agendar_evento(1.5, "chegada_externa", "fila1")

        while self.eventos and self.randoms_usados < self.limite_randoms:
            tempo, tipo, fila = heapq.heappop(self.eventos)
            self.relogio = tempo
            self.fila1.atualizar_estatisticas(tempo)
            self.fila2.atualizar_estatisticas(tempo)

            if tipo == "chegada_externa":
                if not self.usar_random(): break
                prox = self.fila1.gerar_tempo_chegada(rng)
                if prox and self.randoms_usados < self.limite_randoms:
                    self.agendar_evento(self.relogio + prox, "chegada_externa", "fila1")
                self.processar_chegada(self.fila1, "fila1", rng)

            elif tipo == "saida_fila1":
                self.processar_saida(self.fila1, "fila1", rng)
                # tenta entrar na Fila2
                self.processar_chegada(self.fila2, "fila2", rng)

            elif tipo == "saida_fila2":
                self.processar_saida(self.fila2, "fila2", rng)

        tempo_global = self.relogio
        self.relatorio(tempo_global)

    def processar_chegada(self, fila, nome, rng):
        if fila.servidores_ocupados < fila.servidores:
            fila.servidores_ocupados += 1
            if not self.usar_random(): return
            tempo_serv = fila.gerar_tempo_atendimento(rng)
            self.agendar_evento(self.relogio + tempo_serv, f"saida_{nome}", nome)
        else:
            if len(fila.fila) < fila.capacidade - fila.servidores:
                fila.fila.append(self.relogio)
            else:
                fila.clientes_perdidos += 1

    def processar_saida(self, fila, nome, rng):
        fila.clientes_atendidos += 1
        if fila.fila:
            fila.fila.popleft()
            if not self.usar_random(): return
            tempo_serv = fila.gerar_tempo_atendimento(rng)
            self.agendar_evento(self.relogio + tempo_serv, f"saida_{nome}", nome)
        else:
            fila.servidores_ocupados -= 1

    def relatorio(self, tempo_global):
        for i, fila in enumerate([self.fila1, self.fila2], start=1):
            print(f"\nFila {i}: G/G/{fila.servidores}/{fila.capacidade}")
            tempo_total = sum(fila.tempo_por_estado)
            for j, t in enumerate(fila.tempo_por_estado):
                prob = t / tempo_total if tempo_total > 0 else 0
                print(f"Estado {j}: tempo acumulado = {t:.2f}, probabilidade = {prob:.4f}")
            print(f"Clientes atendidos: {fila.clientes_atendidos}, perdidos: {fila.clientes_perdidos}")
        print(f"\nTempo global da simulação: {tempo_global:.2f}")


if __name__ == "__main__":
    sim = SimuladorTandem(limite_randoms=100000)
    sim.rodar()
    tempo_global = self.relogio
    self.relatorio_formatado(tempo_global)




def relatorio_formatado(self, tempo_global):
    # função auxiliar que recebe um objeto fila (com atributos já usados no seu código)
    def imprimir_fila(fila, nome):
        tempo_total = sum(fila.tempo_por_estado)
        print(f"\n{nome}: G/G/{fila.servidores}/{fila.capacidade}")
        print("Distribuição de probabilidade dos estados da fila:")
        for i, t in enumerate(fila.tempo_por_estado):
            prob = t / tempo_total if tempo_total > 0 else 0.0
            print(f"Estado {i}: tempo acumulado = {t:.2f}, probabilidade = {prob:.4f}")
        print(f"Tempo total simulado: {tempo_total:.2f}")
        print(f"Clientes atendidos: {fila.clientes_atendidos}")
        print(f"Clientes perdidos: {fila.clientes_perdidos}")

    # imprime fila 1 e fila 2 no mesmo formato
    imprimir_fila(self.fila1, "Fila 1")
    imprimir_fila(self.fila2, "Fila 2")

    # tempo global da simulação (último tempo do relógio)
    print(f"\nTempo global da simulação: {tempo_global:.2f}")
