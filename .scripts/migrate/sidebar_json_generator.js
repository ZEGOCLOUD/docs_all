// ==UserScript==
// @name         ZEGO文档侧边栏结构提取器 - 生成sidebar.json
// @namespace    http://tampermonkey.net/
// @version      2.1
// @description  从旧文档网站提取侧边栏层级结构，生成新格式的sidebar.json。使用递归方式保持目录和文件的原始混合排序，正确处理多span标题
// @author       You
// @match        https://doc-zh.zego.im/article/*
// @match        https://www.zegocloud.com/*
// @match        https://docs.zegocloud.com/article/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // 等待页面加载完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initGenerator);
    } else {
        initGenerator();
    }

    function initGenerator() {
        // 等待一下确保页面完全加载
        setTimeout(() => {
            addGeneratorButton();
            console.log('ZEGO侧边栏结构生成器已加载');
        }, 1000);
    }

    function addGeneratorButton() {
        // 创建生成按钮
        const button = document.createElement('button');
        button.innerHTML = '🏗️ 生成sidebar.json';
        button.style.cssText = `
            position: fixed;
            top: 150px;
            right: 20px;
            z-index: 10000;
            padding: 10px 15px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        `;
        
        button.addEventListener('click', generateSidebarJson);
        document.body.appendChild(button);
    }

    async function generateSidebarJson() {
        console.log('开始生成sidebar.json...');

        // 显示进度提示
        showProgress('正在分析页面结构...');

        try {
            showProgress('正在展开侧边栏...');

            // 先展开所有折叠项
            await expandAllCollapsedItems();

            showProgress('正在提取侧边栏结构...');

            // 提取侧边栏结构
            const sidebarStructure = extractSidebarStructure();

            // 生成sidebar.json格式
            const sidebarJson = generateSidebarJsonFormat(sidebarStructure);

            // 显示结果
            showSidebarJsonResults(sidebarJson);

        } catch (error) {
            console.error('生成过程中出错:', error);
            alert('生成失败: ' + error.message);
        }
    }

    async function expandAllCollapsedItems() {
        let expandedCount = 0;
        let maxIterations = 20;
        let iteration = 0;

        return new Promise((resolve) => {
            function expandIteration() {
                const mainLeftTreeBox = document.getElementById('mainLeftTreeBox');
                let collapsedIcons;

                if (mainLeftTreeBox) {
                    collapsedIcons = mainLeftTreeBox.querySelectorAll('i.icon.zgfont.doc-left_down_default:not(.list-icon-expand)');
                    console.log(`第${iteration + 1}轮: 在 #mainLeftTreeBox 中找到 ${collapsedIcons.length} 个折叠项`);
                } else {
                    collapsedIcons = document.querySelectorAll('i.icon.zgfont.doc-left_down_default:not(.list-icon-expand)');
                    console.log(`第${iteration + 1}轮: 在整个页面找到 ${collapsedIcons.length} 个折叠项`);
                }

                if (collapsedIcons.length === 0 || iteration >= maxIterations) {
                    console.log(`展开完成，总共展开了 ${expandedCount} 个项目`);
                    resolve(expandedCount);
                    return;
                }

                // 点击每个折叠项
                collapsedIcons.forEach((icon, index) => {
                    try {
                        let clickableElement = findClickableParent(icon);
                        if (clickableElement) {
                            console.log(`点击第${index + 1}个折叠项:`, clickableElement);
                            clickableElement.click();
                            expandedCount++;
                        }
                    } catch (e) {
                        console.log('点击失败:', e);
                    }
                });

                iteration++;
                setTimeout(expandIteration, 1500);
            }

            expandIteration();
        });
    }

    function findClickableParent(icon) {
        let element = icon;
        let maxDepth = 10;
        let depth = 0;

        while (element && depth < maxDepth) {
            if (element.tagName === 'A' ||
                element.onclick ||
                element.classList.contains('tree-node-el') ||
                element.classList.contains('clickable') ||
                element.classList.contains('tree-node') ||
                element.classList.contains('node') ||
                element.style.cursor === 'pointer') {
                return element;
            }

            if (element.addEventListener || element.onclick ||
                (element.tagName === 'DIV' && element.children.length > 0) ||
                (element.tagName === 'SPAN' && element.children.length > 0)) {
                return element;
            }

            element = element.parentElement;
            depth++;
        }

        return icon.parentElement;
    }

    function extractSidebarStructure() {
        const mainLeftTreeBox = document.getElementById('mainLeftTreeBox');

        if (!mainLeftTreeBox) {
            console.log('未找到主侧边栏容器');
            return [];
        }

        // 使用递归方式直接从DOM结构提取，保持原始顺序
        const sidebarStructure = extractStructureRecursively(mainLeftTreeBox);

        return sidebarStructure;
    }

    function extractStructureRecursively(container) {
        console.log('开始递归提取侧边栏结构...');

        // 查找顶级的ul元素
        const topLevelUl = container.querySelector('ul.zego-menu-tree');
        if (!topLevelUl) {
            console.log('未找到顶级菜单容器');
            return [];
        }

        // 递归处理顶级ul的直接子li元素
        return processMenuLevel(topLevelUl);
    }

    function processMenuLevel(ulElement) {
        const items = [];

        // 获取当前ul下的直接子li元素
        const directChildren = Array.from(ulElement.children).filter(child => child.tagName === 'LI');

        directChildren.forEach(li => {
            const item = processMenuItem(li);
            if (item) {
                items.push(item);
            }
        });

        return items;
    }

    function processMenuItem(liElement) {
        // 检查是否是目录（dic类）还是文档（docs类）
        const isDirectory = liElement.classList.contains('dic');
        const isDocument = liElement.classList.contains('docs');

        if (isDirectory) {
            return processDirectoryItem(liElement);
        } else if (isDocument) {
            return processDocumentItem(liElement);
        }

        return null;
    }

    function processDirectoryItem(liElement) {
        // 提取目录名称
        const titleSpan = liElement.querySelector('.node-title span');
        if (!titleSpan) {
            return null;
        }

        const directoryName = titleSpan.textContent.trim();
        console.log(`处理目录: ${directoryName}`);

        // 创建目录项
        const category = {
            type: "category",
            label: directoryName,
            collapsed: false,
            items: []
        };

        // 查找子级ul元素
        const childUl = liElement.querySelector('ul.zego-menu-tree');
        if (childUl) {
            // 递归处理子级项目
            const childItems = processMenuLevel(childUl);
            category.items = childItems;
        }

        return category.items.length > 0 ? category : null;
    }

    function processDocumentItem(liElement) {
        // 查找带data-modulename的元素
        const moduleElement = liElement.querySelector('[data-modulename]');
        if (!moduleElement) {
            return null;
        }

        const moduleName = moduleElement.getAttribute('data-modulename');

        // 查找所有span元素
        const titleSpans = moduleElement.querySelectorAll('span');
        if (titleSpans.length === 0) {
            return null;
        }

        // 如果有多个span，使用最后一个作为标题（第一个通常是标签如"基础"）
        const titleSpan = titleSpans[titleSpans.length - 1];
        const documentTitle = titleSpan.textContent.trim();

        // 从moduleName提取articleId
        const parts = moduleName.split('-');
        const lastPart = parts[parts.length - 1];
        let articleId = null;
        if (/^\d+$/.test(lastPart)) {
            articleId = parseInt(lastPart);
        }

        if (!articleId) {
            console.log(`无法提取文档ID: ${moduleName}`);
            return null;
        }

        // 如果有多个span，记录调试信息
        if (titleSpans.length > 1) {
            const allSpanTexts = Array.from(titleSpans).map(span => span.textContent.trim());
            console.log(`处理多span文档: [${allSpanTexts.join(', ')}] -> 选择: "${documentTitle}" (ID: ${articleId})`);
        } else {
            console.log(`处理文档: ${documentTitle} (ID: ${articleId})`);
        }

        return {
            type: "doc",
            label: documentTitle,
            id: `article-${articleId}`,
            articleID: articleId
        };
    }

    function generateSidebarJsonFormat(structure) {
        return {
            mySidebar: structure
        };
    }

    function showSidebarJsonResults(sidebarJson) {
        // 移除进度提示
        const progress = document.getElementById('zego-progress');
        if (progress) {
            progress.remove();
        }

        // 格式化JSON
        const jsonString = JSON.stringify(sidebarJson, null, 2);

        // 复制到剪贴板
        navigator.clipboard.writeText(jsonString).then(() => {
            alert(`成功生成sidebar.json！\n\n包含 ${sidebarJson.mySidebar.length} 个分类\n\nJSON已复制到剪贴板。`);
        }).catch(() => {
            // 如果复制失败，显示在控制台
            console.log('生成的sidebar.json:', sidebarJson);
            alert(`成功生成sidebar.json！\n\n包含 ${sidebarJson.mySidebar.length} 个分类\n\n请查看浏览器控制台获取完整数据。`);
        });

        // 同时在控制台输出
        console.log('=== 生成的sidebar.json ===');
        console.log(jsonString);
    }

    function showProgress(message) {
        // 移除之前的进度提示
        const existingProgress = document.getElementById('zego-progress');
        if (existingProgress) {
            existingProgress.remove();
        }

        // 创建新的进度提示
        const progress = document.createElement('div');
        progress.id = 'zego-progress';
        progress.innerHTML = message;
        progress.style.cssText = `
            position: fixed;
            top: 70px;
            right: 20px;
            z-index: 10001;
            padding: 10px 15px;
            background: #28a745;
            color: white;
            border-radius: 5px;
            font-size: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        `;

        document.body.appendChild(progress);
    }

})();
