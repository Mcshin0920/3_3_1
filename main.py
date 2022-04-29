import pandas as pd

#converts sat_scores.csv into a list of
#averages for each school district
def district_average(in_file, out_file):
  in_data = pd.read_csv("./" + in_file)
  in_data = in_data[["District Name", "Average Total Score"]]
  out_data = pd.DataFrame(columns=["District", "Average"])

  districts = in_data["District Name"].drop_duplicates()
  for district in districts:
    schools = in_data[in_data["District Name"] == district]
    average = schools["Average Total Score"]
    average = average[average.astype(str).str.isdigit()]
    result = 0
    if len(average) > 0:
      result = sum(map(int, list(average)))//len(average)
    if result > 0:
      out_data = out_data.append([district, result])
    
    out_data.to_csv("./" + out_file, index=False)

district_average("sat_scores.csv", "test.csv")
#in_data = pd.read_csv("./" + "test.csv")
#print(in_data)
