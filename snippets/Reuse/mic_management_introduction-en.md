## 麦位管理

在语聊房内进行麦位管理，能够确保用户根据自身 [角色](!Solution_Implementation#5_1) 有序展开活动。本解决方案是通过调用 [ZIM SDK 接口](!Solution_Implementation#5_2) 实现麦位管理，主要包括 [发起连麦](!Solution_Implementation#5_3)、[结束连麦](!Solution_Implementation#5_4) 以及 [麦位列表同步](!Solution_Implementation#5_5)。

### 角色介绍

语聊房内不同角色的行为如下表所示：

<table>
  <colgroup>
    <col width="20%">
    <col width="80%">
  </colgroup>
<tbody><tr>
<th>角色</th>
<th>行为</th>
</tr>
<tr>
<td>主播</td>
<td>负责语聊房房间的创建和销毁。主播在创建房间后自动上麦，且无法下麦。本方案的麦位更新逻辑对主播有强依赖，因此，只有主播在良好的网络环境下，玩家才能有相对良好的游戏体验。</td>
</tr>
<tr>
<td>麦下观众</td>
<td>所有用户（除主播）在刚进入房间均为此角色。麦下观众只能听麦上玩家的语音聊天，不能参与，如需加入聊天需要上麦。</td>
</tr>
<tr>
<td>麦上玩家</td>
<td>当麦下观众向主播申请上麦，或被主播邀请上麦且同意后，即成为麦上玩家。麦上玩家可互相进行语音聊天。</td>
</tr>
</tbody></table>

### 相关接口

ZIM SDK 提供了一组现成的 [呼叫邀请](!IM-Call_Invitation) 功能接口，包括：   
1. 发起呼叫邀请；
2. 取消呼叫邀请；
3. 接受呼叫邀请；
4. 拒绝呼叫邀；
5. 超时未响应呼叫邀请。

以上接口的示例代码与使用须知，请参考 [呼叫邀请](!IM-Call_Invitation)。下文展示在语聊房中该组接口的使用情况。
