<template>
    <div class="history-sidebar">
        <!-- 顶部系统名称 -->
        <div class="sidebar-header">
            <h1>Math Solver</h1>
        </div>      
        <!-- 开始新对话按钮 -->
        <div class="new-chat-btn" @click="startNewChat">
            开启新对话
        </div>      
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
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
                {{ session.title }}
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
                const response = await axios.get('http://127.0.0.1:4523/m1/6179108-5871515-default/api/chat/getHistoricalSessions', {
                    headers: {
                        'Authorization': token,
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
                        errorMsg = '登录已过期，请重新登录';
                        this.$router.push('/login');
                    } else {
                        errorMsg = `服务器错误: ${err.response.status}`;
                    }
                } else if (err.request) {
                    errorMsg = '无法连接到服务器';
                }
                alert(errorMsg);
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
html, body, #app, .chat-app {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}
.history-sidebar {
    width: 300px;
    height: 100vh;
    background-color: #f7f7f8;
    border-right: 3px solid #e5e5e6;
    display: flex;
    flex-direction: column;
    padding: 10px;
    box-sizing: border-box;
    align-items: center;
}  
.sidebar-header {
    padding: 15px 10px;
    text-align: center;
    border-bottom: 1px solid #e5e5e6;
    margin-bottom: 15px;
}  
.sidebar-header h1 {
    margin: 0;
    font-size: 36px;
    font-weight: bold;
    color: #333;
}  
.new-chat-btn {
    background: linear-gradient(to right, #3f51b5, #7498ff);
    color: white;
    padding: 10px 15px;
    height: 40px;
    width: 210px;
    border-radius: 25px;
    text-align: center;
    margin-bottom: 20px;
    cursor: pointer;
    transition: background-color 0.2s;
    font-size: 24px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: normal;
}
.history-list {
    flex: 1;
    overflow-y: auto;
}
.history-item {
    padding: 10px 15px;
    margin-bottom: 5px;
    width: 250px;
    height: 30px;
    border-radius: 15px;
    cursor: pointer;
    text-align: left;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 16px;
    display: flex;
    align-items: center;
    line-height: normal;
}
.history-item:hover {
    background-color: #e8e8e8;
}
.history-item.active {
    background: linear-gradient(to right, #3f51b5, #7498ff);
    color: white;
}
.loading-state {
    padding: 10px;
    text-align: center;
    color: #666;
    font-size: 14px;
}
</style>