"""
Búsqueda exhaustiva para el Problema del Viajante (TSP).
Este algoritmo garantiza encontrar la solución óptima pero tiene complejidad O((n-1)!/2).
"""
import time
from itertools import permutations


def calcular_longitud_ciclo(ciclo, matriz_dist):
    """
    Calcula la longitud total de un ciclo Hamiltoniano.
    
    Args:
        ciclo: Lista de índices representando el orden de visita
        matriz_dist: Matriz de distancias entre ciudades
    
    Returns:
        float: Longitud total del ciclo
    """
    longitud = 0.0
    n = len(ciclo)
    
    for i in range(n):
        ciudad_actual = ciclo[i]
        ciudad_siguiente = ciclo[(i + 1) % n]
        longitud += matriz_dist[ciudad_actual][ciudad_siguiente]
    
    return longitud


def busqueda_exhaustiva(ciudades, matriz_dist, verbose=True):
    """
    Encuentra el ciclo Hamiltoniano óptimo mediante búsqueda exhaustiva.
    
    Args:
        ciudades: Lista de ciudades
        matriz_dist: Matriz de distancias
        verbose: Si True, muestra progreso durante la búsqueda
    
    Returns:
        dict: Contiene 'ciclo_optimo', 'longitud_optima', 'tiempo_ejecucion',
              'ciclos_evaluados' y 'historial' (para visualización)
    """
    n = len(ciudades)
    inicio_tiempo = time.time()
    
    # Fijamos la primera ciudad (ciudad 0) para evitar ciclos equivalentes
    # Solo permutamos las ciudades restantes
    indices = list(range(1, n))
    
    mejor_ciclo = None
    mejor_longitud = float('inf')
    ciclos_evaluados = 0
    historial = []  # Para visualización: (ciclo, longitud, es_mejor)
    
    total_permutaciones = 1
    for i in range(1, n):
        total_permutaciones *= i
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"BÚSQUEDA EXHAUSTIVA - TSP")
        print(f"{'='*60}")
        print(f"Ciudades: {n}")
        print(f"Permutaciones a evaluar: {total_permutaciones:,}")
        print(f"{'='*60}\n")
    
    # Generar todas las permutaciones
    for perm in permutations(indices):
        # Construir ciclo completo comenzando desde ciudad 0
        ciclo = [0] + list(perm)
        longitud = calcular_longitud_ciclo(ciclo, matriz_dist)
        ciclos_evaluados += 1
        
        # Actualizar si encontramos un mejor ciclo
        es_mejor = False
        if longitud < mejor_longitud:
            mejor_longitud = longitud
            mejor_ciclo = ciclo.copy()
            es_mejor = True
            
            if verbose and ciclos_evaluados % max(1, total_permutaciones // 20) == 0:
                progreso = (ciclos_evaluados / total_permutaciones) * 100
                print(f"Progreso: {progreso:5.1f}% | Ciclos evaluados: {ciclos_evaluados:,} | "
                      f"Mejor hasta ahora: {mejor_longitud:.4f}")
        
        # Guardar para visualización (solo algunos para no saturar memoria)
        if ciclos_evaluados <= 1000 or es_mejor:
            historial.append({
                'ciclo': ciclo.copy(),
                'longitud': longitud,
                'es_mejor': es_mejor,
                'iteracion': ciclos_evaluados
            })
    
    tiempo_ejecucion = time.time() - inicio_tiempo
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"RESULTADO ÓPTIMO ENCONTRADO")
        print(f"{'='*60}")
        print(f"Ciclo óptimo π⋆: {' → '.join([ciudades[i]['nombre'] for i in mejor_ciclo])} → {ciudades[mejor_ciclo[0]]['nombre']}")
        print(f"Longitud óptima L⋆: {mejor_longitud:.4f}")
        print(f"Ciclos evaluados: {ciclos_evaluados:,}")
        print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")
        print(f"{'='*60}\n")
    
    return {
        'ciclo_optimo': mejor_ciclo,
        'longitud_optima': mejor_longitud,
        'tiempo_ejecucion': tiempo_ejecucion,
        'ciclos_evaluados': ciclos_evaluados,
        'historial': historial
    }


def obtener_ruta_legible(ciclo, ciudades):
    """
    Convierte un ciclo de índices a nombres de ciudades.
    
    Args:
        ciclo: Lista de índices
        ciudades: Lista de ciudades
    
    Returns:
        list: Lista de nombres de ciudades en orden
    """
    return [ciudades[i]['nombre'] for i in ciclo]
