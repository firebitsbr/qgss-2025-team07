import math

import numpy as np
import itertools
from qiskit.quantum_info import Pauli, PauliList
from typing import List, Tuple, Dict, Optional, Set, Union
import sys
from numpy.linalg import matrix_rank
from numpy.linalg import matrix_power as m_power

from qiskit.quantum_info import Statevector

def bring_states():
    state_list= [0, 0, 0, 0, 0, 0,
                 0, -1/(2*np.sqrt(2))*1j, 1/(2*np.sqrt(2))*1j,
                 0, 0, 0,0, 0, 0,0, 0, 0,
                 0, 0, 0,0, 0, 0,0, 0, 0,
                 0, 0, 0,0, 0, 0,0, 0, 0,
                 0, 0, 0,0, 0, 0,0, 0, 0,
                 0, 0, 0,0, 0, 0,
                 0, -1/(2*np.sqrt(2))*1j, 0,0, 0, 0,
                 0, 0, 1/(2*np.sqrt(2))*1j,0, 0, 0,
                 0, 0, 0,0, 0, 0, 0, 0, 0,
                 0, 0, 0,0, 0, 0,0, 0, 0,
                 0, -1/(2*np.sqrt(2))*1j, 0,0, 0, 0,
                 0, 0, 0,0, 0, 0,
                 1/(2*np.sqrt(2))*1j, 0, 0,0, -1/(2*np.sqrt(2))*1j, 0,
                 0, 0, 0,0, 0, 0,0, 0, 0,
                 0, 0, 1/(2*np.sqrt(2))*1j,0, 0, 0,
                 0, 0, 0,0, 0, 0,0, 0, 0,
                 0, 0, 0,0, 0]
    State = Statevector(state_list)
    return State


def hamming_distance(s1: Union[str, List[int], Tuple[int]],
                     s2: Union[str, List[int], Tuple[int]]):
    distance = 0
    for i in range(len(s1)):
        # 입력값이 string이면 문자를 변환합니다
        bit1 = int(s1[i]) if isinstance(s1, str) else s1[i]
        bit2 = int(s2[i]) if isinstance(s2, str) else s2[i]
        if bit1 != bit2:
            distance += 1
    return distance


def minimum_distance(code: List[Union[str, List[int], Tuple[int]]]) -> int:
    """
    주어진 코드에서의 최소 Hamming 거리를 구합니다.

    Args:
        code: 각 원소가 코드어인 list입니다.
              (0과 1로 이루어진 string, list, 또는 tuple).
              모든 코드어가 같은 길이로 이루어져 있다고 가정합니다.
              

    Returns:
        코드의 최소 Hamming 거리 d
        만약 코드가 2개의 코드어보다 더 적게 가지고 있으면 float('inf')를 반환합니다.
    """
    num_codewords = len(code)
    if num_codewords < 2:
        # 최소 거리가 잘 정의되지 않았거나 무한대입니다
        return float('inf')

    # 첫 번째와 같이 모든 코드어가 같은 길이를 가지고 있다고 가정합니다
    codeword_length = len(code[0])
    min_dist = codeword_length + 1 # 그 어떠한 가능한 거리보다 더 큰 값으로 초기화합니다

    for i in range(num_codewords):
        for j in range(i + 1, num_codewords):
            dist = hamming_distance(code[i], code[j])
            if dist < min_dist:
                min_dist = dist

    return min_dist


# GF(2) 위에서 정의된 행렬의 rank
def matrixRank(mat):
    M=mat.copy() # mat는 np.array이어야 합니다
    m=len(M) # 행의 개수
    pivots={} # pivot row --> pivot column로 연결해주는 dictionary
    # 행 소거
    for row in range(m):
        pos = next((index for index,value in enumerate(M[row]) if value != 0), -1) # 모두 0이면 -1을 출력하나, 첫 번째 0이 아닌 원소의 위치를 찾습니다
        if pos>-1:
            for row2 in range(m):
                if row2!=row and M[row2][pos]==1:
                    M[row2]=((M[row2]+M[row]) % 2)
            pivots[row]=pos
    return len(pivots)


