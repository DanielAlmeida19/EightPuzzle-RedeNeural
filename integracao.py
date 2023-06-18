from redeNeural import *
from eight_puzzle import *
import numpy as np
import random
import copy
import math
noise_scale = 0.1


class DNA:
    def __init__(self,vetorDNA,tamanhoDNA):
        self.vetorDNA = vetorDNA
        self.tamanhoDNA = tamanhoDNA

class Jogador:
    def __init__(self,tabuleiro,DNA,cerebro,estado,fitness,energia,vetor_encaixe):
        self.tabuleiro = tabuleiro
        self.DNA = DNA
        self.cerebro = cerebro
        self.estado = estado
        self.fitness = fitness
        self.energia = energia
        self.vetor_encaixe = vetor_encaixe
        
    def peca_pra_cima(self):
        subir_peca(self.tabuleiro)
        self.energia-=1
        
    def peca_pra_baixo(self):
        descer_peca(self.tabuleiro)
        self.energia-=1
        
    def peca_pra_esquerda(self):
        esquerda_peca(self.tabuleiro)
        self.energia-=1
        
    def peca_pra_direita(self):
        direita_peca(self.tabuleiro)
        self.energia-=1
        
class Geracao:
    def __init__(self,quatidade_jogadores,players,gen_atual,media_fitness,range_random):
        self.quantidade_jogadores = quatidade_jogadores
        self.players = players
        self.gen_atual = gen_atual
        self.media_fitness = media_fitness
        self.range_random = range_random

def softmax(x):
    exps = np.exp(x - np.max(x))  # Subtrai o valor máximo para evitar problemas de estouro numérico
    return exps / np.sum(exps)

def softmax_with_noise(x, noise_scale):
    noise = np.random.normal(loc=0, scale=noise_scale, size=len(x))
    x_with_noise = x + noise
    softmax_output = softmax(x_with_noise)
    binary_output = np.zeros_like(softmax_output)
    binary_output[np.argmax(softmax_output)] = 1
    return binary_output

def fitness(tabuleiro,vetor):
    tam_solucao = tabuleiro.linhas
    verifica_linha = 0
    verifica_linha_2 = 0
    verifica_coluna = 0
    verifica_coluna_2 = 0
    dif = 0
    matriz_tabuleiro = np.array(tabuleiro.posicoes)
    for i in range(0,tam_solucao):
        for j in range(0,tam_solucao):
            if matriz_tabuleiro[i][j]==0:
                i_real = tam_solucao-1
                j_real = tam_solucao-1
            else:
                i_real = (matriz_tabuleiro[i][j]-0.1)//tam_solucao #Calculando a distancia ate a posicao correta
                j_real = (matriz_tabuleiro[i][j]%tam_solucao)-1
            if j_real < 0:
                j_real = tam_solucao-1
            dif = dif - (abs(i-i_real)+abs(j-j_real))
            """if(i_real == i and j_real == j and (i == 0 and j == 0)): #1 esta na posicao correta

                for k in range(1,tam_solucao):
                    i_aux = k  
                    j_aux = k 
                    i_real = (matriz_tabuleiro[i][j_aux]-0.1)//tam_solucao #Calculando a distancia ate a posicao correta
                    j_real = (matriz_tabuleiro[i][j_aux]%tam_solucao)-1
                    if j_real < 0:
                        j_real = tam_solucao-1
                    if(i_real != i or j_real != j_aux):
                        print(i_real,j_real)
                        verifica_linha = 1
                    i_real = (matriz_tabuleiro[i_aux][j]-0.1)//tam_solucao #Calculando a distancia ate a posicao correta
                    j_real = (matriz_tabuleiro[i_aux][j]%tam_solucao)-1
                    if j_real < 0:
                        j_real = tam_solucao-1
                    if(i_real != i_aux or j_real != j):
                        verifica_coluna = 1
                        print("INVERTEU COLUNA")
                        
                        
                        
                if(verifica_coluna == 0):
                    print("MANDIOCA")
                    if(vetor[0] == 0):
                        vetor[0]=1
                        dif = dif + 5
                        print("+ BATATA")
                    for k in range(0,tam_solucao):
                        i_aux = k  
                        j_aux = k 
                        i_real = (matriz_tabuleiro[i_aux][j+1]-0.1)//tam_solucao #Calculando a distancia ate a posicao correta
                        j_real = (matriz_tabuleiro[i_aux][j+1]%tam_solucao)-1
                        if j_real < 0:
                            j_real = tam_solucao-1
                        if(i_real != i_aux or j_real != j + 1):
                            verifica_coluna_2 = 1
                    if(verifica_coluna_2 == 0):
                        if(vetor[1] == 0):
                            vetor[1]=1
                            #printf("BATATA",dif)
                            dif = dif + 5
                            print("+ BATATA")
                    else:
                        if(vetor[1]==1):
                            vetor[1] = 0
                            dif = dif - 5
                            print("- BATATA")        
                elif(verifica_linha == 1):
                    if(vetor[0]==1):
                        vetor[0] = 0
                        print("- BATATA")    
                        dif = dif - 5
                        
                        
                        
                if(verifica_linha == 0):
                    print("NABO")
                    if(vetor[0] == 0):
                        print("+ BATATA")
                        vetor[0]=1
                        dif = dif + 5
                    for k in range(0,tam_solucao):
                        #print("- BATATA")
                        i_aux = k  
                        j_aux = k 
                        i_real = (matriz_tabuleiro[i+1][j_aux]-0.1)//tam_solucao #Calculando a distancia ate a posicao correta
                        j_real = (matriz_tabuleiro[i+1][j_aux]%tam_solucao)-1
                        if j_real < 0:
                            j_real = tam_solucao-1
                        if(i_real != i+1 or j_real != j_aux):
                            verifica_linha_2 = 1
                    if(verifica_linha_2 == 0):
                        if(vetor[1] == 0):
                            print("+ BATATA")
                            vetor[1]=1
                            dif = dif + 5
                    else:
                        if(vetor[1]==1):
                            print("- BATATA")
                            vetor[1] = 0
                            dif = dif - 5        
                    
                elif(verifica_coluna == 1):
                    if(vetor[0]==1):
                        print("- BATATA")
                        vetor[0] = 0
                        dif = dif - 5
            else:
                verifica_linha = 1
                verifica_coluna = 1
                verifica_linha_2 = 1
                verifica_coluna_2 = 1"""    
    
    return dif,vetor
        
