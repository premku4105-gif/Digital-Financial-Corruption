import urllib.request
import json
from pathlib import Path

# URL for a reliable simplified Indian states GeoJSON
geojson_url = "https://raw.githubusercontent.com/datameet/maps/master/website/docs/data/geojson/states.geojson"
output_path = Path("C:/Users/Likith.N/.gemini/antigravity/scratch/financial-corruption-app/data/india_states.geojson")

output_path.parent.mkdir(parents=True, exist_ok=True)

try:
    print(f"Downloading Indian state boundaries from: {geojson_url}")
    with urllib.request.urlopen(geojson_url) as response:
        data = json.loads(response.read().decode('utf-8'))
        
    # Write the data to local file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully downloaded and saved GeoJSON map to {output_path}")
except Exception as e:
    print(f"Error downloading GeoJSON map: {e}")
    # In case download fails, we write an empty fallback structure
    fallback = {"type": "FeatureCollection", "features": []}
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(fallback, f)
