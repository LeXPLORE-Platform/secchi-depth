# -*- coding: utf-8 -*-
import os
import math
import netCDF4
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
from general.functions import GenericInstrument


class Secchi(GenericInstrument):
    def __init__(self, *args, **kwargs):
        super(Secchi, self).__init__(*args, **kwargs)
        self.general_attributes = {
            "institution": "EPFL",
            "source": "Secchi Depth Measurements",
            "references": "LéXPLORE common instruments camille.minaudo@epfl.ch>",
            "history": "See history on Renku",
            "conventions": "CF 1.7",
            "comment": "Secchi depths collected on Lexplore Platform in Lake Geneva",
            "title": "Lexplore Secchi Depth Measurements"
        }
        self.dimensions = {
            'time': {'dim_name': 'time', 'dim_size': None}
        }
        self.variables = {
            'time': {'var_name': 'time', 'dim': ('time',), 'unit': 'seconds since 1970-01-01 00:00:00',
                     'long_name': 'time'},
            'secchi': {'var_name': 'secchi', 'dim': ('time',), 'unit': 'm', 'long_name': 'secchi depth', },
            'lowering': {'var_name': 'lowering', 'dim': ('time',), 'unit': 'm', 'long_name': 'lowering depth', },
            'raising': {'var_name': 'raising', 'dim': ('time',), 'unit': 'm', 'long_name': 'raising depth', },
        }

    def read_data(self, file):
        self.log.info("Reading data from {}".format(file), 1)
        try:
            df = pd.read_csv(file, sep=";", header=None, encoding = "ISO-8859-1")
            df.columns = ["id","date","hour","lowering","raising","secchi","person"]
            df["datetime"] = pd.to_datetime(df["date"] + df["hour"], format='%Y-%m-%d%H:%M', errors='coerce')
            df = df[df["datetime"].notna()]
            df = df[df["datetime"] <= pd.Timestamp.now()]
            df["time"] = df["datetime"].apply(lambda dt: datetime.timestamp(dt.replace(tzinfo=timezone.utc)))
            df = df.sort_values("time").reset_index(drop=True)
            for variable in self.variables:
                self.data[variable] = np.array(df[variable])
        except Exception as e:
            self.log.info("Failed to read data from {}".format(file), indent=1)
            raise e
        return True
