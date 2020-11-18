#!/bin/bash

python3 run.py images/troyita.png images/mosaic/ 100 3000 results/average/troyita_average_100.jpg
python3 run.py images/troyita.png images/mosaic/ 150 3000 results/average/troyita_average_150.jpg
python3 run.py images/troyita.png images/mosaic/ 300 3000 results/average/troyita_average_300.jpg

python3 run.py images/troyita_buenasnoches.png images/mosaic/ 100 3000 results/average/troyita_buenasnoches_average_100.jpg
python3 run.py images/troyita_buenasnoches.png images/mosaic/ 150 3000 results/average/troyita_buenasnoches_average_150.jpg
python3 run.py images/troyita_buenasnoches.png images/mosaic/ 300 3000 results/average/troyita_buenasnoches_average_300.jpg

python3 run.py images/flores.png images/mosaic/ 100 3000 results/average/flores_average_100.jpg
python3 run.py images/flores.png images/mosaic/ 150 3000 results/average/flores_average_150.jpg
python3 run.py images/flores.png images/mosaic/ 300 3000 results/average/flores_average_300.jpg
