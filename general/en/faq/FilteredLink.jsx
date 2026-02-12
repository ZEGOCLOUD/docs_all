import React from 'react';
import { useFilters } from './FaqFilters.jsx';

const FilteredLink = ({ children, href, product, platform, language = 'zh' }) => {
    const { product: selectedProduct, platform: selectedPlatform } = useFilters();

    // 根据语言设置匹配值
    const allProductsValue = language === 'en' ? 'All' : '全部';
    const allPlatformsValue = language === 'en' ? 'All Platforms' : '全部平台';

    const productList = (product || '').split(',').map(p => p.trim()).filter(Boolean);
    const platformList = (platform || '').split(',').map(p => p.trim()).filter(Boolean);

    // 链接端的“全量”通配判断（确保 platform="全平台" 能匹配任意选择的平台）
    const linkProductIsAll = productList.includes(allProductsValue) || productList.includes('全部') || productList.includes('All');
    const linkPlatformIsAll = platformList.includes(allPlatformsValue) || platformList.includes('全平台') || platformList.includes('All');

    const productMatch = selectedProduct === allProductsValue || linkProductIsAll || productList.includes(selectedProduct);
    const platformMatch = selectedPlatform === allPlatformsValue || linkPlatformIsAll || platformList.includes(selectedPlatform);

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