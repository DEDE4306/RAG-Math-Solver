<template>
    <div class="chat-app">
      <div class="chat-header">
        <h1>{{ sessionTitle }}</h1>
        <div class="header-decoration"></div>
      </div>
      <div class="chat-container">
        <div class="message-list" ref="messageList">
          <div
            v-for="message in messages"
            :key="message.messageid"
            class="message-bubble"
            :class="[message.role, { 'pending': message.status === 'pending' }]"
            @mouseenter="showEditButton(message.messageid)"
            @mouseleave="hideEditButton(message.messageid)"
          >
            <!-- 正常消息显示 -->
            <div v-if="editingMessageId !== message.messageid || message.role !== 'user'" class="message-content-wrapper">
              <div class="message-content" v-html="renderMessage(message.content)"></div>
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
                    placeholder="编辑消息..."
                    :disabled="isEditingSubmitting"
                ></textarea>
                <div class="edit-buttons">
                    <button 
                        @click="submitEditedMessage(message.messageid)" 
                        class="btn-confirm"
                        :disabled="isEditingSubmitting"
                    >
                        <template v-if="!isEditingSubmitting">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="20,6 9,17 4,12"></polyline>
                            </svg>
                            提交
                        </template>
                        <template v-else>
                            <div class="typing-indicator">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                            发送中...
                        </template>
                    </button>
                    <button 
                        @click="cancelEditing" 
                        class="btn-cancel"
                        :disabled="isEditingSubmitting"
                    >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                        取消
                    </button>
                </div>
            </div>
            <span v-if="message.status === 'pending' && message.role === 'user'" class="status">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              发送中...
            </span>
          </div>
        </div>
  
        <div class="input-area">
          <div class="input-wrapper">
            <textarea
              v-model="newMessage"
              @keydown.enter.exact.prevent="sendMessage"
              placeholder="输入你的问题..."
              rows="1"
              ref="textarea"
            ></textarea>
            <button class="upload-button" @click="triggerFileUpload" :disabled="uploading">
                <svg v-if="!uploading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                    <circle cx="8.5" cy="8.5" r="1.5"/>
                    <polyline points="21,15 16,10 5,21"/>
                </svg>
                <div v-else class="upload-spinner"></div>
            </button>
            <input 
                ref="fileInput" 
                type="file" 
                accept="image/jpeg,image/jpg,image/png" 
                @change="handleFileUpload" 
                style="display: none"
            >
            <button class="send-button" @click="sendMessage" :disabled="!newMessage.trim()">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22,2 15,22 11,13 2,9 22,2"></polygon>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import { nextTick } from 'vue';
