<template>
    <div class="change-container">
        <h1>修改个人信息</h1>
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
        <div class="input-group-username">
            <label>用户名</label>
            <input type="text" placeholder="请输入用户名" v-model="username"/>
            <span class="input-hint">20个字符以内</span>
        </div>
        <div class="change-group-phonenum">
            <label>手机号</label>
            <div class="phonenum">{{ this.phoneNumber }}</div>
            <button 
                class="change-phonenum" 
                @click="changePhoneNumber"
            >
                修改手机号
            </button>
        </div>
        <div class="link-group1">
            <a @click="changePassword" class="link">修改密码</a>
        </div>
        <button class="change-button" @click="handleChange">确认修改</button>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            avatarPreview: null, // 头像预览URL
            avatarFile: null,   // 存储选择的头像文件
            username: '',
            phoneNumber: ''
        }
    },
    created() {
        this.getBasicUserInfo();
    },
    methods: {
        checkToken() {
            const token = localStorage.getItem("token");
            if (!token) {
                alert('请先登录');
                return false;
            }
            return true;
        },
        getBasicUserInfo() {
            // if (!this.checkToken()) return;
            
            const token = localStorage.getItem("token");
            console.log(token);
            axios.get('http://110.42.205.158:5000/api/account/getBasicUserInfo', {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            })
            .then(response => {
                if (response.data.success) {
                    this.avatarPreview = response.data.response.avatarUrl;
                    this.username = response.data.response.username;
                    this.phoneNumber = response.data.response.phonenumber;
                } else {
                    alert('获取个人信息失败: ' + response.data.msg);
                }
            })
        },
        triggerFileInput() {
            this.$refs.fileInput.click();
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
        handleChange() {
            if (!this.username) {
                alert('请输入用户名');
                return;
            }
            else if (this.username.length > 20) {
                alert('用户名不得超过20个字符');
                return;
            }
            try {
                const token = localStorage.getItem("token");
                // 准备FormData数据
                const formData = new FormData();
            
                // 只添加有变化的字段
                if (this.avatarFile) {
                    formData.append('newAvatarFile', this.avatarFile);
                }            
                if (this.username && this.username.trim() !== '') {
                    formData.append('newUsername', this.username.trim());
                }

                // 发送请求
                axios.put(
                    'http://110.42.205.158:5000/api/account/changeBasicUserInfo',
                    formData,
                    {
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                )
                .then (response => {
                    if (response.data.success) {
                        alert('修改成功');
                        // 重新获取用户信息更新本地数据
                        this.getBasicUserInfo();
                    } else {
                        alert('修改失败: ' + response.data.msg);
                    }
                })
            } catch (error) {
                console.error('修改信息出错:', error);
                alert('修改失败，请稍后重试');
            }
        }, 
        changePhoneNumber() {
            this.$emit('open-changePhoneNumber-modal');
        },
        changePassword() {
            this.$emit('open-changePassword-modal');
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
.input-group-username, .change-group-phonenum {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 320px;
    margin-bottom: 20px;
    position: relative;
}
.input-group-username label, .change-group-phonenum label {
    width: 70px;
    text-align: right;
    margin-right: 10px;
    font-size: 16px;
}
.input-group-username input {
    flex: 1;
    padding: 8px;
    font-size: 16px;
    border: 1.5px solid #ccc;
    border-radius: 4px;
    min-width: 0; /* 防止flex项目溢出 */
}
/* 输入框选中时的样式 */
.input-group-username input:focus {
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