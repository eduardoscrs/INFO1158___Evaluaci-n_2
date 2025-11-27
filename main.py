"""
PROBLEMA DEL VIAJANTE (TSP) - EVALUACIÓN 2
==========================================

Archivo principal que ejecuta ambos métodos de resolución del TSP:
1. Búsqueda exhaustiva (solución óptima)
2. Heurística del Vecino Más Cercano (solución aproximada)

Genera visualizaciones, animaciones y análisis comparativo.
"""

import sys
import os

# Añadir directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from distance_calculator import construir_matriz_distancias, imprimir_matriz
from exhaustive_search import busqueda_exhaustiva
from nearest_neighbor import vecino_mas_cercano, vecino_mas_cercano_multi_inicio
from visualizer import (plot_ciclo, crear_animacion_exhaustiva, 
                        crear_animacion_nn, comparar_soluciones)
from comparador import (comparar_metodos, generar_tabla_resultados,
                       plot_comparacion_tiempos, plot_comparacion_longitudes)
import matplotlib.pyplot as plt


# ============================================================================
# DEFINICIÓN DE CIUDADES
# ============================================================================
# Dataset 1: 7 Ciudades (Original)
ciudades_7 = [
    {"nombre": "Madrid",    "coords": (40.4168, -3.7038)},
    {"nombre": "París",     "coords": (48.8566, 2.3522)},
    {"nombre": "Londres",   "coords": (51.5074, -0.1278)},
    {"nombre": "Berlín",    "coords": (52.5200, 13.4050)},
    {"nombre": "Roma",      "coords": (41.9028, 12.4964)},
    {"nombre": "Ámsterdam", "coords": (52.3676, 4.9041)},
    {"nombre": "Bruselas",  "coords": (50.8503, 4.3517)}
]

# Dataset 2: 12 Ciudades (Escalabilidad)
ciudades_12 = ciudades_7 + [
    {"nombre": "Viena",     "coords": (48.2082, 16.3738)},
    {"nombre": "Praga",     "coords": (50.0755, 14.4378)},
    {"nombre": "Zúrich",    "coords": (47.3769, 8.5417)},
    {"nombre": "Copenhague","coords": (55.6761, 12.5683)},
    {"nombre": "Budapest",  "coords": (47.4979, 19.0402)}
]


def seleccionar_dataset():
    """Permite al usuario elegir entre los conjuntos de datos."""
    print("\nSeleccione el conjunto de datos:")
    print("1. 7 Ciudades (Rápido - Original)")
    print("2. 12 Ciudades (Prueba de escalabilidad - Puede tardar varios minutos)")
    
    while True:
        opcion = input("\nOpción (1/2): ").strip()
        if opcion == '1':
            return ciudades_7
        elif opcion == '2':
            print("\n ADVERTENCIA: Con 12 ciudades, la búsqueda exhaustiva evaluará")
            print("   (12-1)!/2 = 19,958,400 permutaciones.")
            print("   Esto puede tomar entre 30 segundos y varios minutos dependiendo de tu CPU.")
            confirm = input("   ¿Desea continuar? (s/n): ").strip().lower()
            if confirm == 's':
                return ciudades_12
        else:
            print("Por favor ingrese 1 o 2.")


