import librosa
import os
import numpy as np
import shutil
import pandas as pd


def save_melspec(path, target):
    y, sr = librosa.load(path, sr=None, duration=30.0)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000, n_fft=2048, hop_length=512)
    S_dB = librosa.power_to_db(S, ref=np.max)
    np.save(path.replace('dataset', target).replace('.low.mp3', '.npy'), S_dB)
    # os.remove(path)


def make_mels(filename):
    with open(filename, 'r') as f:
        f.readline()
        for line in f.readlines():
            line = line.split(sep="\t")
            path = line[3].replace('.mp3', '.low.mp3')
            os.makedirs('mels/' + os.path.dirname(path), exist_ok=True)
            save_melspec('dataset/' + path, 'mels')
            # tags = "\t".join(line[5:])

def make_zips():
    root_folder = "mels"
    output_folder = "zips"
    os.makedirs(output_folder, exist_ok=True)

    # iteracja po podkatalogach w mels
    for subdir in os.listdir(root_folder):
        subdir_path = os.path.join(root_folder, subdir)
        if os.path.isdir(subdir_path):
            zip_name = os.path.join(output_folder, f"{subdir}.zip")
            shutil.make_archive(zip_name.replace('.zip',''), 'zip', subdir_path)
            print(f"Zrobiono ZIP: {zip_name}")


def make_new_tsv(old_tsv):
    with open(old_tsv, 'r') as f:
        data = f.readlines()
        for i in range(1, len(data)):
            line = data[i].split('\t')[3:]
            new_line = []
            new_line.append(line[0].replace('.mp3', '.npy'))
            new_line.append(line[1])
            new_line.append((' '.join(line[2:])).replace('mood/theme--', ''))
            data[i] = new_line
        data[0] = data[0].split('\t')[3:]
        data = ''.join(['\t'.join(line) for line in data])

    with open(os.path.dirname(old_tsv) + '/autotagging_moodtheme_mels.tsv', 'w') as f:
        f.write(data)


def add_new_tag(tsv):
    df = pd.read_csv(tsv, sep='\t')
    df['BASE_FREQ'] = ''
    for i, path in enumerate(df["PATH"]):
        mel = np.load(os.path.dirname(tsv) + '/' + path)
        if mel.shape[1] == 2813:
            df.loc[i, 'BASE_FREQ'] = '48k'
        else:
            df.loc[i, 'BASE_FREQ'] = '44.1k'
    df.to_csv(tsv, index=False, sep='\t')


def add_train_and_test(path, destination__path):
    df = pd.read_csv(path, sep='\t', usecols=["PATH"])
    filename, _ = os.path.splitext(os.path.basename(path))
    typ = filename.split('-')[-1]
    destination_df = pd.read_csv(destination__path, sep='\t')

    if "DATASET_TYPE" not in destination_df.columns:
        destination_df["DATASET_TYPE"] = ""
    destination_df["DATASET_TYPE"] = destination_df["DATASET_TYPE"].astype("string")
    destination_df.loc[destination_df["DATASET_TYPE"].isna(), "DATASET_TYPE"] = "validation"
    destination_df.loc[
        destination_df["PATH"].apply(lambda p: p.split('.')[0])
            .isin(
                df["PATH"].apply(lambda p: p.split('.')[0])
            ),
            "DATASET_TYPE"
        ] = typ

    destination_df.to_csv(destination__path, index=False, sep='\t')




if __name__ == "__main__":
    make_mels("mtg-jamendo-dataset/data/autotagging_moodtheme.tsv")
    make_zips()
    make_new_tsv("mels/autotagging_moodtheme.tsv")
    add_new_tag("mels/autotagging_moodtheme_mels.tsv")
    add_train_and_test("mtg-jamendo-dataset/data/splits/split-0/autotagging_moodtheme-test.tsv", "mels/autotagging_moodtheme_mels.tsv")
    add_train_and_test("mtg-jamendo-dataset/data/splits/split-0/autotagging_moodtheme-train.tsv", "mels/autotagging_moodtheme_mels.tsv")
