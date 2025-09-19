CELLS = [1, 3, 4, 7, 9, 12, 13, 16, 19, 21,
  27, 28, 31, 36, 37, 39, 43, 48, 49, 52,
  57, 61, 63, 64, 67, 73, 75, 76, 79, 84,
  91, 93, 97, 108, 109, 111, 112, 117, 124, 127,
  129, 133, 139, 147, 148, 157, 163, 169, 171, 172]

ABC = ["A", "B", "C"]

def numeros_rombicos(cantidad):
    numeros = set()
    limite = 50  # valor máximo aproximado para i y j, lo ajustamos si hace falta
    for i in range(limite):
        for j in range(limite):
            n = i**2 + i*j + j**2
            if n > 0:  
                numeros.add(n)
    return sorted(numeros)[:cantidad]

# Obtener los primeros 50
numbers = numeros_rombicos(50)
#print(numbers)
