import React, { useState } from 'react';

const styles = {
  priceCard: {
    padding: '24px',
    border: '1px solid #E6E6E6',
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
    width: '280px',
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
    padding:'0 6px',
    lineHeight: '22px',
    background: 'rgba(255,77,92,.2)',
    color: '#88000b',
    fontSize: '12px',
    borderRadius: '8px 0 8px 0',
  },
  divider: {
    width: '100%',
    height: 0,
    borderTop: '1px dashed #E6E6E6'
  },
  priceContainer: {
    display: 'flex',
    alignItems: 'baseline',
    gap: '4px'
  },
  price: {
    fontSize: '28px',
    fontWeight: '600',
    color: '#333',
    fontStyle: 'italic'
  },
  unit: {
    fontSize: '16px',
    color: '#333',
    fontStyle: 'italic'
  }
};

function PriceCard({ points, price }) {
  return (
    <div style={styles.priceCard}>
      <div style={styles.header}>
        <span style={styles.points}>{points} 点</span>
        <span style={styles.tag}>数美审核</span>
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
      gap: '20px',
      margin: '20px 0'
    }}>
      <PriceCard points="10000" price="1000" />
      <PriceCard points="20000" price="2000" />
      <PriceCard points="50000" price="5000" />
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
      margin: '20px 0'
    }}>
      {/* 预付费套餐包 */}
      <div style={{
        flex: 1,
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
        }}>预付费套餐包</h3>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}>
          <a 
            href="#预付费套餐包" 
            style={buttonStyle('btn1')}
            onMouseEnter={() => setHoveredButton('btn1')}
            onMouseLeave={() => setHoveredButton(null)}
            onMouseDown={() => setActiveButton('btn1')}
            onMouseUp={() => setActiveButton(null)}
          >
            下滑了解《预付费套餐包》价格、扣减规则
          </a>
          <a 
            href="https://www.zego.im/cloudmarket/cloudMarketDetail?id=idShi" 
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
        flex: 1,
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
        }}>后付费</h3>
        <a 
          href="#后付费服务定价" 
          style={buttonStyle('btn3')}
          onMouseEnter={() => setHoveredButton('btn3')}
          onMouseLeave={() => setHoveredButton(null)}
          onMouseDown={() => setActiveButton('btn3')}
          onMouseUp={() => setActiveButton(null)}
        >
          下滑了解《后付费》服务定价
        </a>
        <p style={{
          margin: 0,
          color: '#666',
          fontSize: '14px'
        }}>如需购买，请联系 ZEGO 商务人员。</p>
      </div>
    </div>
  );
}