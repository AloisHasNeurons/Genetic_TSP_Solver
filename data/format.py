import pandas as pd
def load_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

# Usage
file_path = 'data\countries.txt'
data = load_file(file_path)
lines = data.split('\n')
trimmed_lines = [line.lstrip() for line in lines]
data = '\n'.join(trimmed_lines)
# Sort the lines in alphabetical order
sorted_data = sorted(trimmed_lines)
# Join the sorted lines with newline character
data = '\n'.join(sorted_data)


# Lire le fichier CSV
df = pd.read_csv('data\worldcities.csv')

# Obtenir les pays uniques
unique_countries = df['Country'].unique()

# Convertir data en un ensemble
data_set = set(data.split('\n'))

# Convertir unique_countries en un ensemble
unique_countries_set = set(unique_countries)

# Obtenir les pays communs
common_countries = data_set.intersection(unique_countries_set)

# Convertir l'ensemble en une liste
common_countries_list = sorted(list(common_countries))

# Convertir la liste en une chaîne avec des sauts de ligne
data = '\n'.join(common_countries_list)

# Réécrire le fichier avec les données triées
with open(file_path, 'w') as file:
    file.write(data)
