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
        addSystemMessage('🔄 切换到 A 模式：普通聊天');
    } else {
        modeNormalBtn.classList.remove('active');
        modeAutoglmBtn.classList.add('active');
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

// 初始化
addSystemMessage('👋 欢迎使用 AutoGLM Cockpit');
addSystemMessage('💡 提示：A 模式用于普通对话，B 模式用于控制手机');
