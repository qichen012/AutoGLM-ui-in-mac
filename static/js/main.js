// AutoGLM Cockpit 前端逻辑
const socket = io();
let currentMode = 'normal';

// DOM 元素
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const modeNormalBtn = document.getElementById('mode-normal');
const modeAutoglmBtn = document.getElementById('mode-autoglm');
const screenImage = document.getElementById('screen-image');
const screenPlaceholder = document.getElementById('screen-placeholder');
const startScrcpyBtn = document.getElementById('start-scrcpy-btn');
const adbStatus = document.getElementById('adb-status');
const deviceInfo = document.getElementById('device-info');
const rightPanel = document.querySelector('.right-panel');
const autoglmProcess = document.getElementById('autoglm-process');
const processContent = document.getElementById('process-content');

// 连接事件
socket.on('connect', () => {
    console.log('已连接到服务器');
    addSystemMessage('✅ 已连接到服务器');
    fetchStatus();
});

socket.on('disconnect', () => {
    console.log('与服务器断开连接');
    addSystemMessage('❌ 与服务器断开连接');
});

// 获取状态
function fetchStatus() {
    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            updateStatus(data);
        })
        .catch(err => console.error('获取状态失败:', err));
}

function updateStatus(data) {
    if (data.adb_connected) {
        adbStatus.className = 'status-dot online';
        deviceInfo.textContent = data.device;
    } else {
        adbStatus.className = 'status-dot offline';
        deviceInfo.textContent = '未连接';
    }
}

// 模式切换
modeNormalBtn.addEventListener('click', () => switchMode('normal'));
modeAutoglmBtn.addEventListener('click', () => switchMode('autoglm'));

function switchMode(mode) {
    currentMode = mode;
    socket.emit('switch_mode', { mode });
    
    if (mode === 'normal') {
        modeNormalBtn.classList.add('active');
        modeAutoglmBtn.classList.remove('active');
        rightPanel.classList.remove('autoglm-mode');
        autoglmProcess.style.display = 'none';
        addSystemMessage('🔄 切换到 A 模式：普通聊天');
    } else {
        modeNormalBtn.classList.remove('active');
        modeAutoglmBtn.classList.add('active');
        rightPanel.classList.add('autoglm-mode');
        autoglmProcess.style.display = 'flex';
        
        // 清空左右两侧内容
        if (summaryContent) {
            summaryContent.innerHTML = '<div style="color: #94a3b8; text-align: center; padding: 20px;">等待执行任务...</div>';
        }
        if (detailsContent) {
            detailsContent.innerHTML = '<div style="color: #64748b; text-align: center; padding: 20px;">📡 等待实时日志输出...</div>';
        }
        
        addSystemMessage('🔄 切换到 B 模式：手机控制');
    }
}

// 发送消息
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    socket.emit('send_message', { message });
    userInput.value = '';
    userInput.focus();
}

// 接收消息
socket.on('user_message', (data) => {
    addMessage('user', data.message);
});

let currentAiMessage = null;

socket.on('ai_message_chunk', (data) => {
    if (!currentAiMessage) {
        currentAiMessage = addMessage('ai', data.chunk);
    } else {
        currentAiMessage.textContent += data.chunk;
        scrollToBottom();
    }
});

socket.on('ai_message_complete', (data) => {
    currentAiMessage = null;
    scrollToBottom();
});

socket.on('error', (data) => {
    addSystemMessage(`❌ 错误: ${data.message}`, 'error');
});

// 添加消息到聊天区域
function addMessage(type, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = type === 'user' ? '👤' : '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
    return contentDiv;
}

function addSystemMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    messageDiv.style.justifyContent = 'center';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.style.background = type === 'error' ? '#fee2e2' : '#e0e7ff';
    contentDiv.style.color = type === 'error' ? '#991b1b' : '#3730a3';
    contentDiv.style.textAlign = 'center';
    contentDiv.style.fontSize = '13px';
    contentDiv.textContent = message;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 投屏功能
startScrcpyBtn.addEventListener('click', () => {
    socket.emit('start_scrcpy');
    startScrcpyBtn.textContent = '启动中...';
    startScrcpyBtn.disabled = true;
});

socket.on('scrcpy_started', () => {
    screenPlaceholder.style.display = 'none';
});

socket.on('screen_frame', (data) => {
    screenImage.src = 'data:image/jpeg;base64,' + data.frame;
    screenPlaceholder.style.display = 'none';
});

// ADB 连接
socket.on('adb_status', (data) => {
    if (data.connected) {
        adbStatus.className = 'status-dot online';
        addSystemMessage('✅ ADB 已连接');
    } else {
        adbStatus.className = 'status-dot offline';
        addSystemMessage('❌ ADB 连接失败');
    }
});
// 获取新的DOM元素
const summaryContent = document.getElementById('summary-content');
const detailsContent = document.getElementById('details-content');

