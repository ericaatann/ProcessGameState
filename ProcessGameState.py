import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class ProcessGameState:
    def __init__(self, file_path):
        file_path = 'C:\\Users\\Erica\\Downloads\\game_state_frame_data.parquet'
        self.data = self.load_data(file_path)

    def load_data(self, file_path):
        # Assuming the data is stored in a parquet file format
        # Load the parquet file into a DataFrame
        df = pd.read_parquet(file_path)
        
        # Print column names
        # print(df.columns)
        
        return df
    
    def is_within_boundary(self, x, y, z, boundary_vertices):
        # Check if the given (x, y, z) coordinates fall within the boundary
        # defined by the provided vertices
        x_coords = [coord[0] for coord in boundary_vertices]
        y_coords = [coord[1] for coord in boundary_vertices]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        return x_min <= x <= x_max and y_min <= y <= y_max and 285 <= z <= 421

    def get_common_strategy_usage(self, team, side, boundary_vertices):
        # Calculate the percentage of entries via the provided boundary for the specified team and side
        team_data = self.data[(self.data['team'] == team) & (self.data['side'] == side)]
        total_entries = len(team_data)
        entries_via_boundary = sum(team_data.apply(lambda row: self.is_within_boundary(row['x'], row['y'], row['z'], boundary_vertices), axis=1))
        common_strategy_usage = entries_via_boundary / total_entries
        return common_strategy_usage

    def get_average_entry_timer(self, team, side, min_weapon_count, weapon_classes):
        team_data = self.data[(self.data['team'] == team) & (self.data['side'] == side)]
        filtered_data = team_data[team_data['inventory'].apply(lambda x: any(weapon_class in weapon_classes for weapon_class in self.extract_weapon_classes(x if x is not None else [])))]

        if len(filtered_data) > 0:
            average_entry_timer = filtered_data['timer'].mean()
        else:
            average_entry_timer = 0

        return average_entry_timer

    def extract_weapon_classes(self, inventory_data):
        weapon_classes = [item.get('class', None) for item in inventory_data]
        weapon_classes = [wc for wc in weapon_classes if wc is not None]
        return weapon_classes

    def generate_heatmap(self, team, side):
        filtered_data = self.data[(self.data['team'] == team) & (self.data['side'] == side)]
        plt.figure(figsize=(10, 8))
        sns.kdeplot(data=filtered_data, x='x', y='y', cmap='Reds', shade=True)
        plt.title(f"Player Positions for {team} on the {side} side")
        plt.xlabel("X-coordinate")
        plt.ylabel("Y-coordinate")
        plt.show()


        game_state.generate_heatmap(team="Team2", side="CT")

game_state = ProcessGameState("game_state_frame_data.parquet")

# 2a. Is entering via the light blue boundary a common strategy used by Team2 on the T side?
boundary_vertices = [(-1735, 250), (-2024, 398), (-2806, 742), (-2472, 1233), (-1565, 580)]
common_strategy_usage = game_state.get_common_strategy_usage(team="Team2", side="T", boundary_vertices=boundary_vertices)

if common_strategy_usage >= 0.5:
    print("Entering via the light blue boundary is a common strategy used by Team2 on the T side.")
else:
    print("Entering via the light blue boundary is not a common strategy used by Team2 on the T side.")

# 2b. What is the average timer that Team2 on the T side enters "BombsiteB" with at least 2 rifles or SMGs?
weapon_classes = ["rifle", "smg"]

average_entry_timer = game_state.get_average_entry_timer(team="Team2", side="T", min_weapon_count=2, weapon_classes=weapon_classes)
print(f"The average timer for Team2 on the T side entering any bombsite with at least 2 rifles or SMGs is: {average_entry_timer}")

# 2c. Generate a heatmap of player positions for Team2 on the CT side inside "BombsiteB"
map_image = plt.imread('C:\\Users\\Erica\\Downloads\\map.jpeg') 
game_state.generate_heatmap(team="Team2", side="CT")


# Obtain the dimensions and coordinate range of the map image
map_width = 2000
map_height = 1500
min_x = -3000
max_x = 3000
min_y = -2000
max_y = 2000

# Normalize the coordinates of the heatmap
normalized_x = (game_state.data['x'] - min_x) / (max_x - min_x)
normalized_y = (game_state.data['y'] - min_y) / (max_y - min_y)

# Create a new figure and plot the map image as the background
plt.figure(figsize=(10, 8))
plt.imshow(map_image, extent=[min_x, max_x, min_y, max_y])  # Replace `map_image` with your actual map image

# Plot the heatmap on top of the map image
sns.kdeplot(data=game_state.data, x=normalized_x, y=normalized_y, cmap='Reds', fill=True)

# Customize the plot as needed
plt.title("Player Positions on Map")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
plt.xlim(min_x, max_x)
plt.ylim(min_y, max_y)

# Display the plot
plt.show()

# Close the heatmap window
plt.close()

# 3. Data Visualization and Export Options
# Your solution regarding data visualization and export options is valid. Implementing features in the dashboard that allow the coaching staff to visualize the analyzed data through charts, graphs, and heatmaps, as well as providing export options in different formats like PDF, Excel, or CSV, would enhance the usability and sharing of insights.