def generate_stabilizer_plots(hx_matrix, hz_matrix):
    
    def get_qubit_coords(label):
        if not 0 <= label <= 143: return None
        if label < 72:
            col_idx, row_idx = divmod(label, 6)
            return (col_idx * 2, row_idx * 2)
        else:
            normalized_label = label - 72
            col_idx, row_idx = divmod(normalized_label, 6)
            return (col_idx * 2 + 1, row_idx * 2 + 1)

    def get_stabilizer_coords(index, stabilizer_type):
        if not 0 <= index <= 71: return None
        col_idx, row_idx = divmod(index, 6)
        if stabilizer_type.upper() == 'X':
            return (col_idx * 2, row_idx * 2 + 1)
        elif stabilizer_type.upper() == 'Z':
            return (col_idx * 2 + 1, row_idx * 2)
        else:
            return None
        

    stabilizersZ_to_show = [
        {'index': 5, 'type': 'Z'},
        {'index': 66, 'type': 'Z'},
    ]

    stabilizersX_to_show = [
        {'index': 5, 'type': 'X'},
        {'index': 66, 'type': 'X'},
    ]

    def _create_plot(matrix, stabilizers, title):
        WIDTH, HEIGHT = 24, 12
        NEUTRAL_COLOR, GRID_COLOR = '#d3d3d3', '#e0e0e0'
        HIGHLIGHT_COLORS = ['gold', 'cyan', 'magenta', 'lime']
        
        fig, ax = plt.subplots(figsize=(18, 9))
        ax.set_aspect('equal')


        for j in range(HEIGHT):
            ax.plot([-0.5, WIDTH - 0.5], [j, j], color=GRID_COLOR, linestyle=':', linewidth=1, zorder=1)
        for i in range(WIDTH):
            ax.plot([i, i], [-0.5, HEIGHT - 0.5], color=GRID_COLOR, linestyle=':', linewidth=1, zorder=1)
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if (i % 2) == (j % 2):
                    ax.scatter(i, j, s=50, c=NEUTRAL_COLOR, marker='o', zorder=2)
        

        for i, stab_info in enumerate(stabilizers):
            stabilizer_index = stab_info['index']
            stabilizer_type = stab_info['type'].upper()
            color = HIGHLIGHT_COLORS[i % len(HIGHLIGHT_COLORS)] 
            
            stab_coords = get_stabilizer_coords(stabilizer_index, stabilizer_type)
            if stab_coords:
                sx, sy = stab_coords
                ax.scatter(sx, sy, s=250, c=color, marker='o', zorder=3, label=f"Stabilizer {stabilizer_type}{stabilizer_index}")
                
            user_row = matrix[stabilizer_index]
            connected_qubit_labels = np.where(user_row == 1)[0]
            for label in connected_qubit_labels:
                coords = get_qubit_coords(label)
                if coords:
                    cx, cy = coords
                    ax.scatter(cx, cy, s=300, c=color, marker='o', zorder=4, alpha=0.9)
        
        ax.set_xlim(-1.5, WIDTH); ax.set_ylim(-1.5, HEIGHT)
        ax.set_xticks([]); ax.set_yticks([])
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
        fig.suptitle(title, fontsize=16)
        ax.legend()
        plt.show()
        
        ax.set_xlim(-1.5, WIDTH); ax.set_ylim(-1.5, HEIGHT)
        ax.set_xticks([]); ax.set_yticks([])
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
        fig.suptitle(title, fontsize=16)
        ax.legend()
        plt.show()

    _create_plot(hx_matrix, stabilizersX_to_show, "X-Stabilizer Check - 5, 66")
    _create_plot(hz_matrix, stabilizersZ_to_show, "Z-Stabilizer Check - 5, 66")
