import { useEffect, useRef, useState } from 'react';

const QRCode = ({
  content,
  size = 200,
  errorCorrectionLevel = 'M',
  color = { dark: '#000000', light: '#FFFFFF' },
  title,
  showTitle = false,
  style = {}
}) => {
  const containerRef = useRef(null);
  const [error, setError] = useState(null);
  const [isClient, setIsClient] = useState(false);

  // 检测是否在客户端
  useEffect(() => {
    setIsClient(true);
  }, []);

  // 生成二维码
  useEffect(() => {
    if (!isClient || !content || !containerRef.current) return;

    let isMounted = true;

    const loadAndCreateQRCode = async () => {
      try {
        // 确保QRCode库已加载
        if (!window.QRCode) {
          // 动态加载qrcodejs库
          await new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
          });
        }

        if (!isMounted || !containerRef.current) return;

        // 清空容器
        containerRef.current.innerHTML = '';

        // 映射错误纠正级别
        const correctLevelMap = {
          'L': window.QRCode.CorrectLevel.L,
          'M': window.QRCode.CorrectLevel.M,
          'Q': window.QRCode.CorrectLevel.Q,
          'H': window.QRCode.CorrectLevel.H
        };

        // 创建二维码
        new window.QRCode(containerRef.current, {
          text: content,
          width: size,
          height: size,
          colorDark: color.dark,
          colorLight: color.light,
          correctLevel: correctLevelMap[errorCorrectionLevel] || window.QRCode.CorrectLevel.M
        });

        if (isMounted) {
          setError(null);
        }
      } catch (err) {
        console.error('QRCode generation error:', err);
        if (isMounted) {
          setError('二维码生成失败');
        }
      }
    };

    loadAndCreateQRCode();

    return () => {
      isMounted = false;
    };
  }, [isClient, content, size, errorCorrectionLevel, color]);



  // 服务端渲染时显示占位符
  if (!isClient) {
    return (
      <div style={{
        width: size,
        height: size,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: '1px dashed #ddd',
        color: '#999',
        fontSize: '14px',
        borderRadius: '4px',
        backgroundColor: '#fafafa',
        ...style
      }}>
        二维码加载中...
      </div>
    );
  }

  if (!content) {
    return (
      <div style={{
        width: size,
        height: size,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: '1px dashed #ccc',
        color: '#999',
        fontSize: '14px',
        borderRadius: '4px',
        ...style
      }}>
        请提供content属性
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        width: size,
        height: size,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: '1px solid #ff4d4f',
        color: '#ff4d4f',
        fontSize: '14px',
        borderRadius: '4px',
        backgroundColor: '#fff2f0',
        ...style
      }}>
        {error}
      </div>
    );
  }



  return (
    <div style={{ display: 'inline-block', textAlign: 'center', ...style }}>
      {showTitle && title && (
        <div style={{
          marginBottom: '8px',
          fontSize: '14px',
          color: '#666',
          fontWeight: '500'
        }}>
          {title}
        </div>
      )}
      <div ref={containerRef} style={{ display: 'inline-block' }} />
      {showTitle && !title && (
        <div style={{
          marginTop: '8px',
          fontSize: '12px',
          color: '#999',
          wordBreak: 'break-all',
          maxWidth: size
        }}>
          {content.length > 50 ? content.substring(0, 50) + '...' : content}
        </div>
      )}
    </div>
  );
};

export default QRCode;
