import React from 'react';
import { useFilters } from './FaqFilters.jsx';
import { matchFaq } from './faqMatch.js';
import { allProducts, allPlatforms } from './faqDimensions.js';

// 单条 FAQ 是否命中当前筛选。匹配逻辑统一收敛到 faqMatch.js，
// 使「浏览器端手选」与「脚本端按 instance.id 过滤」命中集合完全一致。
//
// 注意：allProducts/allPlatforms 来自同目录的 faqDimensions.js（每语言各一份），
// 所以哨兵值随语言自动正确。旧的 language prop 仅为兼容已有标注、不再使用。
const FilteredLink = ({ children, href, product, platform }) => {
    const { product: selectedProduct, platform: selectedPlatform } = useFilters();

    const matched = matchFaq(
        { product, platform },
        { product: selectedProduct, platform: selectedPlatform },
        allProducts,
        allPlatforms
    );

    if (!matched) {
        return null;
    }

    return (
        <li>
            <a href={href}>{children}</a>
        </li>
    );
};

export default FilteredLink;
