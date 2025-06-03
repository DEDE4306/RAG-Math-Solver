<template>
    <div class="loginContainer">
        <div class="form-content">
            <div class="title-section">
                <h1>欢迎登录</h1>
                <p class="subtitle">使用密码登录</p>
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
                        <div class="input-icon">🔒</div>
                        <input 
                            type="password" 
                            placeholder="请输入密码" 
                            v-model="password"
                            class="styled-input"
                        />
                    </div>
                </div>
            </div>
            <div class="action-section">
                <div class="link-group1">
                    <a href="/login2" class="link">📱 验证码登录</a>
                </div>
                <button class="login-button" @click="handleLogin">
                    <span>登录</span>
                </button>
                <div class="register-link">
                    <span>还没有账号？</span>
                    <a href="/register" class="link highlight">立即注册</a>
                </div>
            </div>
        </div>
    </div>    
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            phoneNumber: '',
            password: ''
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
        handleLogin() {
            if (!this.phoneNumber) {
                alert('请输入手机号');
                return;
            }
            else if (this.phoneNumber.length != 11 || this.isNumeric(this.phoneNumber) == false) {
                alert('请输入正确手机号');
                return;
            }
            if (!this.password) {
                alert('请输入密码');
                return;
            }
            // 登录逻辑
            axios.post('http://110.42.205.158:5000/api/account/loginWithPassword?apifoxResponseId=653736844', {
                phonenumber: this.phoneNumber,
                password: this.password
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
                    case 400:
                        alert('密码错误');
                        break;
                    case 404:
                        alert('用户不存在');
                        break;
                    default:
                        // 如果没有特定的状态码，显示通用的错误信息
                        alert('登录失败: ' + (error.response?.data?.message || error.message));
                }
            });
        }
    }
}
</script>

<style scoped>
.loginContainer {
  display: flex;
  flex-direction: column;
  position: relative;
  min-height: 75vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
}

.header-section {
  padding: 20px 30px;
}

.form-content {
  height: 100px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px 40px 60px;
  background: white;
  margin: 20px;
  border-radius: 30px;
  box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.1);
}

.title-section {
  text-align: center;
  margin-bottom: 40px;
}

.title-section h1 {
  font-size: 40px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
  background: linear-gradient(135deg, #3f51b5, #7498ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #7f8c8d;
  font-size: 16px;
  margin: 0;
  font-weight: 400;
}

.form-section {
  width: 100%;
  max-width: 350px;
  margin-bottom: 30px;
}

.input-wrapper {
  margin-bottom: 24px;
}

.input-group, .input-group-2 {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  border-radius: 16px;
  padding: 4px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  position: relative;
}

.input-group:focus-within, .input-group-2:focus-within {
  border-color: #3f51b5;
  background: white;
  box-shadow: 0 0 0 4px rgba(63, 81, 181, 0.1);
}

.input-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  border-radius: 12px;
  background: linear-gradient(135deg, #3f51b5, #7498ff);
  color: white;
  margin-right: 12px;
}

.styled-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 16px 8px;
  font-size: 16px;
  color: #2c3e50;
  outline: none;
}

.styled-input::placeholder {
  color: #bdc3c7;
}

.code-input {
  max-width: 140px;
}

.send-code {
  width: 110px;
  height: 40px;
  margin-left: 8px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #3f51b5, #7498ff);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(63, 81, 181, 0.3);
}

.send-code:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(63, 81, 181, 0.4);
}

.send-code:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.action-section {
  width: 100%;
  max-width: 350px;
  text-align: center;
}

.link-group1 {
  margin-bottom: 24px;
}

.link {
  color: #3f51b5;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.link:hover {
  color: #7498ff;
  transform: translateY(-1px);
}

.login-button {
  width: 100%;
  max-width: 280px;
  height: 52px;
  font-size: 18px;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #3f51b5, #7498ff);
  border: none;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(63, 81, 181, 0.3);
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}

.login-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(63, 81, 181, 0.4);
}

.login-button:active {
  transform: translateY(-1px);
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.login-button:hover::before {
  left: 100%;
}

.register-link {
  color: #7f8c8d;
  font-size: 14px;
}

.register-link .highlight {
  color: #e74c3c;
  font-weight: 600;
  margin-left: 4px;
}

.register-link .highlight:hover {
  color: #c0392b;
}
</style>