def controlar_estado_jogador(player):
    esquerda = 0
    direita = 0
    cima = 0
    baixo = 0
    saida_rede = []
    entrada = []
    for i in range(player.tabuleiro.linhas):
        for j in range(player.tabuleiro.colunas):
            entrada.append(player.tabuleiro.posicoes[i][j])
            
    player.cerebro.copiar_para_entrada(entrada)
    player.cerebro.calcular_saida()
    saida_rede = player.cerebro.copiar_saida()
    
    saida_rede = softmax_with_noise(saida_rede,noise_scale)
    
    if(saida_rede[0] == 1):
        esquerda = 1
    else:
        esquerda = 0
    if(saida_rede[1] == 1):
        direita = 1
    else:
        direita = 0
    if(saida_rede[2] == 1):
        cima = 1
    else:
        cima = 0
    if(saida_rede[3] == 1):
        baixo = 1
    else:
        baixo = 0
        
    if(esquerda == 1):
        player.peca_pra_esquerda()
    if(direita == 1):
        player.peca_pra_direita()
    if(cima == 1):
        player.peca_pra_cima()
    if(baixo == 1):
        player.peca_pra_baixo()
    
    if(player.energia == 0):
        player.estado = 1
    else:
        player.fitness,player.vet_encaixe = fitness(player.tabuleiro,player.vet_encaixe)
        if(player.fitness == 0):
            player.estado = 2
    
    #print("PLAYER :",player.cerebro.camadas_escondidas[0].neuronios[0].peso)
    #player.tabuleiro.printa_tabuleiro()
    #print(saida_rede)
    return player

def gerar_dna(quant_pesos):
    dna_vet = []
    for i in range(0,quant_pesos):
        dna_vet.append(random.randint(0,2000)-1000)
    
    return dna_vet
        
def inicializar_jogo(tamanhoGeracao,tamanhoTabuleiro):
    lista_players = []
    gen = Geracao(tamanhoGeracao,lista_players,0,0,0)
    gen.players = []
    vetor_dna = []
    tamanho_dna = 0
    dna = DNA(vetor_dna,tamanho_dna)
    dna.vetorDNA = []
    matriz = []
    vet_encaixe = []
    tabuleiro = Tabuleiro(tamanhoTabuleiro,tamanhoTabuleiro,matriz)
    #Inicializando jogadores
    for i in range(0,tamanhoGeracao):
        cerebro = criar_rede_neural(1,tamanhoTabuleiro*tamanhoTabuleiro,tamanhoTabuleiro*tamanhoTabuleiro,4)
        gen.players.append(Jogador(tabuleiro,copy.deepcopy(dna),cerebro,0,-50,50,copy.deepcopy(vet_encaixe)))
        #gen.players[i].DNA.vetorDNA = gerar_dna(tamanho_dna)
        #gen.players[i].cerebro.copiar_vetor_para_camadas
    gen.range_random = gen.players[0].cerebro.quantidade_pesos
    return gen
    
