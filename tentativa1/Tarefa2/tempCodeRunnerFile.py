def calcularTempoMedio(self):
        if not self.temposOperacoes:
            return 0  # Nenhuma operação registrada
        return sum(self.temposOperacoes) / len(self.temposOperacoes)

    def calcularThroughput(self, tempoTotal):
        if not self.temposOperacoes:
            return 0  
        return len(self.temposOperacoes) / tempoTotal