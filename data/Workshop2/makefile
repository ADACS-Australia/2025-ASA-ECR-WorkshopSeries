.PHONY: AT20G NVSS all clean

AT20G: data/final/AT20G_final.csv data/final/AT20G_header.txt

NVSS: data/final/NVSS_final.csv data/final/NVSS_header.txt

SUMSS: data/final/SUMSS_final.csv data/final/SUMSS_header.txt

all: AT20G NVSS SUMSS

# AT20G survey
data/raw/AT20G.tsv:
	wget -O data/raw/AT20G.tsv https://raw.githubusercontent.com/ADACS-Australia/2025-ASA-ECR-WorkshopSeries/refs/heads/gh-pages/data/Workshop1/AT20G.tsv

data/final/AT20G_header.txt: data/raw/AT20G.tsv
	grep -e '^#' data/raw/AT20G.tsv > data/final/AT20G_header.txt

data/processing/AT20G_table.tsv: data/raw/AT20G.tsv
	grep -v -e '^\#' -e '^-' -e '^deg' -e '^$$' data/raw/AT20G.tsv > data/processing/AT20G_table.tsv

data/final/AT20G_final.csv: data/processing/AT20G_table.tsv src/clean_tables.py
	python src/clean_tables.py -s AT20G -i data/processing/AT20G_table.tsv -o data/final/AT20G_final.csv


# NVSS survey
data/raw/NVSS.tsv:
	wget -O data/raw/NVSS.tsv https://github.com/ADACS-Australia/2025-ASA-ECR-WorkshopSeries/raw/refs/heads/gh-pages/data/Workshop2/NVSS.tsv

data/final/NVSS_header.txt: data/raw/NVSS.tsv
	grep -e '^#' data/raw/NVSS.tsv > data/final/NVSS_header.txt

data/processing/NVSS_table.tsv: data/raw/NVSS.tsv
	grep -v -e '^\#' -e '^-' -e '^deg' -e '^$$' data/raw/NVSS.tsv > data/processing/NVSS_table.tsv

data/final/NVSS_final.csv: data/processing/NVSS_table.tsv src/clean_tables.py
	python src/clean_tables.py -s NVSS -i data/processing/NVSS_table.tsv -o data/final/NVSS_final.csv


# SUMSS survey
data/raw/SUMSS.tsv:
	wget -O data/raw/SUMSS.tsv https://github.com/ADACS-Australia/2025-ASA-ECR-WorkshopSeries/raw/refs/heads/gh-pages/data/Workshop2/SUMSS.tsv

data/final/SUMSS_header.txt: data/raw/SUMSS.tsv
	grep -e '^#' data/raw/SUMSS.tsv > data/final/SUMSS_header.txt

data/processing/SUMSS_table.tsv: data/raw/SUMSS.tsv
	grep -v -e '^\#' -e '^-' -e '^deg' -e '^$$' data/raw/SUMSS.tsv > data/processing/SUMSS_table.tsv

data/final/SUMSS_final.csv: data/processing/SUMSS_table.tsv src/clean_tables.py
	python src/clean_tables.py -s SUMSS -i data/processing/SUMSS_table.tsv -o data/final/SUMSS_final.csv

clean:
	rm data/*/AT20G*
	rm data/*/NVSS*
	rm data/*/SUMSS*
