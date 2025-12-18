## GSN

### Pobranie danych

```bash
git clone https://github.com/MTG/mtg-jamendo-dataset

mkdir dataset
mkdir mels

cd mtg-jamendo-dataset

python3 scripts/download/download.py \
    --dataset autotagging_moodtheme \
    --type audio-low \
    ../dataset \
    --unpack \
    --remove
```

### Link do notatnika na kaggle



### Plik prepare.py

- make_mels - na podstawie pliku z repozytorium mtg-jamendo tworzy melspektrogramy i zapisuje je pod odpowiednią ściężką w katalogu mels.

```py
make_mels("mtg-jamendo-dataset/data/autotagging_moodtheme.tsv")
```

- make_zips - funkcja pomocnicza do stworzenia zipów wewnątrz mels z katalogów $00, 01, ..., 99$, aby stworzyć z tych plików własny dataset na kaggle.

```py
make_zips()
```

- make_new_tsv - tworzy nowy plik tsv na podstawie kopii mtg-jamendo-dataset/data/autotagging_moodtheme.tsv do wykorzystania do własnego datasetu. W nim podmienione są dane w kolumnie PATH, aby nie były to ścieżki do plików .mp3 tylko .npy (spektrogramów) oraz zmieniony znak odstępu między tagami, aby móc potem skorzystać w sposób prostszy z pandasa.

```bash
cp mtg-jamendo-dataset/data/autotagging_moodtheme.tsv mels/
```

```py
make_new_tsv("mels/autotagging_moodtheme.tsv")
```

- add_new_tag - dodaje nową kolumnę BASE_FREQ do pliku mels/autotagging_moodtheme_mels.tsv, w której zawarta będzie informacja o oryginalnej częstotliwości próbkowania

```py
add_new_tag("mels/autotagging_moodtheme_mels.tsv")
```

- add_train_and_test - dodaje nową kolumnę DATASET_TYPE, która mówi, które dane będą należeć, do którego typu datasetu na podstawie pliku wejściowego z repozytorium z mtg-jamendo-dataset, a dokładniej podziału 0 (split-0)

```py
add_train_and_test("mtg-jamendo-dataset/data/splits/split-0/autotagging_moodtheme-test.tsv", "mels/autotagging_moodtheme_mels.tsv")
add_train_and_test("mtg-jamendo-dataset/data/splits/split-0/autotagging_moodtheme-train.tsv", "mels/autotagging_moodtheme_mels.tsv")
```

