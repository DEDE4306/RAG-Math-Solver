<template>
    <div class="chat-app-container">
        <!-- 左侧历史记录栏 -->
        <HistoryChatList 
            ref="historyList"
            @session-selected="loadSession"
            @new-chat="startNewSession"
        />
      
        <!-- 右侧聊天区域 -->
        <ChatComponent 
            ref="chatComponent"
            :session-id="currentSessionId"
            :session-title="currentSessionTitle"
            @update-session="updateSession"
        />
    </div>
</template>
  
<script>
import HistoryChatList from '../components/HistoryChatList.vue'
import ChatComponent from '../components/ChatComponent.vue'
  
export default {
    components: {
        HistoryChatList,
        ChatComponent
    },
    data() {
        return {
            currentSessionId: null,
            currentSessionTitle: '新对话'
        }
    },
    methods: {
        loadSession({ sessionId, title }) {
            console.log('loadSession 调用:', { sessionId, title });
            this.currentSessionId = sessionId
            this.currentSessionTitle = title || '新对话'
            this.$refs.chatComponent.loadMessages(sessionId)
        },
        startNewSession() {
            console.log('startNewSession 调用');
            this.currentSessionId = null
            this.currentSessionTitle = '新对话'
            this.$refs.chatComponent.startNewChat()
        },
        updateSession({ sessionId, title }) {
            console.log('updateSession 调用:', { sessionId, title });
            this.currentSessionId = sessionId
            this.currentSessionTitle = title || '新对话'
            // 仅添加新会话到历史记录，不加载消息
            this.$refs.historyList.addSession({ sessionid: sessionId, title: title || '新对话' })
        }
    }
}
</script>
  
<style scoped>
html, body, #app, .chat-app-container {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}
.chat-app-container {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
}
.chat-component {
    margin-left: 300px;
    flex: 1;
    height: 100vh;
    overflow: hidden;
}
</style>