def main():
    """Función principal del programa."""
    
    print("\n" + "="*70)
    print(" "*15 + "PROBLEMA DEL VIAJANTE (TSP)")
    print(" "*10 + "Búsqueda Exhaustiva vs Vecino Más Cercano")
    print("="*70 + "\n")
    
    # Seleccionar ciudades
    ciudades = seleccionar_dataset()
    
    # Crear directorio para resultados
    os.makedirs('results', exist_ok=True)
    os.makedirs('results/animaciones', exist_ok=True)
    os.makedirs('results/graficos', exist_ok=True)
    
    # ========================================================================
    # 1. CONSTRUIR MATRIZ DE DISTANCIAS
    # ========================================================================
    print("\n[1/7] Construyendo matriz de distancias...")
    print("-" * 70)
    
    # Usar distancia euclidiana como especifica el enunciado
    matriz_dist = construir_matriz_distancias(ciudades, metodo='euclid')
    
    print(f"\nCiudades seleccionadas: {len(ciudades)}")
    print(f"Matriz de distancias D (distancia Euclidiana):\n")
    imprimir_matriz(matriz_dist, ciudades, decimales=4)
    
    # ========================================================================
    # 2. BÚSQUEDA EXHAUSTIVA
    # ========================================================================
    print("\n[2/7] Ejecutando búsqueda exhaustiva...")
    print("-" * 70)
    
    resultado_exhaustivo = busqueda_exhaustiva(ciudades, matriz_dist, verbose=True)
    
    # ========================================================================
    # 3. HEURÍSTICA VECINO MÁS CERCANO
    # ========================================================================
    print("\n[3/7] Ejecutando heurística del Vecino Más Cercano...")
    print("-" * 70)
    
    resultado_nn = vecino_mas_cercano(ciudades, matriz_dist, ciudad_inicio=0, verbose=True)
    
    # Opcional: probar desde todas las ciudades
    # resultado_nn = vecino_mas_cercano_multi_inicio(ciudades, matriz_dist, verbose=True)
    
    # ========================================================================
    # 4. COMPARACIÓN CUANTITATIVA
    # ========================================================================
    print("\n[4/7] Generando análisis comparativo...")
    print("-" * 70)
    
    comparacion = comparar_metodos(resultado_exhaustivo, resultado_nn, ciudades, verbose=True)
    
    # Guardar tabla de resultados
    df_resultados = generar_tabla_resultados(comparacion, 
                                             guardar='results/comparacion.csv')
    print("\n" + str(df_resultados))
    
    # ========================================================================
    # 5. VISUALIZACIÓN DE CICLOS
    # ========================================================================
    print("\n[5/7] Generando visualizaciones de ciclos...")
    print("-" * 70)
    
    # Ciclo óptimo
    fig1 = plt.figure(figsize=(12, 8))
    ax1 = fig1.add_subplot(111)
    plot_ciclo(ciudades, 
              resultado_exhaustivo['ciclo_optimo'], 
              resultado_exhaustivo['longitud_optima'],
              titulo="Solución Óptima - Búsqueda Exhaustiva",
              color='green',
              ax=ax1,
              guardar='results/graficos/ciclo_optimo.png')
    plt.close()
    
    # Ciclo heurístico
    fig2 = plt.figure(figsize=(12, 8))
    ax2 = fig2.add_subplot(111)
    plot_ciclo(ciudades, 
              resultado_nn['ciclo'], 
              resultado_nn['longitud'],
              titulo="Solución Heurística - Vecino Más Cercano",
              color='orange',
              ax=ax2,
              guardar='results/graficos/ciclo_heuristico.png')
    plt.close()
    
    # Comparación lado a lado
    fig_comp = comparar_soluciones(ciudades,
                                   resultado_exhaustivo['ciclo_optimo'],
                                   resultado_exhaustivo['longitud_optima'],
                                   resultado_nn['ciclo'],
                                   resultado_nn['longitud'],
                                   guardar='results/graficos/comparacion_ciclos.png')
    plt.close()
    
    # ========================================================================
    # 6. GRÁFICOS DE COMPARACIÓN
    # ========================================================================
    print("\n[6/7] Generando gráficos de comparación...")
    print("-" * 70)
    
    # Comparación de tiempos
    fig_tiempos = plot_comparacion_tiempos(comparacion, 
                                           guardar='results/graficos/comparacion_tiempos.png')
    plt.close()
    
    # Comparación de longitudes
    fig_longitudes = plot_comparacion_longitudes(comparacion,
                                                 guardar='results/graficos/comparacion_longitudes.png')
    plt.close()
    
    # ========================================================================
    # 7. ANIMACIONES (OPCIONAL - PUEDE TOMAR TIEMPO)
    # ========================================================================
    print("\n[7/7] Generando animaciones...")
    print("-" * 70)
    print("NOTA: Las animaciones pueden tardar varios minutos en generarse.")
    
    respuesta = input("\n¿Desea generar las animaciones? (s/n): ").strip().lower()
    
    if respuesta == 's':
        # Animación búsqueda exhaustiva
        print("\nGenerando animación de búsqueda exhaustiva...")
        anim_exhaustiva = crear_animacion_exhaustiva(
            ciudades,
            resultado_exhaustivo['historial'],
            fps=10,
            guardar='results/animaciones/busqueda_exhaustiva.gif'
        )
        plt.close()
        
        # Animación vecino más cercano
        print("\nGenerando animación de Vecino Más Cercano...")
        anim_nn = crear_animacion_nn(
            ciudades,
            resultado_nn['historial'],
            fps=2,
            guardar='results/animaciones/vecino_mas_cercano.gif'
        )
        plt.close()
        
        print("\n✓ Animaciones generadas exitosamente")
    else:
        print("\n⊘ Generación de animaciones omitida")
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    print("\n" + "="*70)
    print(" "*20 + "EJECUCIÓN COMPLETADA")
    print("="*70)
    print("\n Archivos generados:")
    print("   • results/comparacion.csv")
    print("   • results/graficos/ciclo_optimo.png")
    print("   • results/graficos/ciclo_heuristico.png")
    print("   • results/graficos/comparacion_ciclos.png")
    print("   • results/graficos/comparacion_tiempos.png")
    print("   • results/graficos/comparacion_longitudes.png")
    
    if respuesta == 's':
        print("   • results/animaciones/busqueda_exhaustiva.gif")
        print("   • results/animaciones/vecino_mas_cercano.gif")
    
    print("\n Resultados principales:")
    print(f"   • Longitud óptima (L⋆):      {comparacion['longitud_optima']:.4f}")
    print(f"   • Longitud heurística (LNN): {comparacion['longitud_nn']:.4f}")
    print(f"   • Gap de optimalidad:        {comparacion['gap_porcentaje']:.2f}%")
    print(f"   • Speedup:                   {comparacion['speedup']:.2f}x")
    
    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    main()
