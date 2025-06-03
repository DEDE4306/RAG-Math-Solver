<template>
    <div class="registerContainer">
        <div class="form-content">
            <div class="title-section">
                <h1>创建账号</h1>
                <p class="subtitle">加入我们，开始精彩旅程</p>
            </div>
            <div class="form-section">
                <div class="input-wrapper">
                    <div class="input-group">
                        <div class="input-icon">📱</div>
                        <input 
                            type="text" 
                            placeholder="请输入手机号" 
                            v-model="phoneNumber"
                            class="styled-input"
                        />
                    </div>
                </div>
                <div class="input-wrapper">
                    <div class="input-group">
                        <div class="input-icon">📩</div>
                        <input 
                            type="text" 
                            placeholder="请输入验证码" 
                            v-model="code"
                            class="styled-input code-input"
                        />
                        <button 
                            class="send-code" 
                            :disabled="isCounting"
                            @click="sendVerificationCode"
                        >
                            {{ buttonText }}
                        </button>
                    </div>
                </div>
                <div class="input-wrapper">
                    <div class="input-group">
                        <div class="input-icon">👤</div>
                        <input 
                            type="text" 
                            placeholder="请输入用户名" 
                            v-model="username"
                            class="styled-input"
                        />
                        <span class="input-hint">20字符内</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <div class="input-group">
                        <div class="input-icon">🔒</div>
                        <input 
                            type="password" 
                            placeholder="请输入密码" 
                            v-model="password"
                            class="styled-input"
                        />
                        <span class="input-hint">6-20字符</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <div class="input-group">
                        <div class="input-icon">🔐</div>
                        <input 
                            type="password" 
                            placeholder="请确认密码" 
                            v-model="password2"
                            class="styled-input"
                        />
                        <span class="input-hint">重复密码</span>
                    </div>
                </div>
                <div class="avatar-section">
                    <div class="avatar-upload">
                        <div class="avatar-preview" @click="triggerFileInput">
                            <img 
                                :src="avatarPreview || require('@/../public/default-avatar.png')" 
                                class="avatar-image"
                                alt="头像"
                            >
                            <div class="avatar-overlay">
                                <span></span>
                            </div>
                        </div>
                        <input 
                            type="file" 
                            ref="fileInput"
                            @change="handleAvatarUpload"
                            accept="image/*"
                            style="display: none;"
                        >
                        <a href="javascript:;" class="upload-link" @click="triggerFileInput">
                            ✨ 上传头像
                        </a>
                    </div>
                </div>
            </div>
            <div class="action-section">
                <button class="register-button" @click="handleRegister">
                    <span>立即注册</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            avatarPreview: null, // 头像预览URL
            avatarFile: null,   // 存储选择的头像文件
            phoneNumber: '',
            code: '',
            username: '',
            password: '',
            password2: '',
            isCounting: false,
            countdown: 60,
            timer: null
        }
    },
    created() {
        // 组件创建时加载默认头像
        this.loadDefaultAvatar();
    },
    computed: {
        buttonText() {
            return this.isCounting ? `${this.countdown}秒后重试` : '获取验证码';
        }
    },
    methods: {
        goBack() {
            // this.$router.push('/')
            this.$router.go(-1)
        },
        isNumeric(str) { // 测试是否全是数字
          return /^\d+$/.test(str);
        },
        startCountdown() {
            this.isCounting = true;
            this.timer = setInterval(() => {
                this.countdown--;
                if (this.countdown <= 0) {
                    clearInterval(this.timer);
                    this.isCounting = false;
                    this.countdown = 60;
                }
            }, 1000);
        },
        sendVerificationCode() {
            if (!this.phoneNumber) {
                alert('请输入手机号');
                return;
            }
            else if (this.phoneNumber.length != 11 || this.isNumeric(this.phoneNumber) == false) {
                alert('请输入正确手机号');
                return;
            }       
            // 发送验证码请求
            axios.post('http://110.42.205.158:5000/api/account/sendCode', {
                phonenumber: this.phoneNumber
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.data.success) {
                    alert('验证码发送成功');
                    // 开始倒计时
                    this.startCountdown();
                } else {
                    alert('验证码发送失败: ' + response.data.msg);
                }
            })
            .catch(error => {
                console.error('发送验证码出错:', error);
                alert('发送验证码失败: ' + (error.response?.data?.msg || error.message));
            });
        },
        triggerFileInput() {
            this.$refs.fileInput.click();
        },
        async loadDefaultAvatar() {
            try {
                const response = await fetch('/default-avatar.png');
                const blob = await response.blob();
                this.avatarFile = new File([blob], 'default-avatar.png', { type: blob.type });
                this.avatarPreview = URL.createObjectURL(blob);
            } catch (error) {
                console.error('加载默认头像失败:', error);
            }
        },
        handleAvatarUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
      
            // 验证文件类型
            if (!file.type.match('image.*')) {
                alert('请选择图片文件');
                return;
            }
      
            // 验证文件大小 (例如限制2MB)
            if (file.size > 2 * 1024 * 1024) {
                alert('图片大小不能超过2MB');
                return;
            }
      
            // 创建预览URL
            this.avatarPreview = URL.createObjectURL(file);
            this.avatarFile = file;
        },

        hasLetterAndNumber(str) { // 测试是否同时包括数字和字母
            // 检查是否包含字母和数字
            const hasLetter = /[a-zA-Z]/.test(str);
            const hasNumber = /[0-9]/.test(str);

            return hasLetter && hasNumber;
        },
        handleRegister() {
            if (!this.phoneNumber) {
                alert('请输入手机号');
                return;
            }
            if (!this.code) {
                alert('请输入验证码');
                return;
            }
            if (!this.username) {
                alert('请输入用户名');
                return;
            }
            else if (this.username.length > 20) {
                alert('用户名不得超过20个字符');
                return;
            }
            if (!this.password) {
                alert('请输入密码');
                return;
            }
            else if (this.password.length < 6 || this.password.length > 20) {
                alert('密码必须在6-20个字符以内');
                return;
            }
            else if (!this.hasLetterAndNumber(this.password)) {
                alert('密码必须同时包括数字和字母');
                return;
            }
            if (this.password!=this.password2) {
                alert('两次密码输入不一致');
                return;
            }
            // 注册逻辑
            // console.log('OK')
            // 准备要发送的数据
            const formData = new FormData();
            formData.append('phonenumber', this.phoneNumber);
            formData.append('code', this.code);
            formData.append('username', this.username);
            formData.append('password', this.password);
    
            // 如果有头像文件，也添加到表单数据中
            if (this.avatarFile instanceof File) {
                formData.append('avatar', this.avatarFile);
            }
            // 查看 FormData 的内容
            //for (let [key, value] of formData.entries()) {
            //    console.log(key, value);
            //}

            // 发送 POST 请求到接口
            axios.post('http://110.42.205.158:5000/api/account/register', formData, { // 暂时是本地mock链接
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then(response => {
                console.log('注册成功:', response.data);
                console.log('token:', response.data.response.token);
                alert('注册成功！');
                // 这里可以添加注册成功后的跳转逻辑
                this.$router.push('/login1')
            })
            .catch(error => {
                console.error('注册失败:', error);

                // 安全获取状态码和响应数据
                const status = error.response?.status;
                const responseData = error.response?.data;

                switch (status) {
                    case 400:
                    {
                        // 使用可选链防止 undefined 报错
                        const errorMessage = responseData?.message || '用户已存在';
                        alert(errorMessage);
                    }
                        break;
                    case 500:
                        alert('服务器内部错误，请稍后再试。');
                        break;
                    default:
                        alert('注册失败: ' + (responseData?.message || error.message || '未知错误'));
                }
            });
        }
    },
    beforeUnmount() {
        // 组件销毁前清除定时器
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
}
</script>

<style scoped>
.registerContainer {
  display: flex;
  flex-direction: column;
  position: relative;
  height: 85vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
  overflow: hidden;
}

.header-section {
  padding: 15px 20px;
  flex-shrink: 0;
}

.back-button {
  width: 24px;
  height: 24px;
  cursor: pointer;
  filter: brightness(0) invert(1);
  transition: all 0.3s ease;
  border-radius: 50%;
  padding: 6px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.back-button:hover {
  transform: translateX(-3px);
  background: rgba(255, 255, 255, 0.3);
}

.form-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 20px 20px;
  background: white;
  margin: 15px 15px 15px;
  border-radius: 30px;
  box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  min-height: 0;
}

.title-section {
  text-align: center;
  margin-bottom: 20px;
  flex-shrink: 0;
}

.title-section h1 {
  font-size: 34px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 6px 0;
  background: linear-gradient(135deg, #3f51b5, #7498ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #7f8c8d;
  font-size: 13px;
  margin: 0;
  font-weight: 400;
}

.form-section {
  width: 100%;
  max-width: 340px;
  margin-bottom: 15px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.input-wrapper {
  margin-bottom: 15px;
  position: relative;
  flex-shrink: 0;
}

.input-group {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  border-radius: 14px;
  padding: 3px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  position: relative;
  width: 90%;
  min-width: 0;
}

.input-group:focus-within {
  border-color: #3f51b5;
  background: white;
  box-shadow: 0 0 0 3px rgba(63, 81, 181, 0.1);
}

.input-icon {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  border-radius: 10px;
  background: linear-gradient(135deg, #3f51b5, #7498ff);
  color: white;
  margin-right: 10px;
  flex-shrink: 0;
}

.styled-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px 6px;
  font-size: 14px;
  color: #2c3e50;
  outline: none;
  min-width: 0;
}

.styled-input::placeholder {
  color: #bdc3c7;
}

.code-input {
  flex: 1;
}

.input-hint {
  position: absolute;
  right: 6px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 10px;
  color: #95a5a6;
  background: white;
  padding: 2px 6px;
  border-radius: 6px;
  white-space: nowrap;
  border: 1px solid #ecf0f1;
  z-index: 1;
}

.send-code {
  width: 80px;
  height: 32px;
  margin-left: 6px;
  font-size: 11px;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #3f51b5, #7498ff);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(63, 81, 181, 0.3);
  flex-shrink: 0;
}

.send-code:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(63, 81, 181, 0.4);
}

.send-code:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.avatar-section {
  display: flex;
  justify-content: center;
  margin: 5px 0;
  flex-shrink: 0;
}

.avatar-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-preview {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #3f51b5;
  transition: all 0.3s ease;
  position: relative;
  margin-bottom: 8px;
}

.avatar-preview:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(63, 81, 181, 0.3);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(63, 81, 181, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  font-size: 20px;
}

.avatar-preview:hover .avatar-overlay {
  opacity: 1;
}

.upload-link {
  color: #3f51b5;
  text-decoration: none;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 3px;
}

.upload-link:hover {
  color: #7498ff;
  transform: translateY(-1px);
}

.action-section {
  width: 100%;
  max-width: 340px;
  text-align: center;
  flex-shrink: 0;
}

.register-button {
  width: 100%;
  max-width: 240px;
  height: 46px;
  font-size: 16px;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #3f51b5, #7498ff);
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 16px rgba(63, 81, 181, 0.3);
  position: relative;
  overflow: hidden;
}

.register-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(63, 81, 181, 0.3);
}

.register-button:active {
  transform: translateY(-1px);
}

.register-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.register-button:hover::before {
  left: 100%;
}

/* 响应式优化 */
@media (max-width: 480px) {
  .form-content {
    margin: 0 10px 10px;
    padding: 12px 15px 15px;
  }
  
  .form-section {
    max-width: 100%;
  }
}
</style>