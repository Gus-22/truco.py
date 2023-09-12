import random

class Truco:
    def __init__(self):
        self.rodada = 1
        self.baralho = self.criar_baralho()
        self.primeira_rodada = True
        self.placar_jogador1 = 0
        self.placar_jogador2 = 0
        self.mao1 = []
        self.mao2 = []
        self.jogador1_pontos = 0
        self.jogador2_pontos = 0
        self.envido_pedidos = False
        self.pedido_real_envido = False
        self.pedido_falta_envido = False
        self.pedido_flor = False
        self.truco_pontos = 1
        self.truco_ativo = False
        self.cartas_jogadas = {'Jogador 1': None, 'Jogador 2': None}
        self.resultado_contra_flor = None


    def criar_baralho(self):
        hierarquia_cartas = {
            '4 de Espadas': 1,
        '4 de Bastos': 1,
        '4 de Copas': 1,
        '4 de Ouros': 1,
        '5 de Espadas': 2,
        '5 de Ouros': 2,
        '5 de Copas': 2,
        '5 de Bastos': 2,
        '6 de Copas': 3,
        '6 de Ouros': 3,
        '6 de Espadas': 3,
        '6 de Bastos': 3,
        '7 de Copas': 4,
        '7 de Bastos': 4,
        '10 de Espadas': 5,
        '10 de Copas': 5,
        '10 de Ouros': 5,
        '10 de Bastos': 5,
        '11 de Copas': 6,
        '11 de Ouros': 6,
        '11 de Espadas': 6,
        '11 de Bastos': 6,
        '12 de Ouros': 7,
        '12 de Espadas': 7,
        '12 de Copas': 7,
        '12 de Bastos': 7,
        '1 de Copas': 8,
        '1 de Ouros': 8,
        '2 de Copas': 9,
        '2 de Espadas': 9,
        '2 de Bastos': 9,
        '2 de Ouros': 9,
        '3 de Ouros': 10,
        '3 de Espadas': 10,
        '3 de Bastos': 10,
        '3 de Copas': 10,
        '7 de Ouros': 11,
        '7 de Espadas': 12,
        '1 de Bastos': 13,
        '1 de Espada': 15,
                }
        baralho = [{'valor': carta.split(' de ')[0], 'naipe': carta.split(' de ')[1]} for carta in hierarquia_cartas.keys()]
        random.shuffle(baralho)
        return baralho
    
    def distribuir_cartas(self):
        self.mao1 = self.baralho[:3]
        self.mao2 = self.baralho[3:6]
        self.baralho = self.baralho[6:]

    def mostrar_mao(self):
        print("Mão do Jogador 1:")
        for carta in self.mao1:
            print(f"{carta['valor']} de {carta['naipe']}")
        print("\nMão do Jogador 2:")
        for carta in self.mao2:
            print(f"{carta['valor']} de {carta['naipe']}")
    
    def verificar_flor(self, mao):
        naipes = set(carta['naipe'] for carta in mao)
        return len(naipes) == 1

    def flor(self):
        if self.primeira_rodada:
            jogador1_tem_flor = self.verificar_flor(self.mao1)
            jogador2_tem_flor = self.verificar_flor(self.mao2)

            if jogador1_tem_flor and not jogador2_tem_flor:
                print("Jogador 1 canta Flor e ganha 3 pontos!")
                self.pedido_flor = True
                self.placar_jogador1 += 3
            elif jogador2_tem_flor and not jogador1_tem_flor:
                print("Jogador 2 canta Flor e ganha 3 pontos!")
                self.pedido_flor = True
                self.placar_jogador2 += 3
            elif jogador1_tem_flor and jogador2_tem_flor:
                print("Ambos os jogadores têm Flor. Iniciando Contra Flor.")
                total_jogador1 = self.calcular_total_flor(self.mao1)
                total_jogador2 = self.calcular_total_flor(self.mao2)
                
                if total_jogador1 > total_jogador2:
                    print("Jogador 1 ganha a Contra Flor e ganha 6 pontos!")
                    self.placar_jogador1 += 6
                    self.resultado_contra_flor = "Jogador 1"
                elif total_jogador2 > total_jogador1:
                    print("Jogador 2 ganha a Contra Flor e ganha 6 pontos!")
                    self.placar_jogador2 += 6
                    self.resultado_contra_flor = "Jogador 2"
                else:
                    print("Contra Flor empatada. Nenhum jogador ganha pontos.")
                    self.resultado_contra_flor = "Empate"
            else:
                print("Nenhum jogador tem Flor. A rodada continua.")
                self.pedido_flor = False
    

    def calcular_pontos_envido(self, mao):
        pontos = 0
        naipes = {}

        for carta in mao:
            valor = carta['valor']
            naipe = carta['naipe']

            if valor in ['10', '11', '12']:
                continue  # Cartas com figuras valem zero pontos

            pontos += int(valor)

            if naipe in naipes:
                naipes[naipe] += 1
            else:
                naipes[naipe] = 1

        # Verifique se há duas cartas do mesmo naipe para adicionar a bonificação de 20 pontos
        for naipe, quantidade in naipes.items():
            if quantidade >= 2:
                pontos += 20
                break

        return pontos

    def pedir_envido(self):
        if self.pedido_flor:
            print("Envido não pode ser pedido após Flor.")
        elif self.primeira_rodada and not self.mao1 and not self.mao2 and not self.pedido_flor:
            print("Jogador 1 pede Envido.")
            pontos_jogador1 = self.calcular_pontos_envido(self.mao1)
            pontos_jogador2 = self.calcular_pontos_envido(self.mao2)

            if random.randint(0, 1):  # 50% de chance de pedir envido se tiver mais de 23 pontos
                print("Jogador 2 aceita o Envido.")
                if pontos_jogador1 > pontos_jogador2:
                    print("Jogador 1 ganha o Envido e 2 pontos!")
                    self.jogador1_pontos += 2
                else:
                    print("Jogador 2 ganha o Envido e 2 pontos!")
                    self.jogador2_pontos += 2
                self.envido_pedidos = True  # Atualiza a variável de controle

    def pedir_real_envido(self):
        if self.primeira_rodada and not self.mao1 and not self.mao2 and self.envido_pedidos:
            print("Jogador 1 pede Real Envido.")
            pontos_jogador1 = self.calcular_pontos_envido(self.mao1)
            pontos_jogador2 = self.calcular_pontos_envido(self.mao2)

            if random.randint(0, 3) == 0:  # 30% de chance de pedir Real envido se tiver mais de 25 pontos
                print("Jogador 2 aceita o Real Envido.")
                if pontos_jogador1 > pontos_jogador2:
                    print("Jogador 1 ganha o Real Envido e 5 pontos!")
                    self.jogador1_pontos += 5
                    self.pedido_real_envido = True
                else:
                    print("Jogador 2 ganha o Real Envido e 5 pontos!")
                    self.jogador2_pontos += 5
                    self.pedido_real_envido = True
    

    def pedir_falta_envido(self):
        if self.primeira_rodada and not self.mao1 and not self.mao2 and not self.pedido_real_envido and self.envido_pedidos:
            print("Jogador 1 pede Falta Envido.")
            pontos_jogador1 = self.calcular_pontos_envido(self.mao1)
            pontos_jogador2 = self.calcular_pontos_envido(self.mao2)
            
            if pontos_jogador1 + pontos_jogador2 >= 29:
                if random.randint(0, 3) == 0:  # 25% de chance de aceitar se a soma for 29 ou mais
                    print("Jogador 2 aceita a Falta Envido. Jogador 1 ganha a 'Falta'.")
                    self.jogador1_pontos += 99
                else:
                    print("Jogador 2 foge da Falta Envido. Nenhum jogador ganha pontos.")
            else:
                print("A soma das cartas não é 29 ou mais. Jogador 1 ganha a 'Falta'.")
                self.jogador1_pontos += 99

    def jogar_auto(self):
            print(f"Rodada {self.rodada}")
            self.distribuir_cartas()
            self.mostrar_mao()
            
            if self.rodada == 1:
                self.flor()
                if not self.pedido_flor:
                    self.pedir_envido()
            
            if self.rodada > 1:
                self.pedir_truco()
            
            if self.rodada <= 3:
                self.fazer_jogada_jogador_auto("Jogador 1")
                self.fazer_jogada_jogador_auto("Jogador 2")

            # Lógica adicional do jogo aqui...

            self.rodada += 1

    def fazer_jogada_jogador_auto(self, jogador):
        # Implemente a lógica para a jogada automática do jogador
        mao = self.mao1 if jogador == "Jogador 1" else self.mao2

        if self.rodada > 1:
            # Pode adicionar lógica para fazer jogadas de Truco aqui
            pass
        else:
            if not self.pedido_flor:
                if self.verificar_cartas_para_truco(mao):
                    self.pedir_truco()
                else:
                    # Lógica para jogar carta normalmente
                    carta_a_jogar = self.escolher_carta_auto(mao)
                    self.cartas_jogadas[jogador] = carta_a_jogar
                    print(f"{jogador} jogou: {carta_a_jogar}")
            else:
                # Lógica para jogar carta caso tenha pedido envido
                pass

    def escolher_carta_auto(self, mao):
        # Implemente a lógica para escolher uma carta automaticamente
        # Você pode usar uma estratégia simples, como jogar a carta de maior valor
        # Certifique-se de ajustar essa lógica de acordo com suas regras específicas
        carta_a_jogar = random.choice(mao)
        return carta_a_jogar
    
    def pedir_truco(self):
        if not self.truco_ativo and not self.pedido_flor:
            print("Jogador 1 pede Truco!")
            if random.randint(0, 1):  # 50% de chance de aceitar o Truco
                print("Jogador 2 aceita o Truco!")
                self.truco_ativo = True
                self.truco_pontos = 2  # Pontos do Truco
            else:
                print("Jogador 2 recusa o Truco!")
                self.placar_jogador1 += self.truco_pontos
                print(f"Jogador 1 ganha {self.truco_pontos} pontos!")

    def determinar_vencedor(self, carta1, carta2):
        hierarquia_cartas = {
            '4 de Espadas': 1,
            '4 de Bastos': 1,
            '4 de Copas': 1,
            '4 de Ouros': 1,
            '5 de Espadas': 2,
            '5 de Ouros': 2,
            '5 de Copas': 2,
            '5 de Bastos': 2,
            '6 de Copas': 3,
            '6 de Ouros': 3,
            '6 de Espadas': 3,
            '6 de Bastos': 3,
            '7 de Copas': 4,
            '7 de Bastos': 4,
            '10 de Espadas': 5,
            '10 de Copas': 5,
            '10 de Ouros': 5,
            '10 de Bastos': 5,
            '11 de Copas': 6,
            '11 de Ouros': 6,
            '11 de Espadas': 6,
            '11 de Bastos': 6,
            '12 de Ouros': 7,
            '12 de Espadas': 7,
            '12 de Copas': 7,
            '12 de Bastos': 7,
            '1 de Copas': 8,
            '1 de Ouros': 8,
            '2 de Copas': 9,
            '2 de Espadas': 9,
            '2 de Bastos': 9,
            '2 de Ouros': 9,
            '3 de Ouros': 10,
            '3 de Espadas': 10,
            '3 de Bastos': 10,
            '3 de Copas': 10,
            '7 de Ouros': 11,
            '7 de Espadas': 12,
            '1 de Bastos': 13,
            '1 de Espada': 15,
        }

        carta1_nome = f"{carta1['valor']} de {carta1['naipe']}"
        carta2_nome = f"{carta2['valor']} de {carta2['naipe']}"

        if hierarquia_cartas[carta1_nome] > hierarquia_cartas[carta2_nome]:
            return 1
        elif hierarquia_cartas[carta1_nome] < hierarquia_cartas[carta2_nome]:
            return 2
        else:
            return 0  # Empate 

    def calcular_pontos_envido(self, mao):
        pontos = 0
        naipes = {}

        for carta in mao:
            valor = carta['valor']
            naipe = carta['naipe']

            if valor in ['10', '11', '12']:
                continue  # Cartas com figuras valem zero pontos

            pontos += int(valor)

            if naipe in naipes:
                naipes[naipe] += 1
            else:
                naipes[naipe] = 1

        # Verifique se há duas cartas do mesmo naipe para adicionar a bonificação de 20 pontos
        for naipe, quantidade in naipes.items():
            if quantidade >= 2:
                pontos += 20
                break

        return pontos

    def jogar_auto(self):
        print(f"Rodada {self.rodada}")
        self.distribuir_cartas()
        self.mostrar_mao()
        
        if self.rodada == 1:
            self.flor()
            if not self.pedido_flor:
                self.pedir_envido()
        
        if self.rodada > 1:
            self.pedir_truco()
        
        if self.rodada <= 3:
            self.fazer_jogada_jogador_auto("Jogador 1")
            self.fazer_jogada_jogador_auto("Jogador 2")

        self.rodada += 1

    def fazer_jogada_jogador_auto(self, jogador):
        mao = self.mao1 if jogador == "Jogador 1" else self.mao2

        if self.rodada > 1:
            # Pode adicionar lógica para fazer jogadas de Truco aqui
            pass
        else:
            if not self.pedido_flor:
                if self.verificar_cartas_para_truco(mao):
                    self.pedir_truco()
                else:
                    carta_a_jogar = self.escolher_carta_auto(mao)
                    self.cartas_jogadas[jogador] = carta_a_jogar
                    print(f"{jogador} jogou: {carta_a_jogar}")
            else:
                # Lógica para jogar carta caso tenha pedido envido
                pass

    def escolher_carta_auto(self, mao):
        # Implemente a lógica para escolher uma carta automaticamente
        # Neste exemplo, estamos jogando aleatoriamente
        carta_a_jogar = random.choice(mao)
        return carta_a_jogar

    def verificar_cartas_para_truco(self, mao):
        # Implemente a lógica para verificar se um jogador pode pedir Truco
        # Aqui, você pode adicionar suas próprias regras específicas
        # por exemplo, verificar se o jogador possui um 4 ou um 7 para pedir Truco
        for carta in mao:
            if carta['valor'] in ['4', '7']:
                return True
        return False

if __name__ == "__main__":
    jogo = Truco()
    while jogo.rodada <= 3:
        jogo.jogar_auto()
        
if __name__ == "__main__":
    jogo = Truco()
    while jogo.rodada <= 3:
        jogo.jogar()
