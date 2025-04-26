<template>
    <div class="chat-app">
        <h1> {{ sessionAbstract }} </h1>
        <div class="chat-container">
            <!-- 消息列表 -->
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
        
            <!-- 输入框 -->
            <div class="input-area">
                <textarea
                v-model="newMessage"
                @keydown.enter.exact.prevent="sendMessage"
                placeholder="输入消息..."
                rows="1"
                ref="textarea"
                ></textarea>
                <img
                    src = "@/../public/send.png"
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
    data() {
        return {
            sessionAbstract: '标题标题标题标题标题',
            messages: [],
            newMessage: '',
        };
    },
    created() {
        this.initLoadingMessages()
    },
    mounted() {
        this.scrollToBottom()
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
        initLoadingMessages() {
            const token = localStorage.getItem("token");
            axios.get('http://127.0.0.1:4523/m1/6179108-5871515-default/api/chat/getMessageListBySessionid', {
                "sessionid": 0
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                console.log(response.data.response);
                if (response.data.success) {
                    // 按 createdat 升序排序 response.data.response
                    const sortedMessages = response.data.response.sort((a, b) => {
                        return new Date(a.createdat).getTime() - new Date(b.createdat).getTime();
                    });
                    // 将排序后的消息添加到 messages
                    sortedMessages.forEach(message => {
                        this.messages.push({
                            messageid: message.messageid,
                            role: message.role,
                            content: message.content,
                            createdat: message.createdat
                        });
                    });
                    // 加载消息后滚动到最底部
                    this.scrollToBottom();
                } else {
                    alert('获取消息列表失败: ' + response.data.msg);
                }
            })
            .catch(error => {
                console.error('请求失败:', error);
                alert('请求消息列表失败，请检查网络或服务器');
            });
        },
        // 发送消息
        sendMessage() {
            if (this.newMessage.trim() === '') return;

            // 乐观更新：临时添加用户消息
            const tempMessage = {
                messageid: `user-${Date.now()}`,
                role: 'user',
                content: this.newMessage.trim(),
                createdat: this.getCurrentDateTime(),
                status: 'pending' // 添加状态
            };
            this.messages.push(tempMessage);
            this.scrollToBottom();

            const token = localStorage.getItem("token");
            const messageContent = this.newMessage.trim(); // 保存输入内容
            this.newMessage = '';

            // 模拟服务器延迟（2秒）
            setTimeout(() => {
            axios.post('http://127.0.0.1:4523/m1/6179108-5871515-default/api/chat/sendMessage', {
                'sessionid': 0,
                'content': this.newMessage
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                console.log(response.data.response);
                if(response.data.success) {
                    // 移除临时消息
                    //this.messages = this.messages.filter(msg => msg.messageid !== tempMessage.messageid);
                    // 更新用户消息状态
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
                    this.scrollToBottom();
                } else {
                    // API 返回 success: false
                    this.messages = this.messages.filter(msg => msg.messageid !== tempMessage.messageid);
                    this.newMessage = messageContent; // 恢复输入
                    alert('发送消息失败: ' + response.data.msg);
                }
            })
            .catch(error => {
                // 网络错误或服务器异常
                this.messages = this.messages.filter(msg => msg.messageid !== tempMessage.messageid);
                this.newMessage = messageContent; // 恢复输入
                console.error('发送消息失败:', error);
                alert('发送消息失败，请检查网络或服务器');
            });
            }, 2000); // 模拟 2 秒延迟          
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
    overflow: hidden; /* 禁用所有滚动 */
}
.chat-app {
    position: fixed; /* 使用固定定位确保不产生滚动 */
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
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
    overflow: hidden; /* 禁用容器内部滚动 */
}
.message-list {
    flex: 1;
    overflow-y: auto; /* 只允许消息列表区域滚动 */
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
    margin: 0 auto; /* 水平居中 */
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
    width: 90%; /* 设置宽度为90% */
    height: 67px;
    margin: 0 auto; /* 水平居中 */
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
    width: 6px; /* 滚动条宽度 */
}
textarea::-webkit-scrollbar-button {
    display: none; /* 隐藏滚动条的箭头按钮 */
}
textarea::-webkit-scrollbar-thumb {
    background-color: #ccc; /* 滚动条滑块颜色 */
    border-radius: 15px; /* 与 textarea 的圆角一致 */
}
textarea::-webkit-scrollbar-track {
    background-color: transparent; /* 轨道透明 */
    border-radius: 15px; /* 与 textarea 的圆角一致 */
    margin: 2px; /* 添加内边距，避免滚动条紧贴边缘 */
}
.send-button {
    cursor: pointer; /* 鼠标悬停时显示手型 */
    transition: transform 0.2s;
}
  </style>