import base64
from pathlib import Path
import imghdr

#####################################################
# folder where image files are read
read_img_dir = Path(r'data')

# folder where base64.txt are saved
save_txt_dir = Path(r'data/base64')

#####################################################

### check paths and directory
if not read_img_dir.exists():
    print(f"read_img_dir {read_img_dir} does not exist ")
    quit()

if not save_txt_dir.exists():
    save_txt_dir.mkdir(parents=True, exist_ok=True)

### encode bytes to base64
for img_file in read_img_dir.iterdir():
    # Skip conversion if it is a directory
    if img_file.is_dir():
        continue
    #  Skip conversion if it is not an image
    if imghdr.what(img_file) is not None:
        img_file_path = img_file

        ### read image
        read_img_path = read_img_dir / (img_file_path.name)
        with open(str(read_img_path), 'rb') as reader:
            img_bytes = reader.read()

        ### save text
        save_txt_path = save_txt_dir / (img_file_path.name).replace(img_file_path.suffix, ".txt")
        with open(str(save_txt_path), 'w') as writer:
            img_string = base64.b64encode(img_bytes).decode('utf-8')
            img_string = img_string.replace("\n","")
            writer.write(img_string)