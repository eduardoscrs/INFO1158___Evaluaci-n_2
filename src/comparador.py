"""
Módulo para comparar ambos métodos y generar análisis cuantitativo.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def calcular_gap(longitud_nn, longitud_optima):
    """
    Calcula el gap de optimalidad.
    
    Args:
        longitud_nn: Longitud de la solución heurística
        longitud_optima: Longitud de la solución óptima
    
    Returns:
        float: Gap de optimalidad en porcentaje
    """
    return ((longitud_nn - longitud_optima) / longitud_optima) * 100


def comparar_metodos(resultado_exhaustivo, resultado_nn, ciudades, verbose=True):
    """
    Compara los resultados de ambos métodos.
    
    Args:
        resultado_exhaustivo: Diccionario con resultados de búsqueda exhaustiva
        resultado_nn: Diccionario con resultados de vecino más cercano
        ciudades: Lista de ciudades
        verbose: Si True, imprime el análisis completo
    
    Returns:
        dict: Diccionario con todas las métricas de comparación
    """
    # Extraer datos
    long_optima = resultado_exhaustivo['longitud_optima']
    long_nn = resultado_nn['longitud']
    tiempo_exhaustivo = resultado_exhaustivo['tiempo_ejecucion']
    tiempo_nn = resultado_nn['tiempo_ejecucion']
    ciclos_evaluados = resultado_exhaustivo['ciclos_evaluados']
    
    # Calcular métricas
    gap = calcular_gap(long_nn, long_optima)
    speedup = tiempo_exhaustivo / tiempo_nn if tiempo_nn > 0 else float('inf')
    diferencia_absoluta = long_nn - long_optima
    
    comparacion = {
        'n_ciudades': len(ciudades),
        'longitud_optima': long_optima,
        'longitud_nn': long_nn,
        'diferencia_absoluta': diferencia_absoluta,
        'gap_porcentaje': gap,
        'tiempo_exhaustivo': tiempo_exhaustivo,
        'tiempo_nn': tiempo_nn,
        'speedup': speedup,
        'ciclos_evaluados': ciclos_evaluados,
        'ciclo_optimo': resultado_exhaustivo['ciclo_optimo'],
        'ciclo_nn': resultado_nn['ciclo']
    }
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"{'ANÁLISIS COMPARATIVO':^70}")
        print(f"{'='*70}\n")
        
        print(f"{'CONFIGURACIÓN':-^70}")
        print(f"  Número de ciudades (n): {len(ciudades)}")
        print(f"  Permutaciones evaluadas: {ciclos_evaluados:,}")
        
        print(f"\n{'LONGITUDES DE CICLOS':-^70}")
        print(f"  Longitud óptima (L⋆):      {long_optima:12.4f}")
        print(f"  Longitud heurística (LNN): {long_nn:12.4f}")
        print(f"  Diferencia absoluta:       {diferencia_absoluta:12.4f}")
        print(f"  Gap de optimalidad:        {gap:12.2f}%")
        
        print(f"\n{'TIEMPOS DE EJECUCIÓN':-^70}")
        print(f"  Búsqueda exhaustiva:       {tiempo_exhaustivo:12.6f} segundos")
        print(f"  Vecino más cercano:        {tiempo_nn:12.6f} segundos")
        print(f"  Speedup (aceleración):     {speedup:12.2f}x más rápido")
        
        print(f"\n{'CICLOS ENCONTRADOS':-^70}")
        nombres_optimo = ' → '.join([ciudades[i]['nombre'] for i in comparacion['ciclo_optimo']])
        nombres_nn = ' → '.join([ciudades[i]['nombre'] for i in comparacion['ciclo_nn']])
        print(f"  Ciclo óptimo π⋆:")
        print(f"    {nombres_optimo} → {ciudades[comparacion['ciclo_optimo'][0]]['nombre']}")
        print(f"\n  Ciclo heurístico πNN:")
        print(f"    {nombres_nn} → {ciudades[comparacion['ciclo_nn'][0]]['nombre']}")
        
        print(f"\n{'CONCLUSIONES':-^70}")
        if gap < 5:
            print(f"  ✓ Gap muy pequeño ({gap:.2f}%): la heurística es muy efectiva")
        elif gap < 15:
            print(f"  ⚠ Gap moderado ({gap:.2f}%): la heurística es aceptable")
        else:
            print(f"  ✗ Gap significativo ({gap:.2f}%): la heurística es subóptima")
        
        print(f"  ✓ La heurística es {speedup:.0f}x más rápida que la búsqueda exhaustiva")
        
        if gap < 10 and speedup > 100:
            print(f"  ⭐ Conclusión: Para esta instancia, la heurística es muy conveniente")
        
        print(f"\n{'='*70}\n")
    
    return comparacion


def generar_tabla_resultados(comparacion, guardar=None):
    """
    Genera una tabla con los resultados en formato DataFrame.
    
    Args:
        comparacion: Diccionario con resultados de la comparación
        guardar: Ruta donde guardar CSV (opcional)
    
    Returns:
        pandas.DataFrame: Tabla con los resultados
    """
    datos = {
        'Métrica': [
            'Número de ciudades',
            'Longitud óptima (L⋆)',
            'Longitud heurística (LNN)',
            'Diferencia absoluta',
            'Gap (%)',
            'Tiempo exhaustivo (s)',
            'Tiempo NN (s)',
            'Speedup (x)',
            'Ciclos evaluados'
        ],
        'Valor': [
            comparacion['n_ciudades'],
            f"{comparacion['longitud_optima']:.4f}",
            f"{comparacion['longitud_nn']:.4f}",
            f"{comparacion['diferencia_absoluta']:.4f}",
            f"{comparacion['gap_porcentaje']:.2f}",
            f"{comparacion['tiempo_exhaustivo']:.6f}",
            f"{comparacion['tiempo_nn']:.6f}",
            f"{comparacion['speedup']:.2f}",
            f"{comparacion['ciclos_evaluados']:,}"
        ]
    }
    
    df = pd.DataFrame(datos)
    
    if guardar:
        df.to_csv(guardar, index=False, encoding='utf-8')
        print(f"✓ Tabla guardada: {guardar}")
    
    return df


def plot_comparacion_tiempos(comparacion, guardar=None):
    """
    Genera un gráfico de barras comparando los tiempos de ejecución.
    
    Args:
        comparacion: Diccionario con resultados
        guardar: Ruta donde guardar la figura (opcional)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metodos = ['Búsqueda\nExhaustiva', 'Vecino Más\nCercano']
    tiempos = [comparacion['tiempo_exhaustivo'], comparacion['tiempo_nn']]
    colores = ['#ff6b6b', '#4ecdc4']
    
    barras = ax.bar(metodos, tiempos, color=colores, edgecolor='black', linewidth=2)
    
    # Añadir valores sobre las barras
    for i, (barra, tiempo) in enumerate(zip(barras, tiempos)):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
                f'{tiempo:.6f}s',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Tiempo de ejecución (segundos)', fontsize=12, fontweight='bold')
    ax.set_title(f'Comparación de Tiempos de Ejecución\n'
                f'(Speedup: {comparacion["speedup"]:.2f}x)',
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    
    if guardar:
        plt.tight_layout()
        plt.savefig(guardar, dpi=150, bbox_inches='tight')
        print(f"✓ Gráfico de tiempos guardado: {guardar}")
    
    plt.tight_layout()
    return fig


def plot_comparacion_longitudes(comparacion, guardar=None):
    """
    Genera un gráfico de barras comparando las longitudes de los ciclos.
    
    Args:
        comparacion: Diccionario con resultados
        guardar: Ruta donde guardar la figura (opcional)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metodos = ['Búsqueda\nExhaustiva (L⋆)', 'Vecino Más\nCercano (LNN)']
    longitudes = [comparacion['longitud_optima'], comparacion['longitud_nn']]
    colores = ['#51cf66', '#ffa94d']
    
    barras = ax.bar(metodos, longitudes, color=colores, edgecolor='black', linewidth=2)
    
    # Añadir valores sobre las barras
    for barra, longitud in zip(barras, longitudes):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
                f'{longitud:.4f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Longitud del ciclo', fontsize=12, fontweight='bold')
    ax.set_title(f'Comparación de Longitudes de Ciclos\n'
                f'(Gap: {comparacion["gap_porcentaje"]:.2f}%)',
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Línea horizontal para mostrar la diferencia
    if comparacion['gap_porcentaje'] > 0:
        ax.plot([0, 1], [comparacion['longitud_optima'], comparacion['longitud_optima']], 
               'r--', linewidth=2, alpha=0.5, label='Óptimo')
        ax.legend()
    
    if guardar:
        plt.tight_layout()
        plt.savefig(guardar, dpi=150, bbox_inches='tight')
        print(f"✓ Gráfico de longitudes guardado: {guardar}")
    
    plt.tight_layout()
    return fig
