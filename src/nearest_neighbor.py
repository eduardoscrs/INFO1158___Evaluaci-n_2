"""
Heurística del Vecino Más Cercano para el TSP.
Algoritmo greedy con complejidad O(n²) que construye una solución aproximada.
"""
import time


def vecino_mas_cercano(ciudades, matriz_dist, ciudad_inicio=0, verbose=True):
    """
    Implementa la heurística del Vecino Más Cercano (Nearest Neighbor).
    
    Algoritmo:
    1. Comenzar en ciudad_inicio
    2. Mientras queden ciudades sin visitar:
       - Ir a la ciudad no visitada más cercana
    3. Regresar a ciudad_inicio
    
    Args:
        ciudades: Lista de ciudades
        matriz_dist: Matriz de distancias
        ciudad_inicio: Índice de la ciudad inicial (default: 0)
        verbose: Si True, muestra el proceso paso a paso
    
    Returns:
        dict: Contiene 'ciclo', 'longitud', 'tiempo_ejecucion' e 'historial' (para visualización)
    """
    n = len(ciudades)
    inicio_tiempo = time.time()
    
    # Inicializar
    visitadas = [False] * n
    ciclo = [ciudad_inicio]
    visitadas[ciudad_inicio] = True
    longitud_total = 0.0
    historial = []  # Para visualización
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"HEURÍSTICA DEL VECINO MÁS CERCANO")
        print(f"{'='*60}")
        print(f"Ciudad inicial: {ciudades[ciudad_inicio]['nombre']}")
        print(f"Ciudades totales: {n}")
        print(f"{'='*60}\n")
    
    ciudad_actual = ciudad_inicio
    
    # Construir el ciclo
    for paso in range(n - 1):
        mejor_distancia = float('inf')
        mejor_ciudad = None
        
        # Buscar la ciudad no visitada más cercana
        for ciudad in range(n):
            if not visitadas[ciudad]:
                distancia = matriz_dist[ciudad_actual][ciudad]
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_ciudad = ciudad
        
        # Viajar a la ciudad más cercana
        ciclo.append(mejor_ciudad)
        visitadas[mejor_ciudad] = True
        longitud_total += mejor_distancia
        
        if verbose:
            print(f"Paso {paso + 1}: {ciudades[ciudad_actual]['nombre']} → "
                  f"{ciudades[mejor_ciudad]['nombre']} (distancia: {mejor_distancia:.4f})")
        
        # Guardar estado para visualización
        historial.append({
            'ciclo_parcial': ciclo.copy(),
            'ciudad_origen': ciudad_actual,
            'ciudad_destino': mejor_ciudad,
            'distancia': mejor_distancia,
            'longitud_acumulada': longitud_total,
            'paso': paso + 1
        })
        
        ciudad_actual = mejor_ciudad
    
    # Regresar a la ciudad inicial
    distancia_regreso = matriz_dist[ciudad_actual][ciudad_inicio]
    longitud_total += distancia_regreso
    
    if verbose:
        print(f"Paso {n}: {ciudades[ciudad_actual]['nombre']} → "
              f"{ciudades[ciudad_inicio]['nombre']} (distancia: {distancia_regreso:.4f})")
        print(f"\n{'='*60}")
        print(f"SOLUCIÓN HEURÍSTICA ENCONTRADA")
        print(f"{'='*60}")
        print(f"Ciclo πNN: {' → '.join([ciudades[i]['nombre'] for i in ciclo])} → {ciudades[ciudad_inicio]['nombre']}")
        print(f"Longitud LNN: {longitud_total:.4f}")
    
    historial.append({
        'ciclo_parcial': ciclo + [ciudad_inicio],
        'ciudad_origen': ciudad_actual,
        'ciudad_destino': ciudad_inicio,
        'distancia': distancia_regreso,
        'longitud_acumulada': longitud_total,
        'paso': n
    })
    
    tiempo_ejecucion = time.time() - inicio_tiempo
    
    if verbose:
        print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")
        print(f"{'='*60}\n")
    
    return {
        'ciclo': ciclo,
        'longitud': longitud_total,
        'tiempo_ejecucion': tiempo_ejecucion,
        'historial': historial
    }


def vecino_mas_cercano_multi_inicio(ciudades, matriz_dist, verbose=False):
    """
    Ejecuta la heurística NN desde todas las ciudades posibles y retorna la mejor.
    
    Args:
        ciudades: Lista de ciudades
        matriz_dist: Matriz de distancias
        verbose: Si True, muestra resultados de cada inicio
    
    Returns:
        dict: Mejor solución encontrada entre todos los inicios
    """
    n = len(ciudades)
    mejor_solucion = None
    mejor_longitud = float('inf')
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"VECINO MÁS CERCANO - MULTI-INICIO")
        print(f"{'='*60}")
        print(f"Evaluando desde {n} ciudades iniciales diferentes...\n")
    
    for inicio in range(n):
        solucion = vecino_mas_cercano(ciudades, matriz_dist, ciudad_inicio=inicio, verbose=False)
        
        if verbose:
            print(f"Inicio desde {ciudades[inicio]['nombre']:15} → Longitud: {solucion['longitud']:.4f}")
        
        if solucion['longitud'] < mejor_longitud:
            mejor_longitud = solucion['longitud']
            mejor_solucion = solucion
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Mejor solución: Longitud = {mejor_longitud:.4f}")
        print(f"{'='*60}\n")
    
    return mejor_solucion
