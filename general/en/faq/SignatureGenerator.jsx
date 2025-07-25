import React, { useState } from 'react';

const SignatureGenerator = () => {
    const [appId, setAppId] = useState('');
    const [serverSecret, setServerSecret] = useState('');
    const [signatureNonce, setSignatureNonce] = useState('');
    const [timestamp, setTimestamp] = useState('');
    const [signature, setSignature] = useState('');
    const [copyFeedback, setCopyFeedback] = useState('');

    // MD5 hash function implementation (client-side)
    const md5 = (str) => {
        // Using crypto-js from CDN
        if (typeof CryptoJS !== 'undefined') {
            return CryptoJS.MD5(str).toString();
        }
        
        // Fallback simple MD5 implementation
        const rotateLeft = (lValue, iShiftBits) => {
            return (lValue << iShiftBits) | (lValue >>> (32 - iShiftBits));
        };
        
        const addUnsigned = (lX, lY) => {
            const lX4 = lX & 0x40000000;
            const lY4 = lY & 0x40000000;
            const lX8 = lX & 0x80000000;
            const lY8 = lY & 0x80000000;
            const lResult = (lX & 0x3FFFFFFF) + (lY & 0x3FFFFFFF);
            
            if (lX4 & lY4) {
                return lResult ^ 0x80000000 ^ lX8 ^ lY8;
            }
            if (lX4 | lY4) {
                if (lResult & 0x40000000) {
                    return lResult ^ 0xC0000000 ^ lX8 ^ lY8;
                } else {
                    return lResult ^ 0x40000000 ^ lX8 ^ lY8;
                }
            } else {
                return lResult ^ lX8 ^ lY8;
            }
        };
        
        const F = (x, y, z) => (x & y) | (~x & z);
        const G = (x, y, z) => (x & z) | (y & ~z);
        const H = (x, y, z) => x ^ y ^ z;
        const I = (x, y, z) => y ^ (x | ~z);
        
        const FF = (a, b, c, d, x, s, ac) => {
            a = addUnsigned(a, addUnsigned(addUnsigned(F(b, c, d), x), ac));
            return addUnsigned(rotateLeft(a, s), b);
        };
        
        const GG = (a, b, c, d, x, s, ac) => {
            a = addUnsigned(a, addUnsigned(addUnsigned(G(b, c, d), x), ac));
            return addUnsigned(rotateLeft(a, s), b);
        };
        
        const HH = (a, b, c, d, x, s, ac) => {
            a = addUnsigned(a, addUnsigned(addUnsigned(H(b, c, d), x), ac));
            return addUnsigned(rotateLeft(a, s), b);
        };
        
        const II = (a, b, c, d, x, s, ac) => {
            a = addUnsigned(a, addUnsigned(addUnsigned(I(b, c, d), x), ac));
            return addUnsigned(rotateLeft(a, s), b);
        };
        
        const convertToWordArray = (str) => {
            const wordArray = [];
            let i = 0;
            const len = str.length;
            
            while (i < len) {
                wordArray[i >> 2] |= (str.charCodeAt(i) & 0xFF) << ((i % 4) * 8);
                i++;
            }
            
            return wordArray;
        };
        
        const wordToHex = (lValue) => {
            let wordToHexValue = '';
            let wordToHexValueTemp = '';
            let lByte, lCount;
            
            for (lCount = 0; lCount <= 3; lCount++) {
                lByte = (lValue >>> (lCount * 8)) & 255;
                wordToHexValueTemp = '0' + lByte.toString(16);
                wordToHexValue += wordToHexValueTemp.substr(wordToHexValueTemp.length - 2, 2);
            }
            
            return wordToHexValue;
        };
        
        const utf8Encode = (str) => {
            str = str.replace(/\r\n/g, '\n');
            let utftext = '';
            
            for (let n = 0; n < str.length; n++) {
                const c = str.charCodeAt(n);
                
                if (c < 128) {
                    utftext += String.fromCharCode(c);
                } else if ((c > 127) && (c < 2048)) {
                    utftext += String.fromCharCode((c >> 6) | 192);
                    utftext += String.fromCharCode((c & 63) | 128);
                } else {
                    utftext += String.fromCharCode((c >> 12) | 224);
                    utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                    utftext += String.fromCharCode((c & 63) | 128);
                }
            }
            
            return utftext;
        };
        
        let x = [];
        let k, AA, BB, CC, DD, a, b, c, d;
        const S11 = 7, S12 = 12, S13 = 17, S14 = 22;
        const S21 = 5, S22 = 9, S23 = 14, S24 = 20;
        const S31 = 4, S32 = 11, S33 = 16, S34 = 23;
        const S41 = 6, S42 = 10, S43 = 15, S44 = 21;
        
        str = utf8Encode(str);
        x = convertToWordArray(str);
        
        a = 0x67452301;
        b = 0xEFCDAB89;
        c = 0x98BADCFE;
        d = 0x10325476;
        
        const xl = x.length;
        for (k = 0; k < xl; k += 16) {
            AA = a;
            BB = b;
            CC = c;
            DD = d;
            
            a = FF(a, b, c, d, x[k + 0], S11, 0xD76AA478);
            d = FF(d, a, b, c, x[k + 1], S12, 0xE8C7B756);
            c = FF(c, d, a, b, x[k + 2], S13, 0x242070DB);
            b = FF(b, c, d, a, x[k + 3], S14, 0xC1BDCEEE);
            a = FF(a, b, c, d, x[k + 4], S11, 0xF57C0FAF);
            d = FF(d, a, b, c, x[k + 5], S12, 0x4787C62A);
            c = FF(c, d, a, b, x[k + 6], S13, 0xA8304613);
            b = FF(b, c, d, a, x[k + 7], S14, 0xFD469501);
            a = FF(a, b, c, d, x[k + 8], S11, 0x698098D8);
            d = FF(d, a, b, c, x[k + 9], S12, 0x8B44F7AF);
            c = FF(c, d, a, b, x[k + 10], S13, 0xFFFF5BB1);
            b = FF(b, c, d, a, x[k + 11], S14, 0x895CD7BE);
            a = FF(a, b, c, d, x[k + 12], S11, 0x6B901122);
            d = FF(d, a, b, c, x[k + 13], S12, 0xFD987193);
            c = FF(c, d, a, b, x[k + 14], S13, 0xA679438E);
            b = FF(b, c, d, a, x[k + 15], S14, 0x49B40821);
            
            a = GG(a, b, c, d, x[k + 1], S21, 0xF61E2562);
            d = GG(d, a, b, c, x[k + 6], S22, 0xC040B340);
            c = GG(c, d, a, b, x[k + 11], S23, 0x265E5A51);
            b = GG(b, c, d, a, x[k + 0], S24, 0xE9B6C7AA);
            a = GG(a, b, c, d, x[k + 5], S21, 0xD62F105D);
            d = GG(d, a, b, c, x[k + 10], S22, 0x2441453);
            c = GG(c, d, a, b, x[k + 15], S23, 0xD8A1E681);
            b = GG(b, c, d, a, x[k + 4], S24, 0xE7D3FBC8);
            a = GG(a, b, c, d, x[k + 9], S21, 0x21E1CDE6);
            d = GG(d, a, b, c, x[k + 14], S22, 0xC33707D6);
            c = GG(c, d, a, b, x[k + 3], S23, 0xF4D50D87);
            b = GG(b, c, d, a, x[k + 8], S24, 0x455A14ED);
            a = GG(a, b, c, d, x[k + 13], S21, 0xA9E3E905);
            d = GG(d, a, b, c, x[k + 2], S22, 0xFCEFA3F8);
            c = GG(c, d, a, b, x[k + 7], S23, 0x676F02D9);
            b = GG(b, c, d, a, x[k + 12], S24, 0x8D2A4C8A);
            
            a = HH(a, b, c, d, x[k + 5], S31, 0xFFFA3942);
            d = HH(d, a, b, c, x[k + 8], S32, 0x8771F681);
            c = HH(c, d, a, b, x[k + 11], S33, 0x6D9D6122);
            b = HH(b, c, d, a, x[k + 14], S34, 0xFDE5380C);
            a = HH(a, b, c, d, x[k + 1], S31, 0xA4BEEA44);
            d = HH(d, a, b, c, x[k + 4], S32, 0x4BDECFA9);
            c = HH(c, d, a, b, x[k + 7], S33, 0xF6BB4B60);
            b = HH(b, c, d, a, x[k + 10], S34, 0xBEBFBC70);
            a = HH(a, b, c, d, x[k + 13], S31, 0x289B7EC6);
            d = HH(d, a, b, c, x[k + 0], S32, 0xEAA127FA);
            c = HH(c, d, a, b, x[k + 3], S33, 0xD4EF3085);
            b = HH(b, c, d, a, x[k + 6], S34, 0x4881D05);
            a = HH(a, b, c, d, x[k + 9], S31, 0xD9D4D039);
            d = HH(d, a, b, c, x[k + 12], S32, 0xE6DB99E5);
            c = HH(c, d, a, b, x[k + 15], S33, 0x1FA27CF8);
            b = HH(b, c, d, a, x[k + 2], S34, 0xC4AC5665);
            
            a = II(a, b, c, d, x[k + 0], S41, 0xF4292244);
            d = II(d, a, b, c, x[k + 7], S42, 0x432AFF97);
            c = II(c, d, a, b, x[k + 14], S43, 0xAB9423A7);
            b = II(b, c, d, a, x[k + 5], S44, 0xFC93A039);
            a = II(a, b, c, d, x[k + 12], S41, 0x655B59C3);
            d = II(d, a, b, c, x[k + 3], S42, 0x8F0CCC92);
            c = II(c, d, a, b, x[k + 10], S43, 0xFFEFF47D);
            b = II(b, c, d, a, x[k + 1], S44, 0x85845DD1);
            a = II(a, b, c, d, x[k + 8], S41, 0x6FA87E4F);
            d = II(d, a, b, c, x[k + 15], S42, 0xFE2CE6E0);
            c = II(c, d, a, b, x[k + 6], S43, 0xA3014314);
            b = II(b, c, d, a, x[k + 13], S44, 0x4E0811A1);
            a = II(a, b, c, d, x[k + 4], S41, 0xF7537E82);
            d = II(d, a, b, c, x[k + 11], S42, 0xBD3AF235);
            c = II(c, d, a, b, x[k + 2], S43, 0x2AD7D2BB);
            b = II(b, c, d, a, x[k + 9], S44, 0xEB86D391);
            
            a = addUnsigned(a, AA);
            b = addUnsigned(b, BB);
            c = addUnsigned(c, CC);
            d = addUnsigned(d, DD);
        }
        
        const temp = wordToHex(a) + wordToHex(b) + wordToHex(c) + wordToHex(d);
        return temp.toLowerCase();
    };

    const generateSignature = (params) => {
        const { appId, signatureNonce, serverSecret, timestamp } = params;
        const str = `${appId}${signatureNonce}${serverSecret}${timestamp}`;
        const signature = md5(str);

        console.log('Signature generated successfully:', {
            appId,
            signatureNonce,
            serverSecret,
            timestamp,
            signature
        });

        return signature;
    };

    const generateCommonParams = () => {
        const timestamp = Math.floor(Date.now() / 1000);
        const signatureNonce = Math.random().toString(36).substring(2);

        const signature = generateSignature({
            appId,
            signatureNonce,
            serverSecret,
            timestamp,
        });

        return {
            signatureNonce,
            timestamp,
            signature
        };
    };

    const handleGenerate = () => {
        if (!appId.trim()) {
            alert('Please enter AppId');
            return;
        }

        if (!serverSecret.trim()) {
            alert('Please enter ServerSecret');
            return;
        }

        const params = generateCommonParams();
        setSignatureNonce(params.signatureNonce);
        setTimestamp(params.timestamp.toString());
        setSignature(params.signature);
    };

    const copyToClipboard = (text, fieldName) => {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(() => {
                setCopyFeedback(`${fieldName} copied to clipboard`);
                setTimeout(() => setCopyFeedback(''), 2000);
            }).catch(err => {
                console.error('Copy failed:', err);
                fallbackCopyTextToClipboard(text, fieldName);
            });
        } else {
            fallbackCopyTextToClipboard(text, fieldName);
        }
    };

    const fallbackCopyTextToClipboard = (text, fieldName) => {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            setCopyFeedback(`${fieldName} copied to clipboard`);
            setTimeout(() => setCopyFeedback(''), 2000);
        } catch (err) {
            console.error('Copy failed:', err);
            setCopyFeedback('Copy failed, please copy manually');
            setTimeout(() => setCopyFeedback(''), 2000);
        }
        
        document.body.removeChild(textArea);
    };

    return (
        <>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
            <div style={{ 
                maxWidth: '600px', 
                margin: '20px auto', 
                padding: '20px', 
                border: '1px solid #ddd', 
                borderRadius: '8px',
                backgroundColor: '#f9f9f9'
            }}>
                <h3 style={{ textAlign: 'center', marginBottom: '20px' }}>Signature Generator</h3>
                
                <div style={{ 
                    height: '40px',
                    marginBottom: '15px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
                    {copyFeedback && (
                        <div style={{ 
                            backgroundColor: '#d4edda', 
                            color: '#155724', 
                            padding: '10px', 
                            border: '1px solid #c3e6cb', 
                            borderRadius: '4px',
                            textAlign: 'center'
                        }}>
                            {copyFeedback}
                        </div>
                    )}
                </div>
                
                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                        ServerSecret:
                    </label>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            type="password"
                            value={serverSecret}
                            onChange={(e) => setServerSecret(e.target.value)}
                            placeholder="Enter ServerSecret"
                            style={{
                                flex: 1,
                                padding: '8px',
                                border: '1px solid #ccc',
                                borderRadius: '4px',
                                fontSize: '14px'
                            }}
                        />
                        <button
                            onClick={() => copyToClipboard(serverSecret, 'ServerSecret')}
                            disabled={!serverSecret}
                            style={{
                                padding: '8px 16px',
                                backgroundColor: '#007bff',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: serverSecret ? 'pointer' : 'not-allowed',
                                opacity: serverSecret ? 1 : 0.6
                            }}
                        >
                            Copy
                        </button>
                    </div>
                </div>

                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                        AppId:
                    </label>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            type="text"
                            value={appId}
                            onChange={(e) => setAppId(e.target.value)}
                            placeholder="Enter AppId"
                            style={{
                                flex: 1,
                                padding: '8px',
                                border: '1px solid #ccc',
                                borderRadius: '4px',
                                fontSize: '14px'
                            }}
                        />
                        <button
                            onClick={() => copyToClipboard(appId, 'AppId')}
                            disabled={!appId}
                            style={{
                                padding: '8px 16px',
                                backgroundColor: '#007bff',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: appId ? 'pointer' : 'not-allowed',
                                opacity: appId ? 1 : 0.6
                            }}
                        >
                            Copy
                        </button>
                    </div>
                </div>

                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                        SignatureNonce:
                    </label>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            type="text"
                            value={signatureNonce}
                            readOnly
                            placeholder="Filled after clicking the Generate button"
                            style={{
                                flex: 1,
                                padding: '8px',
                                border: '1px solid #ccc',
                                borderRadius: '4px',
                                fontSize: '14px',
                                backgroundColor: '#f5f5f5'
                            }}
                        />
                        <button
                            onClick={() => copyToClipboard(signatureNonce, 'SignatureNonce')}
                            disabled={!signatureNonce}
                            style={{
                                padding: '8px 16px',
                                backgroundColor: '#007bff',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: signatureNonce ? 'pointer' : 'not-allowed',
                                opacity: signatureNonce ? 1 : 0.6
                            }}
                        >
                            Copy
                        </button>
                    </div>
                </div>

                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                        Timestamp:
                    </label>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            type="text"
                            value={timestamp}
                            readOnly
                            placeholder="Filled after clicking the Generate button"
                            style={{
                                flex: 1,
                                padding: '8px',
                                border: '1px solid #ccc',
                                borderRadius: '4px',
                                fontSize: '14px',
                                backgroundColor: '#f5f5f5'
                            }}
                        />
                        <button
                            onClick={() => copyToClipboard(timestamp, 'Timestamp')}
                            disabled={!timestamp}
                            style={{
                                padding: '8px 16px',
                                backgroundColor: '#007bff',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: timestamp ? 'pointer' : 'not-allowed',
                                opacity: timestamp ? 1 : 0.6
                            }}
                        >
                            Copy
                        </button>
                    </div>
                </div>

                <div style={{ marginBottom: '20px' }}>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                        Signature:
                    </label>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            type="text"
                            value={signature}
                            readOnly
                            placeholder="Filled after clicking the Generate button"
                            style={{
                                flex: 1,
                                padding: '8px',
                                border: '1px solid #ccc',
                                borderRadius: '4px',
                                fontSize: '14px',
                                backgroundColor: '#f5f5f5'
                            }}
                        />
                        <button
                            onClick={() => copyToClipboard(signature, 'Signature')}
                            disabled={!signature}
                            style={{
                                padding: '8px 16px',
                                backgroundColor: '#007bff',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: signature ? 'pointer' : 'not-allowed',
                                opacity: signature ? 1 : 0.6
                            }}
                        >
                            Copy
                        </button>
                    </div>
                </div>

                <button
                    onClick={handleGenerate}
                    style={{
                        width: '100%',
                        padding: '12px',
                        backgroundColor: '#28a745',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        fontSize: '16px',
                        cursor: 'pointer',
                        fontWeight: 'bold'
                    }}
                >
                    Generate Signature
                </button>
            </div>
        </>
    );
};

export default SignatureGenerator;
