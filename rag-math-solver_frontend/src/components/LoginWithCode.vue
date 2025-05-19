<template>
    <div class = "loginContainer">
        <img
            src = "@/../public/back.png"
            class="back-button"
            @click="goBack"
            alt="返回"
        >
        <h1>登录</h1>
        <div class="input-group">
            <label>手机号</label>
            <input type="text" placeholder="请输入手机号" v-model="phoneNumber"/>
        </div>
        <div class="input-group-2">
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
        <div class="link-group1">
            <!--a href="/forgot-password" class="link">忘记密码</a-->
            <a href="/login1" class="link">密码登录</a>
        </div>
        <button class="login-button" @click="handleLogin">登录</button>
        <a href="/register" class="link">没有账号？前往注册</a>
    </div>    
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            phoneNumber: '',
            code: '',
            isCounting: false,
            countdown: 60,
            timer: null
        }
    },
    computed: {
        buttonText() {
            return this.isCounting ? `${this.countdown}秒后重试` : '获取验证码';
        }
    },
    methods: {
        goBack() {
        this.$router.push('/')
        // this.$router.go(-1)
        },

        isNumeric(str) {
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
        handleLogin() {
            if (!this.phoneNumber) {
                alert('请输入手机号');
                return;
            }
            if (!this.code) {
                alert('请输入验证码');
                return;
            }
            // 登录逻辑
            axios.post('http://110.42.205.158:5000/api/account/loginWithCode', {
                phonenumber: this.phoneNumber,
                code: this.code
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.data.success) {
                    alert('登录成功');
                    console.log('token:', response.data.response.token);
                    console.log('username:', response.data.response.username);
                    // 将 Token 存储在 localStorage
                    localStorage.setItem("token", response.data.response.token);
                    this.$router.push('/')
                } else {
                    alert('登录失败: ' + response.data.msg);
                }
            })
            .catch(error => {
                console.error('登录失败:', error);
                // 获取 HTTP 状态码
                const status = error.response?.status;            
                // 根据不同的状态码显示不同的错误提示
                switch (status) {
                    case 404:
                        alert('用户不存在');
                        break;
                    default:
                        // 如果没有特定的状态码，显示通用的错误信息
                        alert('登录失败: ' + (error.response?.data?.message || error.message));
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
.loginContainer {
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
.input-group, .input-group-2 {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 300px;
  margin-bottom: 20px;
}
.input-group label, .input-group-2 label {
  width: 60px;
  text-align: right;
  margin-right: 10px;
  font-size: 16px;
}
.input-group input, .input-group-2 input {
  flex: 1;
  padding: 8px;
  font-size: 16px;
  border: 1.5px solid #ccc;
  border-radius: 4px;
}
.input-group-2 input {
  width: 100px;
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
/* 输入框选中时的样式 */
.input-group input:focus, .input-group-2 input:focus {
  border-color: #1989fa;
  outline: none;
}
.link-group1 {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 5px;
}
.link {
  color: #1989fa;
  text-decoration: underline;
  font-size: 14px;
  cursor: pointer;
}
.link:hover {
  color: #0056b3; /* 悬停时颜色变深，可选 */
}
.login-button {
  margin-top: 10px;
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