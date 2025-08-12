import React, { useState } from 'react';

const styles = {
  priceCard: {
    height: '137px',
    padding: '16px',
    border: '1px solid #E6E6E6',
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    width: '280px',
    borderRadius: '8px',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px'
  },
  points: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#333'
  },
  tag: {
    height: '22px',
    padding: '0 6px',
    lineHeight: '22px',
    width: '60px',
    background: 'rgba(255,77,92,.2)',
    color: '#88000b',
    fontSize: '12px',
    borderRadius: '8px 0 8px 0',
    textAlign: 'center'
  },
  divider: {
    width: '100%',
    height: 0,
    margin: '4px 0',
    borderTop: '1px dashed #E6E6E6'
  },
  priceContainer: {
    display: 'flex',
    alignItems: 'baseline',
    gap: '2px',
    marginTop: 'auto'
  },
  price: {
    fontSize: '26px',
    fontWeight: '600',
    color: '#333',
    fontStyle: 'italic',
    lineHeight: '1'
  },
  unit: {
    fontSize: '14px',
    color: '#333',
    marginLeft: '2px'
  }
};

function PriceCard({ points, price }) {
  return (
    <div style={styles.priceCard}>
      <div style={styles.header}>
        <span style={styles.points}>{points} 点</span>
        <span style={styles.tag}>谷歌翻译</span>
      </div>
      <div style={styles.divider} />
      <div style={styles.priceContainer}>
        <span style={styles.price}>{price}</span>
        <span style={styles.unit}>元</span>
      </div>
    </div>
  );
}

export function PriceList() {
  return (
    <div style={{
      display: 'flex',
      flexWrap: 'wrap',
      gap: '20px',
      margin: '20px 0',
      justifyContent: 'flex-start'
    }}>
      <PriceCard points="700" price="70" />
      <PriceCard points="7070" price="700" />
      <PriceCard points="36500" price="3500" />
      <PriceCard points="377000" price="35000" />
    </div>
  );
}


export  function ChargeMethod() {
  const [hoveredButton, setHoveredButton] = useState(null);
  const [activeButton, setActiveButton] = useState(null);

  const buttonStyle = (id) => ({
    padding: '12px 16px',
    borderRadius: '6px',
    textDecoration: 'none',
    textAlign: 'center',
    fontWeight: '500',
    border: 'none',
    outline: 'none',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    background: activeButton === id ? '#3478F6' : hoveredButton === id ? '#E5E8FF' : '#F5F5FF',
    color: activeButton === id ? '#fff' : '#3478F6'
  });

  return (
    <div style={{
      display: 'flex',
      gap: '20px',
      margin: '20px 0',
      flexWrap: 'wrap'
    }}>
      {/* 预付费套餐包 */}
      <div style={{
        flex: '1 1 calc(50% - 10px)',
        minWidth: '283px',
        border: '1px solid #E6E6E6',
        borderRadius: '8px',
        padding: '24px',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }}>
        <h3 style={{
          fontSize: '18px',
          fontWeight: '600',
          margin: 0,
          color: '#333'
        }}>谷歌（预付费套餐包）</h3>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}>
          <a 
            href="#预付费套餐包价格" 
            style={buttonStyle('btn1')}
            onMouseEnter={() => setHoveredButton('btn1')}
            onMouseLeave={() => setHoveredButton(null)}
            onMouseDown={() => setActiveButton('btn1')}
            onMouseUp={() => setActiveButton(null)}
          >
            下滑了解《预付费套餐包》价格、扣减规则
          </a>
          <a 
            href="https://www.zego.im/cloudmarket/cloudMarketDetail?id=idTrans" 
            target="_blank"
            style={buttonStyle('btn2')}
            onMouseEnter={() => setHoveredButton('btn2')}
            onMouseLeave={() => setHoveredButton(null)}
            onMouseDown={() => setActiveButton('btn2')}
            onMouseUp={() => setActiveButton(null)}
          >
            前往 ZEGO 云市场，购买套餐包
          </a>
        </div>
      </div>

      {/* 后付费 */}
      <div style={{
        flex: '1 1 calc(50% - 10px)',
        minWidth: '283px',
        border: '1px solid #E6E6E6',
        borderRadius: '8px',
        padding: '24px',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }}>
        <h3 style={{
          fontSize: '18px',
          fontWeight: '600',
          margin: 0,
          color: '#333'
        }}>科大讯飞</h3>
        <a 
          href="https://www.zego.im/cloudmarket/cloudMarketDetail?id=idFei" 
          target="_blank"
          style={buttonStyle('btn3')}
          onMouseEnter={() => setHoveredButton('btn3')}
          onMouseLeave={() => setHoveredButton(null)}
          onMouseDown={() => setActiveButton('btn3')}
          onMouseUp={() => setActiveButton(null)}
        >
          如需购买，请联系 ZEGO 商务人员。
        </a>
      </div>
    </div>
  );
}