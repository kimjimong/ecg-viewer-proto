from io import BytesIO
import pyedflib
import matplotlib.pyplot as plt
import os
from flask import current_app

def get_details(details_path):
    # Get Detail from Json
    hr = 70
    start_time = "2021-10-31:00:00:00"
    actual_duration = "24:00:00"
    return hr, start_time, actual_duration

def get_ecg_data(data_path):
    # ===== read edf =====
    f = pyedflib.EdfReader(data_path)
    sigbufs = f.readSignal(0)
    f._close()
    return sigbufs


def ploting_from_signal(signal_arr, one_image_len):
    fig = plt.figure(figsize=(15, 2*6), constrained_layout=True)
    axs = fig.subplots(6, 1)
    for idx, ax in enumerate(axs):
        cut_signal = signal_arr[idx*one_image_len:(idx+1)*one_image_len]
        ax.plot(cut_signal, 'k-', label=f'ecg_{idx}')
    fig.suptitle("Test ECG", fontsize=16)
    img = BytesIO()
    fig.savefig(img, format='png', dpi=200)
    img.seek(0)
    return img


def signal_plot_to_png(signal, region, test_id, page, one_image_len, add_name=""):
    fig = plt.figure(figsize=(15, 2*6), constrained_layout=True)
    axs = fig.subplots(6, 1)
    for idx, ax in enumerate(axs):
        cut_signal = signal[idx*one_image_len:(idx+1)*one_image_len]
        ax.plot(cut_signal, 'k-', label=f'ecg_{idx}')
    fig.suptitle("Test ECG", fontsize=16)
    file_name = f"{region}_{test_id}_{page}{add_name}.png"
    file_path = os.path.join(current_app.root_path, 'static/ecg_png_cache', file_name)
    fig.savefig(file_path, format='png', dpi=200)
    return file_name


# At /ecgtest, Response Form
def make_test_list_for_ecgtest(ecg_tests):
    test_dump = []
    for test_ in ecg_tests:
        test_dump.append({
            "region":test_.region,
            "test_id":test_.test_id,
            "duration":test_.duration,
            "condition":test_.condition,
        })
    return test_dump


# At /ecgtest/region/test_id/page, Response Form
def make_group_list_for_ecgtest(samplegroups):
    dump = []
    for sample in samplegroups:
        dump.append({
            "id": sample.id,
            "name": sample.group_name,
        })
    return dump