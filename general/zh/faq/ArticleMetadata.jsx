import React from 'react';

const ArticleMetadata = ({ language = 'zh', product, platform, lastUpdated }) => {
    // 根据语言设置文案
    const getLabels = () => {
        if (language === 'en') {
            return {
                productLabel: 'Products / Plugins:',
                platformLabel: 'Platform / Framework:',
                lastUpdatedLabel: 'Last updated:'
            };
        }
        return {
            productLabel: '产品 / 解决方案：',
            platformLabel: '平台 / 框架：',
            lastUpdatedLabel: '最后更新：'
        };
    };

    const labels = getLabels();

    // 根据语言设置标签宽度
    const labelWidth = language === 'en' ? '130px' : '100px';

    // 容器样式
    const containerStyle = {
        backgroundColor: 'rgb(247, 249, 251)',
        borderRadius: '2px',
        padding: '12px 16px',
        marginBottom: '20px',
        marginTop: '20px',
        fontSize: '11px',
        fontFamily: 'Inter-Medium',
        fontWeight: '500',
        color: 'var(--docuo-popup-color)',
        opacity: '0.7'
    };

    // 行样式
    const rowStyle = {
        display: 'flex',
        marginBottom: '8px',
        alignItems: 'flex-start'
    };

    // 最后一行不需要 margin-bottom
    const lastRowStyle = {
        ...rowStyle,
        marginBottom: '0'
    };

    // 标签样式
    const labelStyle = {
        fontWeight: '600',
        marginRight: '8px',
        flexShrink: 0,
        whiteSpace: 'nowrap',
        width: labelWidth
    };

    // 值样式
    const valueStyle = {
        flex: 1,
        wordBreak: 'break-word'
    };

    // 计算是否需要显示最后一行
    const hasLastUpdated = !!lastUpdated;
    const hasProduct = !!product;
    const hasPlatform = !!platform;

    return (
        <div style={containerStyle}>
            {hasProduct && (
                <div style={hasPlatform || hasLastUpdated ? rowStyle : lastRowStyle}>
                    <span style={labelStyle}>{labels.productLabel}</span>
                    <span style={valueStyle}>{product}</span>
                </div>
            )}
            {hasPlatform && (
                <div style={hasLastUpdated ? rowStyle : lastRowStyle}>
                    <span style={labelStyle}>{labels.platformLabel}</span>
                    <span style={valueStyle}>{platform}</span>
                </div>
            )}
            {hasLastUpdated && (
                <div style={lastRowStyle}>
                    <span style={labelStyle}>{labels.lastUpdatedLabel}</span>
                    <span style={valueStyle}>{lastUpdated}</span>
                </div>
            )}
        </div>
    );
};

export default ArticleMetadata;

