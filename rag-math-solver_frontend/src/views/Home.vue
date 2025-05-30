<template>
    <img alt="Vue logo" src="../assets/logo.png">
    <div>
      <h1>欢迎来到首页</h1>
      <router-link to="/login1">前往登录页</router-link>
      <a href="javascript:;" @click="openChangeBasicUserInfoModal">修改个人信息</a>
      <a @click="showLogoutModal = true">退出登录</a>
    </div>
    <!-- 弹窗组件 -->
    <div v-if="showChangeBasicUserInfoModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">  <!-- 新增头部容器 -->
          <span class="close" @click="showChangeBasicUserInfoModal = false">&times;</span>
        </div>
        <ChangeBasicUserInfo class="change-component" 
        @open-changePhoneNumber-modal="openChangePhoneNumberModal"
        @open-changePassword-modal="openChangePasswordModal" />
      </div>
    </div>
    <div v-if="showChangePhoneNumberModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">  <!-- 新增头部容器 -->
          <img
            src = "@/../public/back.png"
            class="back-button"
            @click="backtoChangeBasicUserInfoModal"
            alt="返回"
          >
          <span class="close" @click="showChangePhoneNumberModal = false">&times;</span>
        </div>
        <ChangePhoneNumber class="change-component" @changeSuccess="backtoChangeBasicUserInfoModal" />
      </div>
    </div>
    <div v-if="showChangePasswordModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">  <!-- 新增头部容器 -->
          <img
            src = "@/../public/back.png"
            class="back-button"
            @click="backtoChangeBasicUserInfoModal"
            alt="返回"
          >
          <span class="close" @click="showChangePasswordModal = false">&times;</span>
        </div>
        <ChangePassword class="change-component" @changeSuccess="backtoChangeBasicUserInfoModal" />
      </div>
    </div>
    <div v-if="showLogoutModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">  <!-- 新增头部容器 -->
          <span class="close" @click="showLogoutModal = false">&times;</span>
        </div>
        <LogoutModal class="change-component" @close="closeLogoutModal" />
      </div>
    </div>
  </template>
  
<script>
import ChangeBasicUserInfo from '@/components/ChangeBasicUserInfo.vue';
import ChangePhoneNumber from '@/components/ChangePhoneNumber.vue';
import ChangePassword from '@/components/ChangePassword.vue';
import LogoutModal from '@/components/LogoutModal.vue';
export default {
    name: 'HomeView',
    components: {
      ChangeBasicUserInfo,
      ChangePhoneNumber,
      ChangePassword,
      LogoutModal,
    },
    data() {
      return {
        showChangeBasicUserInfoModal: false,
        showChangePhoneNumberModal: false,
        showChangePasswordModal: false,
        showLogoutModal: false,
      }
    },
    methods: {
      // 调试阶段
      clearToken(){localStorage.removeItem('token');},
      openChangeBasicUserInfoModal() {
        const token = localStorage.getItem("token");
        if (!token) {
          alert('请先登录');
          return;
        }
        this.showChangeBasicUserInfoModal = true;
        this.showChangePasswordModal = false;
        this.showChangePhoneNumberModal = false;
      },
      openChangePhoneNumberModal() {
        this.showChangeBasicUserInfoModal = false;
        this.showChangePasswordModal = false;
        this.showChangePhoneNumberModal = true;
      },
      openChangePasswordModal() {
        this.showChangeBasicUserInfoModal = false;
        this.showChangePhoneNumberModal = false;
        this.showChangePasswordModal = true;
      },
      backtoChangeBasicUserInfoModal() {
        this.showChangePhoneNumberModal = false;
        this.showChangePasswordModal = false;
        this.showChangeBasicUserInfoModal = true;
      },
      closeLogoutModal() {
        this.showLogoutModal = false;
      }
    }
}
</script>

<style scoped>
/* 弹窗样式 */
.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}
.modal-content {
  background-color: #fefefe;
  margin: 5% auto;
  padding: 20px;
  width: 27.5%;
  min-width: fit-content;
  height: fit-content;
  border-radius: 20px;
  text-align: center; /* 使内部内容居中 */
  display: flex;
  flex-direction: column;  /* 垂直排列 */
  overflow: hidden;
}
.modal-header {
  display: flex;
  justify-content: flex-end;
  align-items: center; 
  width: 100%;
  margin-bottom: -30px;
  padding: 0 10px;
  box-sizing: border-box;
  position: relative; /* 为绝对定位的返回按钮提供参照 */
}
.back-button {
  width: 24px;
  height: 27.24px;
  cursor: pointer;
  transition: transform 0.2s;
  position: absolute;
  left: 10px;
}
.close {
  color: #3e50b5;
  font-size: 40px;
  font-weight: light;
  cursor: pointer;
  line-height: 1;
}
a {
  display: block;
  margin: 10px 0;
  color: #1989fa;
  text-decoration: underline;
  cursor: pointer;
}
.change-component {
  margin: 0 auto; /* 水平居中 */
  width: fit-content;
}
</style>