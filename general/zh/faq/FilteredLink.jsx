import React from 'react';
import { useFilters } from './FaqFilters.jsx';

const FilteredLink = ({ children, href, product, platform, language = 'zh' }) => {
    const { product: selectedProduct, platform: selectedPlatform } = useFilters();

    // 根据语言设置匹配值
    const allProductsValue = language === 'en' ? 'All' : '全部';
    const allPlatformsValue = language === 'en' ? 'All Platforms' : '全部平台';

    const productMatch = selectedProduct === allProductsValue || (product && product.split(',').map(p => p.trim()).includes(selectedProduct));
    const platformMatch = selectedPlatform === allPlatformsValue || (platform && platform.split(',').map(p => p.trim()).includes(selectedPlatform));

    if (productMatch && platformMatch) {
        return (
            <li>
                <a href={href}>{children}</a>
            </li>
        );
    }

    return null;
};

export default FilteredLink; 