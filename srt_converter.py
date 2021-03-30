import re
import math

file_name = input("Input file name (without extension) : ")

metadata_file = open(f"{file_name}.txt", "r")
read_metadata = metadata_file.read()

#Ekstrasi bujur
long_deg = re.findall(r'\[Doc\d+\]\s+GPS Longitude\s+\:\s+(\d+)\sdeg\s\d+\'\s\d+\.\d+["]\s[EW]', read_metadata)
int_long_deg = [int(i) for i in long_deg]

long_min = re.findall(r'\[Doc\d+\]\s+GPS Longitude\s+\:\s+\d+\sdeg\s(\d+)\'\s\d+\.\d+["]\s[EW]', read_metadata)
int_long_min = [int(i) for i in long_min]

long_sec = re.findall(r'\[Doc\d+\]\s+GPS Longitude\s+\:\s+\d+\sdeg\s\d+\'\s(\d+\.\d+)["]\s[EW]', read_metadata)
float_long_sec = [float(i) for i in long_sec]

long_east_west = long_sec = re.findall(r'\[Doc\d+\]\s+GPS Longitude\s+\:\s+\d+\sdeg\s\d+\'\s\d+\.\d+["]\s([EW])', read_metadata)

for i in range(len(long_east_west)):
	if long_east_west[i] == 'E':
		long_east_west[i] = 1
	elif long_east_west[i] == 'W':
		long_east_west[i] = -1

long_dec = []
for i in range(len(long_deg)):
	dec = int_long_deg[i] + int_long_min[i]/60 + float_long_sec[i]/3600
	long_dec.append(dec)

truth_long_dec = [long_dec[i] * long_east_west[i] for i in range(len(long_dec))]

#Ekstrasi lintang
lat_deg = re.findall(r'\[Doc\d+\]\s+GPS Latitude\s+\:\s+(\d+)\sdeg\s\d+\'\s\d+\.\d+["]\s[NS]', read_metadata)
int_lat_deg = [int(i) for i in lat_deg]


lat_min = re.findall(r'\[Doc\d+\]\s+GPS Latitude\s+\:\s+\d+\sdeg\s(\d+)\'\s\d+\.\d+["]\s[NS]', read_metadata)
int_lat_min = [int(i) for i in lat_min]

lat_sec = re.findall(r'\[Doc\d+\]\s+GPS Latitude\s+\:\s+\d+\sdeg\s\d+\'\s(\d+\.\d+)["]\s[NS]', read_metadata)
float_lat_sec = [float(i) for i in lat_sec]

lat_north_south = re.findall(r'\[Doc\d+\]\s+GPS Latitude\s+\:\s+\d+\sdeg\s\d+\'\s\d+\.\d+["]\s([NS])', read_metadata)

for i in range(len(lat_north_south)):
	if lat_north_south[i] == 'N':
		lat_north_south[i] = 1
	elif lat_north_south[i] == 'S':
		lat_north_south[i] = -1

lat_dec = []
for i in range(len(lat_deg)):
	dec = int_lat_deg[i] + int_lat_min[i]/60 + float_lat_sec[i]/3600
	lat_dec.append(dec)

truth_lat_dec = [lat_dec[i] * lat_north_south[i] for i in range(len(lat_dec))]

lat_long = [f"%.6f, %.6f"%(truth_lat_dec[i], truth_long_dec[i]) for i in range(len(truth_long_dec))]

#Ekstraksi waktu
time_hour = re.findall(r'\[Doc\d+\]\s+GPS Date Time\s+\:\s+\d{4}\:\d{0,2}:\d{0,2}\s(\d{0,2})\:\d{0,2}\:\d{0,2}\.\d+', read_metadata)
int_time_hour = [int(i) for i in time_hour]

time_minute = re.findall(r'\[Doc\d+\]\s+GPS Date Time\s+\:\s+\d{4}\:\d{0,2}:\d{0,2}\s\d{0,2}\:(\d{0,2})\:\d{0,2}\.\d+', read_metadata)
int_time_minute = [int(i) for i in time_minute]

time_second = re.findall(r'\[Doc\d+\]\s+GPS Date Time\s+\:\s+\d{4}\:\d{0,2}:\d{0,2}\s\d{0,2}\:\d{0,2}\:(\d{0,2}\.\d+)', read_metadata)
float_time_second = [float(i) for i in time_second]

time_dec = []
for i in range(len(time_hour)):
	dec = int_time_hour[i] + int_time_minute[i]/60 + float_time_second[i]/3600
	time_dec.append(dec)

time_diff = []
for i in range(len(time_dec) - 1):
	diff = time_dec[i + 1] - time_dec[i]
	time_diff.append(diff)

list_diff_second = []

#Perbedaan waktu dalam format jam menit detik
for i in range(len(time_diff)):
	diff_hour = math.trunc(time_diff[i])
	diff_minute = math.trunc((time_diff[i] - diff_hour) * 60)
	diff_second = (time_diff[i] - diff_hour - diff_minute/60) * 3600
	list_diff_second.append(diff_second)

#Untuk durasi terakhir
last_duration = re.findall(r'\[Doc\d+\]\s+Sample Duration\s+\:\s+(\d+\.\d+)\ss', read_metadata)
float_last_duration = [float(i) for i in last_duration]
list_diff_second.append(float_last_duration[-1])

