
def adj_to_all(u, vtx_set, l):
    for v in vtx_set:
        coincidence = sum(u[i] == v[i] for i in range(len(u)))
        if coincidence != l:
            return False
        
    return True


def find_l1_clique(k):
    matrix = [[(i,)*(k-1) for i in range(1, k)]]
        
    def forbidden(el, pos, m, i):

        indxs = []

        for i_lin in range(i):
            for j_lin in range(k-1):
                if m[i_lin][j_lin][pos] == el:
                    indxs.append((i_lin, j_lin))
        
        return set(indxs)


    def rec_build_tup(tup, m, fbd_indx):

        if len(tup) == k-1:
            vtx_set = [t for lin in m[:-1] for t in lin]

            if adj_to_all(tup, vtx_set, 1):
                yield tup
        
        else:
            pos = len(tup)

            i = len(m)-1
            lin = m[i]
            j = len(lin)

            in_same_lin = {t[pos] for t in lin}
            fbd_elems = {m[i_lin][j_lin][pos] for i_lin, j_lin in fbd_indx}.union(in_same_lin).union(set(tup))

            for x in (set(range(1, k)) - fbd_elems):
                
                yield from rec_build_tup(tup+(x,), m, fbd_indx.union(forbidden(x, pos, m, i)))


    def rec_build_lin(lin, m):
        if len(lin) == k-1:
            yield lin
        
        else:
            i = len(m)
            j = len(lin)

            init_tup = (j+1, ) if j != 0 else ((1, i+1) if i != 1 else tuple(range(1, k-1)))

            frb = forbidden(j+1, 0, m, i)
            frb = frb.union(forbidden(i+1, 1, m, i)) if j==0 else frb

            for tup in rec_build_tup( init_tup, m + [lin], frb):
                print(f'lin {len(m)} = {lin+[tup]}')
                yield from rec_build_lin(lin + [tup], m)
    

    def rec_build_mtx(m):
        if len(m) == k-1:
            print(f'MATRIZ FINALIZADA')
            return m
        
        else:
            for lin in rec_build_lin([], m):
                result = rec_build_mtx(m+[lin])
                if result:
                    return result
                
                print(f'VOLTA')

    print(f"CONSTRUINDO MATRIZ:")
    return rec_build_mtx(matrix)




if __name__=='__main__':
    
    import sys

    if len(sys.argv) >= 2:
        k = int(sys.argv[1])

    m = find_l1_clique(k)

    if m:
        for lin in m:
            print(lin)
    
    else:
        print("MATRIZ NÃO ENCONTRADA")
    