import traceback
from .api import *
from nonebot import on_command, on_message
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent
from nonebot.exception import FinishedException
from nonebot.permission import SUPERUSER
from nonebot.rule import Rule

vf = on_command("vf", aliases={"虚拟朋友"}, block=True)
vfs = on_command("vfs", aliases={"虚拟管理"}, block=True, permission=SUPERUSER)
vf_trans = on_message(block=False)
vf_data_init()


@vf.handle()
async def vf_handle(bot: Bot, event: PrivateMessageEvent):
    try:
        args = event.raw_message.strip().split()
        if args[1] in ["connect", "连接"]:
            result = connect(event.user_id, args[2])
            if result[0]:
                await bot.send_private_msg(user_id=get_vf_data()[args[2]]["vf_id"],
                                           message=random.choice(start_message))
        elif args[1] in ["disconnect", "断开"]:
            result = disconnect(event.user_id)
            if result[0]:
                await bot.send_private_msg(user_id=get_vf_data()[result[2]]["vf_id"], message=random.choice(end_message))
        elif args[1] in ["list", "列出"]:
            result = list_user()
        elif args[1] in ["help", "帮助"]:
            message = "虚拟朋友插件帮助文档\n" \
                      "普通用户命令:\n" \
                      "- 虚拟朋友 连接 虚友名称\n" \
                      "- 虚拟朋友 断开\n" \
                      "- 虚拟朋友 列出\n" \
                      "超级用户命令:\n" \
                      "- 虚拟管理 转接 虚友名称 QQ\n" \
                      "- 虚拟管理 释放 虚友名称\n" \
                      "- 虚拟管理 释放 所有" \
                      "- 虚拟管理 列出\n" \
                      "可前往github查看更详细用法:https://github.com/snowyfirefly/VirtualFriends"
            result = [True, message]
        else:
            result = (False, "未知的参数:%s" % args[1])
        await vf.finish(result[1])
    except BaseException as exception:
        if type(exception) is not FinishedException:
            traceback.print_exc()
            await vf.finish("出现了一些错误, 使用vf help查询帮助, 请检查命令:%s" % exception.__repr__())


@vfs.handle()
async def vfs_handle(bot: Bot, event: PrivateMessageEvent):
    try:
        args = event.raw_message.strip().split()
        if args[1] in ["transfer", "转接"]:
            result = transfer(user_id=int(args[3]), vf_name=args[2])
        elif args[1] in ["release", "释放"]:
            result = release(vf_name=args[2])
            if result[0]:
                # 向机器人告别
                # 向用户发送通知
                if result[2] is not None:
                    user_id = result[2]
                    vf_id = result[3]
                    message2 = result[4]
                    await bot.send_private_msg(user_id=vf_id, message=random.choice(end_message))
                    await bot.send_private_msg(user_id=user_id, message=message2)
        elif args[1] in ["list", "列出"]:
            result = list_superuser()
        else:
            result = (False, "未知的参数:%s" % args[1])
        await vf.finish(result[1])
    except BaseException as exception:
        if type(exception) is not FinishedException:
            traceback.print_exc()
            await vfs.finish("出现了一些错误,请检查命令:%s" % exception.__repr__())


@vf_trans.handle()
async def vf_trans_handle(bot: Bot, event: PrivateMessageEvent):
    try:
        print(event.user_id, get_user_ids(), get_enabled_vf_ids())
        if event.user_id in get_user_ids():
            # 用户发送数据给虚拟朋友
            user_id = event.user_id
            vf_id = get_user_ids()[user_id]
            time_reset(vf_id)
            await bot.send_private_msg(user_id=vf_id, message=event.message)
        elif event.user_id in get_enabled_vf_ids():
            # 虚拟朋友发送数据给用户
            vf_id = event.user_id
            user_id = get_enabled_vf_ids()[vf_id]
            await bot.send_private_msg(user_id=user_id, message=event.message)
        else:
            # 不做处理
            pass
    except BaseException as exception:
        if type(exception) is not FinishedException:
            traceback.print_exc()
            await vfs.finish("消息转发中出现了一些错误:%s" % exception.__repr__())
