import json
import numpy as np
import os

from utils.json_ import jsonYOLO

from ultralytics import YOLO
from glob import glob

def delete_patch_temp(pilihan:str):
    lst = glob(f'public/patch-temp/patch*.{pilihan}')
    for i in lst:
        os.remove(i)

def delete_files_with_extensions(root_folder, extensions):
    # Loop through each extension and delete matching files
    for ext in extensions:
        # Search for files with the given extension recursively in the root folder
        files_to_delete = glob(os.path.join(root_folder, f"**/*{ext}"), recursive=True)
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def delete_png_files(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    # Iterate over the files
    for file in files:
        # Check if the file ends with .png
        if file.endswith(".png"):
            # Construct the full file path
            file_path = os.path.join(folder_path, file)
            # Remove the file
            os.remove(file_path)

class NumpyArrayEncoder(json.JSONEncoder):
    # definisi encoder untuk membaca list sebagai json
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    
class Predict:
    def __init__(self, img, show_box=False, conf=0.4, iou=0.7, model='public/base-model/yolo-nano-5000.pt'):
        self.img = img
        self.show_box = show_box
        self.conf = conf
        self.iou = iou
        self.model = model
        self.res = self.predict()
    
    def predict(self):
        # predict image dengan model yolo, output berupa list ndarray
        model = YOLO(self.model) #best model pake 53 aja
        res = model.predict(
            self.img, 
            show_boxes=self.show_box, 
            conf=self.conf, 
            iou=self.iou,
            verbose=False,
        )

        return res
    
    def to_json(self, save_path, tipe= 'masks' or 'boxes'):    
        # export output list ke data format json
        self.tipe = tipe
        if tipe=='masks':
            if [r.masks for r in self.res] == [None]:
                mask_all = [[]]
                kelas = [[]]
            else:
                mask_all = [r.masks.xyn for r in self.res]
                # tambahan class
                kelas = [r.boxes.cls[0] for r in self.res]

        elif tipe=='boxes':
            if [r.boxes for r in self.res] == [None]:
                mask_all = [[]]
            else:
                mask_all = [r.boxes.xyxyn for r in self.res]

        else:
            raise ValueError("Harus pilih antara 'masks' atau 'boxes'")

        list_hasil = []

        for i in range(len(mask_all[0])):
            isian = {
                'id': f'{self.img}_{i+100}',
                'img_path': self.img,
                'kelas': kelas[0].tolist(),
                'hasil': mask_all[0][i].tolist(),
            }
            list_hasil.append(isian)

        encoded = json.dumps(list_hasil, cls=NumpyArrayEncoder, indent=2)

        with open(save_path, 'w') as f:
            f.write(encoded)

        # print(f'data disimpan di {save_path}')
    
    def combine_json(overlap:float, tipe= 'masks' or 'boxes'):
        lst = glob('public/patch-temp/patch*.json')
        colNrow = np.sqrt(len(lst))
        arr = []

        for i in range(len(lst)):
            # mengatur konstanta transformasi koordinat
            x = (i - (i//colNrow)*colNrow) * overlap
            y = (i // colNrow) * overlap
            # scale = 2-overlap
            scale = 1 - np.power((1-overlap),2)
            # scale = 1
            

            ann = jsonYOLO(f'public/patch-temp/patch{i+10001}.json').load()
            clss = jsonYOLO(f'public/patch-temp/patch{i+10001}.json').load_cls()

            if tipe == 'boxes':
                for j in range(len(ann)):
                    # penyesuaian koordinat box
                    if len(ann[j]) == 0:
                        pass
                    else:
                        for k in range(4):
                            if k%2 == 0:
                                ann[j][k]+=x
                                ann[j][k]*=(scale/colNrow)
                            else:
                                ann[j][k]+=y
                                ann[j][k]*=(scale/colNrow)
            elif tipe == 'masks':
                # penyesuaian koordinat segmentasi
                for j in range(len(ann)):
                    if len(ann[j][:][:]) == 0:
                        pass
                    else:
                        ann[j][:][:][:,0]+=(x) # sumbu x
                        ann[j][:][:][:,1]+=(y) # sumbu y

                        ann[j][:][:][:,0]*=(scale/colNrow) # sumbu x
                        ann[j][:][:][:,1]*=(scale/colNrow) # sumbu y
                        pass
            else:
                raise ValueError("Harus pilih antara 'masks' atau 'boxes'")

            list_hasil = []

            for k in range(len(ann)):
                    isian = {
                        'id': f'{i}_{k+100}',
                        'img_path': f'public/patch-temp/patch{k+10001}.png',
                        'kelas': clss[k],
                        'hasil': ann[k].tolist(),
                    }
                    list_hasil.append(isian)

            with open(f'public/patch-temp/patch{i+10001}.json', 'w') as output_file:
                json.dump(list_hasil, output_file, indent=2, cls=NumpyArrayEncoder)
            

        for i in range(len(lst)):
            if i == 0:
                with open(f'public/patch-temp/patch{i+10001}.json', 'r') as f:
                    arr = json.load(f)

            with open(f'public/patch-temp/patch{i+10001}.json', 'r') as f:
                tambahan = json.load(f)
            
            arr = arr + tambahan

        # clear image patch dalamm folder temp
        delete_patch_temp('png')
        delete_patch_temp('json')
        # delete_png_files('datasets/img')
        delete_files_with_extensions('./', ['.png', '.aux.xml'])
        # delete_png_files('datasets/trial-maret')

        # Write the combined list to a new JSON file
        output_file_path = 'public/patch-temp/combined_file.json'
        with open(output_file_path, 'w') as output_file:
            json.dump(arr, output_file, indent=2)

        # print(f"Combined file disimpan di: {output_file_path}")
