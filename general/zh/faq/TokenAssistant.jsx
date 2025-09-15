import React, { useMemo, useState } from 'react';

// ZEGO Token 助手（纯前端，不发起任何网络请求）
// - 生成：等价于服务端 GenerateToken04 的 AES/CBC/PKCS5Padding 实现（打包: expire + iv + cipher）
// - 校验：按 Go 版本 token_decode.go 的逻辑解包 + 解密（支持 CBC 与 GCM）+ 字段名与类型检查
// props: { defaultTab?: 'generate' | 'verify', language?: 'zh' | 'en' }
const TokenAssistant = ({ defaultTab = 'generate', language = 'zh' } = {}) => {
  // 顶部通用参数
  const [serverSecret, setServerSecret] = useState('');
  const [appId, setAppId] = useState('');
  const [activeTab, setActiveTab] = useState(defaultTab);

  // 生成 tab
  const [userId, setUserId] = useState('');
  const [effective, setEffective] = useState('3600');
  const payloadExample = useMemo(() => (
    JSON.stringify({
      room_id: 'room1',
      privilege: { 1: 1, 2: 0 },
      stream_id_list: null
    }, null, 2)
  ), []);
  const [payload, setPayload] = useState('');
  const [token, setToken] = useState('');

  // 校验 tab
  const [inputToken, setInputToken] = useState('');
  const [verifyResult, setVerifyResult] = useState(null); // { ok, version, mode, plainJson, errors[], expired }

  const [copyFeedback, setCopyFeedback] = useState('');
  const enc = useMemo(() => new TextEncoder(), []);
  const dec = useMemo(() => new TextDecoder(), []);

  // 国际化文案
  const t = useMemo(() => {
    const texts = {
      zh: {
        title: 'ZEGO Token 助手',
        warning: '本工具在浏览器本地计算，不会向服务端发送数据。请勿在生产环境泄露 ServerSecret，仅用于调试验证。',
        serverSecret: 'ServerSecret',
        serverSecretPlaceholder: '从 ZEGO 控制台获取的 ServerSecret（32 字节）',
        appId: 'AppID',
        appIdPlaceholder: '从 ZEGO 控制台获取的 AppID（数字）',
        tabGenerate: '生成临时 Token',
        tabVerify: 'Token 校验',
        userId: 'UserID',
        userIdPlaceholder: '请输入 UserID',
        effective: '有效期（秒）',
        effectivePlaceholder: '默认 3600',
        payload: 'Payload（可选，JSON 字符串）',
        fillExample: '填入示例',
        copy: '复制',
        token: 'Token',
        tokenPlaceholder: '点击下方按钮生成',
        generateBtn: '生成 Token',
        tokenInputPlaceholder: '粘贴以 04 开头的 Token',
        verifyBtn: '开始校验',
        copied: '已复制',
        // 错误提示
        errorServerSecret: '请输入 ServerSecret',
        errorServerSecretLength: 'ServerSecret 必须为 32 字节字符串',
        errorAppId: '请输入数字 AppID',
        errorUserId: '请输入 UserID',
        errorEffective: '有效期需为正整数',
        errorToken: '请输入 Token',
        generateFailed: '生成失败：',
        // 校验结果
        verifyResult: '校验结果：',
        parseSuccess: '解析成功',
        parseFailed: '解析失败',
        failReason: '失败原因：',
        detailReason: '详细原因：',
        version: '版本：',
        mode: '加密模式：',
        expired: '是否过期：',
        yes: '是',
        no: '否',
        parsedFields: '解析参数：',
        plainJson: '明文 JSON：',
        fieldCheck: '字段检查：',
        pass: '通过',
        decryptFailed: '(解密失败)'
      },
      en: {
        title: 'ZEGO Token Assistant',
        warning: 'This tool runs locally in browser and does not send data to server. Do not expose ServerSecret in production, use for debugging only.',
        serverSecret: 'ServerSecret',
        serverSecretPlaceholder: '32-byte ServerSecret from ZEGO Console',
        appId: 'AppID',
        appIdPlaceholder: 'Numeric AppID from ZEGO Console',
        tabGenerate: 'Generate temporary Token',
        tabVerify: 'Verify Token',
        userId: 'UserID',
        userIdPlaceholder: 'Enter UserID',
        effective: 'Effective (seconds)',
        effectivePlaceholder: 'Default 3600',
        payload: 'Payload (optional, JSON string)',
        fillExample: 'Fill Example',
        copy: 'Copy',
        token: 'Token',
        tokenPlaceholder: 'Click button below to generate',
        generateBtn: 'Generate Token',
        tokenInputPlaceholder: 'Paste Token starting with 04',
        verifyBtn: 'Start Verification',
        copied: 'Copied',
        // 错误提示
        errorServerSecret: 'Please input ServerSecret',
        errorServerSecretLength: 'ServerSecret must be 32-byte string',
        errorAppId: 'Please input numeric AppID',
        errorUserId: 'Please input UserID',
        errorEffective: 'Effective time must be positive integer',
        errorToken: 'Please input Token',
        generateFailed: 'Generate failed: ',
        // 校验结果
        verifyResult: 'Validation result: ',
        parseSuccess: 'Parsed successfully',
        parseFailed: 'Parse failed',
        failReason: 'Reason: ',
        detailReason: 'Details: ',
        version: 'Version: ',
        mode: 'Mode: ',
        expired: 'Expired: ',
        yes: 'Yes',
        no: 'No',
        parsedFields: 'Parsed fields: ',
        plainJson: 'Plain JSON: ',
        fieldCheck: 'Field checks: ',
        pass: 'PASS',
        decryptFailed: '(decrypt failed)'
      }
    };
    return texts[language] || texts.zh;
  }, [language]);

  // 小工具：复制
  const copyToClipboard = (text, fieldName = t.copy) => {
    if (!text) return;
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(() => {
        setCopyFeedback(`${fieldName} ${t.copied}`);
        setTimeout(() => setCopyFeedback(''), 2000);
      }).catch(() => fallbackCopy(text, fieldName));
    } else {
      fallbackCopy(text, fieldName);
    }
  };
  const fallbackCopy = (text, fieldName) => {
    const ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.left = '-9999px';
    document.body.appendChild(ta); ta.focus(); ta.select();
    try { document.execCommand('copy'); setCopyFeedback(`${fieldName} ${t.copied}`); } catch {}
    setTimeout(() => setCopyFeedback(''), 2000);
    document.body.removeChild(ta);
  };

  // 随机数/IV
  const rndInt = (a, b) => Math.ceil((a + (b - a)) * Math.random());
  const makeNonce = () => rndInt(-2147483648, 2147483647);
  const makeRandomIv = () => {
    const chars = '0123456789abcdefghijklmnopqrstuvwxyz';
    let out = '';
    for (let i = 0; i < 16; i++) out += chars[Math.floor(Math.random() * chars.length)];
    return enc.encode(out); // Uint8Array(16)
  };

  // BE 写入工具
  const writeUint16BE = (v) => { const b = new Uint8Array(2); b[0] = (v>>>8)&0xff; b[1]=v&0xff; return b; };
  const writeInt64BE = (v) => {
    const b = new Uint8Array(8); let x = BigInt(v);
    for (let i=7;i>=0;i--){ b[i]=Number(x & 0xffn); x >>= 8n; }
    return b;
  };

  // 拼接
  const concatBytes = (arrs) => {
    const total = arrs.reduce((s,a)=>s+a.length,0);
    const out = new Uint8Array(total);
    let off=0; for (const a of arrs){ out.set(a, off); off += a.length; }
    return out;
  };

  // Base64 <-> bytes
  const b64encode = (buf) => {
    const bytes = buf instanceof Uint8Array ? buf : new Uint8Array(buf);
    let bin=''; for (let i=0;i<bytes.length;i++) bin += String.fromCharCode(bytes[i]);
    return btoa(bin);
  };
  const b64decode = (b64) => {
    const bin = atob(b64);
    const out = new Uint8Array(bin.length);
    for (let i=0;i<bin.length;i++) out[i] = bin.charCodeAt(i);
    return out;
  };

  // PKCS7 Padding for AES-CBC
  const pkcs7Pad = (data) => {
    const block = 16; const pad = block - (data.length % block); const out = new Uint8Array(data.length + pad);
    out.set(data,0); out.fill(pad, data.length);
    return out;
  };
  const pkcs7Unpad = (data) => {
    if (!data || data.length===0) return null;
    const pad = data[data.length-1];
    if (pad<=0 || pad>16 || pad>data.length) return null;
    for (let i=data.length-pad;i<data.length;i++) if (data[i]!==pad) return null;
    return data.subarray(0, data.length - pad);
  };

  // AES-CBC 加密/解密（手动PKCS7）
  const aesCbcEncrypt = async (plainBytes, keyStr, ivBytes) => {
    const keyBytes = enc.encode(keyStr);
    if (![16,24,32].includes(keyBytes.length)) throw new Error('secret length invalid');
    const key = await crypto.subtle.importKey('raw', keyBytes, 'AES-CBC', false, ['encrypt']);
    const padded = pkcs7Pad(plainBytes);
    const cipher = await crypto.subtle.encrypt({ name: 'AES-CBC', iv: ivBytes }, key, padded);
    return new Uint8Array(cipher);
  };
  const aesCbcDecrypt = async (cipherBytes, keyStr, ivBytes) => {
    const keyBytes = enc.encode(keyStr);
    if (![16,24,32].includes(keyBytes.length)) throw new Error('secret length invalid');
    const key = await crypto.subtle.importKey('raw', keyBytes, 'AES-CBC', false, ['decrypt']);
    try {
      const plainPadded = await crypto.subtle.decrypt({ name: 'AES-CBC', iv: ivBytes }, key, cipherBytes);
      const unpadded = pkcs7Unpad(new Uint8Array(plainPadded));
      if (!unpadded) throw new Error('pkcs7 unpad failed');
      return unpadded;
    } catch (err) {
      if (err.name === 'OperationError') {
        throw new Error('AesDecrypt failed: invalid key or corrupted data');
      }
      throw err;
    }
  };

  // AES-GCM 解密
  const aesGcmDecrypt = async (cipherBytes, keyStr, nonceBytes) => {
    const keyBytes = enc.encode(keyStr);
    if (![16,24,32].includes(keyBytes.length)) throw new Error('secret length invalid');
    const key = await crypto.subtle.importKey('raw', keyBytes, 'AES-GCM', false, ['decrypt']);
    try {
      const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: nonceBytes, tagLength: 128 }, key, cipherBytes);
      return new Uint8Array(plain);
    } catch (err) {
      if (err.name === 'OperationError') {
        throw new Error('AesGCMDecrypt failed: invalid key or corrupted data');
      }
      throw err;
    }
  };

  // 生成 Token（04 + base64(expire + iv + cipher)） CBC 模式
  const generateToken04Browser = async (appIdNum, userIdStr, secretStr, effectiveSeconds, payloadStr = '') => {
    if (!appIdNum || typeof appIdNum !== 'number') throw new Error('appID invalid');
    if (!userIdStr || typeof userIdStr !== 'string') throw new Error('userId invalid');
    if (!secretStr || typeof secretStr !== 'string' || secretStr.length !== 32) throw new Error('serverSecret must be 32 bytes');
    if (!effectiveSeconds || typeof effectiveSeconds !== 'number') throw new Error('effectiveTimeInSeconds invalid');

    const ctime = Math.floor(Date.now()/1000);
    const tokenInfo = { app_id: appIdNum, user_id: userIdStr, ctime, expire: ctime + effectiveSeconds, nonce: makeNonce(), payload: payloadStr || '' };
    const plain = enc.encode(JSON.stringify(tokenInfo));
    const iv = makeRandomIv();
    const cipherBytes = await aesCbcEncrypt(plain, secretStr, iv);

    const packed = concatBytes([
      writeInt64BE(tokenInfo.expire),
      writeUint16BE(iv.length), iv,
      writeUint16BE(cipherBytes.length), cipherBytes
    ]);
    return '04' + b64encode(packed);
  };

  // 解析结构：int64 expire | u16 ivLen | iv | u16 cipherLen | cipher | [u8 mode]
  const unpackToken04 = (buf) => {
    try {
      let off = 0; const view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
      const readU16 = () => { const v = view.getUint16(off, false); off += 2; return v; };
      const readI64 = () => { const hi = view.getUint32(off, false), lo = view.getUint32(off+4, false); off += 8; return (BigInt(hi)<<32n) + BigInt(lo); };
      const total = buf.length;
      if (total < 12) throw new Error('token len error: too short');
      const expire = readI64();
      const ivLen = readU16();
      if (off + ivLen > total) throw new Error('token len error: iv overflow');
      const iv = buf.subarray(off, off+ivLen); off += ivLen;
      const cipherLen = readU16();
      if (off + cipherLen > total) throw new Error('token len error: cipher overflow');
      const cipher = buf.subarray(off, off+cipherLen); off += cipherLen;
      let mode = 0;
      if (total - off >= 1) { mode = buf[off]; off += 1; }
      return { expire: Number(expire), iv, cipher, mode };
    } catch (err) {
      throw new Error(`Unpack token04 failed: ${err.message}`);
    }
  };


  // 字段名与类型检查（仅 04）
  const checkTokenDataNameAndType04 = (plainJson) => {
    const errors = [];
    let obj;
    try { obj = JSON.parse(plainJson); } catch (e) { return ['token format error: ' + e.message]; }

    const push = (msg) => errors.push(msg);
    // app_id: 可被转换为 uint32 的 number（非负、<= 4294967295，且是整数）
    if (obj.app_id === undefined || obj.app_id === null) push('app_id missing');
    else if (typeof obj.app_id !== 'number') push('app_id type error: expect number');
    else if (!Number.isInteger(obj.app_id) || obj.app_id < 0 || obj.app_id > 0xFFFFFFFF) push('app_id value invalid: must fit uint32');

    // user_id: string
    if (obj.user_id === undefined || obj.user_id === null) push('user_id missing');
    else if (typeof obj.user_id !== 'string') push('user_id type error: expect string');

    // ctime: int64 number
    if (obj.ctime === undefined || obj.ctime === null) push('ctime missing');
    else if (typeof obj.ctime !== 'number') push('ctime type error: expect number');

    // expire: int64 number
    if (obj.expire === undefined || obj.expire === null) push('expire missing');
    else if (typeof obj.expire !== 'number') push('expire type error: expect number');

    // nonce: int32 number
    if (obj.nonce === undefined || obj.nonce === null) push('nonce missing');
    else if (typeof obj.nonce !== 'number') push('nonce type error: expect number');

    // payload: optional string
    if (obj.payload !== undefined && obj.payload !== null && typeof obj.payload !== 'string') push('payload type error: expect string');


    return errors;
  };

  // 工具：尝试解析与时间格式化（模块级）
  const tryParseJson = (s) => { try { return JSON.parse(s); } catch { return null; } };
  const formatTs = (sec) => {
    if (typeof sec !== 'number' || !Number.isFinite(sec)) return '-';
    const d = new Date(sec * 1000);
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
  };

  // 事件：生成
  const onGenerate = async () => {
    if (!serverSecret.trim()) return alert(t.errorServerSecret);
    if (serverSecret.length !== 32) return alert(t.errorServerSecretLength);
    if (!appId.trim() || !/^[0-9]+$/.test(appId.trim())) return alert(t.errorAppId);
    if (!userId.trim()) return alert(t.errorUserId);
    const eff = parseInt(effective, 10); if (!eff || eff <= 0) return alert(t.errorEffective);

    try {
      const token = await generateToken04Browser(Number(appId), userId.trim(), serverSecret, eff, payload);
      setToken(token);
    } catch (e) {
      console.error(e); alert(t.generateFailed + (e?.message || e));
    }
  };

  // 事件：校验
  const onVerify = async () => {
    setVerifyResult(null);
    if (!serverSecret.trim()) return alert(t.errorServerSecret);
    if (serverSecret.length !== 32) return alert(t.errorServerSecretLength);
    if (!inputToken.trim()) return alert(t.errorToken);

    try {
      const ver = inputToken.slice(0,2);
      if (ver !== '04') {
        const errorMsg = language === 'zh' ? '仅支持 04 版本 Token' : 'Only version 04 is supported';
        const failReason = language === 'zh' ? '无效token。原因未知。' : 'Invalid token. Reason unknown.';
        const detailReason = language === 'zh' ? 'token版本不是04' : 'token version is not 04';
        setVerifyResult({ ok: false, version: ver || '(unknown)', mode: '-', plainJson: '', errors: [errorMsg], expired: null, failReason, detailedReason: detailReason });
        return;
      }
      const body = inputToken.slice(2);
      // Step 1: base64 decode
      let all;
      try { all = b64decode(body); }
      catch (err) {
        const failReason = language === 'zh' ? 'token非base64格式' : 'Token is not in base64 format';
        setVerifyResult({ ok:false, version:'04', mode:'-', plainJson:'', errors:[], expired:null, failReason, detailedReason:`dcodeToken04 base64 decode error:${err?.message || err}; tokenStr:${body}` });
        return;
      }
      // Step 2: unpack
      let expire, iv, cipher, mode;
      try {
        const unpack = unpackToken04(all);
        expire = unpack.expire; iv = unpack.iv; cipher = unpack.cipher; mode = unpack.mode;
      } catch (err) {
        const failReason = language === 'zh' ? '无效token。原因未知。' : 'Invalid token. Reason unknown.';
        setVerifyResult({ ok:false, version:'04', mode:'-', plainJson:'', errors:[], expired:null, failReason, detailedReason:`unpack error:${err?.message || err}` });
        return;
      }
      // Step 3: decrypt
      let plain;
      try {
        if (mode === 1) plain = await aesGcmDecrypt(cipher, serverSecret, iv);
        else plain = await aesCbcDecrypt(cipher, serverSecret, iv);
      } catch (err) {
        const failReason = language === 'zh' ? '解密失败' : 'Decryption failed';
        setVerifyResult({ ok:false, version:'04', mode:'-', plainJson:'', errors:[], expired:null, failReason, detailedReason:String(err?.message || err) });
        return;
      }
      // Step 4: parse and check
      const plainJson = dec.decode(plain);
      const errors = checkTokenDataNameAndType04(plainJson);
      const now = Math.floor(Date.now()/1000);
      const expired = typeof expire === 'number' ? expire < now : null;
      const obj = tryParseJson(plainJson);
      setVerifyResult({
        ok: true,
        version: '04',
        mode: mode===1 ? 'GCM' : 'CBC',
        plainJson,
        errors,
        expired,
        parsed: obj ? { app_id: obj.app_id, user_id: obj.user_id, ctime: obj.ctime, expire: obj.expire, nonce: obj.nonce, payload: obj.payload } : null
      });
    } catch (e) {

      const msg = String(e?.message || e);
      let failReason = '无效token。原因未知。';
      if (msg.includes('base64 decode')) failReason = 'token非base64格式';
      else if (msg.includes('AesGCMDecrypt') || msg.includes('AesDecrypt') || msg.includes('unpad') || msg.includes('secret length invalid')) failReason = '解密失败';
      else if (msg.includes('token version') || msg.includes('Unpack') || msg.includes('token len error') || msg.startsWith('dcodeToken04') || msg.includes('DecodeToken04')) failReason = '无效token。原因未知。';
      else failReason = '解析失败';
      setVerifyResult({ ok: false, version: '04', mode: '-', plainJson: '', errors: [], expired: null, failReason, detailedReason: msg });
    }
  };

  // UI
  return (
    <>
      <div style={{ maxWidth: 760, margin: '20px auto', padding: 20, border: '1px solid #ddd', borderRadius: 8, background: '#f9f9f9' }}>
        <p style={{ textAlign: 'center', marginBottom: 12, fontSize: 18, fontWeight: 'bold' }}>{t.title}</p>
        <div style={{ fontSize: 12, color: '#a00', marginBottom: 12 }}>
          {t.warning}
        </div>

        <div style={{ height: 24, marginBottom: 12, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {copyFeedback && <div style={{ background: '#d4edda', color: '#155724', padding: '6px 10px', border: '1px solid #c3e6cb', borderRadius: 4 }}>{copyFeedback}</div>}
        </div>

        <LabeledInput label={t.serverSecret} type="password" value={serverSecret} onChange={setServerSecret} placeholder={t.serverSecretPlaceholder} />
        <LabeledInput label={t.appId} value={appId} onChange={setAppId} placeholder={t.appIdPlaceholder} />

        {/* Tabs */}
        <div style={{ display: 'flex', gap: 16, margin: '12px 0 16px 0', borderBottom: '1px solid #eee' }}>
          <button onClick={() => setActiveTab('generate')} style={tabStyle(activeTab==='generate')}>{t.tabGenerate}</button>
          <button onClick={() => setActiveTab('verify')} style={tabStyle(activeTab==='verify')}>{t.tabVerify}</button>
        </div>

        {activeTab === 'generate' ? (
          <div>
            <LabeledInput label={t.userId} value={userId} onChange={setUserId} placeholder={t.userIdPlaceholder} />
            <LabeledInput label={t.effective} value={effective} onChange={setEffective} placeholder={t.effectivePlaceholder} />

            <div style={{ marginBottom: 12 }}>
              <label style={{ display: 'block', marginBottom: 6, fontWeight: 'bold' }}>{t.payload}</label>
              <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                <textarea value={payload} onChange={(e)=>setPayload(e.target.value)} placeholder={payloadExample} style={{ flex: 1, minHeight: 100, padding: 8, border: '1px solid #ccc', borderRadius: 4, fontSize: 13 }} />
                <button onClick={() => setPayload(payloadExample)} style={copyBtnStyle(false)}>{t.fillExample}</button>
              </div>
            </div>

            <div style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', marginBottom: 6, fontWeight: 'bold' }}>{t.token}</label>
              <div style={{ display: 'flex', gap: 10 }}>
                <input type="text" readOnly value={token} placeholder={t.tokenPlaceholder} style={inputStyle(true)} />
                <button onClick={() => copyToClipboard(token, t.token)} disabled={!token} style={copyBtnStyle(!token)}>{t.copy}</button>
              </div>
            </div>

            <button onClick={onGenerate} style={primaryBtnStyle}>{t.generateBtn}</button>
          </div>
        ) : (
          <div>
            <div style={{ marginBottom: 12 }}>
              <label style={{ display: 'block', marginBottom: 6, fontWeight: 'bold' }}>{t.token}</label>
              <textarea value={inputToken} onChange={(e)=>setInputToken(e.target.value)} placeholder={t.tokenInputPlaceholder} style={{ width: '100%', minHeight: 80, padding: 8, border: '1px solid #ccc', borderRadius: 4, fontSize: 13 }} />
            </div>
            <button onClick={onVerify} style={primaryBtnStyle}>{t.verifyBtn}</button>

            {verifyResult && (
              <div style={{ marginTop: 16, padding: 12, border: '1px solid #eee', borderRadius: 6, background: '#fff' }}>
                <div style={{ marginBottom: 8 }}>
                  <strong>{t.verifyResult}</strong>{verifyResult.ok ? t.parseSuccess : t.parseFailed}
                </div>
                {!verifyResult.ok ? (
                  <div>
                    <div><strong>{t.failReason}</strong>{verifyResult.failReason || t.parseFailed}</div>
                    <div style={{ marginTop: 6, fontSize: 12, color: '#a00', wordBreak: 'break-all' }}>
                      <strong>{t.detailReason}</strong>{verifyResult.detailedReason || '-'}
                    </div>
                  </div>
                ) : (
                  <>
                    <div style={{ marginBottom: 8, fontSize: 13 }}>
                      <strong>{t.version}</strong>{verifyResult.version} &nbsp; <strong>{t.mode}</strong>{verifyResult.mode}
                      {verifyResult.expired!==null && (<>&nbsp; <strong>{t.expired}</strong>{verifyResult.expired ? t.yes : t.no}</>)}
                    </div>
                    {verifyResult.parsed && (
                      <div style={{ marginBottom: 8 }}>
                        <strong>{t.parsedFields}</strong>
                        <div style={{ marginTop: 6, lineHeight: 1.7 }}>
                          <div>app_id：{String(verifyResult.parsed.app_id ?? '-')}</div>
                          <div>user_id：{String(verifyResult.parsed.user_id ?? '-')}</div>
                          <div>ctime：{formatTs(verifyResult.parsed.ctime)}</div>
                          <div>expire：{formatTs(verifyResult.parsed.expire)}</div>
                          <div>nonce：{String(verifyResult.parsed.nonce ?? '-')}</div>
                          <div>payload：{(() => {
                            const p = verifyResult.parsed.payload;
                            try { return <code>{JSON.stringify(JSON.parse(p), null, 0)}</code>; } catch { return <code>{String(p ?? '')}</code>; }
                          })()}</div>
                        </div>
                      </div>
                    )}
                    <div style={{ marginBottom: 8 }}>
                      <strong>{t.plainJson}</strong>
                      <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all', background: '#f6f8fa', padding: 10, borderRadius: 4, fontSize: 12 }}>{verifyResult.plainJson || t.decryptFailed}</pre>
                    </div>
                    <div>
                      <strong>{t.fieldCheck}</strong>
                      {verifyResult.errors && verifyResult.errors.length>0 ? (
                        <ul>{verifyResult.errors.map((e,i)=>(<li key={i} style={{ color: '#a00' }}>{e}</li>))}</ul>
                      ) : (
                        <div style={{ color: '#2b7a0b' }}>{t.pass}</div>
                      )}
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
};

const inputStyle = (readOnly = false) => ({ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: 4, fontSize: 14, backgroundColor: readOnly ? '#f5f5f5' : '#fff' });
const copyBtnStyle = (disabled) => ({ padding: '8px 20px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: 4, cursor: disabled ? 'not-allowed' : 'pointer', opacity: disabled ? 0.6 : 1, minWidth: '80px', whiteSpace: 'nowrap' });
const primaryBtnStyle = { width: '100%', padding: 12, background: '#28a745', color: '#fff', border: 'none', borderRadius: 4, fontSize: 16, fontWeight: 'bold', cursor: 'pointer' };
const tabStyle = (active) => ({ padding: '8px 12px', border: 'none', borderBottom: '2px solid ' + (active ? '#28a745' : 'transparent'), background: 'transparent', color: active ? '#28a745' : '#555', cursor: 'pointer' });

const LabeledInput = ({ label, type = 'text', value, onChange, placeholder, onCopy }) => (
  <div style={{ marginBottom: 12 }}>
    <label style={{ display: 'block', marginBottom: 6, fontWeight: 'bold' }}>{label}:</label>
    {onCopy ? (
      <div style={{ display: 'flex', gap: 10 }}>
        <input type={type} value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} style={{ flex: 1, padding: '8px', border: '1px solid #ccc', borderRadius: 4, fontSize: 14, backgroundColor: '#fff' }} />
        <button onClick={onCopy} disabled={!value} style={copyBtnStyle(!value)}>复制</button>
      </div>
    ) : (
      <input type={type} value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} style={inputStyle()} />
    )}
  </div>
);

export default TokenAssistant;

