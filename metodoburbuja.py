def metodoBurbuja(lista):
    cota = len(lista) - 1
    k=1
    while k != -1:
        k=-1
        for i in range(cota):
            if lista[i] > lista[i+1]:
                aux=lista[i]
                lista[i]=lista[i+1]
                lista[i+1]=aux
                k=i
        cota=k
    return lista




