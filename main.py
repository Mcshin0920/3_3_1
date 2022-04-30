import pandas as pd
import shapefile as sf

def sat_average(in_file, out_file):
  in_data = pd.read_csv(in_file)
  in_data = in_data[["District Name", "Average Total Score"]]
  out_data = pd.DataFrame(columns=["District", "SAT"])

  districts = in_data["District Name"].drop_duplicates()
  for district in districts:
    schools = in_data[in_data["District Name"] == district]
    average = schools["Average Total Score"]
    average = average[average.astype(str).str.isdigit()]
    result = 0
    if len(average) > 0:
      result = int(average.max())
    if result > 0:
      temp_data = pd.DataFrame({
        "District": [district], "SAT": [result]
      })
      out_data = out_data.append(temp_data)
    
    out_data.to_csv(out_file, index=False)
  
def home_to_district(house_file, shape_dir, out_file):
  house_data = pd.read_csv(house_file)
  house_data = house_data[["latitude", "longitude", "median_house_value"]]
  shape_data = sf.Reader(shape_dir)
  out_data = pd.DataFrame(columns=["District", "Price"])
  for i in range(house_data.shape[0]):
    lat, long = float(house_data["latitude"][i]), float(house_data["longitude"][i])
    bbox = [long-0.0005, lat-0.0005, long+0.0005, lat+0.0005]
    fields = ["NAME", "ELSDLEA"]
    for shapeRec in shape_data.iterShapeRecords(bbox=bbox, fields=fields):
      record = shapeRec.record
      if not record[1] and "NOT DEFINED" not in record[0]:
        temp_data = pd.DataFrame({
          "District": [record[0]], "Price": [house_data["median_house_value"][i]]
        })
        out_data = out_data.append(temp_data)
        break
    out_data.to_csv(out_file, index=False)

def price_average(in_file, out_file):
  in_data = pd.read_csv(in_file)
  out_data = pd.DataFrame(columns=["District", "Price"])
  districts = in_data["District"].drop_duplicates()
  for district in districts:
    houses = in_data[in_data["District"] == district]
    average = houses["Price"].mean()
    temp_data = pd.DataFrame({
      "District": [district], "Price": [average]
    })
    out_data = out_data.append(temp_data)
  out_data.to_csv(out_file, index=False)

def make_final(sat_file, house_file, out_file):
    house_data = pd.read_csv(house_file)
    sat_data = pd.read_csv(sat_file)
    out_data = pd.DataFrame(columns=["SAT", "Price"])
    for i in range(house_data.shape[0]):
      district = house_data["District"][i]
      sat = sat_data.loc[sat_data["District"].str.contains(district, case=False)].reset_index()
      if sat.shape[0] > 0:
        sat = sat["SAT"][0]
      else:
        continue
      temp_data = pd.DataFrame({
        "SAT": [sat], "Price": [house_data["Price"][i]]
      })
      out_data = out_data.append(temp_data)
    out_data.to_csv(out_file, index=False)










#sat_average("sat_scores.csv", "district_sat.csv")
#home_to_district("housing_prices.csv", "district_bounds/district_bounds", "test.csv")
#price_average("district_price.csv", "house_average.csv")
make_final("district_sat.csv", "house_average.csv", "final.csv")
