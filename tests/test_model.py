from citycatio import Model
import pandas as pd
import unittest
import rasterio as rio
import numpy as np
from rasterio.transform import Affine
import os
import geopandas as gpd

x = np.linspace(-4.0, 4.0, 240)
y = np.linspace(-3.0, 3.0, 180)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-2 * np.log(2) * ((X - 0.5) ** 2 + (Y - 0.5) ** 2) / 1 ** 2)
Z2 = np.exp(-3 * np.log(2) * ((X + 0.5) ** 2 + (Y + 0.5) ** 2) / 2.5 ** 2)
Z = 10.0 * (Z2 - Z1)
res = (x[-1] - x[0]) / 240.0
transform = Affine.translation(x[0] - res / 2, y[0] - res / 2) * Affine.scale(res, res)

dem_path = 'dem.tif'


class TestModel(unittest.TestCase):

    @classmethod
    def setUp(cls) -> None:
        with rio.open(
                dem_path,
                'w',
                driver='GTiff',
                height=Z.shape[0],
                width=Z.shape[1],
                count=1,
                dtype=Z.dtype,
                crs='+proj=latlong',
                transform=transform,
        ) as dst:
            dst.write(Z, 1)

    @classmethod
    def tearDown(cls) -> None:
        os.remove(dem_path)

    def test_model(self):

        with rio.open(dem_path) as dataset:
            Model(dem=dataset, rainfall=pd.DataFrame([0]), rainfall_polygons=gpd.GeoDataFrame(),
                  buildings=gpd.GeoDataFrame(), green_areas=gpd.GeoDataFrame(), configuration={},
                  friction=gpd.GeoDataFrame(), boundaries=gpd.GeoDataFrame())
