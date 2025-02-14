from io import BytesIO
import pyedflib
import matplotlib.pyplot as plt
import os
from flask import current_app

import numpy as np
from typing import IO, Dict, List, Union

def get_details(details_path: str) -> Union[int, str, str]:
    # Get Detail from Json
    hr = 70
    start_time = "2021-10-31:00:00:00"
    actual_duration = "24:00:00"
    return hr, start_time, actual_duration

def get_ecg_data(data_path: str) -> np.ndarray:
    # ===== read edf =====
    f = pyedflib.EdfReader(data_path)
    sigbufs = f.readSignal(0)
    f._close()
    return sigbufs


def ploting_from_signal(signal_arr: np.ndarray, one_image_len: int) -> IO[bytes]:
    fig = plt.figure(figsize=(15, 2*6), constrained_layout=True)
    axs = fig.subplots(6, 1)
    for idx, ax in enumerate(axs):
        cut_signal = signal_arr[idx*one_image_len:(idx+1)*one_image_len]
        ax.plot(cut_signal, 'b-', label=f'ecg_{idx}')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
    img = BytesIO()
    fig.savefig(img, format='png', dpi=200)
    img.seek(0)
    return img


def signal_plot_to_png(signal: np.ndarray, id: int, page: int, one_image_len: int, add_name: int="") -> str:
    fig = plt.figure(figsize=(15, 2*6), constrained_layout=True)
    axs = fig.subplots(6, 1)
    for idx, ax in enumerate(axs):
        cut_signal = signal[idx*one_image_len:(idx+1)*one_image_len]
        ax.plot(cut_signal, 'b-', label=f'ecg_{idx}')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
    file_name = f"{id}_{page}{add_name}.png"
    file_path = os.path.join(current_app.root_path, 'static/ecg_png_cache', file_name)
    fig.savefig(file_path, format='png', dpi=200)
    return file_name