def inicializar_geracao(geracao,dna_modificado):
    geracao.gen_atual += 1
    tamanho_dna = geracao.players[0].cerebro.quantidade_pesos()
    geracao.media_fitness = 0
    tam_tab = geracao.players[0].tabuleiro.linhas
    fit = 0
    vet = [0,0]
    #Gerar tabuleiro aleatorio para os individuos da geracao
    while (fit >= -16):
        numeros = list(range(tam_tab*tam_tab))
        random.shuffle(numeros)
        matriz = np.array(numeros).reshape((tam_tab, tam_tab))
        tabuleiro = Tabuleiro(tam_tab,tam_tab,matriz)
        fit,vet = fitness(tabuleiro,vet)
    #print("TABULEIRO INICIAL: \n",matriz)
    #print("FITNESS DO TABULEIRO INICIAL: ",fit)
    
    #instanciando tabuleiro e DNAS para os individuos da geracao
    for i in range(0,geracao.quantidade_jogadores):
        if(geracao.gen_atual == 1):
            #print("BATATA")
            geracao.players[i].DNA.vetorDNA = gerar_dna(tamanho_dna)
            
        else:
            geracao.players[i].DNA.vetorDNA = dna_modificado[i].vetorDNA
            
        
        
        geracao.players[i].DNA.tamanhoDNA = tamanho_dna
        #print(geracao.players[0].cerebro.camadas_escondidas[0].neuronios[0].peso)
        geracao.players[i].cerebro.copiar_vetor_para_camadas(geracao.players[i].DNA.vetorDNA)
        geracao.players[i].tabuleiro = copy.deepcopy(tabuleiro)
        geracao.players[i].estado = 0
        geracao.players[i].energia = 200
        geracao.players[i].fitness = -50
        geracao.players[i].vet_encaixe = [0,0]
    if(geracao.gen_atual == 1):
        geracao.range_random = tamanho_dna
    else:
        geracao.range_random = geracao.range_random * 0.99
        if(geracao.range_random < 20):
            geracao.range_random = 20
            
    """print("VETOR DE DNA DO PLAYER 0: ",geracao.players[0].DNA.vetorDNA)
    for i in range(0,geracao.players[0].cerebro.quantidade_camadas_escondidas):
        for j in range(0,geracao.players[0].cerebro.camadas_escondidas[i].quantidade_neuronios):
            print("PESOS PRIMEIRO NEURONIO ",j,"NA CAMADA",i,": ",geracao.players[0].cerebro.camadas_escondidas[i].neuronios[j].peso)
    
    for i in range(0,geracao.players[0].cerebro.camada_saida.quantidade_neuronios):
        print("PESOS PRIMEIRO NEURONIO ",i,"NA CAMADA DE SAIDA: ",geracao.players[0].cerebro.camada_saida.neuronios[i].peso)"""
    
    return geracao

def treinar_geracao(geracao):
    contador_mortos = 0
    terminado = 0
    j=0
    melhor_fitness = -50
    melhor_jogador = 0
    while (contador_mortos < geracao.quantidade_jogadores and j < 1000):
        for i in range(0,geracao.quantidade_jogadores):
            if(geracao.players[i].estado == 0):
                geracao.players[i] = controlar_estado_jogador(geracao.players[i])
                if(geracao.players[i].estado==1):
                    geracao.players[i].fitness,geracao.players[i].vet_encaixe = fitness(geracao.players[i].tabuleiro,geracao.players[i].vet_encaixe)
                    geracao.media_fitness = geracao.media_fitness + geracao.players[i].fitness
                    if(melhor_fitness < geracao.players[i].fitness):
                        melhor_fitness = geracao.players[i].fitness
                        melhor_jogador = i
                    
                    contador_mortos +=1
                if(geracao.players[i].estado == 2):
                    print("INDIVIDUO IDEAL ENCONTRADO")
                    geracao.media_fitness = geracao.media_fitness + geracao.players[i].fitness
                    geracao.players[i].fitness = fitness(geracao.players[i].tabuleiro)
                    melhor_jogador = i
                    terminado = 1
              
        #print("ITERACAO: ",j,"MELHOR FITNESS :",melhor_fitness)
        j+=1
    geracao.media_fitness = geracao.media_fitness / geracao.quantidade_jogadores
    return geracao,terminado,melhor_jogador

