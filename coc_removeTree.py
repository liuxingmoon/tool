# coding:utf-8
import subprocess
import time
import easygui as g
import random
# 清除杂物
#方法：
#清除四周 6*22 个单位像素的杂物

# 元素坐标
pos = {
    'pointleft': [149, 456],
    'pointtop': [622, 100],
    'pointtop_continue': [736, 188],
    'pointright': [1090, 475],
    'pointbot': [658, 525],
    'pointbot_continue': [793, 424],
    'action': [640, 590],
    'cancel': [1200, 350],
    'exitstore': [1230, 50]
}
# 建立字典存储所有位置信息

rm_pos = {}
rm_posRT = {'0:0': [149, 456], '0:1': [172.6, 438.4], '0:2': [196.2, 420.79999999999995], '0:3': [219.79999999999998, 403.19999999999993], '0:4': [243.39999999999998, 385.5999999999999], '0:5': [267.0, 367.9999999999999], '0:6': [290.6, 350.39999999999986], '0:7': [314.20000000000005, 332.79999999999984], '0:8': [337.80000000000007, 315.1999999999998], '0:9': [361.4000000000001, 297.5999999999998], '0:10': [385.0000000000001, 279.9999999999998], '0:11': [408.60000000000014, 262.39999999999975], '0:12': [432.20000000000016, 244.79999999999976], '0:13': [455.8000000000002, 227.19999999999976], '0:14': [479.4000000000002, 209.59999999999977], '0:15': [503.0000000000002, 191.99999999999977], '0:16': [526.6000000000003, 174.39999999999978], '0:17': [550.2000000000003, 156.79999999999978], '0:18': [573.8000000000003, 139.1999999999998], '0:19': [597.4000000000003, 121.5999999999998], '0:20': [621.0000000000003, 103.9999999999998], '0:21': [644.6000000000004, 86.3999999999998], '1:0': [172.6, 473.6], '1:1': [196.2, 456.0], '1:2': [219.79999999999998, 438.4], '1:3': [243.39999999999998, 420.79999999999995], '1:4': [267.0, 403.19999999999993], '1:5': [290.6, 385.5999999999999], '1:6': [314.20000000000005, 367.9999999999999], '1:7': [337.80000000000007, 350.39999999999986], '1:8': [361.4000000000001, 332.79999999999984], '1:9': [385.0000000000001, 315.1999999999998], '1:10': [408.60000000000014, 297.5999999999998], '1:11': [432.20000000000016, 279.9999999999998], '1:12': [455.8000000000002, 262.39999999999975], '1:13': [479.4000000000002, 244.79999999999976], '1:14': [503.0000000000002, 227.19999999999976], '1:15': [526.6000000000003, 209.59999999999977], '1:16': [550.2000000000003, 191.99999999999977], '1:17': [573.8000000000003, 174.39999999999978], '1:18': [597.4000000000003, 156.79999999999978], '1:19': [621.0000000000003, 139.1999999999998], '1:20': [644.6000000000004, 121.5999999999998], '1:21': [668.2000000000004, 103.9999999999998], '2:0': [196.2, 491.20000000000005], '2:1': [219.79999999999998, 473.6], '2:2': [243.39999999999998, 456.0], '2:3': [267.0, 438.4], '2:4': [290.6, 420.79999999999995], '2:5': [314.20000000000005, 403.19999999999993], '2:6': [337.80000000000007, 385.5999999999999], '2:7': [361.4000000000001, 367.9999999999999], '2:8': [385.0000000000001, 350.39999999999986], '2:9': [408.60000000000014, 332.79999999999984], '2:10': [432.20000000000016, 315.1999999999998], '2:11': [455.8000000000002, 297.5999999999998], '2:12': [479.4000000000002, 279.9999999999998], '2:13': [503.0000000000002, 262.39999999999975], '2:14': [526.6000000000003, 244.79999999999976], '2:15': [550.2000000000003, 227.19999999999976], '2:16': [573.8000000000003, 209.59999999999977], '2:17': [597.4000000000003, 191.99999999999977], '2:18': [621.0000000000003, 174.39999999999978], '2:19': [644.6000000000004, 156.79999999999978], '2:20': [668.2000000000004, 139.1999999999998], '2:21': [691.8000000000004, 121.5999999999998], '3:0': [219.79999999999998, 508.80000000000007], '3:1': [243.39999999999998, 491.20000000000005], '3:2': [267.0, 473.6], '3:3': [290.6, 456.0], '3:4': [314.20000000000005, 438.4], '3:5': [337.80000000000007, 420.79999999999995], '3:6': [361.4000000000001, 403.19999999999993], '3:7': [385.0000000000001, 385.5999999999999], '3:8': [408.60000000000014, 367.9999999999999], '3:9': [432.20000000000016, 350.39999999999986], '3:10': [455.8000000000002, 332.79999999999984], '3:11': [479.4000000000002, 315.1999999999998], '3:12': [503.0000000000002, 297.5999999999998], '3:13': [526.6000000000003, 279.9999999999998], '3:14': [550.2000000000003, 262.39999999999975], '3:15': [573.8000000000003, 244.79999999999976], '3:16': [597.4000000000003, 227.19999999999976], '3:17': [621.0000000000003, 209.59999999999977], '3:18': [644.6000000000004, 191.99999999999977], '3:19': [668.2000000000004, 174.39999999999978], '3:20': [691.8000000000004, 156.79999999999978], '3:21': [715.4000000000004, 139.1999999999998], '4:0': [243.39999999999998, 526.4000000000001], '4:1': [267.0, 508.80000000000007], '4:2': [290.6, 491.20000000000005], '4:3': [314.20000000000005, 473.6], '4:4': [337.80000000000007, 456.0], '4:5': [361.4000000000001, 438.4], '4:6': [385.0000000000001, 420.79999999999995], '4:7': [408.60000000000014, 403.19999999999993], '4:8': [432.20000000000016, 385.5999999999999], '4:9': [455.8000000000002, 367.9999999999999], '4:10': [479.4000000000002, 350.39999999999986], '4:11': [503.0000000000002, 332.79999999999984], '4:12': [526.6000000000003, 315.1999999999998], '4:13': [550.2000000000003, 297.5999999999998], '4:14': [573.8000000000003, 279.9999999999998], '4:15': [597.4000000000003, 262.39999999999975], '4:16': [621.0000000000003, 244.79999999999976], '4:17': [644.6000000000004, 227.19999999999976], '4:18': [668.2000000000004, 209.59999999999977], '4:19': [691.8000000000004, 191.99999999999977], '4:20': [715.4000000000004, 174.39999999999978], '4:21': [739.0000000000005, 156.79999999999978], '5:22': [736, 188], '5:23': [759.6, 205.6], '5:24': [783.2, 223.2], '5:25': [806.8000000000001, 240.79999999999998], '5:26': [830.4000000000001, 258.4], '5:27': [854.0000000000001, 276.0], '5:28': [877.6000000000001, 293.6], '5:29': [901.2000000000002, 311.20000000000005], '5:30': [924.8000000000002, 328.80000000000007], '5:31': [948.4000000000002, 346.4000000000001], '5:32': [972.0000000000002, 364.0000000000001], '5:33': [995.6000000000003, 381.60000000000014], '5:34': [1019.2000000000003, 399.20000000000016], '5:35': [1042.8000000000002, 416.8000000000002], '5:36': [1066.4, 434.4000000000002], '5:37': [1090.0, 452.0000000000002], '6:22': [712.4, 205.6], '6:23': [736.0, 223.2], '6:24': [759.6, 240.79999999999998], '6:25': [783.2, 258.4], '6:26': [806.8000000000001, 276.0], '6:27': [830.4000000000001, 293.6], '6:28': [854.0000000000001, 311.20000000000005], '6:29': [877.6000000000001, 328.80000000000007], '6:30': [901.2000000000002, 346.4000000000001], '6:31': [924.8000000000002, 364.0000000000001], '6:32': [948.4000000000002, 381.60000000000014], '6:33': [972.0000000000002, 399.20000000000016], '6:34': [995.6000000000003, 416.8000000000002], '6:35': [1019.2000000000003, 434.4000000000002], '6:36': [1042.8000000000002, 452.0000000000002], '6:37': [1066.4, 469.60000000000025], '7:22': [688.8, 223.2], '7:23': [712.4, 240.79999999999998], '7:24': [736.0, 258.4], '7:25': [759.6, 276.0], '7:26': [783.2, 293.6], '7:27': [806.8000000000001, 311.20000000000005], '7:28': [830.4000000000001, 328.80000000000007], '7:29': [854.0000000000001, 346.4000000000001], '7:30': [877.6000000000001, 364.0000000000001], '7:31': [901.2000000000002, 381.60000000000014], '7:32': [924.8000000000002, 399.20000000000016], '7:33': [948.4000000000002, 416.8000000000002], '7:34': [972.0000000000002, 434.4000000000002], '7:35': [995.6000000000003, 452.0000000000002], '7:36': [1019.2000000000003, 469.60000000000025], '7:37': [1042.8000000000002, 487.2000000000003], '8:22': [665.1999999999999, 240.79999999999998], '8:23': [688.8, 258.4], '8:24': [712.4, 276.0], '8:25': [736.0, 293.6], '8:26': [759.6, 311.20000000000005], '8:27': [783.2, 328.80000000000007], '8:28': [806.8000000000001, 346.4000000000001], '8:29': [830.4000000000001, 364.0000000000001], '8:30': [854.0000000000001, 381.60000000000014], '8:31': [877.6000000000001, 399.20000000000016], '8:32': [901.2000000000002, 416.8000000000002], '8:33': [924.8000000000002, 434.4000000000002], '8:34': [948.4000000000002, 452.0000000000002], '8:35': [972.0000000000002, 469.60000000000025], '8:36': [995.6000000000003, 487.2000000000003], '8:37': [1019.2000000000003, 504.8000000000003], '9:22': [641.5999999999999, 258.4], '9:23': [665.1999999999999, 276.0], '9:24': [688.8, 293.6], '9:25': [712.4, 311.20000000000005], '9:26': [736.0, 328.80000000000007], '9:27': [759.6, 346.4000000000001], '9:28': [783.2, 364.0000000000001], '9:29': [806.8000000000001, 381.60000000000014], '9:30': [830.4000000000001, 399.20000000000016], '9:31': [854.0000000000001, 416.8000000000002], '9:32': [877.6000000000001, 434.4000000000002], '9:33': [901.2000000000002, 452.0000000000002], '9:34': [924.8000000000002, 469.60000000000025], '9:35': [948.4000000000002, 487.2000000000003], '9:36': [972.0000000000002, 504.8000000000003], '9:37': [995.6000000000003, 522.4000000000003]}
rm_posLB = {'10:38': [658, 525], '10:39': [634.4, 507.4], '10:40': [610.8, 489.79999999999995], '10:41': [587.1999999999999, 472.19999999999993], '10:42': [563.5999999999999, 454.5999999999999], '10:43': [539.9999999999999, 436.9999999999999], '10:44': [516.3999999999999, 419.39999999999986], '10:45': [492.79999999999984, 401.79999999999984], '10:46': [469.1999999999998, 384.1999999999998], '10:47': [445.5999999999998, 366.5999999999998], '10:48': [421.9999999999998, 348.9999999999998], '10:49': [398.39999999999975, 331.39999999999975], '10:50': [374.7999999999997, 313.7999999999997], '10:51': [351.1999999999997, 296.1999999999997], '10:52': [327.5999999999997, 278.5999999999997], '10:53': [303.99999999999966, 260.99999999999966], '10:54': [280.39999999999964, 243.39999999999966], '11:38': [681.6, 507.4], '11:39': [658.0, 489.79999999999995], '11:40': [634.4, 472.19999999999993], '11:41': [610.8, 454.5999999999999], '11:42': [587.1999999999999, 436.9999999999999], '11:43': [563.5999999999999, 419.39999999999986], '11:44': [539.9999999999999, 401.79999999999984], '11:45': [516.3999999999999, 384.1999999999998], '11:46': [492.79999999999984, 366.5999999999998], '11:47': [469.1999999999998, 348.9999999999998], '11:48': [445.5999999999998, 331.39999999999975], '11:49': [421.9999999999998, 313.7999999999997], '11:50': [398.39999999999975, 296.1999999999997], '11:51': [374.7999999999997, 278.5999999999997], '11:52': [351.1999999999997, 260.99999999999966], '11:53': [327.5999999999997, 243.39999999999966], '11:54': [303.99999999999966, 225.79999999999967], '12:38': [705.2, 489.79999999999995], '12:39': [681.6, 472.19999999999993], '12:40': [658.0, 454.5999999999999], '12:41': [634.4, 436.9999999999999], '12:42': [610.8, 419.39999999999986], '12:43': [587.1999999999999, 401.79999999999984], '12:44': [563.5999999999999, 384.1999999999998], '12:45': [539.9999999999999, 366.5999999999998], '12:46': [516.3999999999999, 348.9999999999998], '12:47': [492.79999999999984, 331.39999999999975], '12:48': [469.1999999999998, 313.7999999999997], '12:49': [445.5999999999998, 296.1999999999997], '12:50': [421.9999999999998, 278.5999999999997], '12:51': [398.39999999999975, 260.99999999999966], '12:52': [374.7999999999997, 243.39999999999966], '12:53': [351.1999999999997, 225.79999999999967], '12:54': [327.5999999999997, 208.19999999999968], '13:38': [728.8000000000001, 472.19999999999993], '13:39': [705.2, 454.5999999999999], '13:40': [681.6, 436.9999999999999], '13:41': [658.0, 419.39999999999986], '13:42': [634.4, 401.79999999999984], '13:43': [610.8, 384.1999999999998], '13:44': [587.1999999999999, 366.5999999999998], '13:45': [563.5999999999999, 348.9999999999998], '13:46': [539.9999999999999, 331.39999999999975], '13:47': [516.3999999999999, 313.7999999999997], '13:48': [492.79999999999984, 296.1999999999997], '13:49': [469.1999999999998, 278.5999999999997], '13:50': [445.5999999999998, 260.99999999999966], '13:51': [421.9999999999998, 243.39999999999966], '13:52': [398.39999999999975, 225.79999999999967], '13:53': [374.7999999999997, 208.19999999999968], '13:54': [351.1999999999997, 190.59999999999968], '14:38': [752.4000000000001, 454.5999999999999], '14:39': [728.8000000000001, 436.9999999999999], '14:40': [705.2, 419.39999999999986], '14:41': [681.6, 401.79999999999984], '14:42': [658.0, 384.1999999999998], '14:43': [634.4, 366.5999999999998], '14:44': [610.8, 348.9999999999998], '14:45': [587.1999999999999, 331.39999999999975], '14:46': [563.5999999999999, 313.7999999999997], '14:47': [539.9999999999999, 296.1999999999997], '14:48': [516.3999999999999, 278.5999999999997], '14:49': [492.79999999999984, 260.99999999999966], '14:50': [469.1999999999998, 243.39999999999966], '14:51': [445.5999999999998, 225.79999999999967], '14:52': [421.9999999999998, 208.19999999999968], '14:53': [398.39999999999975, 190.59999999999968], '14:54': [374.7999999999997, 172.9999999999997], '15:38': [776.0000000000001, 436.9999999999999], '15:39': [752.4000000000001, 419.39999999999986], '15:40': [728.8000000000001, 401.79999999999984], '15:41': [705.2, 384.1999999999998], '15:42': [681.6, 366.5999999999998], '15:43': [658.0, 348.9999999999998], '15:44': [634.4, 331.39999999999975], '15:45': [610.8, 313.7999999999997], '15:46': [587.1999999999999, 296.1999999999997], '15:47': [563.5999999999999, 278.5999999999997], '15:48': [539.9999999999999, 260.99999999999966], '15:49': [516.3999999999999, 243.39999999999966], '15:50': [492.79999999999984, 225.79999999999967], '15:51': [469.1999999999998, 208.19999999999968], '15:52': [445.5999999999998, 190.59999999999968], '15:53': [421.9999999999998, 172.9999999999997], '15:54': [398.39999999999975, 155.3999999999997], '16:55': [793, 424], '16:56': [816.6, 406.4], '16:57': [840.2, 388.79999999999995], '16:58': [863.8000000000001, 371.19999999999993], '16:59': [887.4000000000001, 353.5999999999999], '16:60': [911.0000000000001, 335.9999999999999], '16:61': [934.6000000000001, 318.39999999999986], '16:62': [958.2000000000002, 300.79999999999984], '16:63': [981.8000000000002, 283.1999999999998], '16:64': [1005.4000000000002, 265.5999999999998], '16:65': [1029.0000000000002, 247.9999999999998], '16:66': [1052.6000000000001, 230.3999999999998], '17:55': [769.4, 406.4], '17:56': [793.0, 388.79999999999995], '17:57': [816.6, 371.19999999999993], '17:58': [840.2, 353.5999999999999], '17:59': [863.8000000000001, 335.9999999999999], '17:60': [887.4000000000001, 318.39999999999986], '17:61': [911.0000000000001, 300.79999999999984], '17:62': [934.6000000000001, 283.1999999999998], '17:63': [958.2000000000002, 265.5999999999998], '17:64': [981.8000000000002, 247.9999999999998], '17:65': [1005.4000000000002, 230.3999999999998], '17:66': [1029.0000000000002, 212.7999999999998], '18:55': [745.8, 388.79999999999995], '18:56': [769.4, 371.19999999999993], '18:57': [793.0, 353.5999999999999], '18:58': [816.6, 335.9999999999999], '18:59': [840.2, 318.39999999999986], '18:60': [863.8000000000001, 300.79999999999984], '18:61': [887.4000000000001, 283.1999999999998], '18:62': [911.0000000000001, 265.5999999999998], '18:63': [934.6000000000001, 247.9999999999998], '18:64': [958.2000000000002, 230.3999999999998], '18:65': [981.8000000000002, 212.7999999999998], '18:66': [1005.4000000000002, 195.19999999999982], '19:55': [722.1999999999999, 371.19999999999993], '19:56': [745.8, 353.5999999999999], '19:57': [769.4, 335.9999999999999], '19:58': [793.0, 318.39999999999986], '19:59': [816.6, 300.79999999999984], '19:60': [840.2, 283.1999999999998], '19:61': [863.8000000000001, 265.5999999999998], '19:62': [887.4000000000001, 247.9999999999998], '19:63': [911.0000000000001, 230.3999999999998], '19:64': [934.6000000000001, 212.7999999999998], '19:65': [958.2000000000002, 195.19999999999982], '19:66': [981.8000000000002, 177.59999999999982], '20:55': [698.5999999999999, 353.5999999999999], '20:56': [722.1999999999999, 335.9999999999999], '20:57': [745.8, 318.39999999999986], '20:58': [769.4, 300.79999999999984], '20:59': [793.0, 283.1999999999998], '20:60': [816.6, 265.5999999999998], '20:61': [840.2, 247.9999999999998], '20:62': [863.8000000000001, 230.3999999999998], '20:63': [887.4000000000001, 212.7999999999998], '20:64': [911.0000000000001, 195.19999999999982], '20:65': [934.6000000000001, 177.59999999999982], '20:66': [958.2000000000002, 159.99999999999983], '21:55': [674.9999999999999, 335.9999999999999], '21:56': [698.5999999999999, 318.39999999999986], '21:57': [722.1999999999999, 300.79999999999984], '21:58': [745.8, 283.1999999999998], '21:59': [769.4, 265.5999999999998], '21:60': [793.0, 247.9999999999998], '21:61': [816.6, 230.3999999999998], '21:62': [840.2, 212.7999999999998], '21:63': [863.8000000000001, 195.19999999999982], '21:64': [887.4000000000001, 177.59999999999982], '21:65': [911.0000000000001, 159.99999999999983], '21:66': [934.6000000000001, 142.39999999999984]}

