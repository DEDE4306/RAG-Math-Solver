<template>
    <div class="change-container">
        <h1>修改密码</h1>
        <div class="change-group-phonenum">
            <label>手机号</label>
            <div class="phonenum">{{ this.phoneNumber }}</div>
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
        <button class="change-button" @click="handleChange">确认修改</button>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            phoneNumber: '',
            code: '',
            password: '',
            password2: '',
            isCounting: false,
            countdown: 60,
            timer: null
        }
    },
    created() {
        this.getBasicUserInfo();
    },
    computed: {
        buttonText() {
            return this.isCounting ? `${this.countdown}秒后重试` : '获取验证码';
        }
    },
    methods: {
        getBasicUserInfo() {
            const token = localStorage.getItem("token");
            console.log(token);
            axios.get('http://110.42.205.158:5000/api/account/getBasicUserInfo', {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            })
            .then(response => {
                if (response.data.success) {
                    this.phoneNumber = response.data.response.phonenumber;
                } else {
                    alert('获取个人信息失败: ' + response.data.msg);
                }
            })
        },
        isNumeric(str) { // 测试是否全是数字
          return /^\d+$/.test(str);
        },
        hasLetterAndNumber(str) { // 测试是否同时包括数字和字母
            // 检查是否包含字母和数字
            const hasLetter = /[a-zA-Z]/.test(str);
            const hasNumber = /[0-9]/.test(str);

            return hasLetter && hasNumber;
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
        handleChange() {
            if (!this.code) {
                alert('请输入验证码');
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
            try {
                const token = localStorage.getItem("token");
                axios.put('http://110.42.205.158:5000/api/account/changePhoneNumber', {
                    phonenumber: this.phoneNumber,
                    code: this.code,
                    newPassword: this.password,
                }, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                })
                .then (response => {
                    if (response.data.success) {
                        alert('修改成功');
                        this.$emit('changeSuccess');
                    } else {
                        alert('修改失败: ' + response.data.msg);
                    }
                })
            }  catch (error) {
                console.error('修改信息出错:', error);
                alert('修改失败，请稍后重试');
            }
        }
    }
}
</script>

<style>
.change-container {
    display: flex;
    flex-direction: column;
    position: relative;
    align-items: center;
    padding-bottom: 30px;
    background-color: rgba(255, 255, 255, 0);
}
h1
{
    text-align: center;
    font-size: 30px;
    margin-bottom: 20px;
}
.input-group-code, .input-group-pw, .input-group-pw2, .change-group-phonenum {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 320px;
    margin-bottom: 20px;
    position: relative;
}
.input-group-code label, .input-group-pw label, .input-group-pw2 label, .change-group-phonenum label {
    width: 70px;
    text-align: right;
    margin-right: 10px;
    font-size: 16px;
}
.input-group-code input, .input-group-pw input, .input-group-pw2 input {
    flex: 1;
    padding: 8px;
    font-size: 16px;
    border: 1.5px solid #ccc;
    border-radius: 4px;
    min-width: 0; /* 防止flex项目溢出 */
}
/* 输入框选中时的样式 */
.input-group-code input:focus, .input-group-pw input:focus, .input-group-pw2 input:focus {
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
.change-group-phonenum {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.phonenum {
    flex: 1;
    text-align: left;
    padding: 8px 0; /* 与输入框相同的垂直padding */
    border: 1.5px solid transparent; /* 保持高度一致 */
    min-height: 36px; /* 与输入框高度一致 */
    box-sizing: border-box;
}
.change-phonenum {
    margin-left: 8px;
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
.change-button {
    margin-top: 15px;
    width: 115px;
    height: 38px;
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background: linear-gradient(to bottom right, #3f51b5, #7498ff); 
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: opacity 0.3s ease;
}
</style>