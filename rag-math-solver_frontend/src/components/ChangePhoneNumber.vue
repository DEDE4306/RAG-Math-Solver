<template>
    <div class="change-container">        
        <h1>修改手机号</h1>
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
        handleChange() {
            if (!this.phoneNumber) {
                alert('请输入手机号');
                return;
            }
            if (!this.code) {
                alert('请输入验证码');
                return;
            }
            try {
                const token = localStorage.getItem("token");
                axios.put('http://110.42.205.158:5000/api/account/changePhoneNumber', {
                    newPhonenumber: this.phoneNumber,
                    code: this.code
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

<style scoped>
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
.input-group-phone, .input-group-code {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 320px;
    margin-bottom: 20px;
    position: relative;
}
.input-group-phone label, .input-group-code label {
    width: 70px;
    text-align: right;
    margin-right: 10px;
    font-size: 16px;
}
.input-group-phone input, .input-group-code input {
    flex: 1;
    padding: 8px;
    font-size: 16px;
    border: 1.5px solid #ccc;
    border-radius: 4px;
    min-width: 0; /* 防止flex项目溢出 */
}
/* 输入框选中时的样式 */
.input-group-phone input:focus, .input-group-code input:focus {
  border-color: #1989fa;
  outline: none;
}
.send-code {
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