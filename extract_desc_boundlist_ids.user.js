// ==UserScript==
// @name         提取文档复用ID列表
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  从页面中提取desc-boundlist元素内的所有文档ID
// @author       Assistant
// @match        https://doc.oa.zego.im/*
// @grant        none
// @run-at       document-end
// ==/UserScript==

(function() {
    'use strict';
    
    // 等待页面完全加载
    function waitForElement(selector, timeout = 15000) {
        return new Promise((resolve) => {
            console.log(`⏳ 等待元素: ${selector}`);
            
            // 立即检查一次
            let element = document.querySelector(selector);
            if (element) {
                console.log(`✅ 立即找到元素: ${selector}`);
                resolve(element);
                return;
            }
            
            let attempts = 0;
            const maxAttempts = Math.floor(timeout / 500);
            
            const observer = new MutationObserver(() => {
                attempts++;
                element = document.querySelector(selector);
                if (element) {
                    console.log(`✅ 经过 ${attempts} 次尝试后找到元素: ${selector}`);
                    observer.disconnect();
                    resolve(element);
                }
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeOldValue: true
            });
            
            // 超时处理
            setTimeout(() => {
                observer.disconnect();
                console.log(`⏰ 等待元素超时: ${selector} (尝试了 ${attempts} 次)`);
                resolve(null);
            }, timeout);
        });
    }
    
    // 多种策略查找元素
    async function findDescBoundlistElement() {
        console.log('🔍 尝试多种策略查找 desc-boundlist 元素...');
        
        // 策略1: 直接查找 .desc-boundlist
        let element = await waitForElement('.desc-boundlist', 5000);
        if (element) {
            console.log('✅ 策略1成功: 找到 .desc-boundlist');
            return element;
        }
        
        // 策略2: 查找包含特定文本的元素
        console.log('🔍 策略2: 查找包含"当前文档被以下文档复用"的元素...');
        const allElements = document.querySelectorAll('*');
        for (let el of allElements) {
            if (el.textContent && el.textContent.includes('当前文档被以下文档复用')) {
                console.log('✅ 策略2成功: 找到包含目标文本的元素');
                // 查找其中的 desc-boundlist 类
                const descElement = el.querySelector('.desc-boundlist') || 
                                   el.closest('.desc-boundlist') ||
                                   (el.classList.contains('desc-boundlist') ? el : null);
                if (descElement) {
                    return descElement;
                }
                return el; // 如果没有desc-boundlist类，返回包含文本的元素
            }
        }
        
        // 策略3: 查找所有包含链接的span元素
        console.log('🔍 策略3: 查找包含多个链接的span元素...');
        const spans = document.querySelectorAll('span');
        for (let span of spans) {
            const links = span.querySelectorAll('a[href*="#"]');
            if (links.length >= 5) { // 如果包含5个或更多的锚点链接
                console.log(`✅ 策略3成功: 找到包含 ${links.length} 个链接的span元素`);
                return span;
            }
        }
        
        console.log('❌ 所有策略都失败了');
        return null;
    }
    
    // 提取ID的主要函数
    async function extractDescBoundlistIds() {
        console.log('🔍 开始查找 desc-boundlist 元素...');
        
        // 使用多种策略查找元素
        const descBoundlistElement = await findDescBoundlistElement();
        
        if (!descBoundlistElement) {
            console.log('❌ 未找到 desc-boundlist 元素');
            
            // 尝试查找所有可能的相似元素进行调试
            const allElements = document.querySelectorAll('*[class*="desc"], *[class*="bound"], *[class*="list"]');
            console.log('🔍 找到可能相关的元素:', allElements.length);
            allElements.forEach((el, index) => {
                if (index < 10) { // 只显示前10个
                    console.log(`  元素${index + 1}:`, el.className, el.tagName);
                }
            });
            
            return [];
        }
        
        console.log('✅ 找到 desc-boundlist 元素:', descBoundlistElement);
        console.log('📄 元素内容预览:', descBoundlistElement.innerHTML.substring(0, 200) + '...');
        
        // 查找所有 a 标签
        const links = descBoundlistElement.querySelectorAll('a');
        console.log(`🔗 在 desc-boundlist 中找到 ${links.length} 个 a 标签`);
        
        const ids = [];
        
        links.forEach((link, index) => {
            const href = link.getAttribute('href');
            const text = link.textContent.trim();
            console.log(`  链接${index + 1}: href="${href}", text="${text}"`);
            
            if (href) {
                // 从 href 中提取数字ID，支持 /zh#16405 这样的格式
                const match = href.match(/#(\d+)$/);
                if (match) {
                    ids.push(match[1]);
                    console.log(`    ✅ 提取到ID: ${match[1]}`);
                } else {
                    console.log(`    ❌ 无法从 "${href}" 中提取ID`);
                }
            } else {
                console.log(`    ❌ 链接没有 href 属性`);
            }
        });
        
        console.log(`🎯 总共提取到 ${ids.length} 个ID:`, ids);
        return ids;
    }
    
    // 创建浮动按钮
    function createFloatingButton() {
        const button = document.createElement('button');
        button.innerHTML = '📋 提取ID';
        button.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        `;
        
        button.addEventListener('mouseenter', () => {
            button.style.background = '#0056b3';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.background = '#007bff';
        });
        
        return button;
    }
    
    // 创建结果展示框
    function createResultDialog(ids) {
        const dialog = document.createElement('div');
        dialog.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 10000;
            background: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            max-width: 500px;
            max-height: 400px;
            overflow-y: auto;
        `;
        
        const title = document.createElement('h3');
        title.textContent = '提取到的文档ID列表';
        title.style.cssText = 'margin-top: 0; color: #333;';
        
        const content = document.createElement('div');
        
        if (ids.length === 0) {
            content.innerHTML = '<p style="color: #999;">未找到任何ID</p>';
        } else {
            const idList = ids.map(id => `"${id}"`).join(',');
            const arrayFormat = `[${idList}]`;
            
            content.innerHTML = `
                <p><strong>找到 ${ids.length} 个ID：</strong></p>
                <div style="background: #f5f5f5; padding: 10px; border-radius: 4px; margin: 10px 0;">
                    <strong>数组格式：</strong><br>
                    <code style="word-break: break-all;">${arrayFormat}</code>
                </div>
                <div style="background: #f5f5f5; padding: 10px; border-radius: 4px; margin: 10px 0;">
                    <strong>逗号分隔：</strong><br>
                    <code>${ids.join(',')}</code>
                </div>
                <div style="background: #f5f5f5; padding: 10px; border-radius: 4px; margin: 10px 0;">
                    <strong>换行分隔：</strong><br>
                    <code style="white-space: pre-line;">${ids.join('\n')}</code>
                </div>
            `;
        }
        
        const buttonContainer = document.createElement('div');
        buttonContainer.style.cssText = 'text-align: right; margin-top: 15px;';
        
        // 复制到剪贴板按钮
        if (ids.length > 0) {
            const copyButton = document.createElement('button');
            copyButton.textContent = '复制数组格式';
            copyButton.style.cssText = `
                background: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                margin-right: 10px;
                cursor: pointer;
            `;
            
            copyButton.addEventListener('click', async () => {
                const arrayFormat = `[${ids.map(id => `"${id}"`).join(',')}]`;
                try {
                    await navigator.clipboard.writeText(arrayFormat);
                    copyButton.textContent = '已복사!';
                    setTimeout(() => {
                        copyButton.textContent = '복사数组格式';
                    }, 2000);
                } catch (err) {
                    console.error('复制失败:', err);
                    // 降级方案
                    const textArea = document.createElement('textarea');
                    textArea.value = arrayFormat;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    copyButton.textContent = '已复制!';
                    setTimeout(() => {
                        copyButton.textContent = '复制数组格式';
                    }, 2000);
                }
            });
            
            buttonContainer.appendChild(copyButton);
        }
        
        // 关闭按钮
        const closeButton = document.createElement('button');
        closeButton.textContent = '关闭';
        closeButton.style.cssText = `
            background: #6c757d;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 12px;
            cursor: pointer;
        `;
        
        closeButton.addEventListener('click', () => {
            document.body.removeChild(dialog);
            document.body.removeChild(overlay);
        });
        
        buttonContainer.appendChild(closeButton);
        
        dialog.appendChild(title);
        dialog.appendChild(content);
        dialog.appendChild(buttonContainer);
        
        // 创建遮罩层
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 9999;
        `;
        
        overlay.addEventListener('click', () => {
            document.body.removeChild(dialog);
            document.body.removeChild(overlay);
        });
        
        document.body.appendChild(overlay);
        document.body.appendChild(dialog);
    }
    
    // 主要执行函数
    async function main() {
        // 创建浮动按钮
        const button = createFloatingButton();
        document.body.appendChild(button);
        
        // 按钮点击事件
        button.addEventListener('click', async () => {
            button.innerHTML = '🔄 提取中...';
            button.disabled = true;
            
            try {
                const ids = await extractDescBoundlistIds();
                
                // 输出到控制台
                console.log('提取到的ID列表:', ids);
                console.log('数组格式:', JSON.stringify(ids));
                
                // 显示结果对话框
                createResultDialog(ids);
                
            } catch (error) {
                console.error('提取ID时出错:', error);
                alert('提取ID时出错，请查看控制台了解详情');
            } finally {
                button.innerHTML = '📋 提取ID';
                button.disabled = false;
            }
        });
        
        // 自动检测并提醒
        setTimeout(async () => {
            const element = document.querySelector('.desc-boundlist');
            if (element) {
                console.log('检测到 desc-boundlist 元素，点击右上角按钮可提取ID列表');
                
                // 自动提取一次并输出到控制台
                const ids = await extractDescBoundlistIds();
                if (ids.length > 0) {
                    console.log('自动提取到的ID列表:', ids);
                    console.log('数组格式:', JSON.stringify(ids));
                }
            }
        }, 2000);
    }
    
    // 暴露调试函数到全局，方便用户在控制台调用
    window.debugDescBoundlist = function() {
        console.log('🐛 开始调试模式...');
        console.log('📄 当前页面URL:', window.location.href);
        console.log('📱 页面加载状态:', document.readyState);
        
        // 查找所有可能的相关元素
        console.log('🔍 查找所有包含"desc"的类名...');
        const descElements = document.querySelectorAll('*[class*="desc"]');
        console.log(`找到 ${descElements.length} 个包含"desc"的元素:`);
        descElements.forEach((el, i) => {
            if (i < 10) console.log(`  ${i+1}. ${el.tagName}.${el.className}`);
        });
        
        console.log('🔍 查找所有包含"bound"的类名...');
        const boundElements = document.querySelectorAll('*[class*="bound"]');
        console.log(`找到 ${boundElements.length} 个包含"bound"的元素:`);
        boundElements.forEach((el, i) => {
            if (i < 10) console.log(`  ${i+1}. ${el.tagName}.${el.className}`);
        });
        
        console.log('🔍 查找包含"复用"文本的元素...');
        const textElements = Array.from(document.querySelectorAll('*')).filter(el => 
            el.textContent && el.textContent.includes('复用')
        );
        console.log(`找到 ${textElements.length} 个包含"复用"的元素:`);
        textElements.forEach((el, i) => {
            if (i < 5) {
                console.log(`  ${i+1}. ${el.tagName}.${el.className}:`, el.textContent.substring(0, 100));
            }
        });
        
        console.log('🔍 查找所有包含锚点链接的元素...');
        const linkElements = document.querySelectorAll('*');
        const elementsWithLinks = [];
        linkElements.forEach(el => {
            const links = el.querySelectorAll('a[href*="#"]');
            if (links.length > 0) {
                elementsWithLinks.push({element: el, linkCount: links.length});
            }
        });
        elementsWithLinks.sort((a, b) => b.linkCount - a.linkCount);
        console.log(`找到 ${elementsWithLinks.length} 个包含锚点链接的元素 (按链接数排序):`);
        elementsWithLinks.slice(0, 10).forEach((item, i) => {
            console.log(`  ${i+1}. ${item.element.tagName}.${item.element.className} (${item.linkCount}个链接)`);
        });
        
        // 尝试直接提取
        return extractDescBoundlistIds();
    };
    
    // 页面加载完成后执行
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', main);
    } else {
        main();
    }
})(); 