#Ekstrasi jumlah data gps per doc
doc_list = re.findall(r'\[Doc(\d+)\]\s+GPS Longitude\s+\:\s+\d+\sdeg\s\d+\'\s\d+\.\d+["]\s[EW]', read_metadata)
int_doc_list = [int(i) for i in doc_list]

total_doc = int_doc_list[-1]

gps_per_doc = []
for i in range(1, total_doc + 1):
	count = int_doc_list.count(i)
	gps_per_doc.append(count)

#Durasi
duration = []
for i in range(len(gps_per_doc)):
	duration_per_doc = list_diff_second[i] / gps_per_doc[i]
	duration.append(duration_per_doc)

gps_range = []
for i in range(len(gps_per_doc)):
	for j in range(gps_per_doc[i]):
		gps_range.append(duration[i])

#Konversi gps range ke format srt
for_end = gps_range[0] + 0
end_range = []
end_range.append(for_end)
for i in range(len(gps_range)):
	for_end += gps_range[i +1]
	if i + 1 == len(gps_range) - 1:
		break
	end_range.append(for_end)
for_end = end_range[-1] + gps_range[-1]
end_range.append(for_end)

first_range = end_range.copy()
first_range.insert(0, 0)
first_range.pop(-1)

#Konversi format detik ke format jam
hour_dec_first = []
for i in range(len(first_range)):
	hour_first = first_range[i]/3600
	hour_dec_first.append(hour_first)

hour_hms_first = []
for i in range(len(hour_dec_first)):
	hour = math.trunc(hour_dec_first[i])
	minute = math.trunc((hour_dec_first[i] - hour) * 60)
	second = (hour_dec_first[i] - hour - minute/60) * 3600
	if len(str(hour)) == 1 and len(str(minute)) == 1 and len(str(math.trunc(second))) == 1:
		join_hms = "0%d:0%d:0%.3f"%(hour, minute, second)
	elif len(str(hour)) == 1 and len(str(minute)) == 1:
		join_hms = "0%d:0%d:%.3f"%(hour, minute, second)
	elif len(str(hour)) == 1 and len(str(math.trunc(second))) == 1:
		join_hms = "0%d:%d:0%.3f"%(hour, minute, second)
	elif len(str(minute)) == 1 and len(str(math.trunc(second))) == 1:
		join_hms = "%d:0%d:0%.3f"%(hour, minute, second)
	elif len(str(hour)) == 1:
		join_hms = "0%d:%d:%.3f"%(hour, minute, second)
	elif len(str(minute)) == 1:
		join_hms = "%d:0%d:%.3f"%(hour, minute, second)
	elif len(str(math.trunc(second))) == 1:
		join_hms = "%d:%d:0%.3f"%(hour, minute, second)
	else:
		join_hms = "%d:%d:%.3f"%(hour, minute, second)
	hour_hms_first.append(join_hms)

hour_dec_end = []
for i in range(len(end_range)):
	hour_end = end_range[i]/3600
	hour_dec_end.append(hour_end)

hour_hms_end = []
for i in range(len(hour_dec_end)):
	hour = math.trunc(hour_dec_end[i])
	minute = math.trunc((hour_dec_end[i] - hour) * 60)
	second = (hour_dec_end[i] - hour - minute/60) * 3600
	if len(str(hour)) == 1 and len(str(minute)) == 1 and len(str(math.trunc(second))) == 1:
		join_hms = "0%d:0%d:0%.3f"%(hour, minute, second)
	elif len(str(hour)) == 1 and len(str(minute)) == 1:
		join_hms = "0%d:0%d:%.3f"%(hour, minute, second)
	elif len(str(hour)) == 1 and len(str(math.trunc(second))) == 1:
		join_hms = "0%d:%d:0%.3f"%(hour, minute, second)
	elif len(str(minute)) == 1 and len(str(math.trunc(second))) == 1:
		join_hms = "%d:0%d:0%.3f"%(hour, minute, second)
	elif len(str(hour)) == 1:
		join_hms = "0%d:%d:%.3f"%(hour, minute, second)
	elif len(str(minute)) == 1:
		join_hms = "%d:0%d:%.3f"%(hour, minute, second)
	elif len(str(math.trunc(second))) == 1:
		join_hms = "%d:%d:0%.3f"%(hour, minute, second)
	else:
		join_hms = "%d:%d:%.3f"%(hour, minute, second)
	hour_hms_end.append(join_hms)

srt_range = []
for i in range(len(hour_hms_first)):
	range_format = f"{hour_hms_first[i]} --> {hour_hms_end[i]}"
	srt_range.append(range_format)

truth_srt_range = []
for i in range(len(srt_range)):
	comma_format = srt_range[i].replace(".", ",")
	truth_srt_range.append(comma_format)

#Konversi ke txt ada di bawah sini

subtitle_file = open(f"Subtitle_{file_name}.srt", "x")

try:
	for i in range(len(lat_long)):
		subtitle_file.write(str(i + 1) + "\n")
		subtitle_file.write(f"{truth_srt_range[i]}\n")
		subtitle_file.write(f"{lat_long[i]}\n")
		subtitle_file.write("\n")
	print(f"Success! Srt file name is Subtitle_{file_name}.srt")
except:
	print("There are errors")