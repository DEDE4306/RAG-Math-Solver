<template>
    <div class="history-sidebar">
        <!-- 顶部系统名称 -->
        <div class="sidebar-header">
            <div class="header-content">
                <h1>MathSage</h1>
                <img src="../assets/logo1.png" alt="Logo" class="header-logo">
            </div>
            <div class="header-decoration"></div>
        </div>    
        
        <!-- 开始新对话按钮 -->
        <div class="new-chat-btn" @click="startNewChat">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14m-7-7h14"/>
            </svg>
            开启新对话
        </div>      
        
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
            <div class="loading-spinner">
                <div class="spinner"></div>
            </div>
            加载中...
        </div>
    
        <!-- 历史对话列表 -->
        <div class="history-list">
            <div 
                v-for="session in sessions" 
                :key="session.sessionid"
                class="history-item"
                :class="{ 'active': activeSessionId === session.sessionid }"
                @click="debouncedSelectSession(session.sessionid, session.title)"
            >
                <div class="history-item-content">
                    <svg class="chat-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    </svg>
                    <span class="history-title">{{ session.title }}</span>
                </div>
            </div>
        </div>
        
        <UserProfile />
    </div>
</template>

<script>
import axios from 'axios';
import _ from 'lodash'; // 引入 lodash 用于防抖
import UserProfile from './UserProfile.vue';

export default {
    name: 'HistorySidebar',
    components: {
        UserProfile,
    },
    data() {
        return {
            sessions: [],
            activeSessionId: null,
            loading: false
        }
    },
    mounted() {
        this.fetchHistoricalSessions();
    },
    methods: {
        refreshSessions() {
            console.log('refreshSessions 调用');
            this.fetchHistoricalSessions();
        },
    
        async fetchHistoricalSessions() {
            console.log('fetchHistoricalSessions 调用');
            this.loading = true;
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get('http://110.42.205.158:5000/api/chat/getHistoricalSessions', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
        
                const data = response.data;
                if (data.success) {
                    this.sessions = data.response;
                    // 选择最新的会话（可选：根据需求调整）
                    if (this.sessions.length > 0 && !this.activeSessionId) {
                        const latestSession = this.sessions[0];
                        this.selectSession(latestSession.sessionid, latestSession.title);
                    }
                } else {
                    alert(`获取历史记录失败: ${data.msg || '未知错误'}`);
                }
            } catch (err) {
                let errorMsg = '网络错误，请重试';
                if (err.response) {
                    if (err.response.status === 401) {
                        errorMsg = '暂未登录，请登录';
                        this.$router.push('/login1');
                        alert(errorMsg);
                    }
                } else if (err.request) {
                    errorMsg = '无法连接到服务器';
                    alert(errorMsg);
                }
                console.error('获取历史记录错误:', err);
            } finally {
                this.loading = false;
            }
        },
    
        selectSession(sessionId, title) {
            console.log('selectSession 调用:', { sessionId, title });
            if (this.activeSessionId !== sessionId) {
                this.activeSessionId = sessionId;
                this.$emit('session-selected', { sessionId, title });
            }
        },
    
        startNewChat() {
            console.log('startNewChat 调用');
            this.activeSessionId = null;
            this.$emit('new-chat');
        },
    
        addSession(session, replaceSessionId = null) {
            console.log('addSession 调用:', { session, replaceSessionId });
            if (replaceSessionId) {
                // 替换旧会话
                const index = this.sessions.findIndex(s => s.sessionid === replaceSessionId);
                if (index !== -1) {
                    this.sessions.splice(index, 1, {
                        sessionid: session.sessionid,
                        title: session.title
                    });
                } else {
                    // 如果未找到旧会话，添加新会话
                    if (!this.sessions.some(s => s.sessionid === session.sessionid)) {
                        this.sessions.unshift(session);
                    }
                }
            } else {
                // 更新或添加会话
                const index = this.sessions.findIndex(s => s.sessionid === session.sessionid);
                if (index !== -1) {
                    // 更新现有会话的标题
                    this.sessions.splice(index, 1, {
                        sessionid: session.sessionid,
                        title: session.title
                    });
                } else {
                    // 添加新会话
                    this.sessions.unshift(session);
                }
            }
            this.activeSessionId = session.sessionid;
        },
    
        debouncedSelectSession: _.debounce(function (sessionId, title) {
            this.selectSession(sessionId, title);
        }, 300)
    }
}
</script>

