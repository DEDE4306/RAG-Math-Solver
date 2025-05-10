<template>
    <div class="chat-app">
        <h1>{{ sessionTitle }}</h1>
        <div class="chat-container">
            <div class="message-list" ref="messageList">
                <div 
                    v-for="message in messages" 
                    :key="message.messageid"
                    :class="['message-bubble', message.role, { 'pending': message.status === 'pending' }]"
                >
                    <div class="message-content">
                        {{ message.content }}
                    </div>
                    <span v-if="message.status === 'pending' && message.role === 'user'" class="status">发送中...</span>
                </div>
            </div>
        
            <div class="input-area">
                <textarea
                    v-model="newMessage"
                    @keydown.enter.exact.prevent="sendMessage"
                    placeholder="输入消息..."
                    rows="1"
                    ref="textarea"
                ></textarea>
                <img
                    src="@/../public/send.png"
                    class="send-button"
                    @click="sendMessage"
                    alt="发送"
                >
            </div>
        </div>
    </div>
</template>
  
<script>
import { nextTick } from 'vue';
import axios from 'axios';
  
export default {
    props: {
        sessionId: {
            type: [String, Number, null],
            default: null
        },
        sessionTitle: {
            type: String,
            default: '新对话'
        }
    },
    data() {
        return {
            messages: [],
            newMessage: '',
            isNewSession: false // 初始化 isNewSession
        };
    },
    watch: {
        sessionId(newVal, oldVal) {
            console.log('sessionId 变化:', { oldVal, newVal, isNewSession: this.isNewSession });
            if (!newVal) {
                console.log('watch 触发 startNewChat');
                this.startNewChat();
            }
            // 移除 loadMessages 调用，依赖 loadSession
        }
    },
    mounted() {
        this.scrollToBottom();
    },
    methods: {
        getCurrentDateTime() {
            const now = new Date();
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        },
      
        loadMessages(sessionId) {
            console.log('loadMessages 调用:', { sessionId, caller: new Error().stack.split('\n')[2] });
            this.messages = [];
            const token = localStorage.getItem("token");
            axios.get(`http://127.0.0.1:4523/m1/6179108-5871515-default/api/chat/getMessageListBySessionid/${sessionId}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                console.log('getMessageListBySessionid 返回:', response.data);
                if (response.data.success) {
                    const sortedMessages = response.data.response.sort((a, b) => {
                        return new Date(a.createdat).getTime() - new Date(b.createdat).getTime();
                    });
                    this.messages = sortedMessages.map(message => ({
                        messageid: message.messageid,
                        role: message.role,
                        content: message.content,
                        createdat: message.createdat
                    }));
                    this.scrollToBottom();
                } else {
                    alert('获取消息列表失败: ' + response.data.msg);
                }
            })
            .catch(error => {
                console.error('getMessageListBySessionid 错误:', error);
                alert('请求消息列表失败，请检查网络或服务器');
            });
        },
      
        startNewChat() {
            console.log('startNewChat 调用');
            this.messages = [];
            this.isNewSession = false;
        },
      
        sendMessage() {
            if (this.newMessage.trim() === '') return;
  
            const tempMessage = {
                messageid: `user-${Date.now()}`,
                role: 'user',
                content: this.newMessage.trim(),
                createdat: this.getCurrentDateTime(),
                status: 'pending'
            };
            this.messages.push(tempMessage);
            console.log('添加临时消息:', tempMessage);
            this.scrollToBottom();
        
            const token = localStorage.getItem("token");
            const messageContent = this.newMessage.trim();
            this.newMessage = '';
  
            setTimeout(() => {
                if (!this.sessionId) {
                    // 新会话：调用 createNewSession
                    this.isNewSession = true;
                    axios.post('http://127.0.0.1:4523/m1/6179108-5871515-default/api/chat/createNewSession', {
                        content: messageContent
                    }, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    })
                    .then(response => {
                        console.log('createNewSession 返回:', response.data);
                        if (response.data.success) {
                            // 移除临时消息
                            this.messages = this.messages.filter(msg => msg.messageid !== tempMessage.messageid);
                            // 添加后端返回的消息列表
                            this.messages = response.data.response.messages.sort((a, b) => {
                                return new Date(a.createdat).getTime() - new Date(b.createdat).getTime();
                            });
                            console.log('更新消息列表:', this.messages);
                            this.scrollToBottom();
                            // 通知父组件更新会话信息
                            this.$emit('update-session', {
                                sessionId: response.data.response.sessionid,
                                title: response.data.response.title || '新对话'
                            });
                            // 重置 isNewSession
                            this.isNewSession = false;
                        } else {
                            this.isNewSession = false;
                            this.messages = this.messages.filter(msg => msg.messageid !== tempMessage.messageid);
                            this.newMessage = messageContent;
                            alert('创建新对话失败: ' + response.data.msg);
                        }
                    })
                    .catch(error => {
                        console.error('createNewSession 错误:', error);
                        this.isNewSession = false;
                        this.messages = this.messages.filter(msg => msg.messageid !== tempMessage.messageid);
                        this.newMessage = messageContent;
                        alert('创建新对话失败，请检查网络或服务器');
                    });
                } else {
                    // 现有会话：调用 sendMessage
                    axios.post('http://127.0.0.1:4523/m1/6179108-5871515-default/api/chat/sendMessage', {
                        sessionid: this.sessionId,
                        content: messageContent
                    }, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    })
                    .then(response => {
                        console.log('sendMessage 返回:', response.data);
                        if (response.data.success) {
                            const userMessageIndex = this.messages.findIndex(msg => msg.messageid === tempMessage.messageid);
                            if (userMessageIndex !== -1) {
                                this.messages[userMessageIndex].status = 'success';
                            }
                            this.messages.push({
                                messageid: response.data.response.messageid,
                                role: response.data.response.role,
                                content: response.data.response.content,
                                createdat: response.data.response.createdat
                            });
                            console.log('更新消息列表:', this.messages);
                            this.scrollToBottom();
                        } else {
                            this.messages = this.messages.filter(msg => msg.messageid !== tempMessage.messageid);
                            this.newMessage = messageContent;
                            alert('发送消息失败: ' + response.data.msg);
                        }
                    })
                    .catch(error => {
                        console.error('sendMessage 错误:', error);
                        this.messages = this.messages.filter(msg => msg.messageid !== tempMessage.messageid);
                        this.newMessage = messageContent;
                        alert('发送消息失败，请检查网络或服务器');
                    });
                }
            }, 2000);
        },
      
        scrollToBottom() {
            nextTick(() => {
                if (this.$refs.messageList) {
                    this.$refs.messageList.scrollTop = this.$refs.messageList.scrollHeight;
                }
            });
        }
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
.chat-app {
    display: flex;
    flex-direction: column;
}
h1 {
    font-size: 30px;
    font-weight: bold;
    color: #000;
    margin-bottom: 30px;
    margin-top: 30px;
}
.chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
    background-color: #ffffff;
    overflow: hidden;
}
.message-list {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
    margin: 0 auto;
}
.message-bubble {
    max-width: 70%;
    padding: 12px 15px;
    border-radius: 18px;
    position: relative;
    word-wrap: break-word;
    text-align: left;
    font-size: 18px;
}
.message-bubble.assistant {
    margin-left: 5%;
    align-self: flex-start;
    background-color: #f0f0f0;
    border-bottom-left-radius: 4px;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}
.message-bubble.user {
    margin-right: 5%;
    align-self: flex-end;
    background: linear-gradient(to right, #3f51b5, #7498ff);
    color: white;
    border-bottom-right-radius: 4px;
    box-shadow: 0 -3px 10px rgba(0, 0, 0, 0.2);
}
.message-bubble.pending {
    opacity: 0.7;
}
.status {
    display: block;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
    text-align: right;
    margin-right: 10px;
    margin-top: 10px;
}
.input-area {
    display: flex;
    gap: 10px;
    padding: 10px;
    background-color: #fff;
    border-radius: 15px;
    width: 90%;
    height: 67px;
    margin: 0 auto;
    margin-bottom: 30px;
}
textarea {
    flex: 1;
    padding: 10px;
    border: 1px solid rgba(0, 0, 0, 0.15);
    border-radius: 15px;
    resize: none;
    max-height: 150px;
    outline: none;
    font-family: inherit;
    font-size: 18px;
}
textarea::-webkit-scrollbar {
    width: 6px;
}
textarea::-webkit-scrollbar-button {
    display: none;
}
textarea::-webkit-scrollbar-thumb {
    background-color: #ccc;
    border-radius: 15px;
}
textarea::-webkit-scrollbar-track {
    background-color: transparent;
    border-radius: 15px;
    margin: 2px;
}
.send-button {
    cursor: pointer;
    transition: transform 0.2s;
}
</style>