# coding:utf-8
import subprocess
import time
import easygui as g
import random
from coc_start import Coc as c
import win32gui
import keyboard as k
import threading
import inspect
import ctypes
import sys
from pynput.keyboard import Key, Listener
import configparser
import random
# coc模板
#方法：

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
    'exitstore': [1230, 50],
    'name': [640, 325],
    'name_done': [640, 235],
    'alias_name': [640, 510],
    'idcard': [640, 470],
    'register': [760, 545],
    'store': [1200, 635],
    'relogin': [500, 825],
    'login_wandoujia': [640, 500],
    'login_kunlun': [640, 250],
    'login_kunlun1': [640, 560],
    'login_kunlun2': [640, 620],
    'store_build': [300, 100],
    'storeitem1': [330, 260],
    'storeitem2': [540, 260],
    'storeitem3': [750, 260],
    'storeitem4': [960, 260],
    'store_1': [200, 440],
    'store_2': [420, 440],
    'store_3': [640, 440],
    'store_4': [860, 440],
    'store_5': [1080, 440],
    'built01': [570, 235],
    'built02': [725, 580],
    'built03': [465, 460],
    'built04': [695, 140],
    'built05': [600, 350],
    'built06': [880, 230],
    'built07': [565, 100],
    'built08': [470, 300],
    'built09': [700, 280],
    'built10': [570, 320],
    'built11': [820, 320],
    'built12': [730, 390],
    'built13': [440, 270],
    'built14': [710, 195],
    'built15': [643, 416],
    'built16': [770, 310],
    'built17': [430, 105],
    'built18': [370, 230],
    'built19': [935, 420],
    'built20': [1035, 160],
    'built21': [1160, 215],
    'built22': [370, 370],
    'built23': [970, 360],
    'built24': [600, 220],
    'backcamp': [640, 640],
    'camp': [420, 420],
    'ruins': [850, 220],
    'base': [640, 380],
    'base2': [630, 325],
    'sure': [360, 935],
    'levelup': [715, 600],
    'levelup2': [615, 600],
    'enter': [640, 630],
    'war': [50, 440],
    'war_1': [360, 280],
    'war_2': [590, 320],
    'war_donate': [480, 550],
    'war_donate_last': [340, 570],
    'war_donate_next': [950, 570],
    'war_donate_trp1': [310, 170],
    'war_donate_trp2': [400, 170],
    'war_donate_trp3': [490, 170],
    'war_donate_trp4': [580, 170],
    'trainning_bt': [700, 600],
    'trainning': [54, 524],
    'trainningitem1': [150, 45],
    'trainningitem2': [370, 45],
    'trainningitem3': [590, 45],
    'trainningitem4': [810, 45],
    'trainningitem5': [1030, 45],
    'train_troop01': [130, 440],
    'train_template00': [1130, 180],
    'train_template01': [1130, 330],
    'train_template02': [1130, 480],
    'train_template03': [1130, 630],
    'attack_troop01': [200, 655],
    'attack_troop02': [300, 655],
    'attack_troop03': [400, 655],
    'attack_troop04': [500, 655],
    'attack_troop05': [600, 655],
    'attack': [100, 650],
    'attack_single': [170, 350],
    'goblin01': [850, 470],
    'goblin02': [1080, 475],
    'goblin03': [865, 475],
    'goblin01_point': [550, 300],
    'goblin02_point1': [670, 337],
    'goblin02_point2': [766, 265],
    'goblin03_point': [988, 552],
    'achievement': [50, 50],
    'achievement1': [1040, 170],
    'achievement2': [1040, 260],
    'achievement3': [1040, 350],
    'achievement4': [1040, 440],
    'achievement5': [1040, 520],
    'achievement6': [1040, 610],
    '2levelup': [713, 593],
    '3levelup': [640, 600],
    '4levelup': [714, 592],
    'mine1': [735, 180],
    'mine2': [735, 520],
    'mine3': [800, 450],
    'collector1': [500, 380],
    'collector2': [470, 500],
    'train1': [380, 320],
    'train2': [600, 440],
    'gold1': [470, 130],
    'water1': [790, 280],
    'rmtree': [640, 590],
    'script_start':[200,1070],
    'script_item1': [130, 290],
    'script_item2': [280, 290],
    'script_item3': [430, 290],
    'script_item4': [590, 290],
    'script_canceltroop': [1200, 135],
    'script_switch_mode': [340, 610],
    'script_swipetop': [340, 740],
    'script_swipebot': [340, 1000],
    'boat': [800, 300],
    'script_play': [340, 660],
    'script_donate': [340, 800],
    'edit_army': [1135, 585],
    'del_army': [1135, 650],
    'del_army_sure': [780, 470],
    'del_army_trp01': [110, 200],
    'del_army_trp02': [210, 200],
    'del_army_trp03': [310, 200],
    'del_army_trp04': [410, 200],
    'del_army_trp05': [510, 200],
    'del_army_trp06': [610, 200],
    'del_army_trp07': [710, 200],
    'del_army_trp08': [810, 200],
    'del_army_pt01': [110, 400],
    'del_army_pt02': [210, 400],
    'del_army_pt03': [310, 400],
    'del_army_pt04': [410, 400],
    'del_army_pt05': [510, 400],
    'del_army_pt06': [610, 400],
    'del_army_pt07': [710, 400]

}
# 建立字典存储所有位置信息
rm_pos = {}
rm_posRT_template = {'0:0': [149, 456], '0:1': [172.6, 438.4], '0:2': [196.2, 420.79999999999995], '0:3': [219.79999999999998, 403.19999999999993], '0:4': [243.39999999999998, 385.5999999999999], '0:5': [267.0, 367.9999999999999], '0:6': [290.6, 350.39999999999986], '0:7': [314.20000000000005, 332.79999999999984], '0:8': [337.80000000000007, 315.1999999999998], '0:9': [361.4000000000001, 297.5999999999998], '0:10': [385.0000000000001, 279.9999999999998], '0:11': [408.60000000000014, 262.39999999999975], '0:12': [432.20000000000016, 244.79999999999976], '0:13': [455.8000000000002, 227.19999999999976], '0:14': [479.4000000000002, 209.59999999999977], '0:15': [503.0000000000002, 191.99999999999977], '0:16': [526.6000000000003, 174.39999999999978], '0:17': [550.2000000000003, 156.79999999999978], '0:18': [573.8000000000003, 139.1999999999998], '0:19': [597.4000000000003, 121.5999999999998], '0:20': [621.0000000000003, 103.9999999999998], '0:21': [644.6000000000004, 86.3999999999998], '1:0': [172.6, 473.6], '1:1': [196.2, 456.0], '1:2': [219.79999999999998, 438.4], '1:3': [243.39999999999998, 420.79999999999995], '1:4': [267.0, 403.19999999999993], '1:5': [290.6, 385.5999999999999], '1:6': [314.20000000000005, 367.9999999999999], '1:7': [337.80000000000007, 350.39999999999986], '1:8': [361.4000000000001, 332.79999999999984], '1:9': [385.0000000000001, 315.1999999999998], '1:10': [408.60000000000014, 297.5999999999998], '1:11': [432.20000000000016, 279.9999999999998], '1:12': [455.8000000000002, 262.39999999999975], '1:13': [479.4000000000002, 244.79999999999976], '1:14': [503.0000000000002, 227.19999999999976], '1:15': [526.6000000000003, 209.59999999999977], '1:16': [550.2000000000003, 191.99999999999977], '1:17': [573.8000000000003, 174.39999999999978], '1:18': [597.4000000000003, 156.79999999999978], '1:19': [621.0000000000003, 139.1999999999998], '1:20': [644.6000000000004, 121.5999999999998], '1:21': [668.2000000000004, 103.9999999999998], '2:0': [196.2, 491.20000000000005], '2:1': [219.79999999999998, 473.6], '2:2': [243.39999999999998, 456.0], '2:3': [267.0, 438.4], '2:4': [290.6, 420.79999999999995], '2:5': [314.20000000000005, 403.19999999999993], '2:6': [337.80000000000007, 385.5999999999999], '2:7': [361.4000000000001, 367.9999999999999], '2:8': [385.0000000000001, 350.39999999999986], '2:9': [408.60000000000014, 332.79999999999984], '2:10': [432.20000000000016, 315.1999999999998], '2:11': [455.8000000000002, 297.5999999999998], '2:12': [479.4000000000002, 279.9999999999998], '2:13': [503.0000000000002, 262.39999999999975], '2:14': [526.6000000000003, 244.79999999999976], '2:15': [550.2000000000003, 227.19999999999976], '2:16': [573.8000000000003, 209.59999999999977], '2:17': [597.4000000000003, 191.99999999999977], '2:18': [621.0000000000003, 174.39999999999978], '2:19': [644.6000000000004, 156.79999999999978], '2:20': [668.2000000000004, 139.1999999999998], '2:21': [691.8000000000004, 121.5999999999998], '3:0': [219.79999999999998, 508.80000000000007], '3:1': [243.39999999999998, 491.20000000000005], '3:2': [267.0, 473.6], '3:3': [290.6, 456.0], '3:4': [314.20000000000005, 438.4], '3:5': [337.80000000000007, 420.79999999999995], '3:6': [361.4000000000001, 403.19999999999993], '3:7': [385.0000000000001, 385.5999999999999], '3:8': [408.60000000000014, 367.9999999999999], '3:9': [432.20000000000016, 350.39999999999986], '3:10': [455.8000000000002, 332.79999999999984], '3:11': [479.4000000000002, 315.1999999999998], '3:12': [503.0000000000002, 297.5999999999998], '3:13': [526.6000000000003, 279.9999999999998], '3:14': [550.2000000000003, 262.39999999999975], '3:15': [573.8000000000003, 244.79999999999976], '3:16': [597.4000000000003, 227.19999999999976], '3:17': [621.0000000000003, 209.59999999999977], '3:18': [644.6000000000004, 191.99999999999977], '3:19': [668.2000000000004, 174.39999999999978], '3:20': [691.8000000000004, 156.79999999999978], '3:21': [715.4000000000004, 139.1999999999998], '4:0': [243.39999999999998, 526.4000000000001], '4:1': [267.0, 508.80000000000007], '4:2': [290.6, 491.20000000000005], '4:3': [314.20000000000005, 473.6], '4:4': [337.80000000000007, 456.0], '4:5': [361.4000000000001, 438.4], '4:6': [385.0000000000001, 420.79999999999995], '4:7': [408.60000000000014, 403.19999999999993], '4:8': [432.20000000000016, 385.5999999999999], '4:9': [455.8000000000002, 367.9999999999999], '4:10': [479.4000000000002, 350.39999999999986], '4:11': [503.0000000000002, 332.79999999999984], '4:12': [526.6000000000003, 315.1999999999998], '4:13': [550.2000000000003, 297.5999999999998], '4:14': [573.8000000000003, 279.9999999999998], '4:15': [597.4000000000003, 262.39999999999975], '4:16': [621.0000000000003, 244.79999999999976], '4:17': [644.6000000000004, 227.19999999999976], '4:18': [668.2000000000004, 209.59999999999977], '4:19': [691.8000000000004, 191.99999999999977], '4:20': [715.4000000000004, 174.39999999999978], '4:21': [739.0000000000005, 156.79999999999978], '5:22': [736, 188], '5:23': [759.6, 205.6], '5:24': [783.2, 223.2], '5:25': [806.8000000000001, 240.79999999999998], '5:26': [830.4000000000001, 258.4], '5:27': [854.0000000000001, 276.0], '5:28': [877.6000000000001, 293.6], '5:29': [901.2000000000002, 311.20000000000005], '5:30': [924.8000000000002, 328.80000000000007], '5:31': [948.4000000000002, 346.4000000000001], '5:32': [972.0000000000002, 364.0000000000001], '5:33': [995.6000000000003, 381.60000000000014], '5:34': [1019.2000000000003, 399.20000000000016], '5:35': [1042.8000000000002, 416.8000000000002], '5:36': [1066.4, 434.4000000000002], '5:37': [1090.0, 452.0000000000002], '6:22': [712.4, 205.6], '6:23': [736.0, 223.2], '6:24': [759.6, 240.79999999999998], '6:25': [783.2, 258.4], '6:26': [806.8000000000001, 276.0], '6:27': [830.4000000000001, 293.6], '6:28': [854.0000000000001, 311.20000000000005], '6:29': [877.6000000000001, 328.80000000000007], '6:30': [901.2000000000002, 346.4000000000001], '6:31': [924.8000000000002, 364.0000000000001], '6:32': [948.4000000000002, 381.60000000000014], '6:33': [972.0000000000002, 399.20000000000016], '6:34': [995.6000000000003, 416.8000000000002], '6:35': [1019.2000000000003, 434.4000000000002], '6:36': [1042.8000000000002, 452.0000000000002], '6:37': [1066.4, 469.60000000000025], '7:22': [688.8, 223.2], '7:23': [712.4, 240.79999999999998], '7:24': [736.0, 258.4], '7:25': [759.6, 276.0], '7:26': [783.2, 293.6], '7:27': [806.8000000000001, 311.20000000000005], '7:28': [830.4000000000001, 328.80000000000007], '7:29': [854.0000000000001, 346.4000000000001], '7:30': [877.6000000000001, 364.0000000000001], '7:31': [901.2000000000002, 381.60000000000014], '7:32': [924.8000000000002, 399.20000000000016], '7:33': [948.4000000000002, 416.8000000000002], '7:34': [972.0000000000002, 434.4000000000002], '7:35': [995.6000000000003, 452.0000000000002], '7:36': [1019.2000000000003, 469.60000000000025], '7:37': [1042.8000000000002, 487.2000000000003], '8:22': [665.1999999999999, 240.79999999999998], '8:23': [688.8, 258.4], '8:24': [712.4, 276.0], '8:25': [736.0, 293.6], '8:26': [759.6, 311.20000000000005], '8:27': [783.2, 328.80000000000007], '8:28': [806.8000000000001, 346.4000000000001], '8:29': [830.4000000000001, 364.0000000000001], '8:30': [854.0000000000001, 381.60000000000014], '8:31': [877.6000000000001, 399.20000000000016], '8:32': [901.2000000000002, 416.8000000000002], '8:33': [924.8000000000002, 434.4000000000002], '8:34': [948.4000000000002, 452.0000000000002], '8:35': [972.0000000000002, 469.60000000000025], '8:36': [995.6000000000003, 487.2000000000003], '8:37': [1019.2000000000003, 504.8000000000003], '9:22': [641.5999999999999, 258.4], '9:23': [665.1999999999999, 276.0], '9:24': [688.8, 293.6], '9:25': [712.4, 311.20000000000005], '9:26': [736.0, 328.80000000000007], '9:27': [759.6, 346.4000000000001], '9:28': [783.2, 364.0000000000001], '9:29': [806.8000000000001, 381.60000000000014], '9:30': [830.4000000000001, 399.20000000000016], '9:31': [854.0000000000001, 416.8000000000002], '9:32': [877.6000000000001, 434.4000000000002], '9:33': [901.2000000000002, 452.0000000000002], '9:34': [924.8000000000002, 469.60000000000025], '9:35': [948.4000000000002, 487.2000000000003], '9:36': [972.0000000000002, 504.8000000000003], '9:37': [995.6000000000003, 522.4000000000003]}
rm_posLB_template = {'10:38': [658, 525], '10:39': [634.4, 507.4], '10:40': [610.8, 489.79999999999995], '10:41': [587.1999999999999, 472.19999999999993], '10:42': [563.5999999999999, 454.5999999999999], '10:43': [539.9999999999999, 436.9999999999999], '10:44': [516.3999999999999, 419.39999999999986], '10:45': [492.79999999999984, 401.79999999999984], '10:46': [469.1999999999998, 384.1999999999998], '10:47': [445.5999999999998, 366.5999999999998], '10:48': [421.9999999999998, 348.9999999999998], '10:49': [398.39999999999975, 331.39999999999975], '10:50': [374.7999999999997, 313.7999999999997], '10:51': [351.1999999999997, 296.1999999999997], '10:52': [327.5999999999997, 278.5999999999997], '10:53': [303.99999999999966, 260.99999999999966], '10:54': [280.39999999999964, 243.39999999999966], '11:38': [681.6, 507.4], '11:39': [658.0, 489.79999999999995], '11:40': [634.4, 472.19999999999993], '11:41': [610.8, 454.5999999999999], '11:42': [587.1999999999999, 436.9999999999999], '11:43': [563.5999999999999, 419.39999999999986], '11:44': [539.9999999999999, 401.79999999999984], '11:45': [516.3999999999999, 384.1999999999998], '11:46': [492.79999999999984, 366.5999999999998], '11:47': [469.1999999999998, 348.9999999999998], '11:48': [445.5999999999998, 331.39999999999975], '11:49': [421.9999999999998, 313.7999999999997], '11:50': [398.39999999999975, 296.1999999999997], '11:51': [374.7999999999997, 278.5999999999997], '11:52': [351.1999999999997, 260.99999999999966], '11:53': [327.5999999999997, 243.39999999999966], '11:54': [303.99999999999966, 225.79999999999967], '12:38': [705.2, 489.79999999999995], '12:39': [681.6, 472.19999999999993], '12:40': [658.0, 454.5999999999999], '12:41': [634.4, 436.9999999999999], '12:42': [610.8, 419.39999999999986], '12:43': [587.1999999999999, 401.79999999999984], '12:44': [563.5999999999999, 384.1999999999998], '12:45': [539.9999999999999, 366.5999999999998], '12:46': [516.3999999999999, 348.9999999999998], '12:47': [492.79999999999984, 331.39999999999975], '12:48': [469.1999999999998, 313.7999999999997], '12:49': [445.5999999999998, 296.1999999999997], '12:50': [421.9999999999998, 278.5999999999997], '12:51': [398.39999999999975, 260.99999999999966], '12:52': [374.7999999999997, 243.39999999999966], '12:53': [351.1999999999997, 225.79999999999967], '12:54': [327.5999999999997, 208.19999999999968], '13:38': [728.8000000000001, 472.19999999999993], '13:39': [705.2, 454.5999999999999], '13:40': [681.6, 436.9999999999999], '13:41': [658.0, 419.39999999999986], '13:42': [634.4, 401.79999999999984], '13:43': [610.8, 384.1999999999998], '13:44': [587.1999999999999, 366.5999999999998], '13:45': [563.5999999999999, 348.9999999999998], '13:46': [539.9999999999999, 331.39999999999975], '13:47': [516.3999999999999, 313.7999999999997], '13:48': [492.79999999999984, 296.1999999999997], '13:49': [469.1999999999998, 278.5999999999997], '13:50': [445.5999999999998, 260.99999999999966], '13:51': [421.9999999999998, 243.39999999999966], '13:52': [398.39999999999975, 225.79999999999967], '13:53': [374.7999999999997, 208.19999999999968], '13:54': [351.1999999999997, 190.59999999999968], '14:38': [752.4000000000001, 454.5999999999999], '14:39': [728.8000000000001, 436.9999999999999], '14:40': [705.2, 419.39999999999986], '14:41': [681.6, 401.79999999999984], '14:42': [658.0, 384.1999999999998], '14:43': [634.4, 366.5999999999998], '14:44': [610.8, 348.9999999999998], '14:45': [587.1999999999999, 331.39999999999975], '14:46': [563.5999999999999, 313.7999999999997], '14:47': [539.9999999999999, 296.1999999999997], '14:48': [516.3999999999999, 278.5999999999997], '14:49': [492.79999999999984, 260.99999999999966], '14:50': [469.1999999999998, 243.39999999999966], '14:51': [445.5999999999998, 225.79999999999967], '14:52': [421.9999999999998, 208.19999999999968], '14:53': [398.39999999999975, 190.59999999999968], '14:54': [374.7999999999997, 172.9999999999997], '15:38': [776.0000000000001, 436.9999999999999], '15:39': [752.4000000000001, 419.39999999999986], '15:40': [728.8000000000001, 401.79999999999984], '15:41': [705.2, 384.1999999999998], '15:42': [681.6, 366.5999999999998], '15:43': [658.0, 348.9999999999998], '15:44': [634.4, 331.39999999999975], '15:45': [610.8, 313.7999999999997], '15:46': [587.1999999999999, 296.1999999999997], '15:47': [563.5999999999999, 278.5999999999997], '15:48': [539.9999999999999, 260.99999999999966], '15:49': [516.3999999999999, 243.39999999999966], '15:50': [492.79999999999984, 225.79999999999967], '15:51': [469.1999999999998, 208.19999999999968], '15:52': [445.5999999999998, 190.59999999999968], '15:53': [421.9999999999998, 172.9999999999997], '15:54': [398.39999999999975, 155.3999999999997], '16:55': [793, 424], '16:56': [816.6, 406.4], '16:57': [840.2, 388.79999999999995], '16:58': [863.8000000000001, 371.19999999999993], '16:59': [887.4000000000001, 353.5999999999999], '16:60': [911.0000000000001, 335.9999999999999], '16:61': [934.6000000000001, 318.39999999999986], '16:62': [958.2000000000002, 300.79999999999984], '16:63': [981.8000000000002, 283.1999999999998], '16:64': [1005.4000000000002, 265.5999999999998], '16:65': [1029.0000000000002, 247.9999999999998], '16:66': [1052.6000000000001, 230.3999999999998], '17:55': [769.4, 406.4], '17:56': [793.0, 388.79999999999995], '17:57': [816.6, 371.19999999999993], '17:58': [840.2, 353.5999999999999], '17:59': [863.8000000000001, 335.9999999999999], '17:60': [887.4000000000001, 318.39999999999986], '17:61': [911.0000000000001, 300.79999999999984], '17:62': [934.6000000000001, 283.1999999999998], '17:63': [958.2000000000002, 265.5999999999998], '17:64': [981.8000000000002, 247.9999999999998], '17:65': [1005.4000000000002, 230.3999999999998], '17:66': [1029.0000000000002, 212.7999999999998], '18:55': [745.8, 388.79999999999995], '18:56': [769.4, 371.19999999999993], '18:57': [793.0, 353.5999999999999], '18:58': [816.6, 335.9999999999999], '18:59': [840.2, 318.39999999999986], '18:60': [863.8000000000001, 300.79999999999984], '18:61': [887.4000000000001, 283.1999999999998], '18:62': [911.0000000000001, 265.5999999999998], '18:63': [934.6000000000001, 247.9999999999998], '18:64': [958.2000000000002, 230.3999999999998], '18:65': [981.8000000000002, 212.7999999999998], '18:66': [1005.4000000000002, 195.19999999999982], '19:55': [722.1999999999999, 371.19999999999993], '19:56': [745.8, 353.5999999999999], '19:57': [769.4, 335.9999999999999], '19:58': [793.0, 318.39999999999986], '19:59': [816.6, 300.79999999999984], '19:60': [840.2, 283.1999999999998], '19:61': [863.8000000000001, 265.5999999999998], '19:62': [887.4000000000001, 247.9999999999998], '19:63': [911.0000000000001, 230.3999999999998], '19:64': [934.6000000000001, 212.7999999999998], '19:65': [958.2000000000002, 195.19999999999982], '19:66': [981.8000000000002, 177.59999999999982], '20:55': [698.5999999999999, 353.5999999999999], '20:56': [722.1999999999999, 335.9999999999999], '20:57': [745.8, 318.39999999999986], '20:58': [769.4, 300.79999999999984], '20:59': [793.0, 283.1999999999998], '20:60': [816.6, 265.5999999999998], '20:61': [840.2, 247.9999999999998], '20:62': [863.8000000000001, 230.3999999999998], '20:63': [887.4000000000001, 212.7999999999998], '20:64': [911.0000000000001, 195.19999999999982], '20:65': [934.6000000000001, 177.59999999999982], '20:66': [958.2000000000002, 159.99999999999983], '21:55': [674.9999999999999, 335.9999999999999], '21:56': [698.5999999999999, 318.39999999999986], '21:57': [722.1999999999999, 300.79999999999984], '21:58': [745.8, 283.1999999999998], '21:59': [769.4, 265.5999999999998], '21:60': [793.0, 247.9999999999998], '21:61': [816.6, 230.3999999999998], '21:62': [840.2, 212.7999999999998], '21:63': [863.8000000000001, 195.19999999999982], '21:64': [887.4000000000001, 177.59999999999982], '21:65': [911.0000000000001, 159.99999999999983], '21:66': [934.6000000000001, 142.39999999999984]}
IDcard = {
    '01':['蒋芳馨',230811197604235589],
    '02':['谢慧月',131022198204225442],
    '03':['卫寒凝',429006198902135782],
    '04':['常芳懿',150626198306245680],
    '05':['严慧秀',340207198703162947],
    '06':['窦涵菡',431000198806214487],
    '07':['苗和怡',410728198503202745],
    '08':['顾虹影',411327198706254249],
    '09':['岑红旭',320125198809105266],
    '10':['雷飞雪',522635197808272243],
    '11':['元含玉',150627198605144122],
    '12':['方晗蕾',512001197707215487],
    '13':['华安娜',421126199005228725],
    '14':['康安卉',420684198104136143],
    '15':['尤芳蕤',320281197302185262],
    '16':['毕晴',340802197202137707],
    '17':['凌冬旭',652801198202286713],
    '18':['邓靖鸣',652801198202282050],
    '19':['彭翰毅',652801198202288532],
    '20':['云邦楠',652801198202285032],
    '22':['盛颢锵',652801198202289033],
    '23':['范季晨',652801198202283256],
    '24':['米鸿聪',652801198202281197],
    '25':['邢向涪',652801198202283571],
    '26':['明锡贤',652801198202287775],
    '27':['熊蒙少',652801198202284259],
    '28':['熊耿羿',652801198202287097],
    '29':['傅洪泉',652801198202282691],
    '30':['唐文冲',652801198202281613],
    '31':['卜钱磊',652801198202287556],
    '32':['危民佑',652801198202284216],
    '33':['狄舟察','65280119820228737X'],
    '34':['酆征科',652801198202285016],
    '35':['滑谱班',652801198202285892],
    '36':['酆向涪',652801198202287759],
    '37':['邢锋滕',652801198202284574],
    '38':['钟冉伯',652801198202288735],
    '39':['酆友水',652801198202288516],
    '40':['万顾尉',652801198202282915],
    '41':['滕资龙',652801198202287134]

}

