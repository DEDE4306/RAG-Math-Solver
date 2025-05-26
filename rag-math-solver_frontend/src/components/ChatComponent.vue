<template>
    <div class="chat-app">
        <h1>{{ sessionTitle }}</h1>
        <div class="chat-container">
            <div class="message-list" ref="messageList">
                <div 
                    v-for="message in messages" 
                    :key="message.messageid"
                    :class="['message-bubble', message.role, { 'pending': message.status === 'pending' }]"
                    @mouseenter="showEditButton(message.messageid)"
                    @mouseleave="hideEditButton(message.messageid)"
                >
                    <!-- 正常消息显示 -->
                    <div v-if="editingMessageId !== message.messageid || message.role !== 'user'" class="message-content">
                        {{ message.content }}
                        <button 
                            v-if="message.role === 'user' && hoveredMessageId === message.messageid && !message.status"
                            class="edit-button"
                            title="编辑"
                            @mouseenter="showEditButton(message.messageid)"
                            @mouseleave="hideEditButton(message.messageid)"
                            @click="startEditing(message)"
                        >
                            <PencilIcon class="edit-icon" />
                        </button>
                    </div>
                    <!-- 编辑模式下的输入框 -->
                    <div v-else class="edit-input-area">
                        <textarea
                            v-model="editingMessageContent"
                            @keydown.enter.exact.prevent="submitEditedMessage(message.messageid)"
                            rows="1"
                            ref="editTextarea"
                            class="edit-textarea"
                        ></textarea>
                        <button @click="submitEditedMessage(message.messageid)">提交</button>
                        <button @click="cancelEditing">取消</button>
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
import { PencilIcon } from '@heroicons/vue/24/solid';

export default {
    components: {
        PencilIcon
    },
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
            isNewSession: false,
            hoveredMessageId: null,
            editingMessageId: null,
            editingMessageContent: ''
        };
    },
    watch: {
        sessionId(newVal, oldVal) {
            console.log('sessionId 变化:', { oldVal, newVal, isNewSession: this.isNewSession });
            if (!newVal) {
                console.log('watch 触发 startNewChat');
                this.startNewChat();
            }
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
            this.editingMessageId = null;
            this.hoveredMessageId = null;
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
                            this.messages = response.data.response.messages.map(message => ({
                                messageid: message.messageid,
                                role: message.role,
                                content: message.content,
                                createdat: message.createdat
                            })).sort((a, b) => {
                                return new Date(a.createdat).getTime() - new Date(b.createdat).getTime();
                            });
                            console.log('更新消息列表:', this.messages);
                            this.scrollToBottom();
                            this.$emit('update-session', {
                                sessionId: response.data.response.sessionid,
                                title: response.data.response.title || '新对话'
                            });
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
                            this.messages = this.messages.filter(msg => msg.messageid !== tempMessage.messageid);
                            this.messages.push({
                                messageid: tempMessage.messageid,
                                role: 'user',
                                content: messageContent,
                                createdat: tempMessage.createdat
                            });
                            this.messages.push({
                                messageid: response.data.response.messageid,
                                role: response.data.response.role,
                                content: response.data.response.content,
                                createdat: response.data.response.createdat || this.getCurrentDateTime()
                            });
                            this.messages.sort((a, b) => {
                                return new Date(a.createdat).getTime() - new Date(b.createdat).getTime();
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
      
        showEditButton(messageId) {
            this.hoveredMessageId = messageId;
        },
      
        hideEditButton(messageId) {
            setTimeout(() => {
                if (this.hoveredMessageId === messageId) {
                    this.hoveredMessageId = null;
                }
            }, 100);
        },
      
        startEditing(message) {
            this.editingMessageId = message.messageid;
            this.editingMessageContent = message.content;
            nextTick(() => {
                if (this.$refs.editTextarea) {
                    this.$refs.editTextarea[0].focus();
                }
            });
        },
      
        cancelEditing() {
            this.editingMessageId = null;
            this.editingMessageContent = '';
        },
      
        submitEditedMessage(messageId) {
            if (this.editingMessageContent.trim() === '') {
                alert('消息内容不能为空');
                return;
            }

            const token = localStorage.getItem("token");
            axios.put(`http://127.0.0.1:4523/m1/6179108-5871515-default/api/chat/editHistoricalMessage/${messageId}`, {
                content: this.editingMessageContent.trim()
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                console.log('editHistoricalMessage 返回:', response.data);
                if (response.data.success) {
                    this.messages = response.data.response.messages.sort((a, b) => {
                        return new Date(a.createdat).getTime() - new Date(b.createdat).getTime();
                    });
                    this.$emit('update-session', {
                        sessionId: response.data.response.sessionid,
                        title: response.data.response.title || '新对话'
                    });
                    this.editingMessageId = null;
                    this.editingMessageContent = '';
                    this.scrollToBottom();
                } else {
                    alert('编辑消息失败: ' + response.data.msg);
                }
            })
            .catch(error => {
                console.error('editHistoricalMessage 错误:', error);
                alert('编辑消息失败，请检查网络或服务器');
            });
        },
      
        scrollToBottom() {
            nextTick(() => {
                if (this.$refs.messageList) {
                    this.$refs.messageList.scrollTop = this.$refs.messageList.scrollHeight;
                }
            });
        },
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
.message-content {
    position: relative;
}
.message-bubble.user::before {
    content: '';
    position: absolute;
    top: 0;
    left: -50px;
    width: 50px;
    height: 100%;
    z-index: -1;
}
.edit-button {
    position: absolute;
    bottom: 0;
    left: -45px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 50%;
    padding: 6px;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: opacity 0.2s ease, transform 0.2s ease;
    opacity: 0;
    transform: translateY(5px);
}
.message-bubble.user:hover .edit-button,
.edit-button:hover {
    opacity: 1;
    transform: translateY(0);
}
.edit-icon {
    width: 16px;
    height: 16px;
    color: #333;
}
.edit-input-area {
    display: flex;
    gap: 10px;
    align-items: flex-end; /* Align buttons to the bottom of the textarea */
}
.edit-textarea {
    flex: 1;
    padding: 10px;
    border: 1px solid rgba(0, 0, 0, 0.15);
    border-radius: 15px;
    resize: none;
    height: 100px;
    width: 690px;
    outline: none;
    font-family: inherit;
    font-size: 18px;
}
.edit-input-area button {
    padding: 8px 12px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
}
.edit-input-area button:first-of-type {
    background-color: #3f51b5;
    color: white;
}
.edit-input-area button:last-of-type {
    background-color: #ccc;
    color: #333;
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