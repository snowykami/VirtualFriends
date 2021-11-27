import json
import os
import random
import threading
import time

plugin_path = os.path.dirname(os.path.realpath(__file__))

waiting_time = 10

start_message = ["在吗", "我来了"]
end_message = ["拜拜", "我先下线了", "我有点事先走了"]


def timer(vf_name):
    while True:
        vf_data = get_vf_data()
        if vf_data[vf_name]["remain_time"] >= 1:
            vf_data[vf_name]["remain_time"] -= 1
            set_vf_data(vf_data)
            time.sleep(60)
        else:
            vf_data[vf_name]["user"] = None
            vf_data[vf_name]["remain_time"] = None
            set_vf_data(vf_data)
            break


def time_reset(vf_id):
    vf_data = get_vf_data()
    for vf in vf_data.items():
        if vf[1]["vf_id"] == vf_id:
            vf_data[vf[0]]["remain_time"] = waiting_time
    set_vf_data(vf_data)


def vf_data_init():
    vf_data = get_vf_data()
    for vf in vf_data.items():
        vf_data[vf[0]]["user"] = None
        vf_data[vf[0]]["remain_time"] = None
    set_vf_data(vf_data)


def get_vf_data() -> dict:
    with open(os.path.join(plugin_path, "resource/vf_data.json"), "r", encoding="utf-8-sig") as file:
        data = json.load(file)
    return data


def set_vf_data(data: dict):
    with open(os.path.join(plugin_path, "resource/vf_data.json"), "w", encoding="utf-8-sig") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return True


def connect(user_id: int, vf_name: str, remain_time: int = waiting_time):
    result = False
    message = None
    vf_data = get_vf_data()
    if vf_name in vf_data:
        # 虚拟朋友存在
        if vf_data[vf_name]["user"] is None:
            # 虚拟朋友未占用
            vf_data[vf_name]["user"] = user_id
            vf_data[vf_name]["remain_time"] = remain_time
            set_vf_data(vf_data)
            result = True
            message = "已连接到%s, 若%s分钟你没有发送新的消息, 系统将自动断开" % (vf_name, remain_time)
            thread = threading.Thread(target=timer, args=(vf_name,))
            thread.start()
        else:
            if vf_data[vf_name]["user"] == user_id:
                message = "你已连接到%s, 无需再次连接" % vf_name
            else:
                message = "%s正在进行其他会话, 请稍等或换一个虚拟朋友吧" % vf_name
    else:
        message = "%s不存在, 请换一个虚拟朋友试试吧" % vf_name
    return result, message


def disconnect(user_id: int):
    result = False
    message = None
    vf_data = get_vf_data()
    for vf in vf_data.items():
        if vf[1]["user"] == user_id:
            result = True
            vf_name = vf[0]
            vf_data[vf[0]]["user"] = None
            vf_data[vf[0]]["remain_time"] = None
            set_vf_data(vf_data)
            message = "已从%s断开连接" % vf[0]
            break
    else:
        vf_name = None
        message = "你当前未连接到任何虚拟朋友"
    return result, message, vf_name


def transfer(user_id: int, vf_name: str, remain_time: int = waiting_time):
    result = False
    message = None
    vf_data = get_vf_data()
    if vf_name in vf_data:
        # 虚拟朋友存在
        if vf_data[vf_name]["user"] is None:
            # 虚拟朋友未占用
            vf_data[vf_name]["user"] = user_id
            vf_data[vf_name]["remain_time"] = remain_time
            set_vf_data(vf_data)
            result = True
            message = "已将%s连接到%s, 若%s分钟目标用户没有发送新的消息, 系统将自动断开" % (user_id, vf_name, remain_time)
            thread = threading.Thread(target=timer, args=(vf_name,))
            thread.start()
        else:
            if vf_data[vf_name]["user"] == user_id:
                message = "%s连接到%s, 无需再次连接" % (user_id, vf_name)
            else:
                message = "%s正在进行其他会话, 请稍等或换一个虚拟朋友吧" % vf_name
    else:
        message = "%s不存在, 请换一个虚拟朋友试试吧" % vf_name
    return result, message


def release(vf_name):
    result = False
    message = None
    vf_data = get_vf_data()
    if vf_name in ["all", "所有"]:
        for vf in vf_data.items():
            if vf[1]["user"] is not None:
                vf_data[vf[0]]["user"] = None
                vf_data[vf[0]]["remain_time"] = None
        set_vf_data(vf_data)
        return True, "已将全部虚拟朋友断开", None
    else:
        for vf in vf_data.items():
            if vf[0] == vf_name:
                result = True
                user_id = vf_data[vf[0]]["user"]
                vf_id = vf[1]["vf_id"]
                vf_data[vf[0]]["user"] = None
                vf_data[vf[0]]["remain_time"] = None
                set_vf_data(vf_data)
                message = "已将%s从%s断开" % (vf[0], user_id)
                message2 = "管理员已将你和%s强制断开" % vf_name
                break
        else:
            message = "%s不存在" % vf_name
            message2 = None
            user_id = None
            vf_id = None

        return result, message, user_id, vf_id, message2


def list_superuser():
    message = "虚拟朋友情况-管理员:\n"
    vf_data = get_vf_data()
    for vf in vf_data.items():
        if vf[1]["user"] is None:
            state = "未占用"
            remain_time = 0
            user = "无"
        else:
            state = "已占用"
            remain_time = vf[1]["remain_time"]
            user = vf[1]["user"]
        message += "\n- %s:\n" \
                   "   - 虚拟id: %s\n" \
                   "   - 占用情况: %s\n" \
                   "   - 占用用户: %s\n" \
                   "   - 剩余时间: %s 分钟\n" % (vf[0], vf[1]["vf_id"], state, user, remain_time)

    return True, message[:-1]


def list_user():
    message = "虚拟朋友情况:\n"
    vf_data = get_vf_data()
    for vf in vf_data.items():
        if vf[1]["user"] is None:
            state = "未占用"
            remain_time = 0
        else:
            state = "已占用"
            remain_time = vf[1]["remain_time"]
        message += "\n- %s:\n" \
                   "   - 虚拟id: %s\n" \
                   "   - 占用情况: %s\n" \
                   "   - 剩余时间: %s 分钟\n" % (vf[0], vf[1]["vf_id"], state, remain_time)

    return True, message[:-1]


def get_vf_ids() -> dict:
    """
    获取虚拟朋友id列表, 用于消息转发判定
    """
    vf_ids = {}
    vf_data = get_vf_data()
    for vf in vf_data.items():
        vf_ids[vf[1]["vf_id"]] = vf[1]["user"]
    return vf_ids


def get_enabled_vf_ids() -> dict:
    """
    获取在线的虚拟朋友id列表, 用于消息转发判定
    """
    vf_ids = {}
    vf_data = get_vf_data()
    for vf in vf_data.items():
        if vf[1]["user"] is not None:
            vf_ids[vf[1]["vf_id"]] = vf[1]["user"]
    return vf_ids


def get_user_ids() -> dict:
    """
    获取使用中用户的id列表, 用于消息转发判定
    """
    user_ids = {}
    vf_data = get_vf_data()
    for vf in vf_data.items():
        if vf[1]["user"] is not None:
            user_ids[vf[1]["user"]] = vf[1]["vf_id"]
    return user_ids
