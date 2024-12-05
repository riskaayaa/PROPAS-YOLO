import numpy as np
import cv2
import patchify as p

from osgeo import gdal

class tile_img:
    def __init__(self, img_path:str, DIM):
        if img_path.endswith('tif') is True:
            gdal.Translate(img_path.replace('tif', 'png'), img_path, format='PNG')
        elif img_path.endswith('ecw') is True:
            gdal.Translate(img_path.replace('ecw', 'png'), img_path, format='PNG')

        self.img = cv2.imread(img_path.replace('tif', 'png'))
        self.h0 = self.img.shape[0]
        self.w0 = self.img.shape[1]

        temp = [DIM*((self.h0//DIM)+1), DIM*((self.w0//DIM)+1)]
        dimm = temp[0] if temp[0] > temp[1] else temp[1]
        self.temp = temp
        self.dim = [dimm, dimm]
        self.h = dimm
        self.w = dimm
        # self.h = self.temp[0]
        # self.w = self.temp[1]

    def patchData(self, patch_dim:int, step_size:float, resize:int=None):
        img = np.array(self.img)
        if resize:
            img = cv2.resize(img, (self.w//resize, self.h//resize))

        # pembulatan channel img
        ch1 = np.ceil(self.h/patch_dim).astype(int)
        ch2 = np.ceil(self.w/patch_dim).astype(int)

        # menambahkan kolom dan baris kosong pd gambar
        arr0 = np.zeros((ch1*patch_dim, ch2*patch_dim, 3))
        arr0[:self.h0, :self.w0] += img
        arr = arr0.astype(np.uint8)
        self.arr = arr.shape
        print(arr.shape)

        # patch image
        patch_shape = (patch_dim, patch_dim, 3)
        patches = p.patchify(arr, patch_shape, step=int(patch_dim*step_size))
        self.patch = patches.shape

        img_patches = []
        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):
                img_patches.append(patches[i,j,0,:,:,:])

        return np.array(img_patches), self
        
    def combineData(self, img_patches:np.ndarray):
        # bagian unpatch gambar
        unpatch_img = img_patches.reshape(self.patch)
        reconstructed_image = p.unpatchify(unpatch_img, self.arr)

        return reconstructed_image[:self.h, :self.w, :]
    

# # contoh penggunaan tiling
# img, _ = tile_img('ortho_Kav2_30cm.png').patchData(patch_dim=DIM, step_size=1)
# print(f'shape tile dataset : {img.shape}')

# for i in range(img.shape[0]):
#     cv2.imwrite(f'public/patch-temp/patch{i+101}.png', img[i])

# # contoh penggunaan untuk menggabungkan tile
# img_full = _.combineData(img)
# print(f'shape combined dataset : {img_full.shape}')

# cv2.imwrite('public/patch-temp/full.png', img_full)