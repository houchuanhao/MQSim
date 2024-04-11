from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
def evaluate(y_pred,y_true,str = "",p = False):
    mse = mean_squared_error(y_true, y_pred)
    # 计算百分比误差
    percentage_error = np.abs((y_true - y_pred) / y_true) * 100
    mean_percentage_error = np.mean(percentage_error)
    # 计算R2值
    r2 = r2_score(y_true, y_pred)
    # 计算平均绝对误差
    mae = mean_absolute_error(y_true, y_pred)
    if p:
        print(str + f'均方误差 (MSE): {mse:.4f}')
        print(str + f'百分比误差 (Mean Percentage Error): {mean_percentage_error:.4f}%')
        print(str + f'R2值: {r2:.4f}')
        print(str + f'平均绝对误差 (MAE): {mae:.4f}')
    return  mse,mean_percentage_error,r2,mae