import axios from 'axios';
import { PencilIcon } from '@heroicons/vue/24/solid';
import MarkdownIt from 'markdown-it';
import katex from 'katex';
import 'katex/dist/katex.min.css'; // 引入 KaTeX 样式

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
    isEditingSubmitting: false, // 添加编辑提交状态
    hoveredMessageId: null,
    editingMessageId: null,
    editingMessageContent: '',
    uploading: false,
    md: new MarkdownIt() // 初始化 markdown-it
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

        // 渲染消息内容，处理 Markdown 和 LaTeX
        renderMessage(content) {
            const latexPlaceholder = '__LATEX__';
            const latexExpressions = [];
            let index = 0;

            // 保护 $...$ 表达式（行内公式）
            let protectedContent = content.replace(/\$([\s\S]*?)\$/g, (match) => {
                if (match.startsWith('$$')) return match; // 跳过 $$...$$
                latexExpressions.push(match);
                return `${latexPlaceholder}${index++}`;
            });

            // 保护 $$...$$ 表达式（块级公式）
            protectedContent = protectedContent.replace(/\$\$([\s\S]*?)\$\$/g, (match) => {
                latexExpressions.push(match);
                return `${latexPlaceholder}${index++}`;
            });

            // 保护 \(...\) 表达式（行内公式）
            protectedContent = protectedContent.replace(/\\\(([\s\S]*?)\\\)/g, (match) => {
                latexExpressions.push(match);
                return `${latexPlaceholder}${index++}`;
            });

            // 使用 markdown-it 渲染非 LaTeX 部分
            let htmlContent = this.md.render(protectedContent);

            // 恢复并渲染 LaTeX 表达式
            latexExpressions.forEach((latex, i) => {
                let tex = latex;
                let displayMode = false;

                // 根据 LaTeX 语法类型提取内容
                if (latex.startsWith('$$') && latex.endsWith('$$')) {
                    tex = latex.slice(2, -2); // 移除 $$...$$
                    displayMode = true;
                } else if (latex.startsWith('\\(') && latex.endsWith('\\)')) {
                    tex = latex.slice(2, -2); // 移除 \(...\)
                } else if (latex.startsWith('$') && latex.endsWith('$')) {
                    tex = latex.slice(1, -1); // 移除 $...$
                }

                try {
                    // 使用 katex 渲染 LaTeX
                    const rendered = katex.renderToString(tex.trim(), { displayMode, throwOnError: false });
                    htmlContent = htmlContent.replace(`${latexPlaceholder}${i}`, rendered);
                } catch (e) {
                    console.error('KaTeX 渲染错误:', e, 'LaTeX 内容:', latex);
                    // 如果渲染失败，显示原始内容并标记为错误
                    htmlContent = htmlContent.replace(`${latexPlaceholder}${i}`, `<span class="latex-error">${tex}</span>`);
                }
            });

            return htmlContent;
        },
      
        loadMessages(sessionId) {
            console.log('loadMessages 调用:', { sessionId, caller: new Error().stack.split('\n')[2] });
            this.messages = [];
            const token = localStorage.getItem("token");
            axios.get(`http://110.42.205.158:5000/api/chat/getMessageListBySessionid/${sessionId}`, {
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
                    axios.post('http://110.42.205.158:5000/api/chat/createNewSession', {
                        content: messageContent
                    }, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    })
                    .then(response => {
                        console.log('createNewSession 返回:', response.data);
                        // 成功发送后，移除临时消息
                        this.messages = this.messages.filter(
                            msg => msg.messageid !== tempMessage.messageid
                        );
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
                    axios.post('http://110.42.205.158:5000/api/chat/sendMessage', {
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
                        // 成功发送后，移除临时消息
                        this.messages = this.messages.filter(
                            msg => msg.messageid !== tempMessage.messageid
                        );
                        if (response.data.success) {
                            // this.messages = this.messages.filter(msg => msg.messageid !== tempMessage.messageid);
                            let messagesResponse = response.data.response.messages.map(message => ({
                                messageid: message.messageid,
                                role: message.role,
                                content: message.content,
                                createdat: message.createdat
                            })).sort((a, b) => {
                                return new Date(a.createdat).getTime() - new Date(b.createdat).getTime();
                            });
                            let message1 = messagesResponse[0];
                            let message2 = messagesResponse[1];
                            this.messages.push({
                                messageid: message1.messageid,
                                role: 'user',
                                content: message1.content,
                                createdat: message1.createdat
                            });
                            this.messages.push({
                                messageid: message2.messageid,
                                role: message2.role,
                                content: message2.content,
                                createdat: message2.createdat || this.getCurrentDateTime()
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
            }, 0);
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

            this.isEditingSubmitting = true; // 开始提交

            const token = localStorage.getItem("token");
            axios.put(`http://110.42.205.158:5000/api/chat/editHistoricalMessage/${messageId}`, {
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
                    // 直接更新当前消息列表，不触发会话更新
                    let updatedMessages = response.data.response;
                    this.messages = updatedMessages.map(message => ({
                                messageid: message.messageid, // 确保messageid是字符串
                                role: message.role,
                                content: message.content,
                                createdat: message.createdat
                            })).sort((a, b) => {
                                return new Date(a.createdat) - new Date(b.createdat);
                            });
            
                    // 移除下面这行，避免触发新会话
                    // this.$emit('update-session', {
                    //     sessionId: response.data.response.sessionid,
                    //     title: response.data.response.title || '新对话'
                    // });
                    this.editingMessageId = null;
                    this.editingMessageContent = '';
                    this.scrollToBottom();
                } else {
                    this.isEditingSubmitting = false;
                    alert('编辑消息失败: ' + response.data.msg);
                }
            })
            .catch(error => {
                console.error('editHistoricalMessage 错误:', error);
                this.isEditingSubmitting = false;
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

        triggerFileUpload() {
            this.$refs.fileInput.click();
        },

        async handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
  
            this.uploading = true;
            const formData = new FormData();
            formData.append('file', file);
  
            try {
                const token = localStorage.getItem("token");
                const response = await axios.post('http://110.42.205.158:5000/api/chat/ocr', formData, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                });
    
                if (response.data.success) {
                    this.newMessage = response.data.response;
                } else {
                    alert('图片识别失败: ' + response.data.msg);
                }
            } catch (error) {
                console.error('OCR错误:', error);
                alert('图片上传失败，请重试');
            } finally {
                this.uploading = false;
                event.target.value = '';
            }
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
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}

.chat-app {
    display: flex;
    flex-direction: column;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    position: relative;
}

.chat-header {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding: 20px 30px;
    position: relative;
    overflow: hidden;
}

.chat-header::before {
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

.chat-header h1 {
    font-size: 28px;
    font-weight: 700;
    color: white;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 1;
}

.header-decoration {
    position: absolute;
    bottom: 0;
    left: 30px;
    right: 30px;
    height: 3px;
    background: linear-gradient(90deg, #3f51b5, #7c4dff, #2196f3);
    border-radius: 2px;
}

.chat-container {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 88px);
    background: white;
    margin: 0;
    position: relative;
    border-radius: 20px 20px 0 0;
    box-shadow: 0 -5px 30px rgba(0, 0, 0, 0.1);
}

.message-list {
    flex: 1;
    overflow-y: auto;
    padding: 30px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    background: linear-gradient(to bottom, #f8f9ff, #ffffff);
}

.message-list::-webkit-scrollbar {
    width: 6px;
}

.message-list::-webkit-scrollbar-track {
    background: transparent;
}

.message-list::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #3f51b5, #7c4dff);
    border-radius: 3px;
}

.message-bubble {
    max-width: 75%;
    padding: 16px 20px;
    border-radius: 20px;
    position: relative;
    word-wrap: break-word;
    text-align: left;
    font-size: 16px;
    line-height: 1.5;
    display: flex;
    flex-direction: column;
    transform: translateY(0);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: messageSlideIn 0.4s ease-out;
}

@keyframes messageSlideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message-bubble:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.message-bubble.assistant {
    margin-left: 0;
    align-self: flex-start;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border: 1px solid rgba(99, 102, 241, 0.1);
    color: #2d3748;
    border-bottom-left-radius: 8px;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.1);
    position: relative;
}

.message-bubble.assistant::before {
    content: '';
    position: absolute;
    left: -8px;
    top: 50%;
    transform: translateY(-50%);
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-right: 8px solid #f5f7fa;
}

.message-bubble.user {
    margin-right: 0;
    align-self: flex-end;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 8px;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    position: relative;
}

.message-bubble.user::before {
    content: '';
    position: absolute;
    right: -8px;
    top: 50%;
    transform: translateY(-50%);
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-left: 8px solid #667eea;
}

.message-bubble.pending {
    opacity: 0.7;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 0.7; }
    50% { opacity: 0.9; }
}

.message-content-wrapper {
    position: relative;
    display: flex;
    align-items: flex-start;
}

.message-content {
    flex: 1;
    overflow: visible;
}

.katex { 
    font-size: 1.1em;
}

.edit-button {
    position: absolute;
    bottom: -5px;
    left: -50px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border: none;
    border-radius: 50%;
    padding: 8px;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    opacity: 0;
    transform: translateY(10px) scale(0.8);
}

.message-bubble.user:hover .edit-button,
.edit-button:hover {
    opacity: 1;
    transform: translateY(0) scale(1);
}

.edit-button:hover {
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    transform: translateY(-2px) scale(1.05);
}

.edit-icon {
    width: 16px;
    height: 16px;
    color: white;
}

.edit-input-area {
    display: flex;
    flex-direction: column;
    gap: 15px;
    width: 600px;
}

.edit-textarea {
    width: 100%;
    padding: 15px;
    border: 2px solid rgba(102, 126, 234, 0.2);
    border-radius: 15px;
    resize: none;
    min-height: 80px;
    outline: none;
    font-family: inherit;
    font-size: 16px;
    line-height: 1.5;
    background: rgba(255, 255, 255, 0.9);
    transition: all 0.3s ease;
    box-sizing: border-box;
}

.edit-textarea:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    background: white;
}

.edit-buttons {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
}

.edit-buttons button {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 10px 16px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.btn-confirm {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.btn-confirm:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.btn-cancel {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.btn-cancel:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
    text-align: right;
    margin-top: 8px;
}

.typing-indicator {
    display: flex;
    gap: 3px;
}

.typing-indicator span {
    width: 4px;
    height: 4px;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

.input-area {
    padding: 20px 30px 30px;
    background: white;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.input-wrapper {
    display: flex;
    align-items: flex-end;
    gap: 15px;
    background: white;
    border: 2px solid rgba(102, 126, 234, 0.1);
    border-radius: 25px;
    padding: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.input-wrapper:focus-within {
    border-color: #667eea;
    box-shadow: 0 4px 25px rgba(102, 126, 234, 0.2);
    transform: translateY(-1px);
}

.input-wrapper textarea {
    flex: 1;
    padding: 12px 16px;
    border: none;
    border-radius: 20px;
    resize: none;
    max-height: 120px;
    outline: none;
    font-family: inherit;
    font-size: 16px;
    line-height: 1.5;
    background: transparent;
}

.input-wrapper textarea::placeholder {
    color: #9ca3af;
}

.send-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 50%;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    color: white;
}

.send-button:hover:not(:disabled) {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.send-button:active:not(:disabled) {
    transform: translateY(0) scale(0.95);
}

.send-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

/* 响应式设计 */
@media (max-width: 768px) {
    .message-bubble {
        max-width: 85%;
        font-size: 15px;
        padding: 14px 16px;
    }
    
    .chat-header {
        padding: 15px 20px;
    }
    
    .chat-header h1 {
        font-size: 24px;
    }
    
    .message-list {
        padding: 20px;
        gap: 15px;
    }
    
    .input-area {
        padding: 15px 20px 20px;
    }
}

.upload-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 50%;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    color: white;
    margin-right: 8px;
}

.upload-button:hover:not(:disabled) {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.upload-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.upload-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
</style>