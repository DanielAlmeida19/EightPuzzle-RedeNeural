#matriz = [[1,2,3],[4,5,6],[0,8,7]]
#n=3
class Tabuleiro:
    def __init__(self,linhas,colunas,posicoes):
        self.linhas = linhas
        self.colunas = colunas
        self.posicoes = posicoes
    def setPosicoes(self,matriz):
        self.posicoes = matriz
    def procura_vazio(self):
        for i in range (0,self.linhas):
            for j in range (0,self.colunas):
                if (self.posicoes[i][j]==0):
                    return [i,j]
        pass
    def printa_tabuleiro(self):
        for i in range(0,self.linhas):
            print(self.posicoes[i])   
        print()
        pass
                   
#tabuleiro = Tabuleiro(n,n,matriz)        
def descer_peca(tabuleiro):
     vazio = tabuleiro.procura_vazio()
     if(vazio[0] != 0):
         matriz = tabuleiro.posicoes
         matriz[vazio[0]][vazio[1]] = matriz[vazio[0]-1][vazio[1]]
         matriz[vazio[0]-1][vazio[1]] = 0
         tabuleiro.setPosicoes(matriz)
         pass
     
     
def subir_peca(tabuleiro):
     vazio = tabuleiro.procura_vazio()
     if(vazio[0] != 2):
        matriz = tabuleiro.posicoes
        matriz[vazio[0]][vazio[1]] = matriz[vazio[0]+1][vazio[1]]
        matriz[vazio[0]+1][vazio[1]] = 0
        tabuleiro.setPosicoes(matriz)
        pass
     
def direita_peca(tabuleiro):
    vazio = tabuleiro.procura_vazio()
    if(vazio[1] != 0):
        matriz = tabuleiro.posicoes
        matriz[vazio[0]][vazio[1]] = matriz[vazio[0]][vazio[1]-1]
        matriz[vazio[0]][vazio[1]-1] = 0
        tabuleiro.setPosicoes(matriz)
        pass
     
def esquerda_peca(tabuleiro):
    vazio = tabuleiro.procura_vazio()
    if(vazio[1] != 2):
        matriz = tabuleiro.posicoes
        matriz[vazio[0]][vazio[1]] = matriz[vazio[0]][vazio[1]+1]
        matriz[vazio[0]][vazio[1]+1] = 0
        tabuleiro.setPosicoes(matriz)
        pass
     
     
"""tabuleiro.printa_tabuleiro()
subir_peca(tabuleiro)     
tabuleiro.printa_tabuleiro()
descer_peca(tabuleiro)
tabuleiro.printa_tabuleiro()
direita_peca(tabuleiro)
tabuleiro.printa_tabuleiro()
esquerda_peca(tabuleiro)
tabuleiro.printa_tabuleiro()"""