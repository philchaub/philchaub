
from numba import jit, cuda 
import numpy as np 
# to measure exec time 
from timeit import default_timer as timer 

# normal function to run on cpu 
def func(a):								 
    for i in range(10000000): 
        a[i]+= 1	

# function optimized to run on gpu 
@cuda.jit  # Utiliser @cuda.jit pour une fonction sur GPU
def func2(a): 
    i = cuda.grid(1)  # Get the index of the thread in the grid
    if i < len(a):    # Ensure that the index is within bounds
        a[i] += 1

if __name__=="__main__": 
    n = 10000000							
    a = np.ones(n, dtype = np.float64) 
	
    start = timer() 
    func(a) 
    print("without GPU:", timer()-start)	 
	
    # Spécifier la configuration du bloc et de la grille pour l'exécution sur GPU
    threads_per_block = 256
    blocks_per_grid = (n + threads_per_block - 1) // threads_per_block  # Nombre de blocs pour couvrir n éléments
    start = timer() 
    func2[blocks_per_grid, threads_per_block](a)  # Appel de la fonction CUDA avec les blocs et les threads
    print("with GPU:", timer()-start)


