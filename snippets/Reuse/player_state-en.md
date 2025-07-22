

![https://doc-media.zego.im/sdk-doc/Pics/zegocloud/mini_game/4Game_status_description.jpg](//doc.oa.zego.imhttps://doc-media.zego.im/sdk-doc/Pics/zegocloud/mini_game/4Game_status_description.jpg)

<table>
  <colgroup>
    <col width="25%">
    <col width="15%">
    <col width="30%">
    <col width="30%">
  </colgroup>
<tbody><tr>
<th>Status</th>
<th>Description</th>
<th>Event to trigger</th>
<th>Common business scenario</th>
</tr>
<tr>
<td>`ZegoPlayerStartPlay`</td>
<td>The player starts to play a game.</td>
<td>- The player calls the [loadGame](@loadGame) operation to load a game in the mode of half- or full-screen gaming with randomly matched players, and joins in the game. - The host calls the [startGame](@startGame) operation to start a game in the mode of host-joined gaming with specified players.</td>
<td>Check whether the player can switch between pages. This prevents unexpected game pauses caused by accidental touches on the UI during gaming.<ul><li>If the status of the player is `ZegoPlayerStartPlay` and the SDK does not obtain the `ZegoPlayerStopPlay` status, the player cannot switch between pages.</li></ul></td>
</tr>
<tr>
<td>`ZegoPlayerStopPlay`</td>
<td>The player stops playing a game.</td>
<td>The game ends normally.</td>
<td>Calculate the total gaming period of the player.<ul><li>Calculate the time difference between the `ZegoPlayerStartPlay` status and the `ZegoPlayerStopPlay` status of multiple games and add up the values. The final value is the total gaming period of the player.</li></ul></td>
</tr>
</tbody></table>

<div class="mk-warning">

After a user calls the [loadGame](@loadGame) operation and views a game as a participant rather than a player, no player status is returned.

</div>