#获取启动port
def getport(startid):
    #获取启动端口
    if startid == 0:
        startport = 5555
        return startport
    else:
        startport = 52550 + startid
        return startport

# 开始
def connect(startid):
    startport = getport(startid)
    # 关闭模拟器连接
    #subprocess.Popen('adb kill-server', shell=True)
    #time.sleep(3)
    # 开启模拟器连接
    subprocess.Popen('adb start-server', shell=True)
    time.sleep(3)
    # 重启并连接连接
    subprocess.Popen(r'adb connect 127.0.0.1:%d' % (startport), shell=True)
    time.sleep(3)

#根据字典值获取索引
def get_keys(dict, value):
     temp = [k for k,v in dict.items() if v == value]
     return temp[0]

# 结束
def finish(startport):
    process = subprocess.Popen('adb disconnect %s' % (startport), shell=True)
    time.sleep(3)


# 点击屏幕
def click(x,y,startport):
    process = subprocess.Popen(r'adb -s 127.0.0.1:%d shell input tap %d %d' %(startport,x,y),shell=True)
    print(x,y)
    time.sleep(1)
    
#长按屏幕
def click_long(x,y,time,startport):
    process = subprocess.Popen(r'adb -s 127.0.0.1:%d shell input swipe %d %d %d %d %d' %(startport,x,y,x,y,time*1000),shell=True)
    print(x,y)

    
