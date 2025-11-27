"""
Módulo para calcular distancias entre ciudades.
Soporta distancia Euclidiana y Haversine.
"""
import math


def distancia_euclidiana(coord1, coord2):
    """
    Calcula la distancia Euclidiana entre dos coordenadas geográficas.
    
    Args:
        coord1: Tupla (latitud, longitud) de la primera ciudad
        coord2: Tupla (latitud, longitud) de la segunda ciudad
    
    Returns:
        float: Distancia Euclidiana en grados
    
    Nota: Esta distancia NO representa kilómetros reales en la superficie terrestre.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


def distancia_haversine(coord1, coord2):
    """
    Calcula la distancia real en kilómetros usando la fórmula de Haversine.
    
    Args:
        coord1: Tupla (latitud, longitud) de la primera ciudad
        coord2: Tupla (latitud, longitud) de la segunda ciudad
    
    Returns:
        float: Distancia en kilómetros sobre la superficie terrestre
    """
    R = 6371.0  # Radio medio de la Tierra en km
    
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def construir_matriz_distancias(ciudades, metodo='euclid'):
    """
    Construye la matriz de distancias D entre todas las ciudades.
    
    Args:
        ciudades: Lista de diccionarios con 'nombre' y 'coords'
        metodo: 'euclid' para distancia euclidiana, 'haversine' para distancia real
    
    Returns:
        list: Matriz n×n con distancias entre todos los pares de ciudades
    """
    metodos = {
        'euclid': distancia_euclidiana,
        'haversine': distancia_haversine
    }
    
    if metodo not in metodos:
        raise ValueError(f"Método desconocido: '{metodo}'. Use 'euclid' o 'haversine'")
    
    func_distancia = metodos[metodo]
    n = len(ciudades)
    matriz = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                matriz[i][j] = 0.0
            else:
                matriz[i][j] = func_distancia(ciudades[i]['coords'], ciudades[j]['coords'])
    
    return matriz


def imprimir_matriz(matriz, ciudades, decimales=2):
    """
    Imprime la matriz de distancias con formato legible.
    
    Args:
        matriz: Matriz de distancias
        ciudades: Lista de ciudades
        decimales: Número de decimales a mostrar
    """
    nombres = [c['nombre'] for c in ciudades]
    ancho = max(len(n) for n in nombres) + 2
    
    # Imprimir cabecera
    print(' ' * ancho, end='')
    for nombre in nombres:
        print(f'{nombre:>12}', end='')
    print()
    
    # Imprimir filas
    for nombre, fila in zip(nombres, matriz):
        print(f'{nombre:<{ancho}}', end='')
        for valor in fila:
            print(f'{valor:>12.{decimales}f}', end='')
        print()