#配置文件路径
configpath = r"E:\Program Files\Python\Python38\works\tool\Config.ini"

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
def connect(startport):
    # 关闭模拟器连接
    subprocess.Popen('adb kill-server', shell=True)
    time.sleep(3)
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
def click(x,y,startport,*args):
    subprocess.Popen(r'adb -s 127.0.0.1:%d shell input tap %d %d' %(startport,x,y),shell=True)
    print(x,y)
    time.sleep(1)
    if len(args) > 0:
        time.sleep(args[0])
# 快速点击屏幕
def click_short(x,y,startport,times):
    for n in range(times):
        process = subprocess.Popen(r'adb -s 127.0.0.1:%d shell input tap %d %d' %(startport,x,y),shell=True)
        time.sleep(0.1)
        print(x,y)
#长按屏幕
def click_long(x,y,time,startport):
    process = subprocess.Popen(r'adb -s 127.0.0.1:%d shell input swipe %d %d %d %d %d' %(startport,x,y,x,y,time*1000),shell=True)
    print(x,y)
# 滑屏
def swipe(drt,startport):
    if drt == 'top':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 640 200 640 700' % (startport), shell=True)
        time.sleep(2)
    elif drt == 'bot':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 640 650 640 150' % (startport), shell=True)
        time.sleep(2)
    elif drt == 'left':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 100 360 1000 360' % (startport), shell=True)
        time.sleep(2)
    elif drt == 'right':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 1000 360 100 360' % (startport), shell=True)
        time.sleep(2)
