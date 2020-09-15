import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import requests, json 



df = pd.read_csv("C:/Users/jaski/OneDrive/Desktop/major project/doctor_dataset.csv")

unique = sorted(list(df["Speciality"].unique()))

unique_specialities = []
unique_specialities.append(('Select',"None"))
for u in unique:
	unique_specialities.append((u,u))


def calculate_distance(lat1, long1, lat2, long2):
	R = 6373.0
	dlon = long2 - long1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

	return distance



def sort_by_distance(lat, lng, speciality):
	df = pd.read_csv("C:/Users/jaski/OneDrive/Desktop/major project/doctor_dataset.csv")
	newdf = df.where(df["Speciality"] == speciality).dropna()
	dist = []
	for i in range(len(newdf)):
		dist.append(calculate_distance(lat, lng, newdf["lat"].iloc[i], newdf["lng"].iloc[i]))
	newdf["distance"] = dist
	newdf = newdf.sort_values(by=["distance"])
	result = []
	for i in range(5):
		try:
			result.append(newdf.iloc[i].dropna().to_dict())
		except:
			pass

	return result

def sort_by_rating(speciality):
	df = pd.read_csv("C:/Users/jaski/OneDrive/Desktop/major project/doctor_dataset.csv")
	newdf = df.where(df["Speciality"] == speciality).dropna()
	newdf = newdf.sort_values(by=["Rating"], ascending=False)
	result = []
	for i in range(5):
		result.append(newdf.iloc[i].dropna().to_dict())

	return result

def sort_by_rate(speciality):
	df = pd.read_csv("C:/Users/jaski/OneDrive/Desktop/major project/doctor_dataset.csv")
	newdf = df.where(df["Speciality"] == speciality).dropna()
	newdf = newdf.sort_values(by=["Rate"])
	result = []
	for i in range(5):
		result.append(newdf.iloc[i].dropna().to_dict())

	return result

