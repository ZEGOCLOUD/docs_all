The following figure shows how a user state changes in an entire call invitation process from call initiation to call termination.
![https://doc-media.zego.im/sdk-doc/Pics/in_app_chat/14243_1.jpg](//doc.oa.zego.imhttps://doc-media.zego.im/sdk-doc/Pics/in_app_chat/14243_1.jpg)
<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="40%">
    <col width="20%">
  </colgroup>
<tbody><tr>
<th>State</th>
<th>Description</th>
<th>Triggering event</th>
<th>Applicable mode</th>
</tr>
<tr>
<td>Inviting</td>
<td>Being invited.</td>
<td>The user is being invited.</td>
<td rowspan="6"><ul><li>Common mode</li><li>Advanced mode</li></ul></td>
</tr>
<tr>
<td>Accepted</td>
<td>Invitation accepted.</td>
<td><ul><li>A user initiates a call invitation.</li><li>A user accepts a call invitation.</li></ul></td>
</tr>
<tr>
<td>Rejected</td>
<td>Invitation rejected.</td>
<td>A user rejects a call invitation.</td>
</tr>
<tr>
<td>Canceled</td>
<td>Invitation canceled.</td>
<td><ul><li>A user cancels a call invitation.</li><li>The called user does not respond to the invitation. The caller gets offline and the heartbeat times out.</li></ul></td>
</tr>
<tr>
<td>Received</td>
<td>Invitation received.</td>
<td><ul><li>An online user receives a call invitation.</li><li>An offline user gets online within the specified timeout period.</li></ul></td>
</tr>
<tr>
<td>Timeout</td>
<td>Invitation times out.</td>
<td>The called user fails to respond to the invitation within the specified timeout period.</td>
</tr>
<tr>
<td>Quit</td>
<td>Quit the call.</td>
<td>A user in the call quit the call.</td>
<td><ul><li>Advanced mode</li></ul></td>
</tr>
<tr>
<td>Unknown</td>
<td>Unknown</td>
<td colspan="2">Contact ZEGOCLOUD technical support.</td>
</tr>
</tbody></table>








