import pandas as pd
import torch
from sklearn.tree import DecisionTreeRegressor
from torch import nn
from torch.utils.data import Dataset
#import model

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
        self.hidden_layers = nn.ModuleList([
            nn.Linear(layer_sizes[i], layer_sizes[i+1]) for i in range(len(layer_sizes)-1)
        ])
        self.batch_norms = nn.ModuleList([
            nn.BatchNorm1d(layer_sizes[i+1]) for i in range(len(layer_sizes)-2)
        ])
        self.relu = nn.ReLU()  # 隐藏层的激活函数
        self.Sigmoids = nn.ModuleList([
            nn.Sigmoid() for i in range(len(layer_sizes) - 1)
        ])
        return

    def forward(self, x):
        for i, layer in enumerate(self.hidden_layers):
            x = layer(x)
            if i < len(self.hidden_layers) - 1:
                x = self.batch_norms[i](x)  # 在隐藏层后应用BatchNormalization
                x = self.Sigmoids[i](x)
        return x
def r2_score(y_test, y_pred):
        # 计算实际值的平均值
    y_mean = torch.mean(y_test)

        # 计算总平方和
    ss_tot = torch.sum((y_test - y_mean) ** 2)

        # 计算残差平方和
    ss_res = torch.sum((y_test - y_pred) ** 2)

        # 计算 R^2 分数
    r2 = 1 - (ss_res / ss_tot)

    return r2.item()  # 将 PyTorch 张量转换为标量值
import numpy as np

class ExtraRandomForest:
    def __init__(self, n_estimators=100, max_depth=None, num_features = 0.9,min_samples_split=2):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.trees = []

    def fit(self, X, y):
        for _ in range(self.n_estimators):
            tree = self.build_tree(X, y)
            self.trees.append(tree)

    def build_tree(self, X, y):
        num_features = X.shape[1]
        feature_indices = np.random.choice(num_features, size=num_features, replace=True)

        tree = DecisionTree(max_depth=self.max_depth, min_samples_split=self.min_samples_split)
        tree.fit(X[:, feature_indices], y)
        return tree

    def predict(self, X):
        predictions = np.zeros((X.shape[0], len(self.trees)))
        for i, tree in enumerate(self.trees):
            predictions[:, i] = tree.predict(X)
        return np.mean(predictions, axis=1)

class DecisionTree:
    y_train = None
    def __init__(self, **kwargs):
        self.acc = None
        super().__init__(**kwargs)

    def predict(self, X):
        y_pred = super().predict()
        self.acc = self.percentage_error(DecisionTree.y_train,y_pred)
        return y_pred

    def percentage_error(self, y_true, y_pred):
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

