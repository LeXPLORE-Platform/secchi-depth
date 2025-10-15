import os
import json
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from envass import qualityassurance
from datetime import datetime, timezone


def import_files(folder):
    df = pd.DataFrame()
    filelist = os.listdir(folder)
    filelist.sort()
    for file in filelist:
        ds = xr.open_dataset(os.path.join(folder, file))
        df = df.append(ds.to_dataframe())
    df = df.reset_index()
    df["datetime"] = df.time.apply(lambda x: datetime.timestamp(datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)))
    return df


def load_qa(file):
    qa = json.load(open(file))
    try:
        if qa["time"]["simple"]["bounds"][1] == "now":
            qa["time"]["simple"]["bounds"][1] = datetime.now().timestamp()
        return qa
    except:
        return qa


def plot_data(df, params):
    for param in params:
        if param != "time":
            t = np.array(df["time"])
            p = np.array(df[param])
            qa = np.array(df[param+"_qual"])
            p_qa = p.copy()
            p_qa[qa > 0] = np.nan
            plt.plot(t, p, color="lightgrey")
            plt.plot(t, p_qa, color="red")
            plt.title(param)
            plt.show()


def quality_flags(qa, df):
    var_name = qa.keys()
    for var in var_name:
        if var in qa:
            qa_arr_simple = qualityassurance(np.array(df[var]), np.array(df["datetime"]), **qa[var]["simple"])
            qa_arr_adv = qualityassurance(np.array(df[var]), np.array(df["datetime"]), **qa[var]["advanced"])
            df[var + "_qual"] = qa_arr_simple + qa_arr_adv
    return df


def sub_df(df,range_bounds):
    #Create a subset for visualisation
    subset_index = list(range(range_bounds[0],range_bounds[1]))
    df_sub = df.iloc[subset_index].reset_index()
    return df_sub,subset_index

def idxtotime(df,idx_skytemp):
    return str(list(df.iloc[idx_skytemp].time.apply(lambda x: datetime.timestamp(datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))))).replace("[","").replace("]","")

def log(str, indent=0, start=False):
    if start:
        out = "\n" + str + "\n"
        with open("log.txt", "w") as file:
            file.write(out + "\n")
    else:
        out = datetime.now().strftime("%H:%M:%S.%f") + (" " * 3 * (indent + 1)) + str
        with open("log.txt", "a") as file:
            file.write(out + "\n")
    print(out)

def update_log(quality_assurance_dict,old_quality_assurance_dict,var_name):
    for var in var_name:
        added_test = []
        for i in list(quality_assurance_dict[var]["advanced"].keys()):
            if i not in list(old_quality_assurance_dict[var]["advanced"].keys()):
                added_test = np.append(added_test,i)
        removed_test = []
        for j in list(old_quality_assurance_dict[var]["advanced"].keys()):
            if j not in list(quality_assurance_dict[var]["advanced"].keys()):
                removed_test = np.append(removed_test,j)
        if len(added_test)!=0:
            log(str(added_test) + " tests have been added to variable " +str(var))
        if len(removed_test)!=0:
            log(str(removed_test) + " tests have been removed to variable " +str(var))

def plot_quality_assurance(df_sub):
    import plotly.graph_objs as go
    import plotly.offline as py
    from ipywidgets import interactive, HBox, VBox
    py.init_notebook_mode()
    variables=df_sub.columns


    py.init_notebook_mode()
    f = go.FigureWidget([go.Scatter(y = df_sub.index, x = df_sub.index, mode = 'markers')])
    scatter = f.data[0]
    N = len(df_sub)
    scatter.marker.opacity = 0.8
    def update_axes(xaxis, yaxis):
        scatter = f.data[0]
        scatter.x = df_sub[xaxis]
        scatter.y = df_sub[yaxis]

        with f.batch_update():
            f.layout.xaxis.title = xaxis
            f.layout.yaxis.title = yaxis
            if "_qual" not in yaxis:
                f.add_trace(go.Scatter(y = df_sub[yaxis][df_sub[yaxis+"_qual"]==0], x = df_sub[xaxis][df_sub[yaxis+"_qual"]==0], mode = 'markers', marker = dict(color = 'blue'), name = f'{yaxis} Trusted (=0)'))
                f.add_trace(go.Scatter(y = df_sub[yaxis][df_sub[yaxis+"_qual"]==1], x = df_sub[xaxis][df_sub[yaxis+"_qual"]==1], mode = 'markers', marker = dict(color = 'darkred'), name = f'{yaxis} Not trusted (=1)'))
            else:
                scatter.x = df_sub[xaxis]
                scatter.y = df_sub[yaxis]

    axis_dropdowns = interactive(update_axes, yaxis = df_sub.columns, xaxis = df_sub.columns)

    # Create a table FigureWidget that updates on selection from points in the scatter plot of f
    t = go.FigureWidget([go.Table(
    header=dict(values=variables,
                fill = dict(color='#C2D4FF'),
                align = ['left'] * 5),
    cells=dict(values=[df_sub[col] for col in variables],
               fill = dict(color='#F5F8FF'),
               align = ['left'] * 5))])

    def selection_fn(trace,points,selector):
        t.data[0].cells.values = [df_sub.loc[points.point_inds][col] for col in variables]

    scatter.on_selection(selection_fn)

    # Put everything together
    return VBox((HBox(axis_dropdowns.children),f,t))