#定点滑动
def swipeport(x1,y1,x2,y2,startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe %d %d %d %d' % (startport,x1,y1,x2,y2), shell=True)
    time.sleep(3)
# 输入文本
def text(text,startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input text %s' % (startport, text), shell=True)
    time.sleep(1)
# 返回
def back(startport):
    print('back')
    subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 4' % (startport), shell=True)
    time.sleep(3)
# HOME
def home(startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 3' % (startport), shell=True)
    time.sleep(3)
# HOME
def menu(startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 82' % (startport), shell=True)
    time.sleep(3)

# 熄灭
def interest(startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 223' % (startport), shell=True)
    time.sleep(3)
# 点亮
def light(startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 224' % (startport), shell=True)
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

def removeTree(startid,timewait):
    timewait = 2
    startport = getport(startid)
    connect(startport)
    clickTimes = 0
    swipeTimes = 1
    #归到右上角
    swipe('top', startport)
    swipe('right', startport)
    rm_posRT = rm_posRT_template.copy()
    rm_posLB = rm_posLB_template.copy()
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
        #每隔50次进行一次定位
        if (clickTimes // 50) == swipeTimes:
            swipeTimes += 1
            swipe('top', startport)
            swipe('right', startport)

    # 归到左下角
    swipe('bot', startport)
    swipe('left', startport)
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
        #每隔50次进行一次定位
        if (clickTimes // 50) == swipeTimes:
            swipeTimes += 1
            swipe('bot', startport)
            swipe('left', startport)

    g.msgbox(msg='已经移除完毕！')


#训练士兵
def train(train_troopid,num,startport):
    click(pos['trainning'][0], pos['trainning'][1], startport)
    click(pos['trainningitem2'][0], pos['trainningitem2'][1], startport)
    click_short(pos[train_troopid][0], pos[train_troopid][1], startport,num)
    click(pos['exitstore'][0], pos['exitstore'][1], startport)

#训练捐兵
def train_template(train_template,startport):
    click(pos['trainning'][0], pos['trainning'][1], startport,3)
    #12本上
    click(pos['trainningitem5'][0], pos['trainningitem5'][1], startport,3)
    swipe('top', startport)
    click(pos[train_template][0], pos[train_template][1], startport,3)
    #click(pos[train_template][0], pos[train_template][1], startport,3)
    #12本以下,多点一次因为会触发强化军队按钮
    click(pos['trainningitem4'][0], pos['trainningitem4'][1], startport,3)
    click(pos['trainningitem4'][0], pos['trainningitem4'][1], startport,3)
    swipe('top', startport)
    click(pos[train_template][0], pos[train_template][1], startport,3)
    #关闭
    click(pos['exitstore'][0], pos['exitstore'][1], startport,3)

#取消训练中的兵种
def cancel_troop(startport):
    click(pos['trainning'][0], pos['trainning'][1], startport)
    print('取消兵种')
    click(pos['trainningitem2'][0], pos['trainningitem2'][1], startport)
    click_short(pos['script_canceltroop'][0], pos['script_canceltroop'][1], startport, 400)
    click(pos['exitstore'][0], pos['exitstore'][1], startport,3)

#取消训练中的药水
def cancel_potion(startport):
    click(pos['trainning'][0], pos['trainning'][1], startport)
    print('取消药水')
    click(pos['trainningitem3'][0], pos['trainningitem3'][1], startport)
    click_short(pos['script_canceltroop'][0], pos['script_canceltroop'][1], startport, 50)
    click(pos['exitstore'][0], pos['exitstore'][1], startport,3)

#取消现有兵种和药水
def cancel_army(startport):
    click(pos['trainning'][0], pos['trainning'][1], startport)
    print('取消现有兵种和药水')
    click(pos['trainningitem1'][0], pos['trainningitem1'][1], startport)
    click(pos['edit_army'][0], pos['edit_army'][1], startport)
    #取消兵种
    for n in range(1,9):
        click_short(pos['del_army_trp0%d' %(n)][0], pos['del_army_trp0%d' %(n)][1], startport, 200)
    #取消药水
    for n in range(1,8):
        click_short(pos['del_army_pt0%d' %(n)][0], pos['del_army_pt0%d' %(n)][1], startport, 10)
    #确定删除
    click(pos['del_army'][0], pos['del_army'][1], startport,3)
    click(pos['del_army_sure'][0], pos['del_army_sure'][1], startport,3)
    #退出
    click(pos['exitstore'][0], pos['exitstore'][1], startport, 3)

#启动coc
def startcoc(startport):
    connect(startport)
    try:
        #九游
        subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.supercell.clashofclans.uc/com.supercell.titan.kunlun.uc.GameAppKunlunUC' % (startport), shell=True)
        subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.tencent.tmgp.supercell.clashofclans/com.supercell.titan.tencent.GameAppTencent' % (startport), shell=True)
    except:
        #腾讯
        subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.tencent.tmgp.supercell.clashofclans/com.supercell.titan.tencent.GameAppTencent' % (startport), shell=True)
        subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.supercell.clashofclans.uc/com.supercell.titan.kunlun.uc.GameAppKunlunUC' % (startport), shell=True)
    #豌豆荚
    #subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.supercell.clashofclans.uc/com.supercell.titan.kunlun.uc.GameAppKunlunUC' % (startport), shell=True)
    time.sleep(30)
    click(pos['exitstore'][0], pos['exitstore'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    if startport == 52555:#如果是星陨，尝试点击登录 
        click(pos['login_wandoujia'][0], pos['login_wandoujia'][1], startport,3)
    else:
        click(pos['login_kunlun1'][0], pos['login_kunlun1'][1], startport,3)
        click(pos['login_kunlun2'][0], pos['login_kunlun2'][1], startport,3)
        click(pos['login_kunlun'][0], pos['login_kunlun'][1], startport,3)
#重启coc
def restartcoc(startport):
    home(startport)
    time.sleep(60)
    startcoc(startport)

def close():
    subprocess.Popen('taskkill /f /t /im DunDiEmu.exe & taskkill /f /t /im DdemuHandle.exe',shell=True)
    time.sleep(3)

#等待
def timewait(min,startport):
    for n in range(min):
        time.sleep(60)
        click(pos['cancel'][0], pos['cancel'][1], startport)

#取消
def cancel(startport):
    click(pos['cancel'][0], pos['cancel'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    click(pos['exitstore'][0], pos['exitstore'][1], startport)

#升级
def levelup(itemnum,startport):
    time.sleep(1)
    click(pos['%dlevelup' %(itemnum)][0], pos['%dlevelup' %(itemnum)][1], startport)
    time.sleep(1)
    click(pos['3levelup'][0], pos['3levelup'][1], startport)
    time.sleep(1)
    click(pos['cancel'][0], pos['cancel'][1], startport)

def levelup_mine0(startport):
    #收集一次资源确保选中不会出意外
    click(pos['mine1'][0], pos['mine1'][1], startport)
    click(pos['mine3'][0], pos['mine3'][1], startport)
    click(pos['collector1'][0], pos['collector1'][1], startport)
    click(pos['collector2'][0], pos['collector2'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    #升级矿场1,2
    click(pos['mine1'][0], pos['mine1'][1], startport)
    levelup(3,startport)
    time.sleep(5)
    click(pos['mine3'][0], pos['mine3'][1], startport)
    levelup(3, startport)
    
def levelup_mine(startport):
    #收集一次资源确保选中不会出意外
    click(pos['mine1'][0], pos['mine1'][1], startport)
    click(pos['mine2'][0], pos['mine2'][1], startport)
    click(pos['collector1'][0], pos['collector1'][1], startport)
    click(pos['collector2'][0], pos['collector2'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    #升级矿场1,2
    click(pos['mine1'][0], pos['mine1'][1], startport)
    levelup(3,startport)
    time.sleep(5)
    click(pos['mine2'][0], pos['mine2'][1], startport)
    levelup(3, startport)
    
def levelup_mine1(startport):
    #收集一次资源确保选中不会出意外
    click(pos['mine1'][0], pos['mine1'][1], startport)
    click(pos['mine2'][0], pos['mine2'][1], startport)
    click(pos['collector1'][0], pos['collector1'][1], startport)
    click(pos['collector2'][0], pos['collector2'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    #升级矿场1,2
    click(pos['mine1'][0], pos['mine1'][1], startport)
    levelup(3,startport)
    time.sleep(5)
    click(pos['mine2'][0] + 20, pos['mine2'][1] - 20, startport)
    levelup(3, startport)


def levelup_collector(startport):
    # 收集一次资源确保选中不会出意外
    click(pos['mine1'][0], pos['mine1'][1], startport)
    click(pos['mine2'][0], pos['mine2'][1], startport)
    click(pos['collector1'][0], pos['collector1'][1], startport)
    click(pos['collector2'][0], pos['collector2'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    #升级收集器1,2
    click(pos['collector1'][0], pos['collector1'][1], startport)
    levelup(3,startport)
    time.sleep(5)
    click(pos['collector2'][0], pos['collector2'][1], startport)
    levelup(3, startport)

def levelup_collector1(startport):
    # 收集一次资源确保选中不会出意外
    click(pos['mine1'][0], pos['mine1'][1], startport)
    click(pos['mine2'][0], pos['mine2'][1], startport)
    click(pos['collector1'][0], pos['collector1'][1], startport)
    click(pos['collector2'][0], pos['collector2'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    #升级收集器1,2
    click(pos['collector1'][0] + 20, pos['collector1'][1] - 20, startport)
    levelup(3,startport)
    time.sleep(5)
    click(pos['collector2'][0] + 20, pos['collector2'][1] - 20, startport)
    levelup(3, startport)
    
def levelup_saver(startport):
    # 收集一次资源
    click(pos['collector1'][0], pos['collector1'][1], startport)
    click(pos['mine1'][0], pos['mine1'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    #升级罐子
    click(pos['gold1'][0], pos['gold1'][1], startport)
    levelup(2,startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    #升级瓶子
    click(pos['water1'][0], pos['water1'][1], startport)
    levelup(2,startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)

def levelup_train(startport):
    #点击一下取消
    click(pos['cancel'][0], pos['cancel'][1], startport)
    #升级训练营1,2
    click(pos['train1'][0], pos['train1'][1], startport)
    levelup(4,startport)
    time.sleep(5)
    click(pos['train2'][0], pos['train2'][1], startport)
    levelup(4, startport)
    
def storebuild(startport):
    click(pos['store'][0], pos['store'][1], startport,1)
    click(pos['store_build'][0], pos['store_build'][1], startport)

#注册新id并且升级
def register(name,startid):
    #连接模拟器
    startport = getport(startid)
    connect(startport)
    #click(pos['name'][0],pos['name'][1],startport)
    #text(IDcard['01'][0])
    #注册身份证
    g.msgbox(msg=IDcard['18'][0])
    click(pos['idcard'][0], pos['idcard'][1],startport)
    time.sleep(1)
    text(IDcard['18'][1],startport)
    time.sleep(2)
    click(pos['register'][0], pos['register'][1],startport)
    time.sleep(15)
    click(pos['alias_name'][0], pos['alias_name'][1], startport)
    back(startport)
    #重启,菜单栏无效只能home然后等1分钟再重进
    restartcoc(startport)
    time.sleep(5)
    #取消广告
    click(pos['cancel'][0], pos['cancel'][1], startport)
    time.sleep(5)
    #开始默认教程
    #教程
    for n in range(5):
        click(pos['cancel'][0], pos['cancel'][1], startport)
    #造加农炮
    storebuild(startport)
    click(pos['store_3'][0], pos['store_3'][1], startport)
    click(pos['built01'][0], pos['built01'][1], startport)
    time.sleep(15)
    #哥布林攻打
    click(pos['built02'][0], pos['built02'][1], startport)
    time.sleep(15)
    for n in range(5):
        click(pos['cancel'][0], pos['cancel'][1], startport)
    click(pos['built03'][0], pos['built03'][1], startport)
    #打哥布林
    time.sleep(5)
    click_short(pos['built03'][0], pos['built03'][1], startport, 20)
    time.sleep(40)
    click(pos['backcamp'][0], pos['backcamp'][1], startport)
    time.sleep(5)
    #造圣水收集器
    click(pos['cancel'][0], pos['cancel'][1], startport)
    storebuild(startport)
    click(pos['store_3'][0], pos['store_3'][1], startport)
    click(pos['built04'][0], pos['built04'][1], startport)
    # 造圣水瓶
    click(pos['cancel'][0], pos['cancel'][1], startport)
    storebuild(startport)
    click(pos['store_3'][0], pos['store_3'][1], startport)
    click(pos['built05'][0], pos['built05'][1], startport)
    time.sleep(15)
    # 造矿场
    click(pos['cancel'][0], pos['cancel'][1], startport)
    storebuild(startport)
    click(pos['store_3'][0], pos['store_3'][1], startport)
    click(pos['built06'][0], pos['built06'][1], startport)
    time.sleep(15)
    # 造储金罐
    click(pos['cancel'][0], pos['cancel'][1], startport)
    storebuild(startport)
    click(pos['store_3'][0], pos['store_3'][1], startport)
    click(pos['built07'][0], pos['built07'][1], startport)
    time.sleep(15)
    # 造训练营
    click(pos['cancel'][0], pos['cancel'][1], startport)
    storebuild(startport)
    click(pos['store_1'][0], pos['store_1'][1], startport)
    click(pos['built08'][0], pos['built08'][1], startport)
    time.sleep(15)
    #造兵
    click(pos['cancel'][0], pos['cancel'][1], startport)
    click(pos['camp'][0], pos['camp'][1], startport)
    click(pos['trainning_bt'][0], pos['trainning_bt'][1], startport)
    click_short(pos['train_troop01'][0], pos['train_troop01'][1], startport,50)
    #等待造兵
    timewait(7,startport)
    #进攻哥布林
    time.sleep(5)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    time.sleep(1)
    click(pos['attack'][0],pos['attack'][1],startport)
    click(pos['goblin01'][0],pos['goblin01'][1],startport)
    time.sleep(5)
    click_short(pos['goblin01_point'][0],pos['goblin01_point'][1],startport,50)
    time.sleep(20)
    click(pos['backcamp'][0], pos['backcamp'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    time.sleep(1)
    #取名
    text(name,startport)
    click(pos['name_done'][0], pos['name_done'][1], startport)
    time.sleep(10)
    #升级大本营
    click(pos['cancel'][0], pos['cancel'][1], startport)
    click(pos['base'][0], pos['base'][1], startport)
    click(pos['levelup'][0], pos['levelup'][1], startport)
    click(pos['enter'][0], pos['enter'][1], startport)
    time.sleep(15)
    #成就
    click(pos['cancel'][0], pos['cancel'][1], startport)
    click(pos['achievement'][0], pos['achievement'][1], startport)
    click(pos['achievement4'][0], pos['achievement4'][1], startport)
    for n in range(3):
        click(pos['cancel'][0], pos['cancel'][1], startport)
    click(pos['exitstore'][0], pos['exitstore'][1], startport)
    time.sleep(10)
    #重启
    restartcoc(startport)
    #造兵营
    storebuild(startport)
    click(pos['store_2'][0], pos['store_2'][1], startport)
    click(pos['built09'][0], pos['built09'][1], startport)
    # 造收集器
    time.sleep(10)
    storebuild(startport)
    click(pos['storeitem2'][0], pos['storeitem2'][1], startport)
    click(pos['store_2'][0], pos['store_2'][1], startport)
    click(pos['built10'][0], pos['built10'][1], startport)
    time.sleep(7)
    #造矿场
    storebuild(startport)
    click(pos['storeitem2'][0], pos['storeitem2'][1], startport)
    click(pos['store_2'][0], pos['store_2'][1], startport)
    click(pos['built11'][0], pos['built11'][1], startport)
    time.sleep(7)
    #造加农炮
    storebuild(startport)
    click(pos['storeitem3'][0], pos['storeitem3'][1], startport)
    click(pos['store_1'][0], pos['store_1'][1], startport)
    click(pos['built12'][0], pos['built12'][1], startport)
    time.sleep(7)
    #造弓箭
    storebuild(startport)
    click(pos['storeitem3'][0], pos['storeitem3'][1], startport)
    click(pos['store_1'][0], pos['store_1'][1], startport)
    click(pos['built13'][0], pos['built13'][1], startport)
    time.sleep(7)
    #造兵
    train('train_troop01',40,startport)
    timewait(25,startport)
    #升级矿场1,2
    levelup_mine1(startport)
    time.sleep(60)
    #升级收集器1,2
    levelup_collector1(startport)
    time.sleep(60)
    #等待造兵完成
    time.sleep(20)
    #打哥布林
    click(pos['attack'][0], pos['attack'][1], startport)
    click(pos['attack_single'][0], pos['attack_single'][1], startport)
    click(pos['goblin02'][0], pos['goblin02'][1], startport)
    time.sleep(5)
    click(pos['attack_troop01'][0], pos['attack_troop01'][1], startport)
    click_short(pos['goblin02_point1'][0], pos['goblin02_point1'][1], startport,40)
    time.sleep(30)
    click(pos['backcamp'][0], pos['backcamp'][1], startport)
    time.sleep(5)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    #造城墙
    timewait(15,startport)
    #收集一次资源确保选中不会出意外
    click(pos['mine1'][0], pos['mine1'][1], startport)
    click(pos['mine2'][0], pos['mine2'][1], startport)
    click(pos['collector1'][0], pos['collector1'][1], startport)
    click(pos['collector2'][0], pos['collector2'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)
    for n in range(2):
        swipe('top', startport)
    storebuild(startport)
    click(pos['storeitem3'][0], pos['storeitem3'][1], startport)
    click(pos['store_1'][0], pos['store_1'][1], startport)
    subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 623 349 651 274' % (startport), shell=True)
    time.sleep(1)
    for n in range(40):
        click(pos['built14'][0], pos['built14'][1], startport)
    #重启
    restartcoc(startport)
    #升级矿场
    levelup_mine(startport)
    cancel(startport)
    #造兵
    train('train_troop01', 40, startport)
    #等待矿场升级完毕
    timewait(20, startport)
    #打哥布林
    click(pos['attack'][0], pos['attack'][1], startport)
    click(pos['attack_single'][0], pos['attack_single'][1], startport)
    click(pos['goblin03'][0], pos['goblin03'][1], startport)
    time.sleep(5)
    click(pos['attack_troop01'][0], pos['attack_troop01'][1], startport)
    click_short(pos['goblin03_point'][0], pos['goblin03_point'][1], startport,40)
    time.sleep(60)
    click(pos['backcamp'][0], pos['backcamp'][1], startport)
    time.sleep(5)
    #升级收集器
    levelup_collector(startport)
    cancel(startport)
    #造兵
    train('train_troop01', 40, startport)
    #等待收集器升级完毕
    timewait(20, startport)
    #升级罐子和瓶子
    levelup_saver(startport)
    cancel(startport)
    g.msgbox(msg='初始化完成')

#升级资源
def resource(startid,endid):
    for nowid in range(startid,endid+1):
        action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %s -disable_audio  -fps 40' % (nowid)
        c().start(action, nowid,1)#最小化
        startport = getport(nowid)
        connect(startport)
        #重新登录qq
        click(pos['relogin'][0], pos['relogin'][1], startport)
        time.sleep(10)
        startcoc(startport)
        cancel(startport)
        levelup_mine(startport)
        cancel(startport)
        levelup_collector(startport)
        cancel(startport)
        levelup_saver(startport)
        cancel(startport)
        levelup_train(startport)
        #升级大本营
        click(pos['base2'][0], pos['base2'][1], startport)
        click(pos['levelup2'][0], pos['levelup2'][1], startport)
        click(pos['enter'][0], pos['enter'][1], startport)
        close()
    g.msgbox(msg='升级完成')

#部落战捐兵
def wardonate(startlist):
    for nowid in startlist:
        nowid = int(nowid)
        action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' % (nowid)
        c().start(action, nowid,1)#最小化
        startport = getport(nowid)
        connect(startport)
        #重新登录qq
        click(pos['relogin'][0], pos['relogin'][1], startport)
        time.sleep(10)
        startcoc(startport)
        cancel(startport)
        #等待1分
        timewait(1,startport)
        #夜世界切换
        #归到右上角
        swipe('top',startport)
        swipe('right',startport)
        #船
        click(pos['boat'][0], pos['boat'][1], startport, 5)
        #进入部落战界面
        click(pos['war'][0], pos['war'][1], startport)
        #部落战第一个开始捐兵
        swipe('top', startport)
        swipe('top', startport)
        click(pos['war_1'][0], pos['war_1'][1], startport)
        #点击下一个到最后一个
        click_short(pos['war_donate_next'][0], pos['war_donate_next'][1], startport,80)
        #增援按钮
        click(pos['war_donate'][0], pos['war_donate'][1], startport)
        #捐兵
        for clan in range(40):
            #time.sleep(1)
            click_short(pos['war_donate_trp2'][0], pos['war_donate_trp2'][1], startport,10)
            click_short(pos['war_donate_trp3'][0], pos['war_donate_trp3'][1], startport,10)
            click_short(pos['war_donate_trp1'][0], pos['war_donate_trp1'][1], startport,10)
            click(pos['war_donate_last'][0], pos['war_donate_last'][1], startport)
        #训练部落战兵种
        train_template('train_template01',startport)
        #关闭
        close()
    #g.msgbox(msg='部落战捐兵完成')

#启动coc
def start_coc(startidlist):
    for nowid in startidlist:
        action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' % (int(nowid))
        c().start(action, int(nowid),0)
        startport = getport(int(nowid))
        connect(startport)
        #重新登录qq
        click(pos['relogin'][0], pos['relogin'][1], startport)
        time.sleep(10)
        startcoc(startport)
        cancel(startport)
    g.msgbox(msg='启动各个部落完成')
    
#3本新建
def levelup_3(startid,endid):
    for nowid in range(startid,endid+1):
        action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %s -disable_audio  -fps 40' % (nowid)
        c().start(action, nowid,1)#最小化
        startport = getport(nowid)
        connect(startport)
        #重新登录qq
        click(pos['relogin'][0], pos['relogin'][1], startport)
        time.sleep(10)
        startcoc(startport)
        cancel(startport)
        #收集资源
        click(pos['mine1'][0], pos['mine1'][1], startport)
        click(pos['mine2'][0], pos['mine2'][1], startport)
        click(pos['collector1'][0], pos['collector1'][1], startport)
        click(pos['collector2'][0], pos['collector2'][1], startport)
        click(pos['cancel'][0], pos['cancel'][1], startport)
        #点击废墟
        for n in range(50):
            click_short(random.randint(400,900), random.randint(100,600), startport,1)
        cancel(startport)
        # 造炸弹
        storebuild(startport)
        click(pos['storeitem4'][0], pos['storeitem4'][1], startport)
        click(pos['store_1'][0], pos['store_1'][1], startport)
        click(pos['built16'][0], pos['built16'][1], startport)
        click(pos['built16'][0], pos['built16'][1], startport)
        # 造收集器
        storebuild(startport)
        click(pos['storeitem2'][0], pos['storeitem2'][1], startport)
        click(pos['store_2'][0], pos['store_2'][1], startport)
        click(pos['built17'][0], pos['built17'][1], startport)
        # 造瓶子
        storebuild(startport)
        click(pos['storeitem2'][0], pos['storeitem2'][1], startport)
        click(pos['store_2'][0], pos['store_2'][1], startport)
        click(pos['built18'][0], pos['built18'][1], startport)
        time.sleep(5)
        # 造矿场
        storebuild(startport)
        click(pos['storeitem2'][0], pos['storeitem2'][1], startport)
        click(pos['store_2'][0], pos['store_2'][1], startport)
        click(pos['built19'][0], pos['built19'][1], startport)
        # 造罐子
        storebuild(startport)
        click(pos['storeitem2'][0], pos['storeitem2'][1], startport)
        click(pos['store_2'][0], pos['store_2'][1], startport)
        time.sleep(1)
        click(pos['built20'][0], pos['built20'][1], startport)
        time.sleep(5)
        # 造兵营
        storebuild(startport)
        click(pos['storeitem1'][0], pos['storeitem1'][1], startport)
        click(pos['store_2'][0], pos['store_2'][1], startport)
        time.sleep(1)
        click(pos['built21'][0], pos['built21'][1], startport)
        # 造迫击炮
        storebuild(startport)
        click(pos['storeitem3'][0], pos['storeitem3'][1], startport)
        click(pos['store_2'][0], pos['store_2'][1], startport)
        time.sleep(1)
        click(pos['built22'][0], pos['built22'][1], startport)
        timewait(5,startport)
        # 造实验室
        storebuild(startport)
        click(pos['storeitem1'][0], pos['storeitem1'][1], startport)
        click(pos['store_2'][0], pos['store_2'][1], startport)
        time.sleep(2)
        click(pos['built23'][0], pos['built23'][1], startport)
        #退出一次
        home(startport)
        #造城墙
        for n in range(2):
            swipe('top', startport)
        storebuild(startport)
        click(pos['storeitem3'][0], pos['storeitem3'][1], startport)
        click(pos['store_1'][0], pos['store_1'][1], startport)
        subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 647 368 550 290' % (startport), shell=True)
        time.sleep(1)
        for n in range(45):
            click(pos['built24'][0], pos['built24'][1], startport)
        close()
    g.msgbox(msg='升级完成')



def on_press_s(key):#监听@键作为开始
    # 监听按键`
    global s_flag
    if str(key)=="'"+'@'+"'" and s_flag == 0:
        print('开始',s_flag)
        #s_flag信号量加一
        semaphore_flag.release()
    elif str(key)=="'"+'@'+"'" and s_flag == 1:
        print("结束",s_flag)
        s_flag = 0

def press_s():
    global s_flag
    while True:
        # 消费一个s_flag信号量
        semaphore_flag.acquire()
        # 全局变量s_flag赋值为1，阻断监控函数的介入
        s_flag = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        try:
            while s_flag==1:
                k.mouse_click()
                click_short(pos['rmtree'][0], pos['rmtree'][1], startport,1)
                click_short(pos['exitstore'][0], pos['exitstore'][1], startport,1)
                time.sleep(0.5)
        except KeyboardInterrupt:
            sys.exit()
        #全局变量s_flag赋值为0，监控函数又可以介入了
        s_flag = 0
        print('夜世界砍树')


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident , SystemExit)


#移除夜世界树木
def removeTree_night(startid):
    global flag,flag_switch
    # 分别定义a键的信号量对象
    global semaphore_flag,startport
    startport = getport(startid)
    print(int(startport),startport)
    connect(startport)
    semaphore_flag = threading.Semaphore(0)
    # 定义全局变量作为监测线程介入的开关
    global s_flag
    s_flag = 0
    # 定义全局变量作为整个程序的开关
    flag = 0
    # 运行进程
    t1 = Listener(on_press=on_press_s)
    t1.daemon = True
    t2 = threading.Thread(target=press_s, name='sendThreads')
    t2.daemon = True
    if flag == 0:
        t1.start()
        t2.start()
        flag = 1
    elif flag == 1:
        stop_thread(t1)
        stop_thread(t2)
        flag = 0

#启动黑松鼠
def start_script(startport,*args):
    connect(startport)
    # 启动黑松鼠
    subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.ais.foxsquirrel.coc/ui.activity.SplashActivity' % (startport),shell=True)
    time.sleep(10)
    #点击更新
    click(pos['sure'][0], pos['sure'][1], startport)
    time.sleep(10)
    # 点击模式设置
    click(pos['script_item3'][0], pos['script_item3'][1], startport, 3)
    click(pos['script_switch_mode'][0], pos['script_switch_mode'][1], startport, 3)
    # 滑动
    swipeport(pos['script_swipetop'][0], pos['script_swipetop'][1], pos['script_swipebot'][0],pos['script_swipebot'][1], startport)
    time.sleep(5)
    if len(args) > 0:
        if args[0] == "donate":
            click(pos['script_donate'][0], pos['script_donate'][1], startport, 3)
        elif args[0] == "play":
            click(pos['script_play'][0], pos['script_play'][1], startport, 3)
    click(pos['script_start'][0], pos['script_start'][1], startport)
    time.sleep(20)
    click(pos['login_kunlun1'][0], pos['login_kunlun1'][1], startport,3)
    click(pos['login_kunlun2'][0], pos['login_kunlun2'][1], startport,3)
    click(pos['login_kunlun'][0], pos['login_kunlun'][1], startport,3)

#切换打鱼和捐兵
def convert_mode(startlist,*args):
    #args[0]表示当前状态，args[1]表示删掉已经造好的兵种的模拟器id
    config = configparser.ConfigParser()
    for nowid in startlist:
        #读取一次配置文件
        config.read(configpath, encoding="utf-8")
        nowid = int(nowid)
        startport = getport(nowid)
        #查看是否在捐兵配置中，没有就配置为捐兵
        try:
            if len(args) > 0:
                status = args[0]
                statusnow = config.get("coc", "startid%d"%(nowid))
            else:
                status = config.get("coc", "startid%d"%(nowid))
                statusnow = config.get("coc", "startid%d"%(nowid))
        except:
            config.set("coc", "startid%d"%(nowid),"donate")
            config.write(open(configpath, "w",encoding='utf-8'))
            status = "donate"
        #转换状态并保存
        if status == statusnow:
            if status == "donate":
                print("切换状态为 play")
                status = "play"
                #启动模拟器
                action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' % (nowid)
                c().start(action, nowid)
                # 重新登录qq
                click(pos['relogin'][0], pos['relogin'][1], startport,3)
                #切换为打资源
                start_script(startport,status)
            else:
                print("切换状态为 donate")
                status = "donate"
                #启动模拟器
                action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' % (nowid)
                c().start(action, nowid)
                # 重新登录qq
                click(pos['relogin'][0], pos['relogin'][1], startport,3)
                #click(pos['script_donate'][0], pos['script_donate'][1], startport, 3)
                #启动coc
                startcoc(startport)
                #等待1分
                timewait(1,startport)
                #夜世界切换
                #归到右上角
                swipe('top',startport)
                swipe('right',startport)
                #船
                click(pos['boat'][0], pos['boat'][1], startport, 5)
                #取消训练中的兵种
                cancel_troop(startport)
                if len(args) >= 2:
                    print('开始执行删除现有兵种，需要全部删除的id为%s'%(args[1]))
                    if (str(nowid) in args[1]):
                        print('删除%d的现有兵种和药水并造兵' %(nowid))
                        # 取消训练中的药水
                        cancel_potion(startport)
                        #取消现有兵种和药水
                        cancel_army(startport)
                        # 造捐兵兵种
                        train_template('train_template02', startport)
                print('删除兵种结束')
                #造捐兵兵种
                train_template('train_template03', startport)
                #切换为捐兵
                home(startport)
                start_script(startport,status)
            #暂停几秒钟保存切换后状态
            time.sleep(5)
            close()
        else:
            status = statusnow
            close()
        #保存当前状态
        config.set("coc", "startid%d"%(nowid),status)
        config.write(open(configpath, "w",encoding='utf-8'))