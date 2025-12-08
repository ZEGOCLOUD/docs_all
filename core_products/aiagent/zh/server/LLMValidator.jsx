import React, { useState, useEffect } from 'react';

const LLMValidator = ({ lang = 'zh' }) => {
  const i18n = {
    zh: { systemprompt: "你是一个友好的助手",title: 'LLM 校验器', vendor: 'LLM 厂商', language: '开发语言', llmConfig: 'LLM 配置', sampleCode: '示例代码', response: '响应结果', requestParams: '实际请求LLM参数', userMessage: '用户消息',userMessageDefault: '你好,请介绍一下你自己', userMessagePlaceholder: '如果Params中没填写messages参数或者messages参数未包含role为user的消息，则使用该值请求LLM。', validate: '校验', validating: '校验中...', success: '校验成功', error: '校验失败', receivedContent: '收到的内容', fullResponse: '完整响应', paramError: '参数错误', caseMismatch: '参数大小写不匹配', invalidParam: '不是有效参数', missingRequired: '缺少必填参数', paramsInvalid: 'Params 值不是一个有效的 Object', paramsJsonError: 'Params JSON 格式错误', trailingComma: '检测到多余的逗号' },
    en: { systemprompt: "You are a friendly assistant", title: 'LLM Validator', vendor: 'LLM Vendor', language: 'Programming Language', llmConfig: 'LLM Configuration', sampleCode: 'Sample Code', response: 'Response', requestParams: 'Actual Request LLM Parameters', userMessage: 'User Message', userMessageDefault: 'Hello, please introduce yourself', userMessagePlaceholder: 'If Params does not contain messages parameter or messages parameter does not include a user role message, this value will be used to request LLM.', validate: 'Validate', validating: 'Validating...', success: 'Validation Successful', error: 'Validation Failed', receivedContent: 'Received Content', fullResponse: 'Full Response', paramError: 'Parameter Error', caseMismatch: 'parameter case mismatch', invalidParam: 'is not a valid parameter', missingRequired: 'Missing required parameter', paramsInvalid: 'Params value is not a valid Object', paramsJsonError: 'Params JSON format error', trailingComma: 'Trailing comma detected' }
  };
  const t = i18n[lang] || i18n.zh;

  const vendors = [
    { id: 'volcengine', name: '火山方舟', url: 'https://ark.cn-beijing.volces.com/api/v3/chat/completions', model: 'doubao-seed-1-6-lite-251015' },
    { id: 'aliyun', name: '阿里云百炼', url: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', model: 'qwen-plus' },
    { id: 'minimax', name: 'MiniMax', url: 'https://api.minimax.chat/v1/text/chatcompletion_v2', model: 'MiniMax-Text-01' },
    { id: 'openai', name: 'OpenAI', url: 'https://api.openai.com/v1/chat/completions', model: 'gpt-4' },
    { id: 'deepseek', name: 'DeepSeek', url: 'https://api.deepseek.com/chat/completions', model: 'deepseek-chat' },
    // { id: 'anthropic', name: 'Anthropic', url: 'https://api.anthropic.com/v1/messages', model: 'claude-3-opus-20240229' },
    // { id: 'baidu', name: '百度千帆', url: 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions', model: 'ERNIE-Bot-4' },
    // { id: 'google', name: 'Google AI', url: 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions', model: 'gemini-pro' },
    // { id: 'moonshot', name: 'Moonshot AI', url: 'https://api.moonshot.cn/v1/chat/completions', model: 'moonshot-v1-8k' },
    // { id: 'stepfun', name: '阶跃星辰', url: 'https://api.stepfun.com/v1/chat/completions', model: 'step-1-8k' },
    // { id: 'zhipu', name: '智谱AI', url: 'https://open.bigmodel.cn/api/paas/v4/chat/completions', model: 'glm-4' },
    { id: 'custom', name: lang === 'zh' ? '自定义/其他' : 'Custom/Other', url: '', model: '' },
  ];

  const languages = ['JavaScript', 'TypeScript', 'Java', 'Go', 'PHP', 'C++', 'C#'];
  const [selectedVendor, setSelectedVendor] = useState(vendors[0]);
  const [selectedLanguage, setSelectedLanguage] = useState('JavaScript');
  const [llmConfig, setLlmConfig] = useState('');
  const [sampleCode, setSampleCode] = useState('');
  const [response, setResponse] = useState('');
  const [requestParams, setRequestParams] = useState('');
  const [isValidating, setIsValidating] = useState(false);
  const [activeTab, setActiveTab] = useState('config');
  const [responseTab, setResponseTab] = useState('response');
  const [userMessage, setUserMessage] = useState('');

  const generateLLMConfig = (vendor, language) => {
    const baseConfig = { Url: vendor.url, ApiKey: 'your_api_key', Model: vendor.model, SystemPrompt: t.systemprompt, Temperature: 0.7, TopP: 0.9, Params: { max_tokens: 16384 } };
    if (language === 'PHP') {
      return `"LLM" => [\n    "Url" => "${baseConfig.Url}",\n    "ApiKey" => "${baseConfig.ApiKey}",\n    "Model" => "${baseConfig.Model}",\n    "SystemPrompt" => "${baseConfig.SystemPrompt}",\n    "Temperature" => ${baseConfig.Temperature},\n    "TopP" => ${baseConfig.TopP},\n    "Params" => ["max_tokens" => ${baseConfig.Params.max_tokens}]\n],`;
    }
    return `"LLM": ${JSON.stringify(baseConfig, null, 4)},`;
  };

  const generateSampleCode = (currentLlmConfig, language) => {
    const configs = {
      JavaScript: `// JavaScript (Node.js) 示例
const https = require('https');

async function registerAgent(agentId, agentName) {
    const action = 'RegisterAgent';
    const body = {
        AgentId: agentId,
        Name: agentName,
        ${currentLlmConfig}
    };

    const data = JSON.stringify(body);
    const options = {
        hostname: 'aigc-aiagent-api.zegotech.cn',
        path: \`/?Action=\${action}\`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': data.length
        }
    };

    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let responseData = '';
            res.on('data', (chunk) => { responseData += chunk; });
            res.on('end', () => { resolve(JSON.parse(responseData)); });
        });
        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

registerAgent('my_agent_id', 'My Agent Name').then(console.log);`,

      TypeScript: `// TypeScript (Node.js) 示例
import * as https from 'https';

async function registerAgent(agentId: string, agentName: string): Promise<any> {
    const action = 'RegisterAgent';
    const body = {
        AgentId: agentId,
        Name: agentName,
        ${currentLlmConfig}
    };

    const data = JSON.stringify(body);
    const options: https.RequestOptions = {
        hostname: 'aigc-aiagent-api.zegotech.cn',
        path: \`/?Action=\${action}\`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': data.length
        }
    };

    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let responseData = '';
            res.on('data', (chunk) => { responseData += chunk; });
            res.on('end', () => { resolve(JSON.parse(responseData)); });
        });
        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

registerAgent('my_agent_id', 'My Agent Name').then(console.log);`,

      Java: `// Java 示例
import java.net.http.*;
import java.net.URI;
import com.google.gson.Gson;
import java.util.*;

public class AgentRegistration {
    public static void registerAgent(String agentId, String agentName) throws Exception {
        String action = "RegisterAgent";
        String url = "https://aigc-aiagent-api.zegotech.cn?Action=" + action;

        Map<String, Object> body = new HashMap<>();
        body.put("AgentId", agentId);
        body.put("Name", agentName);

        // LLM 配置
        Map<String, Object> llm = new HashMap<>();
        ${currentLlmConfig.replace(/"(\w+)":/g, 'llm.put("$1", ').replace(/,\s*$/g, ');')}
        body.put("LLM", llm);

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(new Gson().toJson(body)))
            .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
    }
}`,

      Go: `// Go 示例
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

type LLMConfig struct {
    ${currentLlmConfig.replace(/"(\w+)":\s*"([^"]+)"/g, '$1 string `json:"$1"`\n    ').replace(/"(\w+)":\s*([\d.]+)/g, '$1 float64 `json:"$1"`\n    ')}
}

func registerAgent(agentId, agentName string) error {
    action := "RegisterAgent"
    url := fmt.Sprintf("https://aigc-aiagent-api.zegotech.cn?Action=%s", action)

    body := map[string]interface{}{
        "AgentId": agentId,
        "Name":    agentName,
        ${currentLlmConfig}
    }

    jsonData, _ := json.Marshal(body)
    resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    respBody, _ := ioutil.ReadAll(resp.Body)
    fmt.Println(string(respBody))
    return nil
}`,

      PHP: `// PHP 示例
<?php
function registerAgent($agentId, $agentName) {
    $action = 'RegisterAgent';
    $url = "https://aigc-aiagent-api.zegotech.cn?Action=" . $action;

    $body = [
        'AgentId' => $agentId,
        'Name' => $agentName,
        ${currentLlmConfig}
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);

    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}
?>`,

      'C++': `// C++ 示例 (使用 nlohmann/json 库)
#include <iostream>
#include <string>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

std::string registerAgent(const std::string& agentId, const std::string& agentName) {
    std::string action = "RegisterAgent";
    std::string url = "https://aigc-aiagent-api.zegotech.cn?Action=" + action;

    json body = {
        {"AgentId", agentId},
        {"Name", agentName},
        ${currentLlmConfig}
    };

    CURL* curl = curl_easy_init();
    if(curl) {
        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");

        std::string jsonStr = body.dump();
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonStr.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        CURLcode res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
    return "";
}`,

      'C#': `// C# 示例
using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class AgentRegistration
{
    public static async Task<string> RegisterAgent(string agentId, string agentName)
    {
        string action = "RegisterAgent";
        string url = $"https://aigc-aiagent-api.zegotech.cn?Action={action}";

        var body = new
        {
            AgentId = agentId,
            Name = agentName,
            ${currentLlmConfig.replace(/"(\w+)":/g, '$1 = ').replace(/,\s*$/g, '')}
        };

        using var client = new HttpClient();
        var json = JsonSerializer.Serialize(body);
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        var response = await client.PostAsync(url, content);
        return await response.Content.ReadAsStringAsync();
    }
}`
    };
    return configs[language] || configs.JavaScript;
  };

  // 检测JSON格式问题（特别是尾随逗号）
  const detectJSONIssues = (jsonStr) => {
    const issues = [];

    // 检测对象或数组中的尾随逗号：,} 或 ,]
    const trailingCommaPattern = /,\s*[}\]]/g;
    let match;
    while ((match = trailingCommaPattern.exec(jsonStr)) !== null) {
      const position = match.index;
      // 计算行号和列号
      const beforeMatch = jsonStr.substring(0, position);
      const lineNumber = (beforeMatch.match(/\n/g) || []).length + 1;
      const lastNewline = beforeMatch.lastIndexOf('\n');
      const columnNumber = position - lastNewline;

      issues.push({
        type: 'trailingComma',
        position,
        line: lineNumber,
        column: columnNumber,
        snippet: jsonStr.substring(Math.max(0, position - 20), Math.min(jsonStr.length, position + 20))
      });
    }

    return issues;
  };

  // 校验LLM配置参数
  const validateLLMConfig = (params) => {
    const validParams = ['Url', 'ApiKey', 'Model', 'SystemPrompt', 'Temperature', 'TopP', 'Params', 'AddAgentInfo', 'AgentExtraInfo'];
    const requiredParams = ['Url', 'Model'];
    const errors = [];

    // 检查必填参数
    for (const required of requiredParams) {
      if (!params[required]) {
        errors.push(`${t.missingRequired} ${required}！`);
      }
    }

    // 检查参数拼写和大小写
    for (const key in params) {
      if (!validParams.includes(key)) {
        // 检查是否是大小写错误
        const lowerKey = key.toLowerCase();
        const matchedParam = validParams.find(p => p.toLowerCase() === lowerKey);
        if (matchedParam) {
          errors.push(`${t.paramError}，${matchedParam} ${t.caseMismatch}！`);
        } else {
          errors.push(`${t.paramError}，${key} ${t.invalidParam}！`);
        }
      }
    }

    // 特别校验Params参数
    if (params.Params !== undefined) {
      if (typeof params.Params !== 'object' || params.Params === null || Array.isArray(params.Params)) {
        errors.push(`${t.paramsInvalid}！`);
      }
    }

    return errors;
  };

  const extractLLMParams = (configText) => {
    try {
      const cleanText = configText.trim();

      // 处理JSON格式
      if (cleanText.startsWith('"LLM":')) {
        const jsonStr = cleanText.replace(/^"LLM":\s*/, '').replace(/,\s*$/, '');

        // 先检测常见的JSON格式问题（尾随逗号等）
        const jsonIssues = detectJSONIssues(jsonStr);
        if (jsonIssues.length > 0) {
          const issue = jsonIssues[0];
          if (issue.type === 'trailingComma') {
            return {
              error: `${t.paramsJsonError}：${t.trailingComma}（${lang === 'zh' ? '第' : 'line '}${issue.line}${lang === 'zh' ? '行第' : ' column '}${issue.column}${lang === 'zh' ? '列' : ''}）`
            };
          }
        }

        let params;
        try {
          params = JSON.parse(jsonStr);
        } catch (jsonError) {
          // 尝试提供更详细的错误信息
          const errorMsg = jsonError.message;

          // 检查是否是Params的JSON错误
          if (jsonStr.includes('"Params"')) {
            // 尝试提取Params的值进行单独检查
            const paramsMatch = jsonStr.match(/"Params"\s*:\s*(\{(?:[^{}]|\{[^{}]*\})*\})/);
            if (paramsMatch) {
              const paramsJsonIssues = detectJSONIssues(paramsMatch[1]);
              if (paramsJsonIssues.length > 0) {
                return {
                  error: `${t.paramsJsonError}：Params ${lang === 'zh' ? '内' : 'contains '}${t.trailingComma}`
                };
              }
            }
          }

          return { error: `Params JSON ${lang === 'zh' ? '格式错误' : 'format error'}：${errorMsg}` };
        }
        return params;
      }

      // 处理PHP格式
      if (cleanText.startsWith('"LLM" =>')) {
        const params = {};
        const urlMatch = cleanText.match(/"Url"\s*=>\s*"([^"]*)"/);
        const apiKeyMatch = cleanText.match(/"ApiKey"\s*=>\s*"([^"]*)"/);
        const modelMatch = cleanText.match(/"Model"\s*=>\s*"([^"]*)"/);
        const systemPromptMatch = cleanText.match(/"SystemPrompt"\s*=>\s*"([^"]*)"/);
        const temperatureMatch = cleanText.match(/"Temperature"\s*=>\s*([\d.]+)/);
        const topPMatch = cleanText.match(/"TopP"\s*=>\s*([\d.]+)/);
        const maxTokensMatch = cleanText.match(/"max_tokens"\s*=>\s*(\d+)/);
        if (urlMatch) params.Url = urlMatch[1];
        if (apiKeyMatch) params.ApiKey = apiKeyMatch[1];
        if (modelMatch) params.Model = modelMatch[1];
        if (systemPromptMatch) params.SystemPrompt = systemPromptMatch[1];
        if (temperatureMatch) params.Temperature = parseFloat(temperatureMatch[1]);
        if (topPMatch) params.TopP = parseFloat(topPMatch[1]);
        if (maxTokensMatch) params.Params = { max_tokens: parseInt(maxTokensMatch[1]) };
        return params;
      }

      return { error: lang === 'zh' ? '无法识别配置格式，请检查是否以 "LLM": 或 "LLM" => 开头' : 'Cannot recognize config format, please check if it starts with "LLM": or "LLM" =>' };
    } catch (error) {
      console.error('参数提取失败:', error);
      return { error: `${lang === 'zh' ? '参数提取失败' : 'Parameter extraction failed'}：${error.message}` };
    }
  };

  const validateLLM = async () => {
    setIsValidating(true);
    setResponse('');
    setRequestParams('');

    try {
      // 第一步：提取参数
      const llmParams = extractLLMParams(llmConfig);
      console.log('=== 提取到的LLM参数 ===');
      console.log(llmParams);

      // 第二步：检查提取过程是否有错误
      if (llmParams && llmParams.error) {
        setResponse(`${t.error}: ${llmParams.error}`);
        setIsValidating(false);
        return;
      }

      if (!llmParams) {
        setResponse(`${t.error}: ${lang === 'zh' ? '无法解析LLM配置' : 'Cannot parse LLM configuration'}`);
        setIsValidating(false);
        return;
      }

      // 第三步：校验参数（必填、拼写、类型等）
      const validationErrors = validateLLMConfig(llmParams);
      if (validationErrors.length > 0) {
        setResponse(`${t.error}:\n${validationErrors.join('\n')}`);
        setIsValidating(false);
        return;
      }

      // 第四步：参数校验通过，开始构建请求体并发起请求
      // 构建请求体，优先使用Params中的参数
      const requestBody = {
        model: llmParams.Params?.model || llmParams.Model || 'gpt-3.5-turbo',
        temperature: llmParams.Params?.temperature ?? llmParams.Temperature ?? 0.7,
        top_p: llmParams.Params?.top_p ?? llmParams.TopP ?? 0.9,
        stream: true
      };

      // 处理messages参数
      let messages = [];

      // 1. 如果Params中有messages，使用它
      if (llmParams.Params?.messages && Array.isArray(llmParams.Params.messages)) {
        messages = [...llmParams.Params.messages];
      }

      // 2. 如果设置了SystemPrompt且不为空，必须在messages最前面插入（不是替换）
      if (llmParams.SystemPrompt && llmParams.SystemPrompt.trim() !== '') {
        messages.unshift({ role: 'system', content: llmParams.SystemPrompt });
      }

      // 3. 检查是否包含user消息
      const hasUserMessage = messages.some(msg => msg.role === 'user');

      // 4. 如果没有user消息，添加一条
      if (!hasUserMessage) {
        const userContent = userMessage || t.userMessageDefault;
        messages.push({ role: 'user', content: userContent });
      }

      requestBody.messages = messages;

      // 添加其他Params参数
      if (llmParams.Params) {
        Object.keys(llmParams.Params).forEach(key => {
          if (!['model', 'temperature', 'top_p', 'messages'].includes(key)) {
            requestBody[key] = llmParams.Params[key];
          }
        });
      }

      console.log('=== 发送给OpenAI的请求体 ===');
      console.log('URL:', llmParams.Url);
      console.log('Headers:', {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${llmParams.ApiKey ? '***' : '(empty)'}`
      });
      console.log('Body:', JSON.stringify(requestBody, null, 2));

      // 保存请求参数用于显示
      const paramsDisplay = `URL: ${llmParams.Url}\n\nHeaders:\n${JSON.stringify({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${llmParams.ApiKey || '(empty)'}`
      }, null, 2)}\n\nBody:\n${JSON.stringify(requestBody, null, 2)}`;
      setRequestParams(paramsDisplay);

      const res = await fetch(llmParams.Url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${llmParams.ApiKey || ''}` },
        body: JSON.stringify(requestBody)
      });

      if (!res.ok) {
        const errorText = await res.text();
        setResponse(`${t.error}: HTTP ${res.status} - ${errorText}`);
        setIsValidating(false);
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = '';
      let content = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        fullResponse += chunk;
        const lines = chunk.split('\n');
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            try {
              const parsed = JSON.parse(data);
              if (parsed.choices?.[0]?.delta?.content) content += parsed.choices[0].delta.content;
            } catch (e) {}
          }
        }
      }
      setResponse(`${t.success}!\n\n${t.receivedContent}:\n${content}\n\n${t.fullResponse}:\n${fullResponse}`);
    } catch (error) {
      setResponse(`${t.error}: ${error.message}`);
    } finally {
      setIsValidating(false);
    }
  };

  useEffect(() => {
    const config = generateLLMConfig(selectedVendor, selectedLanguage);
    setLlmConfig(config);
    setSampleCode(generateSampleCode(config, selectedLanguage));
  }, [selectedVendor, selectedLanguage]);

  useEffect(() => {
    if (activeTab === 'sample') {
      setSampleCode(generateSampleCode(llmConfig, selectedLanguage));
    }
  }, [activeTab, llmConfig, selectedLanguage]);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '1200px', margin: '20px auto', padding: '20px', background: '#f8f9fa', border: '1px solid #dee2e6', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
      <div style={{ textAlign: 'center', color: '#333', marginBottom: '15px', fontSize: '20px', fontWeight: 'bold', borderBottom: '2px solid #007bff', paddingBottom: '10px' }}>{t.title}</div>

      <div style={{ display: 'flex', gap: '15px', marginBottom: '15px' }}>
        <div style={{ flex: 1 }}>
          <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold', color: '#495057', fontSize: '14px' }}>{t.vendor}</label>
          <select value={selectedVendor.id} onChange={(e) => setSelectedVendor(vendors.find(v => v.id === e.target.value))} style={{ width: '100%', padding: '10px', border: '1px solid #ced4da', borderRadius: '4px', fontSize: '14px', background: 'white' }}>
            {vendors.map(vendor => (<option key={vendor.id} value={vendor.id}>{vendor.name}</option>))}
          </select>
        </div>
        <div style={{ flex: 1 }}>
          <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold', color: '#495057', fontSize: '14px' }}>{t.language}</label>
          <select value={selectedLanguage} onChange={(e) => setSelectedLanguage(e.target.value)} style={{ width: '100%', padding: '10px', border: '1px solid #ced4da', borderRadius: '4px', fontSize: '14px', background: 'white' }}>
            {languages.map(lang => (<option key={lang} value={lang}>{lang}</option>))}
          </select>
        </div>
      </div>

      <div style={{ marginBottom: '15px', background: 'white', borderRadius: '6px', overflow: 'hidden', border: '1px solid #dee2e6' }}>
        <div style={{ display: 'flex', borderBottom: '1px solid #dee2e6', background: '#f8f9fa' }}>
          <button onClick={() => setActiveTab('config')} style={{ flex: 1, padding: '10px 16px', border: 'none', background: 'transparent', color: activeTab === 'config' ? '#007bff' : '#495057', cursor: 'pointer', fontWeight: activeTab === 'config' ? 'bold' : 'normal', borderBottom: activeTab === 'config' ? '3px solid #007bff' : '3px solid transparent', transition: 'all 0.3s' }}>{t.llmConfig}</button>
          <button onClick={() => setActiveTab('sample')} style={{ flex: 1, padding: '10px 16px', border: 'none', background: 'transparent', color: activeTab === 'sample' ? '#007bff' : '#495057', cursor: 'pointer', fontWeight: activeTab === 'sample' ? 'bold' : 'normal', borderBottom: activeTab === 'sample' ? '3px solid #007bff' : '3px solid transparent', transition: 'all 0.3s' }}>{t.sampleCode}</button>
        </div>
        <div style={{ padding: '12px' }}>
          {activeTab === 'config' && (
            <>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                <label style={{ fontWeight: 'bold', color: '#495057', fontSize: '13px', whiteSpace: 'nowrap' }}>{t.userMessage}</label>
                <input
                  type="text"
                  value={userMessage}
                  onChange={(e) => setUserMessage(e.target.value)}
                  placeholder={t.userMessagePlaceholder}
                  style={{ flex: 1, padding: '10px', border: '1px solid #ced4da', borderRadius: '4px', fontSize: '13px' }}
                />
              </div>
              <textarea value={llmConfig} onChange={(e) => setLlmConfig(e.target.value)} style={{ width: '100%', height: '180px', fontFamily: 'Consolas, Monaco, monospace', fontSize: '13px', padding: '12px', border: '1px solid #ced4da', borderRadius: '4px', resize: 'vertical' }} />
            </>
          )}
          {activeTab === 'sample' && (<textarea value={sampleCode} readOnly style={{ width: '100%', height: '180px', fontFamily: 'Consolas, Monaco, monospace', fontSize: '13px', padding: '12px', border: '1px solid #ced4da', borderRadius: '4px', background: '#f8f9fa', resize: 'vertical' }} />)}
        </div>
      </div>

      <div style={{ marginBottom: '15px', background: 'white', borderRadius: '6px', overflow: 'hidden', border: '1px solid #dee2e6' }}>
        <div style={{ display: 'flex', borderBottom: '1px solid #dee2e6', background: '#f8f9fa' }}>
          <button onClick={() => setResponseTab('response')} style={{ flex: 1, padding: '10px 16px', border: 'none', background: 'transparent', color: responseTab === 'response' ? '#007bff' : '#495057', cursor: 'pointer', fontWeight: responseTab === 'response' ? 'bold' : 'normal', borderBottom: responseTab === 'response' ? '3px solid #007bff' : '3px solid transparent', transition: 'all 0.3s' }}>{t.response}</button>
          <button onClick={() => setResponseTab('params')} style={{ flex: 1, padding: '10px 16px', border: 'none', background: 'transparent', color: responseTab === 'params' ? '#007bff' : '#495057', cursor: 'pointer', fontWeight: responseTab === 'params' ? 'bold' : 'normal', borderBottom: responseTab === 'params' ? '3px solid #007bff' : '3px solid transparent', transition: 'all 0.3s' }}>{t.requestParams}</button>
        </div>
        <div style={{ padding: '12px' }}>
          {responseTab === 'response' && (<textarea value={response} readOnly style={{ width: '100%', height: '150px', fontFamily: 'Consolas, Monaco, monospace', fontSize: '13px', padding: '12px', border: '1px solid #ced4da', borderRadius: '4px', background: '#f8f9fa', resize: 'vertical' }} />)}
          {responseTab === 'params' && (<textarea value={requestParams} readOnly style={{ width: '100%', height: '150px', fontFamily: 'Consolas, Monaco, monospace', fontSize: '13px', padding: '12px', border: '1px solid #ced4da', borderRadius: '4px', background: '#f8f9fa', resize: 'vertical' }} />)}
        </div>
      </div>

      <div style={{ textAlign: 'center', marginTop: '10px' }}>
        <button onClick={validateLLM} disabled={isValidating} style={{ padding: '10px 35px', background: isValidating ? '#6c757d' : '#28a745', color: 'white', border: 'none', borderRadius: '6px', cursor: isValidating ? 'not-allowed' : 'pointer', fontSize: '15px', fontWeight: 'bold', boxShadow: '0 2px 4px rgba(0,0,0,0.2)', transition: 'all 0.3s' }}>
          {isValidating ? t.validating : t.validate}
        </button>
      </div>
    </div>
  );
};

export default LLMValidator;
