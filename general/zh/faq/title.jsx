import React from 'react';

export const Title = ({ children }) => {
  return (
    <h1 style={{
      fontSize: '26px',
      fontWeight: '700',
      lineHeight: '40px',
      marginTop: '24px',
      marginBottom: '16px',
      color: '#28292e'
    }}>
      {children}
    </h1>
  );
};