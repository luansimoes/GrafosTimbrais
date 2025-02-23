"""
Este módulo contém funções para verificar automorfismos em grafos timbrais e exportar os resultados para uma planilha CSV.

Classes:
    Nenhuma

Funções:
    checar_automorfismo(f, g)
    buscar_automorfismo_entre_pares(u, v, x, y)
    computar_distancia(g, u, v)
    checar_distancia_transitividade(n, k, l)
    formatar_automorfismos(certificado)
    exportar_automorfismos_para_planilha(certificado, nome_arquivo)
"""

from grafo_timbral import GrafoTimbral
import networkx as nx
import pandas as pd


def checar_automorfismo(f, g):
    """
    Determina se uma função f (um dicionário) é um automorfismo de um grafo g.
    Args:
        f (dict): Dicionário que representa a função.
        g (nx.Graph): Grafo.
    Retorna:
        bool: True se f é um automorfismo de g, False caso contrário.
    """
    for v1 in f:
        for v2 in f:

            if not ((g.has_edge(v1, v2) and g.has_edge(f[v1], f[v2])) or 
                    ( (not g.has_edge(v1, v2)) and (not g.has_edge(f[v1], f[v2]))) ):
                return False

    return True

def buscar_automorfismo_entre_pares(g, u, v, x, y):
    """
    Busca um automorfismo entre dois pares de vértices em um grafo timbral.
    Args:
        g (GrafoTimbral): O grafo timbral no qual o automorfismo será buscado.
        u (int): Primeiro vértice do primeiro par.
        v (int): Segundo vértice do primeiro par.
        x (int): Primeiro vértice do segundo par.
        y (int): Segundo vértice do segundo par.
    Retorna:
        dict or bool: Um dicionário representando o automorfismo encontrado, onde as chaves são os vértices do grafo original
                      e os valores são a imagem dos vértice pelo automorfismo. Retorna False se nenhum automorfismo for encontrado.
    """

    n1 = list(g.vizinhos_em_comum(u,v))
    n2 = list(g.vizinhos_em_comum(x,y))

    outros1 = [node for node in g.grafo.nodes if (node not in n1 and node not in [u,v])]
    outros2 = [node for node in g.grafo.nodes if (node not in n2 and node not in [x,y])]

    viz1 = nx.induced_subgraph(g.grafo, n1)
    viz2 = nx.induced_subgraph(g.grafo, n2)

    comp1 = nx.induced_subgraph(g.grafo, outros1)
    comp2 = nx.induced_subgraph(g.grafo, outros2)

    #isomorphism = nx.vf2pp_isomorphism(comp1, comp2)
    automorfismos_complemento = nx.vf2pp_all_isomorphisms(comp1, comp2)

    # Se não há vizinhos em comum, precisamos verificar automorfismos de todo o grafo
    if len(n1) == len(n2) == 0:
        for automorfismo in automorfismos_complemento:
            automorfismo[u] = x
            automorfismo[v] = y

            if checar_automorfismo(automorfismo, g.grafo):
                return automorfismo
        return False
    
    # Se há vizinhos em comum, podemos "encaixar" automorfismos dos subgrafos
    else:
        i=1
        for auto_comp in automorfismos_complemento:
            for automorfismo in nx.vf2pp_all_isomorphisms(viz1, viz2):
                print(f'AUTOMORFISMO {i}')
                for vtx in auto_comp:
                    automorfismo[vtx] = auto_comp[vtx]
                automorfismo[u] = x
                automorfismo[v] = y

                if checar_automorfismo(automorfismo, g.graph):
                    return automorfismo

                i+=1

        return False


def computar_distancia(g, u, v):
    """
    Computa a distância mais curta entre dois nós em um grafo.
    Args:
        g (networkx.Graph): O grafo no qual a distância será calculada.
        u (Tuple): O vértice de origem.
        v (Tuple): O vértice de destino.
    Retorna:
    int ou str: A distância mais curta entre os nós u e v. Se não houver caminho, retorna 'INF'.
    """
    try:
        d = nx.shortest_path_length(g, u, v)
    except:
        d = 'INF'
    return d

def checar_distancia_transitividade(n, k, l):
    """
    Verifica se um Grafo Timbral é distância-transitivo.
    Args:
        n (int): Número de valores admitidos para cada coordenada.
        k (int): Comprimento dos vértices.
        l (int): Índice de coincidência entre vértices adjacentes.
    Retorna:
        dict ou bool: Um dicionário contendo os pares de vértices e seus respectivos automorfismos, 
              caso a distância-transitividade seja verificada. Retorna False se existirem
              pares de vértices à mesma distância para o qual não há automorfismo.
    """

    g = GrafoTimbral(n, k, l)

    # Basta verificar para pares do tipo (0^k, {0^c}{1^(k-c)})
    u = tuple(0 for _ in range(k))

    v_vec = [tuple(0 for _ in range(ic))+tuple(1 for _ in range(k-ic)) for ic in range(k) if not ic==l]

    certificado = dict()

    for i in range(len(v_vec)):
        for j in range(i+1, len(v_vec)):
            d_i = computar_distancia(g.grafo, u, v_vec[i])
            d_j = computar_distancia(g.grafo, u, v_vec[j])
            if d_i == d_j:
                automorfismo = buscar_automorfismo_entre_pares(g, u, v_vec[i], u, v_vec[j])
                if not automorfismo:
                    print(f'Não há automorfismo entre {(u, v_vec[i])} e {(u, v_vec[j])}')
                    return False
                else:
                    print(f'Há automorfismo entre {(u, v_vec[i])} e {(u, v_vec[j])}')
                    certificado[(v_vec[i], v_vec[j])] = automorfismo
            else:
                print(f'Os pares ({u}, {v_vec[i]}) e ({u}, {v_vec[j]}) não estão à mesma distância [{d_i} x {d_j}]')
    
    return certificado

def formatar_automorfismos(certificado):
    """
    Formata os automorfismos de um certificado.
    Args:
        certificado (dict): Um dicionário onde as chaves são pares de vértices e os 
        valores são dicionários de automorfismos.
    Returns:
        dict: Um dicionário formatado onde as chaves são pares e os valores são dicionários de automorfismos ordenados.
    """

    fmt_aut = {}
    for par in certificado:
        pares = []
        for u in certificado[par]:
            str_u = ''.join([str(el) for el in u])
            str_v = ''.join([str(el) for el in certificado[par][u]])
            pares.append((str_u, str_v))
        ords = sorted(pares)
        fmt_aut[par] = dict(ords)
    return fmt_aut


def exportar_automorfismos_para_planilha(certificado, nome_arquivo):
    """
    Exporta os automorfismos formatados para uma planilha CSV.
    Args:
        certificado (dict): Dicionário contendo os automorfismos a serem exportados.
        nome_arquivo (str): Caminho e nome do arquivo CSV onde os dados serão salvos.
    Returns:
        None
    """

    fmt_aut = formatar_automorfismos(certificado)
    df = pd.DataFrame.from_dict(fmt_aut)
    df.to_csv(nome_arquivo)



if __name__=='__main__':


    parametros = [(4,3,1), (3,4,1), (2,5,2), (2,7,3)]

    for n, k, l in parametros:
        certificado = checar_distancia_transitividade(n, k, l)
        exportar_automorfismos_para_planilha(certificado, f'automorfismos_{n}_{k}_{l}.csv')

    

    


