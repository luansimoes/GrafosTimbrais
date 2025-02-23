import networkx as nx
import random as rd

class GrafoTimbral:
    """
    Classe para representar um Grafo Timbral.
    Attributes:
        n (int): Número de vértices.
        k (int): Número de dimensões.
        l (int): Número de arestas.
        grafo (Optional[nx.Graph]): O grafo construído, se `construir` for True.
    Methods:
        hamiltoniano() -> bool:
            Verifica se o grafo é hamiltoniano.
        construir_grafo() -> nx.Graph:
            Constrói o grafo timbral.
        gerar_vertices() -> Generator[Tuple[int, ...], None, None]:
            Gera os vértices do grafo.
        gerar_vizinhos(vertice: Tuple[int, ...]) -> Generator[Tuple[int, ...], None, None]:
            Gera os vizinhos de um vértice.
        distancia_de_hamming(u: Tuple[int, ...], v: Tuple[int, ...]) -> int:
            Calcula a distância de Hamming entre dois vértices.
        indice_de_coincidencia(u: Tuple[int, ...], v: Tuple[int, ...]) -> int:
            Calcula o índice de coincidência entre dois vértices.
        construir_ciclo_hamiltoniano_binario() -> List[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
            Constrói um ciclo hamiltoniano binário no grafo.
    """


    def __init__(self, n, k, l, construir = True):
        """
        Inicializa a classe GrafoTimbral.
        Args:
            n (int): Número de vértices.
            k (int): Número de dimensões.
            l (int): Número de arestas.
            construir (bool, optional): Se True, constrói o grafo. Default é True.
        """

        self.n = n
        self.k = k
        self.l = l

        self.grafo = self.construir_grafo() if construir else None
    
    @property
    def hamiltoniano(self):
        """
        Verifica se o grafo é hamiltoniano.
        Retorna:
            bool: True se o grafo é hamiltoniano, False caso contrário.
        """
        return not (self.n == 2 and (self.l==0 or (self.k-self.l)%2==0))
    
    def construir_grafo(self):
        """
        Constrói o grafo timbral.
        Retorna:
            nx.Graph: O grafo construído.
        """

        g = nx.Graph()

        for vertice in self.gerar_vertices():
            g.add_node(vertice)
            for vizinho in self.gerar_vizinhos(vertice):
                g.add_edge(vertice, vizinho)

        return g
    
    def gerar_vertices(self):
        """
        Gera os vértices do grafo.
        Retorna:
            Generator[Tuple[int, ...], None, None]: Um gerador de vértices.
        """

        k = self.k
        n = self.n

        def popular_tupla(atual, k_lin):
            if len(atual)==k:
                yield tuple(atual)
            else:
                for x in range(n):
                    yield from popular_tupla(atual + [x], k_lin-1)

        return popular_tupla([], k)
    
    def gerar_vizinhos(self, vertice):
        """
        Gera os vizinhos de um vértice.
        Args:
            vertice (Tuple[int, ...]): O vértice para o qual gerar vizinhos.
        Retorna:
            Generator[Tuple[int, ...], None, None]: Um gerador de vizinhos.
        """

        n = self.n
        k = self.k
        l = self.l

        def vizinhos(vizinho, atual, l_lin):
            if k-atual == l_lin:
                yield tuple(vizinho)

            elif k-atual > l_lin:

                for x in range(n):
                    if x != vizinho[atual]:
                        aux = [y for y in vizinho]
                        aux[atual] = x

                        yield from vizinhos(aux, atual+1, l_lin)

                if l_lin > 0:
                    yield from vizinhos(vizinho, atual+1, l_lin-1)
            
        return vizinhos(vertice, 0, l)
    
    def distancia_de_hamming(self, u, v):
        """
        Calcula a distância de Hamming entre dois vértices.
        Args:
            u (Tuple[int, ...]): O primeiro vértice.
            v (Tuple[int, ...]): O segundo vértice.
        Retorna:
            int: A distância de Hamming entre os vértices.
        """
        assert len(u)==len(v)==self.k, 'Os vértices devem pertencer ao grafo.'
        return sum(u[i] != v[i] for i in range(self.k))
    
    def indice_de_coincidencia(self, u, v):
        """
        Calcula o índice de coincidência entre dois vértices.
        Args:
            u (Tuple[int, ...]): O primeiro vértice.
            v (Tuple[int, ...]): O segundo vértice.
        Retorna:
            int: O índice de coincidência entre os vértices.
        """
        return self.k - self.distancia_de_hamming(u, v)

    def construir_ciclo_hamiltoniano_binario(self):
        """
        Constrói um ciclo hamiltoniano binário no grafo.
        Retorna:
            List[Tuple[Tuple[int, ...], Tuple[int, ...]]]: O ciclo hamiltoniano binário.
        """

        assert self.hamiltoniano and self.n==2, 'O grafo deve ser hamiltoniano e binário.'
        
        def ciclo_complementar(C, limit=self.k):
            C_neg = []

            # u e v são tuplas com k numeros
            for u,v in C:
                u_neg = tuple([1 if x==0 else 0 for x in u[:limit]] + list(u[limit:]))
                v_neg = tuple([1 if x==0 else 0 for x in v[:limit]] + list(v[limit:]))
                C_neg.append((u_neg, v_neg))
            
            return C_neg
        
        def construir_ciclo_base():

            if self.k == 2:       
                return nx.find_cycle(self.grafo)
            
            G = GrafoTimbral(2, self.k - 2, 1)
            C = G.construir_ciclo_hamiltoniano_binario()
            C_neg = ciclo_complementar(C)

            # Choose a random edge to remove
            indice_aresta = rd.randint(0, len(C)-1)

            # Building the paths according to the rule
            P1 = []
            P2_lin = []
            P3 = []
            P4_lin = []

            for i in range(indice_aresta+1, indice_aresta + len(C)):

                w,z = C[i%len(C)]
                w_neg,z_neg = C_neg[(2*indice_aresta-i)%len(C_neg)]

                if sum(w)%2 == 1:
                    P1.append((tuple([1, 1] + [x for x in w]), tuple([0, 0] + [x for x in z])))
                    P2_lin.append((tuple([1, 0] + [x for x in z_neg]), tuple([0, 1] + [x for x in w_neg])))
                    P3.append((tuple([0, 0] + [x for x in w]), tuple([1, 1] + [x for x in z])))
                    P4_lin.append((tuple([0, 1] + [x for x in z_neg]), tuple([1, 0] + [x for x in w_neg])))
                    
                else:  
                    P1.append((tuple([0, 0] + [x for x in w]), tuple([1, 1] + [x for x in z])))
                    P2_lin.append((tuple([0, 1] + [x for x in z_neg]), tuple([1, 0] + [x for x in w_neg])))
                    P3.append((tuple([1, 1] + [x for x in w]), tuple([0, 0] + [x for x in z])))
                    P4_lin.append((tuple([1, 0] + [x for x in z_neg]), tuple([0, 1] + [x for x in w_neg])))
                    
            # Joining the paths
            C_lin = (P1 + [(P1[-1][1], P2_lin[0][0])] + P2_lin + [(P2_lin[-1][1], P3[0][0])] + 
                    P3 + [(P3[-1][1], P4_lin[0][0])] + P4_lin + [(P4_lin[-1][1], P1[0][0])])
                
            return C_lin
        
        def construir_ciclo_geral():

            G = GrafoTimbral(2, self.k - 1, self.l-1)

            C = G.construir_ciclo_hamiltoniano_binario()
            C_neg = ciclo_complementar(C, self.k - 1 - self.l)

            # Escolhe uma aresta aleatória para remover
            indice_aresta = rd.randint(0, len(C)-1)

            # Constrói os caminhos de acordo com a regra
            P1 = []
            P2_lin = []

            for i in range(indice_aresta+1, indice_aresta + len(C)):

                w,z = C[i%len(C)]
                w_neg,z_neg = C_neg[(2*indice_aresta-i)%len(C_neg)]

                P1.append((tuple([0] + [x for x in w]), tuple([0] + [x for x in z])))
                P2_lin.append((tuple([1] + [x for x in z_neg]), tuple([1] + [x for x in w_neg])))

            # Junta os caminhos
            C_lin = (P1 + [(P1[-1][1], P2_lin[0][0])] + P2_lin + [(P2_lin[-1][1], P1[0][0])])

            return C_lin
        

        if self.l==1:
            return construir_ciclo_base()
            
        else:
            return construir_ciclo_geral()
