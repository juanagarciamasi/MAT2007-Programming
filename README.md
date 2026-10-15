# MAT2007-Programming
Intro to Programming repository
# Humboldt Penguin Speed Analysis
Research Question: How do individual Humboldt penguins differ in their hourly movement speed, and how much of the variation in speed is explained by individual identity?

# Dataset: 
- Source: Movebank (https://datarepository.movebank.org/entities/datapackage/60a9c039-becf-464c-9e86-d54f8e5b87e8)
- File used: Humboldt penguin GPS tracking 2022 (Hourly averages)

# What the script does
- Cleans the dataset
- Calculates distance between consecutive hourly positions, using the haversine formula, and converts it to speed (km/h)
- Computes the mean speed per penguin
- One-way ANOVA test across individuals
- Visualizes:
  - Mean speed per penguin (km/h) with standard deviation
  - Distribution of hourly speeds pooled together
  - GPS tracks of all penguins

# Output
The script generates:
- `plot_individuals.png`
- `plot_distribution.png`
- `plot_tracks.png`

# How to run code
- python3 Project.py
- Requires: numpy, pandas, matplotlib and scipy
