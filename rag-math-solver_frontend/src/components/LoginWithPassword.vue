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
        <div class="input-group">
            <label>密码</label>
            <input type="password" placeholder="请输入密码" v-model="password"/>
        </div>
        <div class="link-group1">
            <!--a href="/forgot-password" class="link">忘记密码</a-->
            <a href="/login2" class="link">验证码登录</a>
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
            password: ''
        }
    },
    methods: {
        goBack() {
            this.$router.push('/')
            // this.$router.go(-1)
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
            axios.post('http://127.0.0.1:4523/m1/6179108-5871515-default/api/account/loginWithPassword?apifoxResponseId=653736844', {
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
.input-group {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 300px; 
  margin-bottom: 20px;
}
.input-group label {
  width: 60px;
  text-align: right;
  margin-right: 10px;
  font-size: 16px;
}
.input-group input {
  flex: 1;
  padding: 8px;
  font-size: 16px;
  border: 1.5px solid #ccc;
  border-radius: 4px;
}
/* 输入框选中时的样式 */
.input-group input:focus {
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