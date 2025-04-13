<template>
    <div class = "registerContainer">
        <img
            src = "@/../public/back.png"
            class="back-button"
            @click="goBack"
            alt="返回"
        >
        <h1>注册</h1>
        <div class="input-group-phone">
            <label>手机号</label>
            <input type="text" placeholder="请输入手机号" v-model="phoneNumber"/>
        </div>
        <div class="input-group-code">
            <label>验证码</label>
            <input type="text" placeholder="请输入验证码" v-model="code"/>
            <button 
                class="send-code" 
                :disabled="isCounting"
                @click="sendVerificationCode"
            >
                {{ buttonText }}
            </button>
        </div>
        <div class="input-group-username">
            <label>用户名</label>
            <input type="text" placeholder="请输入用户名" v-model="username"/>
            <span class="input-hint">20个字符以内</span>
        </div>
        <div class="input-group-pw">
            <label>密码</label>
            <input type="password" placeholder="请输入密码" v-model="password"/>
            <span class="input-hint">6-20个字符,<nav></nav>字母+数字</span>
        </div>
        <div class="input-group-pw2">
            <label>确认密码</label>
            <input type="password" placeholder="请确认密码" v-model="password2"/>
            <span class="input-hint">6-20个字符,<nav></nav>字母+数字</span>
        </div>
        <div class="avatar-upload">
            <div class="avatar-preview" @click="triggerFileInput">
                <img 
                    :src="avatarPreview || require('@/../public/default-avatar.png')" 
                    class="avatar-image"
                    alt="头像"
                >
            </div>
            <input 
                type="file" 
                ref="fileInput"
                @change="handleAvatarUpload"
                accept="image/*"
                style="display: none;"
            >
            <a href="javascript:;" class="upload-link" @click="triggerFileInput">上传头像</a>
        </div>
        <button class="register-button" @click="handleRegister">注册</button>
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
            axios.post('http://127.0.0.1:4523/m1/6179108-5871515-default/api/account/sendCode', {
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
            formData.append('phoneNumber', this.phoneNumber);
            formData.append('code', this.code);
            formData.append('username', this.username);
            formData.append('password', this.password);
    
            // 如果有头像文件，也添加到表单数据中
            if (this.avatarFile instanceof File) {
                formData.append('avatar', this.avatarFile);
            }
            // 查看 FormData 的内容
            //for (let [key, value] of formData.entries()) {
                //console.log(key, value);
            //}

            // 发送 POST 请求到接口
            axios.post('http://127.0.0.1:4523/m1/6179108-5871515-default/api/account/register', formData, { // 暂时是本地mock链接
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then(response => {
                console.log('注册成功:', response.data);
                console.log('token:', response.data.response.token);
                alert('注册成功！');
                // 这里可以添加注册成功后的跳转逻辑
                this.$router.push('/')
            })
            .catch(error => {
                console.error('注册失败:', error);
                // 获取 HTTP 状态码
                const status = error.response?.status;
            
                // 根据不同的状态码显示不同的错误提示
                switch (status) {
                    case 400:
                        console.log('token:', error.response.data.response.token);
                        alert('用户已存在');
                        break;
                    case 500:
                        alert('服务器内部错误，请稍后再试。');
                        break;
                    default:
                        // 如果没有特定的状态码，显示通用的错误信息
                        alert('注册失败: ' + (error.response?.data?.message || error.message));
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
  align-items: center;
  padding-bottom: 40px;
  background-color: #fff;
  border-radius: 20px;
}
.back-button {
  width: 24px;
  height: 27.24px;
  cursor: pointer; /* 鼠标悬停时显示手型 */
  align-self: start;
  margin-left: 30px;
  margin-top: 45px;
  transition: transform 0.2s;
}
h1
{
  text-align: center;
  font-size: 40px;
  margin-top: -12px;
  margin-bottom: 40px;
}
.input-group-phone, .input-group-code, .input-group-username, .input-group-pw, .input-group-pw2 {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 320px;
  margin-bottom: 20px;
  position: relative;
}
.input-group-phone label, .input-group-code label, .input-group-username label, .input-group-pw label, .input-group-pw2 label {
  width: 70px;
  text-align: right;
  margin-right: 10px;
  font-size: 16px;
}
.input-group-phone input, .input-group-code input, .input-group-username input, .input-group-pw input, .input-group-pw2 input {
  flex: 1;
  padding: 8px;
  font-size: 16px;
  border: 1.5px solid #ccc;
  border-radius: 4px;
}
.input-group-code input {
  width: 100px;
}
.input-group-username input, .input-group-pw input, .input-group-pw2 input {
  width: 100px; 
}
/* 输入框选中时的样式 */
.input-group-phone input:focus, .input-group-code input:focus, .input-group-username input:focus, .input-group-pw input:focus, .input-group-pw2 input:focus {
  border-color: #1989fa;
  outline: none;
}
.input-hint {
    left: 100%;
    margin-left: 5px;
    align-items: center;
    white-space: nowrap;
    font-size: 12px;
    color: #999;
    width: auto;
}
.send-code {
  width: 100px;
  height: 32px;
  margin-left: 8px;
  font-size: 16px;
  color: #fff;
  background: linear-gradient(to bottom right, #3f51b5, #7498ff); 
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 0.3s ease;
}
.send-code:disabled {
  background: #ccc !important;
  cursor: not-allowed;
  opacity: 0.7;
}
.avatar-upload {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
}
.avatar-preview {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    cursor: pointer;
    background-color: #f0f0f0;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
}
.avatar-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.upload-link {
  color: #1989fa;
  text-decoration: underline;
  font-size: 14px;
  cursor: pointer;
}
.upload-link:hover {
  color: #0056b3; /* 悬停时颜色变深，可选 */
}
.register-button {
  margin-top: 0px;
  margin-bottom: 10px;
  width: 138px;
  height: 46px;
  padding: 10px 0;
  font-size: 20px;
  font-weight: bolder;
  color: #fff;
  background: linear-gradient(to bottom right, #3f51b5, #7498ff); 
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 0.3s ease;
}
</style>