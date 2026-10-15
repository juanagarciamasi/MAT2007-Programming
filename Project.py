import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Humboldt penguin GPS tracking 2022 (Hourly averages).csv", parse_dates=["timestamp"]) #tells panda that "timestamp" contains dates/times, not text

print(df.shape) # number of rows and columns
print(df.dtypes)

# Cleaning data
df = df[["individual-local-identifier", "timestamp", "location-lat", "location-long"]] # selects the columns I want
df = df.rename(columns={"individual-local-identifier": "id",
                        "location-lat": "lat",
                        "location-long": "lon"})

print(df.head())
print(df.columns)

df = df.dropna() # removes rows with missing values
df = df.drop_duplicates(["id", "timestamp"]) # removes any duplicates
df = df.sort_values(["id", "timestamp"]).reset_index(drop=True) # sorts the rows first by penguin, then by time within each penguin
print (df.shape)

# Checks for penguins with same data
mask = df.duplicated(["timestamp", "lat", "lon"], keep=False) # returnrs True if duplicate rows, aside from ID, and marks all copies
suspects = df[mask] # shows only the flagged rows
print(suspects["id"].unique())
print(suspects.groupby("id").size())

df = df[df["id"] != "CH-W-18_Vendetta"] # produces a column of True/False values, and keeps all the True, which are not Vendetta
print(df["id"].nunique())

## Function to calculate the distance between points
def haversine_km (lat1, lon1, lat2, lon2): # function with 4 inputs
    R = 6371.0088 # Earth's mean radius in km
    phi1 = np.radians(lat1) # convert degrees to radians
    phi2 = np.radians(lat2)
    dphi = phi2 - phi1 # difference in latitude
    dlambda = np.radians(lon2 - lon1) # converts the longitude difference to radians
    a = np.sin(dphi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2)**2
    return 2 * R * np.arcsin(np.sqrt(a)) # Haversine formula

# Testing
d1 = haversine_km(-29.3, -71.4, -29.3, -71.4) # # identical locations
print(d1) # expected 0

# Location based on previous lat/lon
df["prev_lat"] = df.groupby("id")["lat"].shift() # splits the table into one group per pinguin, looking only at the latitude/longitud
df["prev_lon"] = df.groupby("id")["lon"].shift() #shift goes down by row within each group
df["prev_time"] = df.groupby("id")["timestamp"].shift() # gives the previous timestamp, aligned in current row

print(df.head(8))

# checking all is in hour intervals
df["dt_hours"] = (df["timestamp"] - df["prev_time"]).dt.total_seconds() / 3600 # subtracts two datetime columns, makes them into numbers and then converted into hours
df["dist_km"] = haversine_km(df["prev_lat"], df["prev_lon"], df["lat"], df["lon"]) # applied in whole columns, computes the distance from the previous point to the current point, for every row at once.
df["speed"] = df["dist_km"] / df["dt_hours"] # to get speed in km/hour
print(df.head(8))
# filtering to one hour steps
steps = df[df["dt_hours"] == 1].copy() # gives True only for rows exactly 1 hour after their previous fix, and keeps only those rows
print(steps.shape)
print(steps["speed"].describe())

# Per penguin summary
summary = steps.groupby("id")["speed"].agg(["mean", "std", "count"]) # groups the steps by penguin and selects the speed column within each group. "agg" computes the stats for each penguin (mean, std)
print(summary)

# First plot
summary_sorted = summary.sort_values("mean") # sorts the rows, smallest to largest mean
plt.figure(figsize=(8, 6)) # creates a rectangle for the plot window
plt.barh(summary_sorted.index, summary_sorted["mean"], xerr=summary_sorted["std"]) # horizontal bar chart, with error bars of the standard deviation
plt.xlabel("Mean speed (km/h)")
plt.title("Mean speed per penguin")
plt.tight_layout() # axis labels don't get cut off
plt.savefig("plot_individuals.png")
plt.show()

# Stats
groups = [steps.loc[steps["id"] == pid, "speed"].to_numpy() for pid in steps["id"].unique()] # what
print(len(groups))
print(groups[0])

from scipy import stats
F, p = stats.f_oneway(*groups) # unpacks the list, spreading its 20 elements out as 20 separate arguments automatically.
print(F)
print(p)

# Plot 2
plt.figure(figsize=(8, 5))
plt.hist(steps["speed"], bins=20, edgecolor="white") # draws a histogram of every speed value across all penguins combined
plt.xlabel("Speed (km/h)")
plt.ylabel("Number of steps")
plt.title("Distribution of hourly speeds, all penguins pooled")
plt.tight_layout()
plt.savefig("plot_distribution.png")
plt.show()

from scipy.stats import skew
print(skew(steps["speed"])) # skewness coefficient

# Plot 3
plt.figure(figsize=(7, 7))

for pid in df["id"].unique(): # goes over each ID, using all positions, 
    track = df[df["id"] == pid]
    plt.plot(track["lon"], track["lat"], marker="o", markersize=2, linewidth=0.7, alpha=0.7) #plots longitude and latitude

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("GPS tracks of 20 Humboldt penguins")
plt.tight_layout()
plt.savefig("plot_tracks.png")
plt.show()