import random
taxa_aprendizado = 0.1
peso_inicial = 1
BIAS = 1

def relu(X):
    if(X < 0):
        return 0
    return X

def ativacao_oculta(X):
    return relu(X)

def ativacao_saida(X):
    return relu(X)

class Neuronio:
    def __init__(self,peso,erro,saida,quantidade_ligacoes):
        self.peso = peso
        self.erro = erro
        self.saida = saida
        self.quantidade_ligacoes = quantidade_ligacoes
    
    
class Camada:
    def __init__(self,neuronios,quantidade_neuronios):
        self.neuronios = neuronios
        self.quantidade_neuronios = quantidade_neuronios
        
class RedeNeural:
    def __init__(self,camada_entrada,camadas_escondidas,camada_saida,quantidade_camadas_escondidas):
        self.camada_entrada = camada_entrada
        self.camadas_escondidas = camadas_escondidas
        self.camada_saida = camada_saida
        self.quantidade_camadas_escondidas = quantidade_camadas_escondidas
        
    def copiar_vetor_para_camadas(self,vetor):
        j = 0
        #Passando vetor de DNA para a rede neural
        #print("DENTRO DA FUNCAO VETOR: ",vetor)
        for i in range(0,self.quantidade_camadas_escondidas):
            for k in range(0,self.camadas_escondidas[i].quantidade_neuronios):
                self.camadas_escondidas[i].neuronios[k].peso = []
                for l in range(0,self.camadas_escondidas[i].neuronios[k].quantidade_ligacoes):
                    self.camadas_escondidas[i].neuronios[k].peso.append(vetor[j])
                    j+=1
                    
        for k in range(0,self.camada_saida.quantidade_neuronios):
            self.camada_saida.neuronios[k].peso = []
            for l in range(0,self.camada_saida.neuronios[k].quantidade_ligacoes):
                self.camada_saida.neuronios[k].peso.append(vetor[j])
                j+=1
        #print("DENTRO DA FUNCAO NEURONIO :",self.camadas_escondidas[0].neuronios[0].peso)
        
    def copiar_para_entrada(self,vetor_entrada):
        #print(self.camada_entrada.quantidade_neuronios)
        for i in range(0,self.camada_entrada.quantidade_neuronios - BIAS):
            self.camada_entrada.neuronios[i].saida = vetor_entrada[i]
            
    def quantidade_pesos(self):
        soma = 0 
        for i in range(0,self.quantidade_camadas_escondidas):
            for j in range(0,self.camadas_escondidas[i].quantidade_neuronios):
                soma = soma + self.camadas_escondidas[i].neuronios[j].quantidade_ligacoes
                
        for i in range(0,self.camada_saida.quantidade_neuronios):
            soma = soma + self.camada_saida.neuronios[i].quantidade_ligacoes
            
        return soma
    
    def copiar_saida(self):
        vetor_saida = []
        for i in range(0,self.camada_saida.quantidade_neuronios):
            vetor_saida.append(self.camada_saida.neuronios[i].saida)
            #print(" DENTRO DA FUNCAO",vetor_saida,"QUANTIDADE NEURONIO CAMADA SAIDA",self.camada_saida.quantidade_neuronios)
            
        return vetor_saida 
        
    def calcular_saida(self):
        #Calculando saida entre a camada de entrada e a primeira camada escondida
        for i in range(0,self.camadas_escondidas[0].quantidade_neuronios - BIAS):
            somatorio = 0
            for j in range(0,self.camada_entrada.quantidade_neuronios):
                somatorio = somatorio + self.camada_entrada.neuronios[j].saida * self.camadas_escondidas[0].neuronios[i].peso[j]
                
            self.camadas_escondidas[0].neuronios[i].saida = ativacao_oculta(somatorio)
        #Calculando as saidas entre a camada k e a camada k-1
        for k in range(1,self.quantidade_camadas_escondidas):
            for i in range(0,self.camadas_escondidas[k].quantidade_neuronios - BIAS):
                somatorio = 0
                for j in range(self.camadas_escondidas[k-1].quantidade_neuronios):
                    somatorio = somatorio + self.camadas_escondidas[k-1].neuronios[j].saida * self.camadas_escondidas[k].neuronios[i].peso[j]
                
                self.camadas_escondidas[k].neuronios[i].saida = ativacao_oculta(somatorio)
        #Calculando as saidas entre a ultima camada escondida e a camada de saida
        for i in range(0,self.camada_saida.quantidade_neuronios):
            somatorio = 0
            for j in range(0,self.camadas_escondidas[self.quantidade_camadas_escondidas-1].quantidade_neuronios):
                somatorio = somatorio + self.camadas_escondidas[self.quantidade_camadas_escondidas-1].neuronios[j].saida * self.camada_saida.neuronios[i].peso[j]
                self.camada_saida.neuronios[i].saida = ativacao_saida(somatorio)
                
def criar_neuronio(quantidade_Ligacoes):
    peso = []
    for i in range(0,quantidade_Ligacoes):
        #print("MANDIOCA")
        peso.append(random.randint(0,2000)-1000)
    
    neuron = Neuronio(peso,0,1,quantidade_Ligacoes)
    #print(neuron.peso)
    return neuron

def criar_rede_neural(quantidadeEscondidas,quantidadeNeurioniosEntrada,quantidadeNeuroniosEscondida,quantidadeNeuroniosSaida):
    #print("NABO")
    quantidadeNeurioniosEntrada = quantidadeNeurioniosEntrada + BIAS
    quantidadeNeuroniosEscondida = quantidadeNeuroniosEscondida + BIAS
    #Cria a camada de entrada
    vetor_neuronios = []
    camadaEntrada = Camada(vetor_neuronios,quantidadeNeurioniosEntrada)
    camadaEntrada.neuronios = []
    for i in range(0,quantidadeNeurioniosEntrada):
       camadaEntrada.neuronios.append(criar_neuronio(2))
    #print("QUANTIDADE DE NEURONIOS NA CAMADA DE ENTRADA: ",camadaEntrada.quantidade_neuronios)
    
    
    
    #Cria as camadas escondidas
    camadaEscondida = []
    vetor_neuronios = []
    camadaSaida = Camada(vetor_neuronios,quantidadeNeuroniosSaida)
    camadaSaida.neuronios = []
    #print("CAMADA DE SAIDA")
    for i in range(0,quantidadeNeuroniosSaida):
        #print("NEURONIO",i)
        camadaSaida.neuronios.append(criar_neuronio(quantidadeNeuroniosEscondida))
        #print("DENTRO DA FUNÇAO:",camadaSaida.neuronios[i].peso)
    
    
        
    rede = RedeNeural(camadaEntrada,camadaEscondida,camadaSaida,quantidadeEscondidas)
    rede.camadas_escondidas = []
    for i in range(0,quantidadeEscondidas):
        #print("CAMADA ESCONDIDA ",i)
        vetor_neuronios = []
        rede.camadas_escondidas.append(Camada(vetor_neuronios,quantidadeNeuroniosEscondida))
        rede.camadas_escondidas[i].neuronios = []
        for j in range(0,quantidadeNeuroniosEscondida):
            #print("NEURONIO ",j)
            if (i == 0):
                rede.camadas_escondidas[i].neuronios.append(criar_neuronio(quantidadeNeurioniosEntrada))
            else:
                rede.camadas_escondidas[i].neuronios.append(criar_neuronio(quantidadeNeuroniosEscondida))
        
       
    return rede

#redeneural = criar_rede_neural(6,3,4,1)

#print("FORA DA FUNCAO",redeneural.camadas_escondidas[0].neuronios[3].peso)
                