// AutoGLM 执行步骤
socket.on('autoglm_step', (data) => {
    addProcessStep(data.type, data.content);
});

function addProcessStep(type, content) {
    // 添加到总结区域（左侧）
    addSummaryItem(type, content);
    
    // 添加到详细日志区域（右侧）
    addDetailLog(type, content);
}

// 添加总结项（左侧简洁版）
function addSummaryItem(type, content) {
    const summaryItem = document.createElement('div');
    summaryItem.className = `summary-item ${type}`;
    
    const typeDiv = document.createElement('div');
    typeDiv.className = 'item-type';
    
    const typeLabels = {
        'thinking': '🤔 思考中',
        'action': '⚡ 执行操作',
        'result': '✅ 执行结果',
        'finish': '🎉 任务完成',
        'error': '❌ 错误'
    };
    
    typeDiv.textContent = typeLabels[type] || '📝 步骤';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'item-content';
    
    // 对于总结区域，只显示关键信息（截断长文本）
    const shortContent = content.length > 100 ? content.substring(0, 100) + '...' : content;
    contentDiv.textContent = shortContent;
    
    summaryItem.appendChild(typeDiv);
    summaryItem.appendChild(contentDiv);
    summaryContent.appendChild(summaryItem);
    
    // 自动滚动到底部
    summaryContent.scrollTop = summaryContent.scrollHeight;
}

// 添加详细日志（右侧详细版）
function addDetailLog(type, content) {
    // 检查是否包含性能指标
    if (content.includes('性能指标') || content.includes('TTFT') || content.includes('延迟')) {
        addPerformanceMetrics(content);
        return;
    }
    
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'log-time';
    const now = new Date();
    timeDiv.textContent = `[${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}]`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'log-content';
    contentDiv.textContent = content;
    
    logEntry.appendChild(timeDiv);
    logEntry.appendChild(contentDiv);
    detailsContent.appendChild(logEntry);
    
    // 自动滚动到底部
    detailsContent.scrollTop = detailsContent.scrollHeight;
}

// 添加性能指标（特殊样式）
function addPerformanceMetrics(content) {
    const perfDiv = document.createElement('div');
    perfDiv.className = 'perf-metrics';
    
    const titleDiv = document.createElement('div');
    titleDiv.className = 'metric-title';
    titleDiv.textContent = '⏱️ 性能指标';
    
    perfDiv.appendChild(titleDiv);
    
    // 解析性能指标
    const lines = content.split('\n');
    lines.forEach(line => {
        if (line.trim() && !line.includes('===') && !line.includes('性能指标')) {
            const metricDiv = document.createElement('div');
            metricDiv.className = 'metric-item';
            
            // 高亮数值部分
            const match = line.match(/([\d.]+[ms|s])/g);
            if (match) {
                const parts = line.split(match[0]);
                metricDiv.innerHTML = parts[0] + `<span class="metric-value">${match[0]}</span>` + (parts[1] || '');
            } else {
                metricDiv.textContent = line;
            }
            
            perfDiv.appendChild(metricDiv);
        }
    });
    
    detailsContent.appendChild(perfDiv);
    detailsContent.scrollTop = detailsContent.scrollHeight;
}
// 监听 AutoGLM 实时日志输出
socket.on('autoglm_realtime_log', (data) => {
    addRealtimeLog(data.content);
});

// 添加实时日志到详细日志区域
function addRealtimeLog(content) {
    if (!content || !content.trim()) return;
    
    // 如果是分隔线，添加视觉分隔符
    if (content.includes('====') || content.includes('----')) {
        const separator = document.createElement('div');
        separator.className = 'log-separator';
        detailsContent.appendChild(separator);
        // 自动滚动
        detailsContent.scrollTop = detailsContent.scrollHeight;
        return;
    }
    
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    
    // 根据内容判断类型并高亮
    if (content.includes('性能指标') || content.includes('TTFT') || content.includes('延迟') || content.includes('⏱️')) {
        logEntry.classList.add('performance');
    } else if (content.includes('思考过程') || content.includes('思考') || content.includes('💭')) {
        logEntry.classList.add('thinking');
    } else if (content.includes('执行动作') || content.includes('动作') || content.includes('🎯') || content.includes('Parsing action')) {
        logEntry.classList.add('action');
    }
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'log-time';
    const now = new Date();
    timeDiv.textContent = `[${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}]`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'log-content';
    contentDiv.textContent = content;
    
    logEntry.appendChild(timeDiv);
    logEntry.appendChild(contentDiv);
    detailsContent.appendChild(logEntry);
    
    // 自动滚动到底部
    detailsContent.scrollTop = detailsContent.scrollHeight;
}

// 初始化
addSystemMessage('👋 欢迎使用 AutoGLM Cockpit');
addSystemMessage('💡 提示：A 模式用于普通对话，B 模式用于控制手机');
