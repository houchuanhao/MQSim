import os
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from script.tools import collection
from script.tools import tools

keys = []
range = []

def key_range():
    ssdsheet = "ssd0"
    workloadsheet = "workload0"
    workspace = "workspace_" + ssdsheet + "_"+workloadsheet
    #tree_ssd, root_ssd = tools.getTree(tools.path_ssd)
    lst_ssd = tools.xlsx2lst(tools.xlsx_config, ssdsheet)
    lst_workload = tools.xlsx2lst(tools.xlsx_config, workloadsheet)
    print("hello")

key_range()
def update_plot():
    clear_frame(plot_frame)
    fig, ax = plt.subplots()

    selected_param = radio_value.get()
    if selected_param != -1:  # 检查是否有选中的参数
        values = [scales[j].get() for j in range(n)]
        x = np.linspace(-10, 10, 400)
        y = [func_value(values, selected_param, xi) for xi in x]
        ax.plot(x, y, label=f'x{selected_param+1}')

    ax.set_title("Plot of f(x1, x2, ..., xn)")
    ax.set_xlabel("Parameter Value")
    ax.set_ylabel("Function Output")
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def func_value(values, index, new_value):
    """计算函数值，其中一个参数被替换为新值"""
    new_values = values.copy()
    new_values[index] = new_value
    return sum(val**(i+1) for i, val in enumerate(new_values))

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# 设置参数数量
n = 5  # 可以根据需要更改这个值

# 创建主窗口
root = tk.Tk()
root.title("Function Plotter")

# 创建左侧的控制面板
control_frame = tk.Frame(root)
control_frame.pack(side=tk.LEFT, padx=10, pady=10)

# 创建右侧的绘图区域
plot_frame = tk.Frame(root)
plot_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# 动态创建滑动条和单选按钮
scales = []
radio_value = tk.IntVar(value=-1)  # 初始值为-1，表示没有选中任何参数

for i in range(n):
    scale = tk.Scale(control_frame, from_=-10, to=10, orient="horizontal", command=lambda val: update_plot())
    scale.grid(row=i, column=0)
    scales.append(scale)

    radio_button = tk.Radiobutton(control_frame, text=f"x{i+1}", variable=radio_value, value=i)
    radio_button.grid(row=i, column=1)

update_plot()  # 初始绘图

# 运行主循环
root.mainloop()