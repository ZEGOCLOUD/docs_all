// faqMatch.js — FAQ 过滤的纯匹配逻辑（zh/en 共用同一份，因 allProducts/allPlatforms 由参数传入）。
//
// 被 FilteredLink.jsx（浏览器端）和 .scripts/faq/faq-by-instance.mjs（脚本端）共用，
// 保证「网页手选」与「脚本按 instance.id 过滤」得到完全一致的命中集合（零漂移）。

// 把逗号分隔的标注字符串拆成去空值的数组。
const parseList = (s) =>
    String(s || '')
        .split(',')
        .map((p) => p.trim())
        .filter(Boolean);

// 链接端是否标注为「全量」。把 zh/en 的哨兵值都算进去，避免脏数据导致漏匹配。
const isAllValue = (list, ...sentinels) =>
    sentinels.some((sentinel) => list.includes(sentinel));

// ★ LEARNING —— 这里是整个过滤系统唯一值得你来定的「策略」：
//
//   一个 FAQ 的 product 标注为空（迁移后被清空的老产品 FAQ，如 RoomKit 课堂、下架说明）时，
//   它应当出现在「每个」产品筛选下，还是从所有产品筛选中隐藏？
//
//     'visible-everywhere'：空 product = 不限定产品，任何产品筛选 +「全部」都可见。
//     'hidden'（当前）：空 product 的 FAQ 只在「全部」可见，选具体产品时隐藏。
//
//   选 'hidden'：被清空的多是退役/老产品（屏幕共享、文件共享、RoomKit…）专属 FAQ，
//   不应污染具体产品的筛选结果；用户仍可在「全部」浏览到它们。
export const EMPTY_PRODUCT_BEHAVIOR = 'hidden';

// 核心：判断单条 link 是否命中当前选择。
//   link      : { product, platform } —— FilteredLink 标注（逗号分隔字符串）
//   selection : { product, platform } —— 当前选中值（来自下拉或 ?instance= 解析出的 instanceMap）
//   allProducts / allPlatforms ：「全部」哨兵值
export function matchFaq(link, selection, allProducts, allPlatforms) {
    const productList = parseList(link.product);
    const platformList = parseList(link.platform);

    const selProduct = selection.product;
    const selPlatform = selection.platform;

    // —— product 维度 ——
    const linkProductIsAll = isAllValue(productList, allProducts, '全部', 'All');
    const productEmpty = productList.length === 0;
    let productMatch;
    if (productEmpty) {
        // ★ LEARNING 的策略生效点（见上方常量说明）
        productMatch = EMPTY_PRODUCT_BEHAVIOR === 'visible-everywhere' ? true : selProduct === allProducts;
    } else {
        productMatch =
            selProduct === allProducts ||
            linkProductIsAll ||
            productList.includes(selProduct);
    }

    // —— platform 维度 ——
    const linkPlatformIsAll = isAllValue(platformList, allPlatforms, '全平台', '全部平台', 'All', 'All Platforms');
    const platformMatch =
        selPlatform === allPlatforms ||
        linkPlatformIsAll ||
        platformList.includes(selPlatform);

    return productMatch && platformMatch;
}
