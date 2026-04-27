"use client";

import { useEffect, useState, useMemo } from "react";

const defaultTextPool = [
  "您好，这里是 ZEGO 数字人演示。",
  "服务器将定时推送不同的文本给数字人。",
  "您的客户端只需拉流并播放数字人音视频内容。",
  "请保持网络畅通以获得最佳观看体验。"
].join("\n");

function ConfigPage() {
  const [digitalHumans, setDigitalHumans] = useState([]);
  const [digitalHumanId, setDigitalHumanId] = useState("");
  const [selectedTimbreId, setSelectedTimbreId] = useState("");
  const [roomId, setRoomId] = useState("room_digital_human");
  const [streamId, setStreamId] = useState("stream_digital_human");
  const [textPool, setTextPool] = useState(defaultTextPool);
  const [publicTimbres, setPublicTimbres] = useState([]);
  const [privateTimbres, setPrivateTimbres] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingPublicTimbres, setLoadingPublicTimbres] = useState(false);
  const [loadingDigitalHumans, setLoadingDigitalHumans] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [starting, setStarting] = useState(false);
  const [stopping, setStopping] = useState(false);
  const [error, setError] = useState(null);
  const [broadcastIndex, setBroadcastIndex] = useState(0);
  const [digitalHumanError, setDigitalHumanError] = useState(null);
  const [statusInfo, setStatusInfo] = useState(null);
  const [outputMode, setOutputMode] = useState(1);  // 1=Web模式, 2=Mobile模式

  const allTimbres = useMemo(() => {
    const timbreMap = new Map();
    publicTimbres.forEach((timbre) => {
      timbreMap.set(timbre.TimbreId, timbre);
    });
    privateTimbres.forEach((timbre) => {
      timbreMap.set(timbre.TimbreId, timbre);
    });
    return Array.from(timbreMap.values());
  }, [publicTimbres, privateTimbres]);

  const textList = useMemo(() => {
    return textPool
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0);
  }, [textPool]);

  const canStart = digitalHumanId && selectedTimbreId && roomId.trim() && streamId.trim() && textList.length > 0;

  const fetchStatus = async () => {
    try {
      const response = await fetch("/api/broadcast");
      const data = await response.json();
      const broadcasts = data.broadcastList || {};
      const broadcastKeys = Object.keys(broadcasts);

      if (broadcastKeys.length > 0) {
        const firstIndex = Number(broadcastKeys[0]);
        setIsRunning(true);
        setStatusInfo({
          running: true,
          roomId: broadcasts[firstIndex].roomId,
          streamId: broadcasts[firstIndex].streamId,
          userId: null,
          broadcastIndex: firstIndex,
        });
        setBroadcastIndex(firstIndex);
      } else {
        setIsRunning(false);
        setStatusInfo(null);
      }
    } catch (err) {
      console.error("获取状态失败:", err);
    }
  };

  const fetchDigitalHumanList = async () => {
    setLoadingDigitalHumans(true);
    setDigitalHumanError(null);

    try {
      const params = new URLSearchParams({
        fetchMode: "1",
        offset: "0",
        limit: "20",
      });
      const response = await fetch(`/api/digital-humans?${params.toString()}`);
      const data = await response.json();

      if (data.error) {
        setDigitalHumanError(data.error);
        setDigitalHumans([]);
      } else {
        setDigitalHumans(data.DigitalHumans);
      }
    } catch (err) {
      setDigitalHumanError(err instanceof Error ? err.message : "获取数字人列表失败 / Failed to fetch digital human list");
      setDigitalHumans([]);
    } finally {
      setLoadingDigitalHumans(false);
    }
  };

  const fetchPublicTimbres = async () => {
    setLoadingPublicTimbres(true);
    try {
      const params = new URLSearchParams({
        offset: "0",
        limit: "20",
      });
      const url = `/api/timbres?${params.toString()}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`);
      }

      const data = await response.json();

      if (data.error) {
        console.error("获取公共音色失败:", data.error);
        setPublicTimbres([]);
      } else if (data && typeof data === "object" && "Timbres" in data) {
        setPublicTimbres(data.Timbres || []);
      } else {
        setPublicTimbres([]);
      }
    } catch (err) {
      console.error("获取公共音色异常:", err);
      setPublicTimbres([]);
    } finally {
      setLoadingPublicTimbres(false);
    }
  };

  const fetchPrivateTimbres = async (dhId) => {
    if (!dhId.trim()) {
      setPrivateTimbres([]);
      setError(null);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        digitalHumanId: dhId.trim(),
        offset: "0",
        limit: "20",
      });
      const url = `/api/timbres?${params.toString()}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`);
      }

      const data = await response.json();

      if (data.error) {
        setError(data.error);
        setPrivateTimbres([]);
      } else if (data && typeof data === "object" && "Timbres" in data) {
        setPrivateTimbres(data.Timbres || []);
      } else {
        setError("响应数据格式错误");
        setPrivateTimbres([]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "获取私有音色失败");
      setPrivateTimbres([]);
    } finally {
      setLoading(false);
    }
  };

  const handleStart = async () => {

    setStarting(true);
    setError(null);

    try {
      const response = await fetch("/api/broadcast", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          broadcastIndex,
          digitalHumanId,
          timbreId: selectedTimbreId,
          roomId: roomId.trim(),
          streamId: streamId.trim(),
          textPool: textList,
          outputMode,
        }),
      });

      const data = await response.json();

      if (!data.success) {
        setError(data.error || "启动失败 / Start failed");
      } else {
        setIsRunning(true);
        setStatusInfo({
          running: true,
          roomId: roomId.trim(),
          streamId: streamId.trim(),
          userId: null,
          broadcastIndex,
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "启动失败 / Start failed");
    } finally {
      setStarting(false);
    }
  };

  const handleStop = async () => {
    setStopping(true);
    setError(null);

    try {
      const indexToStop = statusInfo?.broadcastIndex ?? broadcastIndex;
      const response = await fetch(`/api/broadcast?index=${indexToStop}`, {
        method: "DELETE",
      });

      const data = await response.json();

      if (!data.success) {
        setError(data.error || "停止失败 / Stop failed");
      } else {
        setIsRunning(false);
        setStatusInfo(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "停止失败 / Stop failed");
    } finally {
      setStopping(false);
    }
  };

  useEffect(() => {
    fetchDigitalHumanList();
    fetchStatus();
    fetchPublicTimbres();
  }, []);

  useEffect(() => {
    if (!isRunning) {
      const timer = setTimeout(() => {
        fetchPrivateTimbres(digitalHumanId);
      }, 500);

      return () => clearTimeout(timer);
    } else {
      setPrivateTimbres([]);
      setSelectedTimbreId("");
    }
  }, [digitalHumanId, isRunning]);

  useEffect(() => {
    if (selectedTimbreId && allTimbres.length > 0) {
      const exists = allTimbres.some((t) => t.TimbreId === selectedTimbreId);
      if (!exists) {
        setSelectedTimbreId("");
      }
    }
  }, [allTimbres, selectedTimbreId]);

  const isDisabled = isRunning;

  return (
    <div className="space-y-4">
      <section className="bg-white border border-gray-200 rounded-lg p-4">
        <h1 className="text-lg font-medium">
          数字人播报配置 / Digital Human Broadcast Configuration
        </h1>
        <p className="text-sm text-gray-500">
          {isRunning
            ? "播报任务运行中，请先停止任务才能修改配置 / Broadcast task is running, please stop the task first to modify configuration"
            : "请先选择数字人和音色，然后启动播报任务 / Please select a digital human and timbre first, then start the broadcast task"}
        </p>

        {isRunning && statusInfo && (
          <div className="mt-4 p-3 bg-green-50 border border-green-300 rounded text-sm">
            <div className="font-medium text-green-700 mb-2">
              运行状态 / Running Status
            </div>
            <div className="text-green-600 text-xs space-y-1">
              <div>房间ID / Room ID: {statusInfo.roomId}</div>
              <div>流ID / Stream ID: {statusInfo.streamId}</div>
              <div>播报索引 / Broadcast Index: {statusInfo.broadcastIndex ?? broadcastIndex}</div>
            </div>
          </div>
        )}

        <div className="mt-4">
          <label className="block text-sm font-medium mb-2">
            1. 选择数字人 / Select Digital Human
          </label>
          {loadingDigitalHumans ? (
            <p className="text-sm text-gray-400">
              加载数字人列表中... / Loading digital human list...
            </p>
          ) : digitalHumanError ? (
            <div className="p-3 bg-red-50 border border-red-300 rounded text-sm text-red-600">
              {digitalHumanError}
            </div>
          ) : (
            <div className="grid grid-cols-fill-minmax gap-3" style={{gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))"}}>
              {digitalHumans.map((dh) => (
                  <label
                    key={dh.DigitalHumanId}
                    className={`border rounded p-3 cursor-pointer ${digitalHumanId === dh.DigitalHumanId ? "border-2 border-blue-500 bg-blue-50" : "border border-gray-200 bg-gray-50"} ${isDisabled ? "opacity-50 pointer-events-none" : ""}`}
                  >
                    <input
                      type="radio"
                      name="digital-human"
                      value={dh.DigitalHumanId}
                      checked={digitalHumanId === dh.DigitalHumanId}
                      onChange={(e) => e.target.checked && setDigitalHumanId(dh.DigitalHumanId)}
                      disabled={isDisabled}
                      className="hidden"
                    />
                    {dh.AvatarUrl && (
                      <img
                        src={dh.AvatarUrl}
                        alt={dh.Name}
                        className="w-full aspect-square object-cover rounded mb-2"
                      />
                    )}
                    <div className="text-xs text-gray-500 break-all mb-1">
                      ID: {dh.DigitalHumanId}
                    </div>
                    <div className="text-sm font-medium flex items-center justify-between">
                      <span>{dh.Name}</span>
                      <span className={`text-xs px-1.5 py-0.5 rounded ${dh.IsPublic ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"}`}>
                        {dh.IsPublic ? "公有 / Public" : "私有 / Private"}
                      </span>
                    </div>
                  </label>
                ))}
            </div>
          )}
        </div>

        {(loading || loadingPublicTimbres) && (
          <p className="mt-4 text-sm text-gray-400">
            加载音色中... / Loading timbres...
          </p>
        )}

        {error && !isRunning && (
          <div className="mt-4 p-3 bg-orange-50 border border-orange-300 rounded text-sm text-orange-600">
            {error}
          </div>
        )}

        {!loading && !loadingPublicTimbres && allTimbres.length > 0 && (
          <div className="mt-6">
            <label className="block text-sm font-medium mb-3">
              2. 选择音色 / Select Timbre
              <span className="text-xs text-gray-500 ml-2">
                (共 {allTimbres.length} 个 / Total: {allTimbres.length})
              </span>
            </label>
            <div className="grid grid-cols-fill-minmax gap-3" style={{gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))"}}>
              {allTimbres.map((timbre) => {
                const isPublic = publicTimbres.some((t) => t.TimbreId === timbre.TimbreId);
                const isPrivate = privateTimbres.some((t) => t.TimbreId === timbre.TimbreId);
                return (
                  <label
                    key={timbre.TimbreId}
                    className={`border rounded p-3 cursor-pointer ${selectedTimbreId === timbre.TimbreId ? "border-2 border-blue-500 bg-blue-50" : "border border-gray-200 bg-gray-50"} ${isDisabled ? "opacity-50 pointer-events-none" : ""}`}
                  >
                    <input
                      type="radio"
                      name="timbre"
                      value={timbre.TimbreId}
                      checked={selectedTimbreId === timbre.TimbreId}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedTimbreId(timbre.TimbreId);
                          setError(null);
                        }
                      }}
                      disabled={isDisabled}
                      className="hidden"
                    />
                    <div className="text-xs text-gray-500 break-all mb-1">
                      ID: {timbre.TimbreId}
                    </div>
                    <div className="text-sm font-medium flex items-center justify-between">
                      <span>{timbre.Name}</span>
                      {isPublic && isPrivate && (
                        <span className="text-xs px-1.5 py-0.5 rounded bg-blue-100 text-blue-700">
                          公共+私有 / Public+Private
                        </span>
                      )}
                      {isPublic && !isPrivate && (
                        <span className="text-xs px-1.5 py-0.5 rounded bg-green-100 text-green-700">
                          公有 / Public
                        </span>
                      )}
                      {!isPublic && isPrivate && (
                        <span className="text-xs px-1.5 py-0.5 rounded bg-yellow-100 text-yellow-700">
                          私有 / Private
                        </span>
                      )}
                    </div>
                  </label>
                );
              })}
            </div>
          </div>
        )}

        {!loading && !loadingPublicTimbres && allTimbres.length === 0 && (
          <p className="mt-4 text-sm text-gray-400">
            未找到音色 / No timbres found
          </p>
        )}

        <div className="mt-6">
          <label className="block text-sm font-medium mb-2">
            3. 配置房间和流信息 / Configure Room and Stream Info
          </label>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label htmlFor="room-id" className="block text-xs text-gray-500 mb-1">
                实时音视频(RTC)房间ID
              </label>
              <label htmlFor="room-id" className="block text-xs text-gray-500 mb-1">
                Video Call(RTC) Room ID
              </label>
              <input
                id="room-id"
                type="text"
                value={roomId}
                onChange={(e) => setRoomId(e.target.value)}
                placeholder="room_digital_human"
                disabled={isDisabled}
                className={`w-full px-3 py-2 text-sm border border-gray-300 rounded ${isDisabled ? "bg-gray-100 opacity-50" : ""}`}
              />
            </div>
            <div>
              <label htmlFor="stream-id" className="block text-xs text-gray-500 mb-1">
                RTC 流ID。客户端根据该流ID拉流播放数字人音视频
              </label>
              <label htmlFor="stream-id" className="block text-xs text-gray-500 mb-1">
                Client plays the digital human audio and video with this stream ID
              </label>
              <input
                id="stream-id"
                type="text"
                value={streamId}
                onChange={(e) => setStreamId(e.target.value)}
                placeholder="stream_digital_human"
                disabled={isDisabled}
                className={`w-full px-3 py-2 text-sm border border-gray-300 rounded ${isDisabled ? "bg-gray-100 opacity-50" : ""}`}
              />
            </div>
          </div>
        </div>

        <div className="mt-6">
          <label className="block text-sm font-medium mb-2">
            4. 选择输出模式 / Select Output Mode
          </label>
          <div className="flex gap-4">
            <label className={`flex items-center px-4 py-2 border rounded cursor-pointer ${outputMode === 1 ? "border-2 border-blue-500 bg-blue-50" : "border border-gray-200 bg-gray-50"} ${isDisabled ? "opacity-50 pointer-events-none" : ""}`}>
              <input
                type="radio"
                name="output-mode"
                value="1"
                checked={outputMode === 1}
                onChange={() => setOutputMode(1)}
                disabled={isDisabled}
                className="mr-2"
              />
              <div>
                <div className="text-sm font-medium">Web 模式 / Web Mode</div>
                <div className="text-xs text-gray-500">适用于 Web 端 / For Web clients</div>
              </div>
            </label>
            <label className={`flex items-center px-4 py-2 border rounded cursor-pointer ${outputMode === 2 ? "border-2 border-blue-500 bg-blue-50" : "border border-gray-200 bg-gray-50"} ${isDisabled ? "opacity-50 pointer-events-none" : ""}`}>
              <input
                type="radio"
                name="output-mode"
                value="2"
                checked={outputMode === 2}
                onChange={() => setOutputMode(2)}
                disabled={isDisabled}
                className="mr-2"
              />
              <div>
                <div className="text-sm font-medium">Mobile 模式 / Mobile Mode</div>
                <div className="text-xs text-gray-500">适用于 Android/iOS 客户端 / For Android/iOS clients</div>
              </div>
            </label>
          </div>
        </div>

        <div className="mt-6">
          <label htmlFor="text-pool" className="block text-sm font-medium mb-2">
            5. 配置播报内容列表 / Configure Broadcast Content List
          </label>
          <textarea
            id="text-pool"
            value={textPool}
            onChange={(e) => setTextPool(e.target.value)}
            placeholder={`请输入播报内容，每行一条 / Enter broadcast content, one per line`}
            disabled={isDisabled}
            rows={6}
            className={`w-full px-3 py-2 text-sm border border-gray-300 rounded resize-y ${isDisabled ? "bg-gray-100 opacity-50" : ""}`}
          />
          <p className="mt-1 text-xs text-gray-400">
            系统会随机从这些内容中选择一条进行播报 / System will randomly select one content for broadcast
          </p>
        </div>

        <div className="mt-6 flex gap-3">
          <button
            onClick={handleStart}
            disabled={isRunning || starting || !canStart}
            className={`px-5 py-2.5 text-sm font-medium text-white rounded ${isRunning || starting || !canStart ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"}`}
          >
            {starting ? "启动中... / Starting..." : "6. 启动播报任务 / Start Broadcast Task"}
          </button>
          <button
            onClick={handleStop}
            disabled={!isRunning || stopping}
            className={`px-5 py-2.5 text-sm font-medium text-white rounded ${!isRunning || stopping ? "bg-gray-400 cursor-not-allowed" : "bg-red-500 hover:bg-red-600"}`}
          >
            {stopping ? "停止中... / Stopping..." : "停止播报任务 / Stop Broadcast Task"}
          </button>
        </div>
      </section>
    </div>
  );
}

export default ConfigPage;
