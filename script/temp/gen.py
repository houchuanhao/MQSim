import random
import xml.etree.ElementTree as ET
import openpyxl

# 从 XML 文件中读取参数
def read_parameters_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    parameters = {}
    for param_set in root:
        for param in param_set:
            parameters[param.tag] = param.text
    return parameters,root,tree

# 将参数写入 Excel 文件
def write_parameters_to_excel(parameters, excel_file):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Parameter", "Value"])
    for param, value in parameters.items():
        ws.append([param, value])
    wb.save(excel_file)
def write_root_to_xml(parameters, root):
    i = 0

# 为参数赋随机值
def assign_random_values(parameters):
    # 这里使用了之前编写的赋值代码，从第一个参数开始
    # 请根据之前的赋值代码继续完成

    # 1. PCIe_Lane_Bandwidth
    parameters['PCIe_Lane_Bandwidth'] = str(random.randint(1, 10))

    # 2. PCIe_Lane_Count
    parameters['PCIe_Lane_Count'] = str(random.randint(1, 10))

    # 3. SATA_Processing_Delay
    parameters['SATA_Processing_Delay'] = str(random.randint(1, 100000))

    # 4. Enable_ResponseTime_Logging
    parameters['Enable_ResponseTime_Logging'] = random.choice(['true', 'false'])

    # 5. ResponseTime_Logging_Period_Length
    parameters['ResponseTime_Logging_Period_Length'] = str(random.randint(1, 1000000))

    # 6. Seed
    parameters['Seed'] = str(random.randint(1, 1000))

    # 7. Enabled_Preconditioning
    parameters['Enabled_Preconditioning'] = random.choice(['true', 'false'])

    # 8. Memory_Type
    parameters['Memory_Type'] = 'FLASH'

    # 9. HostInterface_Type
    parameters['HostInterface_Type'] = random.choice(['NVME', 'SATA'])

    # 10. IO_Queue_Depth
    parameters['IO_Queue_Depth'] = str(random.randint(1, 100000))

    # 11. Queue_Fetch_Size
    parameters['Queue_Fetch_Size'] = str(random.randint(1, 100000))

    # 12. Caching_Mechanism
    parameters['Caching_Mechanism'] = random.choice(['SIMPLE', 'ADVANCED'])

    # 13. Data_Cache_Sharing_Mode
    parameters['Data_Cache_Sharing_Mode'] = random.choice(['SHARED', 'EQUAL_PARTITIONING'])

    # 14. Data_Cache_Capacity
    parameters['Data_Cache_Capacity'] = str(random.randint(1, 100000))

    # 15. Data_Cache_DRAM_Row_Size
    parameters['Data_Cache_DRAM_Row_Size'] = str(2 ** random.randint(1, 10))

    # 16. Data_Cache_DRAM_Data_Rate
    parameters['Data_Cache_DRAM_Data_Rate'] = str(random.randint(1, 1000))

    # 17. Data_Cache_DRAM_Data_Burst_Size
    parameters['Data_Cache_DRAM_Data_Burst_Size'] = str(random.randint(1, 1000))

    # 18. Data_Cache_DRAM_tRCD
    parameters['Data_Cache_DRAM_tRCD'] = str(random.randint(1, 100))

    # 19. Data_Cache_DRAM_tCL
    parameters['Data_Cache_DRAM_tCL'] = str(random.randint(1, 100))

    # 20. Data_Cache_DRAM_tRP
    parameters['Data_Cache_DRAM_tRP'] = str(random.randint(1, 100))

    # 21. Address_Mapping
    parameters['Address_Mapping'] = random.choice(['PAGE_LEVEL', 'HYBRID'])

    # 22. Ideal_Mapping_Table
    parameters['Ideal_Mapping_Table'] = random.choice(['true', 'false'])

    # 23. CMT_Capacity
    parameters['CMT_Capacity'] = str(random.randint(1, 100000))

    # 24. CMT_Sharing_Mode
    parameters['CMT_Sharing_Mode'] = random.choice(['SHARED', 'EQUAL_PARTITIONING'])

    # 25. Plane_Allocation_Scheme
    parameters['Plane_Allocation_Scheme'] = random.choice(
        ['CWDP', 'CWPD', 'CDWP', 'CDPW', 'CPWD', 'CPDW', 'WCDP', 'WCPD', 'WDCP', 'WDPC', 'WPCD', 'WPDC', 'DCWP', 'DCPW',
         'DWCP', 'DWPC', 'DPCW', 'DPWC', 'PCWD', 'PCDW', 'PWCD', 'PWDC', 'PDCW', 'PDWC'])

    # 26. Transaction_Scheduling_Policy
    parameters['Transaction_Scheduling_Policy'] = random.choice(['OUT_OF_ORDER', 'PRIORITY_OUT_OF_ORDER'])

    # 27. Overprovisioning_Ratio
    parameters['Overprovisioning_Ratio'] = str(round(random.uniform(0.1, 0.9), 4))

    # 28. GC_Exec_Threshold
    parameters['GC_Exec_Threshold'] = str(round(random.uniform(0.1, 0.9), 4))

    # 29. GC_Block_Selection_Policy
    parameters['GC_Block_Selection_Policy'] = random.choice(
        ['GREEDY', 'RGA', 'RANDOM', 'RANDOM_P', 'RANDOM_PP', 'FIFO'])

    # 30. Use_Copyback_for_GC
    parameters['Use_Copyback_for_GC'] = random.choice(['true', 'false'])

    # 31. Preemptible_GC_Enabled
    parameters['Preemptible_GC_Enabled'] = random.choice(['true', 'false'])

    # 32. GC_Hard_Threshold
    parameters['GC_Hard_Threshold'] = str(round(random.uniform(0.1, 0.9), 4))

    # 33. Dynamic_Wearleveling_Enabled
    parameters['Dynamic_Wearleveling_Enabled'] = random.choice(['true', 'false'])

    # 34. Static_Wearleveling_Enabled
    parameters['Static_Wearleveling_Enabled'] = random.choice(['true', 'false'])

    # 35. Static_Wearleveling_Threshold
    parameters['Static_Wearleveling_Threshold'] = str(random.randint(1, 100))

    # 36. Preferred_suspend_erase_time_for_read
    parameters['Preferred_suspend_erase_time_for_read'] = str(random.randint(1, 1000000))

    # 37. Preferred_suspend_erase_time_for_write
    parameters['Preferred_suspend_erase_time_for_write'] = str(random.randint(1, 1000000))

    # 38. Preferred_suspend_write_time_for_read
    parameters['Preferred_suspend_write_time_for_read'] = str(random.randint(1, 1000000))

    # 39. Flash_Channel_Count
    parameters['Flash_Channel_Count'] = str(random.randint(1, 100))

    # 40. Flash_Channel_Width
    parameters['Flash_Channel_Width'] = str(random.randint(1, 100))

    # 41. Channel_Transfer_Rate
    parameters['Channel_Transfer_Rate'] = str(random.randint(1, 1000))

    # 42. Chip_No_Per_Channel
    parameters['Chip_No_Per_Channel'] = str(random.randint(1, 100))

    # 43. Flash_Comm_Protocol
    parameters['Flash_Comm_Protocol'] = 'NVDDR2'

    # 44. Flash_Technology
    parameters['Flash_Technology'] = random.choice(['SLC', 'MLC', 'TLC'])

    # 45. CMD_Suspension_Support
    parameters['CMD_Suspension_Support'] = random.choice(['NONE', 'PROGRAM', 'PROGRAM_ERASE', 'ERASE'])

    # 46. Page_Read_Latency_LSB
    parameters['Page_Read_Latency_LSB'] = str(random.randint(1, 100000))

    # 47. Page_Read_Latency_CSB
    parameters['Page_Read_Latency_CSB'] = str(random.randint(1, 100000))

    # 48. Page_Read_Latency_MSB
    parameters['Page_Read_Latency_MSB'] = str(random.randint(1, 100000))

    # 49. Page_Program_Latency_LSB
    parameters['Page_Program_Latency_LSB'] = str(random.randint(1, 100000))

    # 50. Page_Program_Latency_CSB
    parameters['Page_Program_Latency_CSB'] = str(random.randint(1, 100000))

    # 51. Page_Program_Latency_MSB
    parameters['Page_Program_Latency_MSB'] = str(random.randint(1, 100000))

    # 52. Block_Erase_Latency
    parameters['Block_Erase_Latency'] = str(random.randint(1, 100000))

    # 53. Block_PE_Cycles_Limit
    parameters['Block_PE_Cycles_Limit'] = str(random.randint(1, 10000))

    # 54. Suspend_Erase_Time
    parameters['Suspend_Erase_Time'] = str(random.randint(1, 100000))

    # 55. Suspend_Program_Time
    parameters['Suspend_Program_Time'] = str(random.randint(1, 100000))

    # 56. Die_No_Per_Chip
    parameters['Die_No_Per_Chip'] = str(random.randint(1, 100))

    # 57. Plane_No_Per_Die
    parameters['Plane_No_Per_Die'] = str(random.randint(1, 100))

    # 58. Block_No_Per_Plane
    parameters['Block_No_Per_Plane'] = str(random.randint(1, 2048))

    # 59. Page_No_Per_Block
    parameters['Page_No_Per_Block'] = str(random.randint(1, 256))

    # 60. Page_Capacity
    parameters['Page_Capacity'] = str(random.randint(1, 8192))

    # 61. Page_Metadat_Capacity
    parameters['Page_Metadat_Capacity'] = str(random.randint(1, 448))

    # 现在所有参数都已经赋值完毕

    # 继续完成剩余的参数赋值

    return parameters

# 为节点赋值
def assign_values_from_parameters(node, parameters):
    for child in node:
        if len(child) > 0:
            assign_values_from_parameters(child, parameters)
        else:
            param_name = child.tag
            if param_name in parameters:
                child.text = child.text + "......."+ str(parameters[param_name])

# 读取 XML 文件
xml_file = "ssdconfig.xml"
parameters,root,tree = read_parameters_from_xml(xml_file)

# 为参数赋随机值
parameters = assign_random_values(parameters)

#为节点赋值
assign_values_from_parameters(root,parameters)
tree.write('out.xml')

# 生成 Excel 文件
write_parameters_to_excel(parameters, "parameters.xlsx")
