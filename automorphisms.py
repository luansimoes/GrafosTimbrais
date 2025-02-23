from timbral_graph import TimbralGraph
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

N = 4
K = 3
L = 1


def check_iso(iso, g):
    for v1 in iso:
        for v2 in iso:

            if not ((g.has_edge(v1, v2) and g.has_edge(iso[v1], iso[v2])) or 
                    ( (not g.has_edge(v1, v2)) and (not g.has_edge(iso[v1], iso[v2]))) ):
                return False

    return True

def test_dist_trans_pairs(u, v, x, y):

    g = TimbralGraph(N, K, L)

    n1 = list(g.get_common_neighbors(u,v))
    n2 = list(g.get_common_neighbors(x,y))

    other1 = [node for node in g.graph.nodes if (node not in n1 and node not in [u,v])]
    other2 = [node for node in g.graph.nodes if (node not in n2 and node not in [x,y])]

    sub1 = nx.induced_subgraph(g.graph, n1)
    sub2 = nx.induced_subgraph(g.graph, n2)

    comp1 = nx.induced_subgraph(g.graph, other1)
    comp2 = nx.induced_subgraph(g.graph, other2)

    #isomorphism = nx.vf2pp_isomorphism(comp1, comp2)
    isomorphisms = nx.vf2pp_all_isomorphisms(comp1, comp2)

    if len(n1) == len(n2) == 0:
        for isomorphism in isomorphisms:
            isomorphism[u] = x
            isomorphism[v] = y

            if check_iso(isomorphism, g.graph):
                return isomorphism
        return False
    
    else:
        i=1
        for isomorphism in isomorphisms:
            for iso in nx.vf2pp_all_isomorphisms(sub1, sub2):
                print(f'ISO {i}')
                for vtx in isomorphism:
                    iso[vtx] = isomorphism[vtx]
                iso[u] = x
                iso[v] = y

                if check_iso(iso, g.graph):
                    return iso

                i+=1

        return False


def compute_distance(g, u, v):
    try:
        d = nx.shortest_path_length(g, u, v)
    except:
        d = 'INF'
    return d

def test_dist_trans(n, k, l):

    g = TimbralGraph(n, k, l)

    u = tuple(0 for _ in range(k))

    v_vec = [tuple(0 for _ in range(ic))+tuple(1 for _ in range(k-ic)) for ic in range(k) if not ic==l]

    isos = dict()

    for i in range(len(v_vec)):
        for j in range(i+1, len(v_vec)):
            d_i = compute_distance(g.graph, u, v_vec[i])
            d_j = compute_distance(g.graph, u, v_vec[j])
            if d_i == d_j:
                iso = test_dist_trans_pairs(u, v_vec[i], u, v_vec[j])
                if not iso:
                    print(f'Não há isomorfismo entre {v_vec[i]} e {v_vec[j]}')
                    return False
                else:
                    print(f'Há entre {v_vec[i]} e {v_vec[j]}')
                    isos[(v_vec[i], v_vec[j])] = iso
            else:
                print(f'Os pares ({u}, {v_vec[i]}) e ({u}, {v_vec[j]}) não estão à mesma distância [{d_i} x {d_j}]')
    
    return isos


def output_iso_to_file(n, k, l, isos):

    with open(f'iso_{n}_{k}_{l}.txt', 'w') as fl:
        
        keys_1 = sorted(isos.keys())

        for k1 in keys_1:

            fl.write(f'\n\n\n*******ISOMORFISMO {k1}*******\n\n')

            keys_2 = sorted(isos[k1].keys())

            for k2 in keys_2:

                fl.write(f'{k2} : {isos[k1][k2]}\n')


def format_isos(isos):
    fmt_isos = {}
    for par in isos:
        pares = []
        for u in isos[par]:
            str_u = ''.join([str(el) for el in u])
            str_v = ''.join([str(el) for el in isos[par][u]])
            pares.append((str_u, str_v))
        ords = sorted(pares)
        fmt_isos[par] = dict(ords)
    return fmt_isos


def output_isos_to_excel(n, k, l, isos):
    fmt_isos = format_isos(isos)
    df = pd.DataFrame.from_dict(fmt_isos)
    df.to_csv(f'iso_{n}_{k}_{l}.csv')



if __name__=='__main__':

    isos = test_dist_trans(N,K,L)

    output_isos_to_excel(N,K,L, isos)

    

    


