from PIL import Image
import exifread
from datetime import datetime as dt
import os
import shutil
import sys

###
# detect if the file is an image
##
def check_image_with_pil(path):
	try:
		Image.open(path)
	except IOError:
		return False
	return True

destination_path="c:/temp/organized"
src_path="c:/temp/images"

if not os.path.exists(destination_path):
	os.mkdir(destination_path)


#src_path = sys.argv[1]
img_files = [f for f in os.listdir(src_path) if os.path.isfile(os.path.join(src_path, f))]
print ("Files to process %s" % len(img_files))
clean_target_dir_path = ""

for fname in img_files:
	img_path = "%s/%s" % (src_path, fname)
	if check_image_with_pil(img_path):
			f = open(img_path, "rb")
			tags = exifread.process_file(f, details=False)
			meta_keys = tags.keys()
			datetime_meta_key = "Image DateTime"
			print (tags)
			if not "Image DateTime" in meta_keys:
				if "EXIF DateTimeOriginal" in meta_keys:
					datetime_meta_key = "EXIF DateTimeOriginal"
				else:
					# no datetime metadata
					datetime_meta_key = None
			if datetime_meta_key is not None:
				img_datetime = dt.strptime("%s" % tags[datetime_meta_key], "%Y:%m:%d %H:%M:%S")
				year_date_str = img_datetime.strftime("%Y")
				month_date_str = img_datetime.strftime("%m")
				day_date_str = img_datetime.strftime("%d")
				clean_target_dir_path = "%s/%s/%s/%s " % (destination_path,year_date_str,month_date_str, day_date_str)
				print ("The file [%s] -- Key: %s, value is %s" % (img_path, datetime_meta_key, clean_target_dir_path))
			else:
				clean_target_dir_path = destination_path + "/nometa"
				print ("The file [%s] does not contain date time meta-info [%s]" % (img_path, datetime_meta_key))
	else:
		clean_target_dir_path = detination_path + "/waiting"
		print ("The file [%s] is not an available image." % img_path)

	if not os.path.exists(clean_target_dir_path):
		os.mkdir(clean_target_dir_path)
	#copy this image into the date time tagged directory
	shutil.copy2(img_path, clean_target_dir_path)
	
	
