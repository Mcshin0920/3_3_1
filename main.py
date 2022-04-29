import pandas as pd
import shapefile as sf

#converts sat_scores.csv into a list of
#averages for each school district
def district_average(in_file, out_file):
  in_data = pd.read_csv(in_file)
  in_data = in_data[["District Number", "Average Total Score"]]
  out_data = pd.DataFrame(columns=["District", "Average"])

  districts = in_data["District Number"].drop_duplicates()
  for district in districts:
    schools = in_data[in_data["District Number"] == district]
    average = schools["Average Total Score"]
    average = average[average.astype(str).str.isdigit()]
    result = 0
    if len(average) > 0:
      result = sum(map(int, list(average)))//len(average)
    if result > 0:
      temp_data = pd.DataFrame({
        "District": [district], "Average": [result]
      })
      out_data = out_data.append(temp_data)
    
    out_data.to_csv(out_file, index=False)
  
def home_to_district(house_file, shape_dir, out_file):
  house_data = pd.read_csv(house_file)
  house_data = house_data[["latitude", "longitude", "median_house_value"]]
  shape_data = sf.Reader(shape_dir)
  print(shape_data.fields)
  for i in range(house_data.shape[0]):
    lat, long = float(house_data["latitude"][i]), float(house_data["longitude"][i])
    bbox = [long-0.01, lat-0.01, long+0.01, lat+0.01]
    fields = ["SCSDLEA", "UNSDLEA"]
    for shapeRec in shape_data.iterShapeRecords(bbox=bbox, fields=fields):
      print(shapeRec.record)


#district_average("sat_scores.csv", "test.csv")
home_to_district("housing_prices.csv", "district_bounds/district_bounds", "test")