# 滑屏
def swipe(drt,startport):
    if drt == 'top':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 640 150 640 650' % (startport), shell=True)
        time.sleep(1)
    elif drt == 'bot':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 640 650 640 150' % (startport), shell=True)
        time.sleep(1)
    elif drt == 'left':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 100 360 1000 360' % (startport), shell=True)
        time.sleep(1)
    elif drt == 'right':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 1000 360 100 360' % (startport), shell=True)
        time.sleep(1)
# 输入文本
def text(text,startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input text %s' % (startport, text), shell=True)
    time.sleep(3)
# 返回
def back(startport):
    print('back')
    process = subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 4' % (startport), shell=True)
    time.sleep(3)
# HOME
def home(startport):
    process = subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 3' % (startport), shell=True)
    time.sleep(3)
# 熄灭
def interest(startport):
    process = subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 223' % (startport), shell=True)
    time.sleep(3)
# 点亮
def light(startport):
    process = subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 224' % (startport), shell=True)
    time.sleep(3)
# 静音
def silence(startport):
    process = subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 164' % (startport), shell=True)
    time.sleep(1.5)
    click(pos['silence'][0], pos['silence'][1])
#获取位置信息
def get_pos():
    #归到右上角
    #swipe('top', startport)
    #swipe('right', startport)
    # 从左往上移除
    pointleft = pos['pointleft'].copy()
    for y in range(5):
        pointindex = pointleft.copy()
        pointleft[0] += 23.6
        pointleft[1] += 17.6
        for x in range(22):
            rm_pos[str(y) + ":" + str(x)] = []
            rm_pos[str(y) + ":" + str(x)].append(pointindex[0])
            rm_pos[str(y) + ":" + str(x)].append(pointindex[1])
            '''
            click(pointindex[0], pointindex[1], startport)
            time.sleep(1)
            click(pos['action'][0], pos['action'][1], startport)
            time.sleep(1)
            click(pos['exitstore'][0], pos['exitstore'][1], startport)
            time.sleep(1)
            click(pos['cancel'][0], pos['cancel'][1], startport)
            '''
            pointindex[0] += 23.6
            pointindex[1] -= 17.6
            # time.sleep(timewait)
    # 从上往右移除
    pointtop_continue = pos['pointtop_continue'].copy()
    for y in range(5, 10):
        pointindex = pointtop_continue.copy()
        pointtop_continue[0] -= 23.6
        pointtop_continue[1] += 17.6
        for x in range(16):
            rm_pos[str(y) + ":" + str(x + 22)] = []
            rm_pos[str(y) + ":" + str(x + 22)].append(pointindex[0])
            rm_pos[str(y) + ":" + str(x + 22)].append(pointindex[1])
            '''
            click(pointindex[0], pointindex[1], startport)
            time.sleep(1)
            click(pos['action'][0], pos['action'][1], startport)
            time.sleep(1)
            click(pos['exitstore'][0], pos['exitstore'][1], startport)
            time.sleep(1)
            click(pos['cancel'][0], pos['cancel'][1], startport)
            '''
            pointindex[0] += 23.6
            pointindex[1] += 17.6
            # time.sleep(timewait)
    # 归到左下角
    # swipe('bot', startport)
    # swipe('left', startport)
    # 从下往左移除,接着上次移除的地方开始
    pointbot = pos['pointbot'].copy()
    for y in range(10, 16):
        pointindex = pointbot.copy()
        pointbot[0] += 23.6
        pointbot[1] -= 17.6
        for x in range(17):
            rm_pos[str(y) + ":" + str(x + 22 + 16)] = []
            rm_pos[str(y) + ":" + str(x + 22 + 16)].append(pointindex[0])
            rm_pos[str(y) + ":" + str(x + 22 + 16)].append(pointindex[1])
            '''
            click(pointindex[0], pointindex[1], startport)
            time.sleep(1)
            click(pos['action'][0], pos['action'][1], startport)
            time.sleep(1)
            click(pos['exitstore'][0], pos['exitstore'][1], startport)
            time.sleep(1)
            click(pos['cancel'][0], pos['cancel'][1], startport)
            '''
            pointindex[0] -= 23.6
            pointindex[1] -= 17.6
            # time.sleep(timewait)
    # 从下往右移除,接着上次移除的地方开始
    pointbot_continue = pos['pointbot_continue'].copy()
    for y in range(16, 22):
        pointindex = pointbot_continue.copy()
        pointbot_continue[0] -= 23.6
        pointbot_continue[1] -= 17.6
        for x in range(12):
            rm_pos[str(y) + ":" + str(x + 22 + 16 + 17)] = []
            rm_pos[str(y) + ":" + str(x + 22 + 16 + 17)].append(pointindex[0])
            rm_pos[str(y) + ":" + str(x + 22 + 16 + 17)].append(pointindex[1])
            '''
            click(pointindex[0], pointindex[1], startport)
            time.sleep(1)
            click(pos['action'][0], pos['action'][1], startport)
            time.sleep(1)
            click(pos['exitstore'][0], pos['exitstore'][1], startport)
            time.sleep(1)
            click(pos['cancel'][0], pos['cancel'][1], startport)
            '''
            pointindex[0] += 23.6
            pointindex[1] -= 17.6
            # time.sleep(timewait)

    print(rm_pos)

def removeTree(startport,timewait):
    clickTimes = 0
    swipeTimes = 1
    #归到右上角
    swipe('top', startport)
    swipe('right', startport)
    for position in range(len(rm_posRT)):
        #随机获取右上坐标索引
        posIndex = random.sample(rm_posRT.keys(), 1)[0]
        #根据index获取坐标地址的值
        posValue = rm_posRT[posIndex]
        #并且将其在字典中删除
        rm_posRT.pop(posIndex)
        click(posValue[0], posValue[1], startport)
        time.sleep(1)
        click(pos['action'][0], pos['action'][1], startport)
        time.sleep(1)
        click(pos['exitstore'][0], pos['exitstore'][1], startport)
        time.sleep(1)
        click(pos['cancel'][0], pos['cancel'][1], startport)
        time.sleep(timewait)
        clickTimes += 1
        #每隔20次进行一次定位
        if (clickTimes // 20) == swipeTimes:
            swipeTimes += 1
            swipe('top', startport)
            swipe('right', startport)

    # 归到左下角
    swipe('bot', startport)
    swipe('left', startport)
    for position in range(len(rm_posLB)):
        #随机获取左下坐标索引
        posIndex = random.sample(rm_posLB.keys(), 1)[0]
        #根据index获取坐标地址的值
        posValue = rm_posLB[posIndex]
        #并且将其在字典中删除
        rm_posLB.pop(posIndex)
        click(posValue[0], posValue[1], startport)
        time.sleep(1)
        click(pos['action'][0], pos['action'][1], startport)
        time.sleep(1)
        click(pos['exitstore'][0], pos['exitstore'][1], startport)
        time.sleep(1)
        click(pos['cancel'][0], pos['cancel'][1], startport)
        time.sleep(timewait)
        clickTimes += 1
        #每隔20次进行一次定位
        if (clickTimes // 20) == swipeTimes:
            swipeTimes += 1
            swipe('bot', startport)
            swipe('left', startport)

    g.msgbox(msg='已经移除完毕！')

def start(startid):
    #values = g.multenterbox(msg='输入对应参数',title='砍树除草',fields=['模拟器id','时间间隔'],values=[1,2])
    #startid = int(values[0])
    #timewait = int(values[1])
    #时间间隔
    timewait =2
    startport = getport(startid)
    connect(startid)
    removeTree(startport,timewait)