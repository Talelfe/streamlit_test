import pandas as pd
import scipy.stats
import streamlit as st
import time

# --- Configuración de la página ---
st.set_page_config(
    page_title="Lanzar una Moneda",
    page_icon=":coin:", # Un emoji de moneda para el ícono de la pestaña
    layout="centered" # Puedes cambiar a "wide" si prefieres un diseño más amplio
)

# --- Variables de estado de la sesión ---
# Estas variables se conservan cuando Streamlit vuelve a ejecutar el script (por ejemplo, al interactuar con un widget).
# 'experiment_no' para llevar la cuenta del número de experimentos realizados.
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

# 'df_experiment_results' para almacenar los resultados de cada experimento en un DataFrame.
if 'df_experiment_results' not in st.session_state:
    # Definimos las columnas del DataFrame para almacenar el número de experimento, iteraciones y la media.
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

# --- Título de la aplicación ---
st.header('Simulador de Lanzamiento de Monedas')

# --- Gráfico de líneas inicial ---
# Creamos un gráfico de líneas que se actualizará en tiempo real.
# Se inicializa con un valor de 0.5 para que la línea empiece en el centro.
chart = st.line_chart([0.5])

# --- Función para lanzar la moneda ---
# Esta función simula 'n' lanzamientos de moneda y calcula la media.
# También actualiza el gráfico en tiempo real.
def toss_coin(n):
    # scipy.stats.bernoulli.rvs(p=0.5, size=n) simula 'n' lanzamientos de moneda.
    # 'p=0.5' significa 50% de probabilidad para cada resultado (0 o 1).
    # 'size=n' es el número total de lanzamientos.
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None # La media actual de los resultados
    outcome_no = 0 # Contador de lanzamientos hasta el momento en esta simulación
    outcome_1_count = 0 # Contador de veces que salió '1' (por ejemplo, Cara)

    # Iteramos sobre cada resultado del lanzamiento
    for r in trial_outcomes:
        outcome_no += 1 # Incrementamos el número de lanzamientos
        if r == 1:
            outcome_1_count += 1 # Si el resultado es 1, incrementamos el contador de '1's
        
        # Calculamos la media acumulada
        mean = outcome_1_count / outcome_no
        
        # Agregamos el nuevo punto de la media al gráfico.
        # Esto hace que el gráfico se actualice en tiempo real.
        chart.add_rows([mean])
        
        # Pausa breve para que la animación del gráfico sea visible.
        time.sleep(0.05)

    return mean # Devolvemos la media final de todos los lanzamientos

# --- Widgets de entrada para el usuario ---
# Control deslizante para que el usuario elija el número de intentos (lanzamientos).
# Rango: de 1 a 1000, valor inicial: 10.
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)

# Botón para iniciar la simulación.
start_button = st.button('Ejecutar')

# --- Lógica cuando se presiona el botón ---
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    
    # Incrementamos el número de experimento para la sesión actual.
    st.session_state['experiment_no'] += 1
    
    # Ejecutamos la simulación de lanzar la moneda.
    mean = toss_coin(number_of_trials)
    
    # Agregamos los resultados del experimento actual al DataFrame de resultados.
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iteraciones', 'media'])
        ],
        axis=0)
    
    # Reseteamos el índice del DataFrame para que sea consecutivo.
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

# --- Mostrar la tabla de resultados ---
# st.write(st.session_state['df_experiment_results'])
# Mejor usar st.dataframe para una visualización más interactiva de la tabla.
st.subheader("Resultados de Experimentos Anteriores")
st.dataframe(st.session_state['df_experiment_results'])

# --- Mensaje de pie de página o instrucciones adicionales ---
st.markdown("---")
st.markdown("Ajusta el número de intentos y haz clic en 'Ejecutar' para ver cómo la media se acerca al 0.5.")

