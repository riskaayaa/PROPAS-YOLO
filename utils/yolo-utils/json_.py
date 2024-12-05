import json 
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.patches as patches

class jsonYOLO:
    def __init__(self, path:str):
        self.path = path

    def load(self):
        # meload file json dari direktori
        with open(self.path, 'r') as r:
            array = json.load(r)
        
        hasil_array = [entry['hasil'] for entry in array]
        hasil_array = [np.array(hasil) for hasil in hasil_array]

        return hasil_array
    
    def load_cls(self):
        with open(self.path, 'r') as r:
            array = json.load(r)
        
        hasil_array = [entry['kelas'] for entry in array]
        hasil_array = [np.array(hasil) for hasil in hasil_array]

        return hasil_array

    def plot_polygons(data_list, image_shape=(320, 320)):
        # Create a blank image
        image = np.ones((image_shape[0], image_shape[1], 3), dtype=np.uint8) * 255

        # Create subplots
        fig, ax = plt.subplots()

        # Plot each polygon from the data list
        for i, data in enumerate(data_list):
            # handle error list kosong
            if len(data) > 0:
                polygon = patches.Polygon(np.array(data) * [image_shape[1], image_shape[0]], edgecolor='r', facecolor='none')
                ax.add_patch(polygon)
            else:
                pass

        # Display the image with all polygons
        plt.imshow(image)
        plt.show()

# class Converter:
#     def __init__(self, input_path:str, output_path:str, epsg:int, extent, dim):
#         with open(input_path, 'r') as r:
#             self.input = json.load(r)

#         rangeX = extent[2] - extent[0]
#         rangeY = extent[3] - extent[1]

#         # menambahkan 1,2 sebagai konstanta sementara buat data bogor
#         extent[2] = extent[0] + (rangeX*(dim.dim[1]/dim.w0))
#         extent[1] = extent[3] - (rangeY*(dim.dim[0]/dim.h0))

#         self.output = output_path
#         self.epsg = epsg
#         self.extent = extent

class Converter:
    def __init__(self, input_path:str, output_path:str, epsg:int, extent, dim, DIM):
        with open(input_path, 'r') as r:
            self.input = json.load(r)

        # coefficients = [-1.416e-06, 3.160e-04, -0.0176, 0.435, -0.948]
        # scale = sum(coefficients[i] * luas ** (4 - i) for i in range(len(coefficients)))

        rangeX = extent[2] - extent[0]
        rangeY = extent[3] - extent[1]

        # Calculate the scaling factor for width and height
        # dim.dim[1] += DIM
        # dim.dim[0] += DIM

        scaleX = ((dim.patch[0] * DIM) / (dim.w0))
        scaleY = ((dim.patch[0] * DIM) / (dim.h0))
        # scaleX = ((dim.dim[1]) / dim.w0)
        # scaleY = ((dim.dim[1]) / dim.w0)

        # # eksperimen
        # if rangeX > rangeY:
        #     rangeY = rangeX
        #     scaleY = scaleX
        # else:
        #     rangeX = rangeY
        #     scaleX = scaleY

        # Adjust the extent coordinates
        extent[2] = extent[0] + (rangeX * scaleX)
        extent[1] = extent[3] - (rangeY * scaleY)

        self.metadata = [rangeX, rangeY, scaleX, scaleY, extent[2], extent[1]]
        self.meta2 = [dim.dim[1], dim.dim[0], dim.w0, dim.h0]

        self.output = output_path
        self.epsg = epsg
        self.extent = extent

    # Rest of your class implementation...

    def to_geojson(self):
        feature = []

        for data in self.input:
            if data['hasil'] == []:
                pass
            else:
                # transformasi
                for i in range(len(data['hasil'])):
                    data['hasil'][i][1]*=(-1)
                    data['hasil'][i][1]+=1
                    for j in [0,1]:
                        data['hasil'][i][j]*=(self.extent[j+2] - self.extent[j])
                        data['hasil'][i][j]+=self.extent[j]

                # struktur feature
                geojson = {
                    'type':'Feature',
                    'properties':{
                        'id':data['id'],
                        'kelas':data['kelas']
                    },
                    'geometry':{
                        'type':'Polygon',
                        'coordinates':[data['hasil']]
                    }
                }

                feature.append(geojson)

        feature_coll = {
            'type':'FeatureCollection',
            'name':self.output,
            'crs':{
                'type':'name',
                'properties':{
                    'name':f'urn:ogc:def:crs:EPSG::{self.epsg}'
                }
            },
            'features':feature
        }

        print(f'rangeXY {self.metadata[0]}, {self.metadata[1]}')
        print(f'scaleXY {self.metadata[2]}, {self.metadata[3]}')
        print(f'extent21 {self.metadata[4]}, {self.metadata[5]}')
        print(f'dimm {self.meta2}')
        
        with open(self.output, 'w') as f:
            f.write(json.dumps(feature_coll, indent=2))