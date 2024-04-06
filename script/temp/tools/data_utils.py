import pandas as pd
import torch
from torch import nn


class data_utils:
    def set_df_type(self, df):
        # df = df.astype(str)
        for index, row in df.iterrows():
            if row['type'] == 'int':
                df.at[index, 'min'] = int(row['min'])
                df.at[index, 'max'] = int(row['max'])
                df.at[index, 'Default Value'] = int(row['Default Value'])
            if row['type'] == 'double':
                df.at[index, 'min'] = float(row['min'])
                df.at[index, 'max'] = float(row['max'])
                df.at[index, 'Default Value'] = float(row['Default Value'])
            if row['type'] == 'Boolean':
                if row['Default Value'] == 'true' or row['Default Value'] == 'True':
                    df.at[index, 'Default Value'] = 1
                else:
                    df.at[index, 'Default Value'] = 0
        # return df
        # df['Parameter'] = df['Parameter'].astype(str)

    def replace(self, df, key, ori, target):
        for index, row in df.iterrows():
            if row[key] == ori:
                df.at[index, key] = target
    def preprocess(self):
        self.rmLst = ["ssdSeed", "workloadSeed"]
        self.oneHotLst = []
        self.targetLst = ['IOPS_Read', 'IOPS_Write', 'Bandwidth_Read', 'Bandwidth_Write']
        for index, row in self.df_config.iterrows():
            if row['type'] == 'enumeration':
                self.oneHotLst.append(row['Parameter'])
            if row['type']=='ignore':
                self.rmLst.append(row['Parameter'])
        #print("one HotLst: \n", self.oneHotLst)
        #print("rmLst: \n",self.rmLst)
    def dorp_and_encode(self):
        self.df_result_droped = self.df_result.drop(columns=self.rmLst, errors='ignore')
        self.df_result_encoded = pd.get_dummies(self.df_result_droped, columns=self.oneHotLst)
        self.X = self.df_result_encoded.drop(columns=self.targetLst)
        self.Y = self.df_result_encoded[self.targetLst]
        return self.X, self.Y
    def getParameterLst(self):
        col = self.df_config['Parameter']
        return col.to_list()

    def __init__(self, path_config, path_result):
        self.path_config = path_config
        self.path_result = path_result
        self.df_config_ssd = pd.read_excel(path_config, sheet_name="ssd")
        self.df_config_workload = pd.read_excel(path_config, sheet_name="workload")
        self.replace(self.df_config_ssd, 'Parameter', 'Seed', 'ssdSeed')
        self.replace(self.df_config_workload, 'Parameter', 'Seed', 'workloadSeed')
        self.df_config = pd.concat([self.df_config_ssd, self.df_config_workload])
        # 将布尔类型转化为 01
        self.set_df_type(self.df_config)
        self.df_result = pd.read_excel(path_result)
        self.rmLst = []
        self.oneHotLst = []
        self.targetLst = []
        #self.preprocess()
        #self.dorp_and_encode()
    def drop(self,columns_to_check,value,df =None):
        if df is None:
            df =self.df_result
        df = df.drop(df[(df[columns_to_check] == value).any(axis=1)].index)
        return df
    def get_statement(self, parameter):
        df_config_ssd = self.df_config_ssd
        df_config_workload = self.df_config_workload
        row = df_config_ssd[df_config_ssd['Parameter'] == parameter]
        if len(row) == 0:
            row = df_config_workload[df_config_workload['Parameter'] == parameter]
            if len(row) == 0:
                raise KeyError(parameter + "不存在")
        return row
        # raise KeyError(parameter + "不存在")


# 自定义MPE损失函数
class MPERegressionLoss(nn.Module):
    def __init__(self):
        super(MPERegressionLoss, self).__init__()

    def forward(self, y_pred, y_true):
        # 计算平均百分比误差
        mpe = torch.mean(torch.abs((y_true - y_pred) / y_true))
        return mpe
# 定义模型
# 定义模型
class MLP(nn.Module):
    def __init__(self, layer_sizes):
        super(MLP, self).__init__()
        self.layers = nn.ModuleList()
        for i in range(len(layer_sizes) - 1):
            self.layers.append(nn.Linear(layer_sizes[i], layer_sizes[i+1]))
            if i < len(layer_sizes) - 2:
                self.layers.append(nn.Sigmoid())

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x