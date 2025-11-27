"""
Módulo para generar visualizaciones y animaciones del TSP.
Genera gráficos del proceso de búsqueda y ciclos encontrados.
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch
import numpy as np
import os


def configurar_estilo():
    """Configura el estilo visual de los gráficos."""
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10


def plot_ciudades(ciudades, ax=None, mostrar=False):
    """
    Dibuja las ciudades en un gráfico.
    
    Args:
        ciudades: Lista de ciudades con coordenadas
        ax: Axes de matplotlib (opcional)
        mostrar: Si True, muestra el gráfico
    
    Returns:
        matplotlib.axes.Axes: Objeto axes con las ciudades dibujadas
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))
    
    # Extraer coordenadas
    lats = [c['coords'][0] for c in ciudades]
    lons = [c['coords'][1] for c in ciudades]
    nombres = [c['nombre'] for c in ciudades]
    
    # Dibujar ciudades
    ax.scatter(lons, lats, c='red', s=200, zorder=5, edgecolors='black', linewidth=2)
    
    # Etiquetar ciudades
    for i, nombre in enumerate(nombres):
        ax.annotate(nombre, (lons[i], lats[i]), 
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    ax.set_xlabel('Longitud', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitud', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    if mostrar:
        plt.tight_layout()
        plt.show()
    
    return ax


def plot_ciclo(ciudades, ciclo, longitud, titulo="Ciclo Hamiltoniano", 
               color='blue', ax=None, mostrar=False, guardar=None):
    """
    Dibuja un ciclo Hamiltoniano completo.
    
    Args:
        ciudades: Lista de ciudades
        ciclo: Lista de índices del ciclo
        longitud: Longitud total del ciclo
        titulo: Título del gráfico
        color: Color de las aristas
        ax: Axes de matplotlib (opcional)
        mostrar: Si True, muestra el gráfico
        guardar: Ruta donde guardar la figura (opcional)
    
    Returns:
        matplotlib.axes.Axes: Objeto axes con el ciclo dibujado
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))
    
    # Dibujar ciudades
    plot_ciudades(ciudades, ax=ax)
    
    # Dibujar aristas del ciclo
    n = len(ciclo)
    for i in range(n):
        ciudad_origen = ciclo[i]
        ciudad_destino = ciclo[(i + 1) % n]
        
        coord_origen = ciudades[ciudad_origen]['coords']
        coord_destino = ciudades[ciudad_destino]['coords']
        
        # Dibujar flecha
        ax.annotate('', xy=(coord_destino[1], coord_destino[0]),
                   xytext=(coord_origen[1], coord_origen[0]),
                   arrowprops=dict(arrowstyle='->', lw=2, color=color, alpha=0.7))
    
    ax.set_title(f"{titulo}\nLongitud: {longitud:.4f}", 
                fontsize=14, fontweight='bold', pad=20)
    
    if guardar:
        plt.tight_layout()
        plt.savefig(guardar, dpi=150, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {guardar}")
    
    if mostrar:
        plt.tight_layout()
        plt.show()
    
    return ax


def crear_animacion_exhaustiva(ciudades, historial, fps=10, guardar=None):
    """
    Crea una animación del proceso de búsqueda exhaustiva.
    
    Args:
        ciudades: Lista de ciudades
        historial: Lista de estados durante la búsqueda
        fps: Frames por segundo
        guardar: Ruta donde guardar la animación (opcional)
    
    Returns:
        matplotlib.animation.FuncAnimation: Objeto de animación
    """
    configurar_estilo()
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Seleccionar frames clave para la animación (solo los mejores)
    frames_mejores = [h for h in historial if h['es_mejor']]
    
    # Si hay demasiados frames, submuestrear
    if len(frames_mejores) > 100:
        indices = np.linspace(0, len(frames_mejores) - 1, 100, dtype=int)
        frames_mejores = [frames_mejores[i] for i in indices]
    
    print(f"Generando animación con {len(frames_mejores)} frames...")
    
    def actualizar(frame_num):
        ax.clear()
        estado = frames_mejores[frame_num]
        ciclo = estado['ciclo']
        longitud = estado['longitud']
        iteracion = estado['iteracion']
        
        # Dibujar ciudades
        plot_ciudades(ciudades, ax=ax)
        
        # Dibujar ciclo actual
        n = len(ciclo)
        for i in range(n):
            ciudad_origen = ciclo[i]
            ciudad_destino = ciclo[(i + 1) % n]
            
            coord_origen = ciudades[ciudad_origen]['coords']
            coord_destino = ciudades[ciudad_destino]['coords']
            
            ax.annotate('', xy=(coord_destino[1], coord_destino[0]),
                       xytext=(coord_origen[1], coord_origen[0]),
                       arrowprops=dict(arrowstyle='->', lw=2, color='blue', alpha=0.6))
        
        progreso = (frame_num + 1) / len(frames_mejores) * 100
        ax.set_title(f"BÚSQUEDA EXHAUSTIVA - Progreso: {progreso:.1f}%\n"
                    f"Iteración: {iteracion:,} | Mejor longitud actual: {longitud:.4f}",
                    fontsize=14, fontweight='bold', pad=20)
    
    anim = animation.FuncAnimation(fig, actualizar, frames=len(frames_mejores),
                                  interval=1000//fps, repeat=True)
    
    if guardar:
        print(f"Guardando animación (esto puede tomar varios minutos)...")
        writer = animation.PillowWriter(fps=fps)
        anim.save(guardar, writer=writer, dpi=100)
        print(f"✓ Animación guardada: {guardar}")
    
    return anim


def crear_animacion_nn(ciudades, historial, fps=2, guardar=None):
    """
    Crea una animación del proceso de Vecino Más Cercano.
    
    Args:
        ciudades: Lista de ciudades
        historial: Lista de pasos del algoritmo
        fps: Frames por segundo
        guardar: Ruta donde guardar la animación (opcional)
    
    Returns:
        matplotlib.animation.FuncAnimation: Objeto de animación
    """
    configurar_estilo()
    fig, ax = plt.subplots(figsize=(14, 10))
    
    print(f"Generando animación Vecino Más Cercano con {len(historial)} frames...")
    
    def actualizar(frame_num):
        ax.clear()
        estado = historial[frame_num]
        ciclo_parcial = estado['ciclo_parcial']
        paso = estado['paso']
        longitud_acum = estado['longitud_acumulada']
        
        # Dibujar ciudades
        lats = [c['coords'][0] for c in ciudades]
        lons = [c['coords'][1] for c in ciudades]
        nombres = [c['nombre'] for c in ciudades]
        
        # Ciudades visitadas y no visitadas
        visitadas = set(ciclo_parcial[:-1]) if len(ciclo_parcial) > 1 and ciclo_parcial[-1] == ciclo_parcial[0] else set(ciclo_parcial)
        
        for i, nombre in enumerate(nombres):
            color = 'green' if i in visitadas else 'lightgray'
            size = 200 if i in visitadas else 150
            ax.scatter(lons[i], lats[i], c=color, s=size, zorder=5, 
                      edgecolors='black', linewidth=2)
            
            ax.annotate(nombre, (lons[i], lats[i]), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=11, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', 
                                facecolor='lightgreen' if i in visitadas else 'lightgray', 
                                alpha=0.7))
        
        # Dibujar aristas del ciclo parcial
        for i in range(len(ciclo_parcial) - 1):
            ciudad_origen = ciclo_parcial[i]
            ciudad_destino = ciclo_parcial[i + 1]
            
            coord_origen = ciudades[ciudad_origen]['coords']
            coord_destino = ciudades[ciudad_destino]['coords']
            
            # Última arista en rojo (la que se acaba de agregar)
            color = 'red' if i == len(ciclo_parcial) - 2 else 'blue'
            width = 3 if i == len(ciclo_parcial) - 2 else 2
            
            ax.annotate('', xy=(coord_destino[1], coord_destino[0]),
                       xytext=(coord_origen[1], coord_origen[0]),
                       arrowprops=dict(arrowstyle='->', lw=width, color=color, alpha=0.7))
        
        ax.set_xlabel('Longitud', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitud', fontsize=12, fontweight='bold')
        ax.set_title(f"VECINO MÁS CERCANO - Paso {paso}/{len(ciudades)}\n"
                    f"Longitud acumulada: {longitud_acum:.4f}",
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
    
    anim = animation.FuncAnimation(fig, actualizar, frames=len(historial),
                                  interval=1000//fps, repeat=True)
    
    if guardar:
        print(f"Guardando animación...")
        writer = animation.PillowWriter(fps=fps)
        anim.save(guardar, writer=writer, dpi=100)
        print(f"✓ Animación guardada: {guardar}")
    
    return anim


def comparar_soluciones(ciudades, ciclo_optimo, long_optima, ciclo_nn, long_nn, guardar=None):
    """
    Crea una figura comparativa de ambas soluciones lado a lado.
    
    Args:
        ciudades: Lista de ciudades
        ciclo_optimo: Ciclo de búsqueda exhaustiva
        long_optima: Longitud óptima
        ciclo_nn: Ciclo de vecino más cercano
        long_nn: Longitud heurística
        guardar: Ruta donde guardar la figura (opcional)
    """
    configurar_estilo()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Solución óptima
    plot_ciclo(ciudades, ciclo_optimo, long_optima, 
              titulo="BÚSQUEDA EXHAUSTIVA (Óptimo)", 
              color='green', ax=ax1)
    
    # Solución heurística
    plot_ciclo(ciudades, ciclo_nn, long_nn, 
              titulo="VECINO MÁS CERCANO (Heurística)", 
              color='orange', ax=ax2)
    
    # Calcular gap
    gap = ((long_nn - long_optima) / long_optima) * 100
    
    fig.suptitle(f"COMPARACIÓN DE SOLUCIONES TSP\n"
                f"Gap de optimalidad: {gap:.2f}% | "
                f"L⋆ = {long_optima:.4f} | LNN = {long_nn:.4f}",
                fontsize=16, fontweight='bold', y=0.98)
    
    if guardar:
        plt.tight_layout()
        plt.savefig(guardar, dpi=150, bbox_inches='tight')
        print(f"✓ Comparación guardada: {guardar}")
    
    plt.tight_layout()
    return fig