def mutacoes_aleatorias(melhor_dna,quantidade_individuos,range_random):
    dna_modificado = []
    #Realizando clonagem do melhor DNA para todos os individuos
    for i in range(0,quantidade_individuos):
        dna_modificado.append(DNA(copy.deepcopy(melhor_dna.vetorDNA),melhor_dna.tamanhoDNA))
    
    #print("DENTRO DA FUNCAO: ",dna_modificado[0].vetorDNA)
    #Aplicando mutacoes aleatorias sobre os DNAs dos individuos    
    for j in range(1,quantidade_individuos):
        mutacoes = random.randint(1,math.trunc(range_random))
        for k in range(0,mutacoes):
            tipo = random.randint(0,2)
            indice = random.randint(0,melhor_dna.tamanhoDNA-1)
            if(tipo == 0):
                dna_modificado[j].vetorDNA[indice] = random.randint(0,20000)/10 - 1000 #Coloca um valor aleatorio
            elif(tipo == 1):
                number = (random.randint(0,10000)/20000)+ 0.3
                dna_modificado[j].vetorDNA[indice] = dna_modificado[j].vetorDNA[indice] * number #Multiplicacao aleatoria
            else:
                number = (random.randint(0,20000)/10 - 1000) / 100
                dna_modificado[j].vetorDNA[indice] = dna_modificado[j].vetorDNA[indice] + number #Soma aleatoria
    
    #print("DENTRO DA FUNCAO DEPOIS: ",dna_modificado[0].vetorDNA)    
    return dna_modificado

def algoritmo_genetico(quantidade_geracoes,quantidade_individuos,tamanho_tabuleiro):
    fit_melhor_sempre = -50
    melhor_sempre = 0
    dna_modificado = []
    vet = [0,0]
    gen = inicializar_jogo(quantidade_individuos,tamanho_tabuleiro)
    for i in range(0,quantidade_geracoes):
        melhor_sempre = 0
        
        if(i > 0):
            dna_modificado = mutacoes_aleatorias(melhor_dna,quantidade_individuos,gen.range_random)
        gen = inicializar_geracao(gen,dna_modificado)
        print("GERACAO :",gen.gen_atual)
        print("TABULEIRO INICIAL DA GERACAO")
        gen.players[0].tabuleiro.printa_tabuleiro()
        fitness_tabuleiro,vet = fitness(gen.players[0].tabuleiro,vet)
        print("FITNESS DO TABULEIRO: ",fitness_tabuleiro)
        gen,terminado,melhor = treinar_geracao(gen)
        
        print("MEDIA DA GERACAO: ",gen.media_fitness)
        print("FITNESS DO MELHOR DE TODOS: ",fit_melhor_sempre,"INDIVIDUO :",melhor_sempre)
        print("MELHOR INDIVIDUO: ",melhor," COM FITNESS: ",gen.players[melhor].fitness)
        print("TABULEIRO FINAL DO MELHOR INDIVIDUO")
        gen.players[melhor].tabuleiro.printa_tabuleiro()
       
        print("------------------------------------------------------")
        
        if(fit_melhor_sempre < gen.players[melhor].fitness):
            melhor_sempre = melhor
            fit_melhor_sempre = gen.players[melhor].fitness
        print(gen.players[melhor_sempre].DNA.vetorDNA)
        melhor_dna = gen.players[melhor_sempre].DNA
        if (terminado == 1):
            return gen
    print(gen.players[melhor_sempre].DNA.vetorDNA)
    return gen,melhor_sempre
        
        
    
    
"""vetorDna = [1,2,3]
dna = DNA(vetorDna)
matriz = [[1,2,3],[0,5,6],[4,8,7]]
n=3
tabuleiro = Tabuleiro(n,n,matriz)
cerebro = criar_rede_neural(1,3,3,1)
player = Jogador(tabuleiro,dna,cerebro)
player.tabuleiro.printa_tabuleiro()
player.peca_pra_cima()
player.tabuleiro.printa_tabuleiro()"""

        
        