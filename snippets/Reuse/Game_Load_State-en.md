![https://doc-media.zego.im/sdk-doc/Pics/zegocloud/mini_game/Game_status.jpg](//doc.oa.zego.imhttps://doc-media.zego.im/sdk-doc/Pics/zegocloud/mini_game/Game_status.jpg)

The loading status of a game transits based on the loading progress of game resources. The following table describes the definitions, trigger events, and common business scenarios of different loading statuses.

<table>
  <colgroup>
    <col width="20%">
    <col width="15%">
    <col width="30%">
    <col width="">
  </colgroup>
<tbody><tr>
<th>Status</th>
<th>Description</th>
<th>Event to trigger</th>
<th>Common business scenario</th>
</tr>
<tr>
<td>`ZegoGameLoading`</td>
<td>The game is loading.</td>
<td>After you call the [loadGame](@loadGame) operation, the system starts to download game resources and load the game.</td>
<td>Obtain the first loading duration of the game.<ul><li>To obtain the first loading duration of the game, you can calculate the time difference between the time point when the [loadGame](@loadGame) operation is called for the first time and the time point when you are notified of the `ZegoGameLoading` status.</li></ul></td>
</tr>
<tr>
<td>`ZegoGameLoaded`</td>
<td>The game loading is complete.</td>
<td>The game loading is complete.</td>
<td>Obtain the loading duration of the game.<ul><li>If the game is loaded not for the first time, you can obtain the loading duration of the game by calculating the time difference between the time point when the [loadGame](@loadGame) operation is called and the time point when you are notified of the `ZegoGameLoaded` status.</li></ul></td>
</tr>
</tbody></table>




