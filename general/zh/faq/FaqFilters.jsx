import React, { useState, createContext, useContext, useEffect, useRef } from 'react';

const FilterContext = createContext();

export const useFilters = () => useContext(FilterContext);

export const FaqFilters = ({ children, productData, platformData, language = 'zh' }) => {
    // 根据语言设置默认值和文案
    const getDefaultValues = () => {
        if (language === 'en') {
            return {
                allProducts: 'All',
                allPlatforms: 'All Platforms',
                productLabel: 'Product / Solution:',
                platformLabel: 'Platform / Framework:'
            };
        }
        return {
            allProducts: '全部',
            allPlatforms: '全部平台',
            productLabel: '产品 / 解决方案：',
            platformLabel: '平台 / 框架：'
        };
    };

    const { allProducts, allPlatforms, productLabel, platformLabel } = getDefaultValues();

    const [product, setProduct] = useState(allProducts);
    const [platform, setPlatform] = useState(allPlatforms);
    const [productOpen, setProductOpen] = useState(false);
    const [platformOpen, setPlatformOpen] = useState(false);
    const productRef = useRef(null);
    const platformRef = useRef(null);

    // 点击外部关闭下拉框
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (productRef.current && !productRef.current.contains(event.target)) {
                setProductOpen(false);
            }
            if (platformRef.current && !platformRef.current.contains(event.target)) {
                setPlatformOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const dropdownWrapperStyle = {
        height: '36px',
        background: 'var(--docuo-dropdown-label-bg)',
        borderRadius: '6px',
        border: 'var(--docuo-dropdown-label-border)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '6px 12px',
        marginRight: '10px',
        cursor: 'pointer',
        position: 'relative',
        minWidth: '160px'
    };

    const dropdownWrapperHoverStyle = {
        ...dropdownWrapperStyle,
        background: 'var(--docuo-dropdown-label-bg-hover)'
    };

    const labelStyle = {
        fontSize: '14px',
        fontFamily: 'Inter-Medium',
        fontWeight: '500',
        color: 'var(--docuo-color-primary)',
        lineHeight: '24px',
        whiteSpace: 'nowrap',
        overflow: 'hidden',
        textOverflow: 'ellipsis'
    };

    const iconStyle = {
        fontSize: '12px',
        marginLeft: '6px',
        color: 'var(--docuo-dropdown-icon-color)',
        transition: 'transform 0.3s',
        flexShrink: '0'
    };

    const popupStyle = {
        position: 'absolute',
        top: '40px',
        left: '0',
        right: '0',
        zIndex: '1000',
        display: 'flex',
        flexDirection: 'column',
        gap: '0',
        maxHeight: '258px',
        overflow: 'auto',
        padding: '8px',
        boxShadow: '0px 1px 12px 0px rgba(0, 0, 0, 0.05)',
        borderRadius: '6px',
        border: 'var(--docuo-popup-border)',
        background: 'var(--docuo-popup-bg)'
    };

    const optionStyle = {
        height: '40px',
        flexShrink: '0',
        padding: '6px 8px',
        fontSize: '14px',
        fontFamily: 'Inter-Medium',
        fontWeight: '500',
        color: 'var(--docuo-popup-color)',
        borderRadius: '4px',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center'
    };

    const optionHoverStyle = {
        ...optionStyle,
        background: 'var(--docuo-popup-bg-hover)'
    };

    const activeOptionStyle = {
        ...optionStyle,
        color: 'var(--docuo-color-primary-active)'
    };

    return (
        <FilterContext.Provider value={{ product, platform }}>
            <div style={{ display: 'flex', gap: '20px', marginBottom: '20px', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '14px', color: 'var(--docuo-color-primary)' }}>{productLabel}</span>
                    <div
                        ref={productRef}
                        style={productOpen ? dropdownWrapperHoverStyle : dropdownWrapperStyle}
                        onClick={() => setProductOpen(!productOpen)}
                        onMouseEnter={(e) => {
                            if (!productOpen) {
                                Object.assign(e.target.style, dropdownWrapperHoverStyle);
                            }
                        }}
                        onMouseLeave={(e) => {
                            if (!productOpen) {
                                Object.assign(e.target.style, dropdownWrapperStyle);
                            }
                        }}
                    >
                        <span style={labelStyle}>{product}</span>
                        <span style={{
                            ...iconStyle,
                            transform: productOpen ? 'rotate(-90deg)' : 'rotate(90deg)'
                        }}>▶</span>
                        {productOpen && (
                            <div style={popupStyle}>
                                <div
                                    style={product === allProducts ? activeOptionStyle : optionStyle}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        setProduct(allProducts);
                                        setProductOpen(false);
                                    }}
                                    onMouseEnter={(e) => {
                                        if (product !== allProducts) {
                                            Object.assign(e.target.style, optionHoverStyle);
                                        }
                                    }}
                                    onMouseLeave={(e) => {
                                        if (product !== allProducts) {
                                            Object.assign(e.target.style, optionStyle);
                                        }
                                    }}
                                >
                                    {allProducts}
                                </div>
                                {Object.keys(productData).map(group => (
                                    <div key={group}>
                                        {productData[group].map(item => (
                                            <div
                                                key={item}
                                                style={product === item ? activeOptionStyle : optionStyle}
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    setProduct(item);
                                                    setProductOpen(false);
                                                }}
                                                onMouseEnter={(e) => {
                                                    if (product !== item) {
                                                        Object.assign(e.target.style, optionHoverStyle);
                                                    }
                                                }}
                                                onMouseLeave={(e) => {
                                                    if (product !== item) {
                                                        Object.assign(e.target.style, optionStyle);
                                                    }
                                                }}
                                            >
                                                {item}
                                            </div>
                                        ))}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '14px', color: 'var(--docuo-color-primary)' }}>{platformLabel}</span>
                    <div
                        ref={platformRef}
                        style={platformOpen ? dropdownWrapperHoverStyle : dropdownWrapperStyle}
                        onClick={() => setPlatformOpen(!platformOpen)}
                        onMouseEnter={(e) => {
                            if (!platformOpen) {
                                Object.assign(e.target.style, dropdownWrapperHoverStyle);
                            }
                        }}
                        onMouseLeave={(e) => {
                            if (!platformOpen) {
                                Object.assign(e.target.style, dropdownWrapperStyle);
                            }
                        }}
                    >
                        <span style={labelStyle}>{platform}</span>
                        <span style={{
                            ...iconStyle,
                            transform: platformOpen ? 'rotate(-90deg)' : 'rotate(90deg)'
                        }}>▶</span>
                        {platformOpen && (
                            <div style={popupStyle}>
                                <div
                                    style={platform === allPlatforms ? activeOptionStyle : optionStyle}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        setPlatform(allPlatforms);
                                        setPlatformOpen(false);
                                    }}
                                    onMouseEnter={(e) => {
                                        if (platform !== allPlatforms) {
                                            Object.assign(e.target.style, optionHoverStyle);
                                        }
                                    }}
                                    onMouseLeave={(e) => {
                                        if (platform !== allPlatforms) {
                                            Object.assign(e.target.style, optionStyle);
                                        }
                                    }}
                                >
                                    {allPlatforms}
                                </div>
                                {platformData.map(item => (
                                    <div
                                        key={item}
                                        style={platform === item ? activeOptionStyle : optionStyle}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setPlatform(item);
                                            setPlatformOpen(false);
                                        }}
                                        onMouseEnter={(e) => {
                                            if (platform !== item) {
                                                Object.assign(e.target.style, optionHoverStyle);
                                            }
                                        }}
                                        onMouseLeave={(e) => {
                                            if (platform !== item) {
                                                Object.assign(e.target.style, optionStyle);
                                            }
                                        }}
                                    >
                                        {item}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
            {children}
        </FilterContext.Provider>
    );
};