<style scoped>
.history-sidebar {
    width: 300px;
    height: 100vh;
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    display: flex;
    flex-direction: column;
    padding: 0;
    box-sizing: border-box;
    position: relative;
    overflow: hidden;
}

.history-sidebar::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 100%);
    pointer-events: none;
}

.sidebar-header {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding: 20px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.sidebar-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    position: relative;
    z-index: 1;
}

.sidebar-header h1 {
    margin: 0;
    font-size: 32px;
    font-weight: 700;
    color: white;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    letter-spacing: -0.5px;
    line-height: 1;
}

.header-logo {
    height: 40px;
    width: auto;
    object-fit: contain;
    opacity: 0.9;
    transition: all 0.3s ease;
}

.header-logo:hover {
    opacity: 1;
    transform: scale(1.05);
}

.header-decoration {
    position: absolute;
    bottom: 0;
    left: 20px;
    right: 20px;
    height: 3px;
    background: linear-gradient(90deg, #3f51b5, #7c4dff, #2196f3);
    border-radius: 2px;
}

.new-chat-btn {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8));
    color: #667eea;
    padding: 16px 24px;
    margin: 20px;
    border-radius: 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 16px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    transform: translateY(0);
}

.new-chat-btn:hover {
    background: linear-gradient(135deg, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0.95));
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    color: #5a67d8;
}

.new-chat-btn:active {
    transform: translateY(0);
}

.history-list {
    flex: 1;
    overflow-y: auto;
    padding: 0 15px 20px;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.history-list::-webkit-scrollbar {
    width: 6px;
}

.history-list::-webkit-scrollbar-track {
    background: transparent;
}

.history-list::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
}

.history-item {
    margin-bottom: 8px;
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 15px;
    display: flex;
    align-items: center;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
    position: relative;
    transform: translateY(0);
    animation: itemSlideIn 0.4s ease-out;
}

@keyframes itemSlideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.history-item:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
}

.history-item.active {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.15));
    color: white;
    border-color: rgba(255, 255, 255, 0.4);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
}

.history-item.active::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(to bottom, #3f51b5, #7c4dff);
    border-radius: 0 4px 4px 0;
}

.history-item-content {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    width: 100%;
    color: rgba(255, 255, 255, 0.9);
}

.history-item.active .history-item-content {
    color: white;
}

.chat-icon {
    opacity: 0.7;
    transition: opacity 0.3s ease;
    flex-shrink: 0;
}

.history-item:hover .chat-icon,
.history-item.active .chat-icon {
    opacity: 1;
}

.history-title {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 500;
    line-height: 1.4;
}

.loading-state {
    padding: 20px;
    text-align: center;
    color: rgba(255, 255, 255, 0.8);
    font-size: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}

.loading-spinner {
    display: flex;
    justify-content: center;
    align-items: center;
}

.spinner {
    width: 24px;
    height: 24px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-top: 3px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .history-sidebar {
        width: 280px;
    }
    
    .sidebar-header h1 {
        font-size: 28px;
    }
    
    .header-logo {
        height: 35px;
    }
    
    .header-content {
        gap: 10px;
    }
    
    .sidebar-header h1 {
        font-size: 28px;
    }
    
    .new-chat-btn {
        margin: 15px;
        padding: 14px 20px;
        font-size: 15px;
    }
    
    .history-item-content {
        padding: 12px 16px;
    }
    
    .history-title {
        font-size: 14px;
    }
}

/* 暗色模式适配 */
@media (prefers-color-scheme: dark) {
    .new-chat-btn {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
    }
    
    .new-chat-btn:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0.95));
    }
}

.history-sidebar :deep(.user-profile) {
    height: 98px; /* 与 ChatComponent 输入区域高度一致 */
}
</style>