#!/usr/bin/python3

from scipy.optimize import linprog
import sys

def leInputs(inputs):
    # Lê do stdin
    for line in sys.stdin:

        #Coloca os valores em um vetor chamado inputs
        for word in line.split():
            inputs.append(int(word))

    return inputs

def leTarefas(inputs, tarefas):
    #inputs[0] indica a quantidade de tarefas
    quantidadeTarefas = inputs[0]
    i = 2
    k = 0
    # Aloca os valores das tarefas no dicionário tarefas
    while (quantidadeTarefas > 0):
        tarefas['H'+str(k)] = str(inputs[i])
        i += 1
        k += 1
        quantidadeTarefas -= 1

    return tarefas

def leMaquinas(inputs, maquinas):
    # inputs[1] indica a quantidade de máquinas.
    quantidadeMaquinas = inputs[1]
    #inputs[0] indica a quantidade de tarefas.
    quantidadeTarefas = inputs[0]
    i = 2 + quantidadeTarefas
    j = 0
    while (quantidadeMaquinas > 0):
        #Custo
        maquinas['C'+str(j)] = str(inputs[i])
        i += 1

        # Tempo máximo de execução
        maquinas['U'+str(j)] = str(inputs[i])
        i += 1

        j += 1
        quantidadeMaquinas -= 1


    return maquinas

def arrumandoMaquinas(inputs, matriZerada):
    # Indice que indica o início da atribuição de tarefas Ti,j
    i = 2 + inputs[0] + (inputs[1] * 2)

    k = 0
    while(i < len(inputs)):
        j = 0
        aux = inputs[i]
        while(j < aux):
            i += 1
            indice = inputs[i]
            matriZerada[k][indice-1] = 1 # Se a tarefa foi atríbuida, indica o valor de 1
            j += 1

        k += 1
        i += 1

    return matriZerada

# Indica os custos que cada máquina custa e cria a função mínima. Ex: c1 * x1 -> 100 * x1.
def min(matrizAtribuitiva, c, maquinas):
    for i in range(len(matrizAtribuitiva)):
        for j in range(len(matrizAtribuitiva[i])):
            c.append(int(maquinas['C'+str(i)]))
    


    return c

# Indica a 2° restrição da modelagem, em que a soma da coluna precisa ser igual a tarefa
def xizesEQ(matrizAtribuitiva, maquinas, tarefas, a, inputs):
    for i in range(inputs[0]):
        k = 0
        for j in range(inputs[1]):
            a[i][j+k+i] = matrizAtribuitiva[j][i]
            k += 1


    return a

#Indica vetores que precisam ser menores iguais ao tempo máximo de execuçã oda máquina
def xizesUB(matrizAtribuitiva, maquinas, tarefas, a, inputs):
    k = 0
    for i in range(inputs[1]):
        for j in range(inputs[0]):
            a[i][j+k] = matrizAtribuitiva[i][j]
        k += inputs[0]
            
    return a

#Aqui, indica um vetor de tarefas, onde xizesEQ, precisa ser igual aos 
# valores atribuidos nesta função
def restricoesEQ(tarefas, maquinas, B, inputs):
    for i in range(inputs[0]):
        B.append(int(tarefas['H'+str(i)]))

    
    return B

# Indica um vetor de tempo de execução, que vai ser combinado com "xizesUB"
def restricoesUB(tarefas, maquinas, B, inputs):
    for i in range(len(maquinas)//2):
        B.append(int(maquinas['U'+str(i)]))


    return B

def limites(matrizAtribuitiva, bounds):
    k = 0
    for i in range(len(matrizAtribuitiva)):
        for j in range(len(matrizAtribuitiva[i])):
            if matrizAtribuitiva[i][j] == 1:
                globals()['x'+str(k)+'_bounds'] = (0, None)
                bounds.append(globals()['x'+str(k)+'_bounds'])
                k += 1
            else:
                globals()['x'+str(k)+'_bounds'] = (0, 0)
                bounds.append(globals()['x'+str(k)+'_bounds'])
                k += 1


    return bounds

def main():

    #definir tudo como 1 depois, caso não funcione

    inputs = []
    tarefas = {}
    maquinas = {}
    leInputs(inputs)
    matrizAtribuitiva = []
    # Indica qual tarefa, cada máquina vai realizar
    colunas = inputs[0]
    linhas  = inputs[1]
    for i in range(linhas):
        matrizAtribuitiva.append( [0] * colunas)


    tarefas = leTarefas(inputs, tarefas)
    maquinas = leMaquinas(inputs, maquinas)
    matrizAtribuitiva = arrumandoMaquinas(inputs, matrizAtribuitiva)

    # c retorna um vetor do custo mínimo
    c = []
    c = min(matrizAtribuitiva, c, maquinas)
   
    # A_eq indica um vetor que precisa ser igual a outra coisa. Ex a = b.
    # Porém, o A_eq precisa ser igual a quantidade máxima de tarefas
    A_eq = []
    colunas = inputs[0]*inputs[1]
    linhas  = inputs[0]
    for i in range(linhas):
        A_eq.append( [0] * colunas)

    # A_ub indica um vetor que precisa ser menor igual a outra coisa. Ex a <= b.
    # Porém, A_ub precisa ser menor igual a quantidade máxima que uma máquina pode ficar em execução.
    A_ub = []
    colunas = inputs[0]*inputs[1]
    linhas  = ((inputs[0]*inputs[1]) // 2)
    for i in range(linhas):
        A_ub.append( [0] * colunas)

    A_ub = xizesUB(matrizAtribuitiva, maquinas, tarefas, A_ub, inputs)
    A_eq = xizesEQ(matrizAtribuitiva, maquinas, tarefas, A_eq, inputs)

    # Os valores do vetor A_ub precisam ser menores iguais que b_ub. Ex: A_ub[x,y] ; b_ub[k,l]
    #Então, x <= k e y <= k 
    b_ub = []
    b_ub = restricoesUB(tarefas, maquinas, b_ub, inputs)

    # Os valores do vetor A_eq precisam ser iguais que b_eq. Ex: A_ub[x,y] ; b_ub[k,l]
    #Então, x = k e y = k 
    b_eq = []
    b_eq = restricoesEQ(tarefas, maquinas, b_eq, inputs)

    # Os bounds são os limites da modelagem. 
    bounds = []
    bounds = limites(matrizAtribuitiva, bounds)

    res = linprog(c,
                  A_ub=A_ub,
                  b_ub=b_ub,
                  A_eq=A_eq,
                  b_eq=b_eq,
                  bounds=bounds
                  )

    for i in range(len(c)):
        if i % inputs[0] == 0:
           print()
           
        print(f"{res['x'][i]:.1f}", end=' ')

    print("\n")
    print(f"{res['fun']:.1f}")


if __name__=="__main__":
    main()
