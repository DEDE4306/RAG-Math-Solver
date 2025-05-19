<template>
    <div class="user-profile">
      <!-- 头像 -->
      <img
        :src="avatarUrl"
        class="avatar"
        alt="用户头像"
        @click="handleAvatarClick"
      />
      <!-- 用户名 -->
      <span class="username" @click="handleUsernameClick">
        {{ username }}
      </span>
      <!-- 菜单（仅在已登录时显示） -->
      <div v-if="isLoggedIn && showMenu" class="menu">
        <div class="menu-item" @click="openChangeBasicUserInfoModal">修改个人信息</div>
        <div class="menu-item" @click="showLogoutModal = true">退出登录</div>
      </div>
      <!-- 弹窗组件（保持不变） -->
      <div v-if="showChangeBasicUserInfoModal" class="modal">
        <div class="modal-content">
          <div class="modal-header">
            <span class="close" @click="showChangeBasicUserInfoModal = false">&times;</span>
          </div>
          <ChangeBasicUserInfo
            class="change-component"
            @open-changePhoneNumber-modal="openChangePhoneNumberModal"
            @open-changePassword-modal="openChangePasswordModal"
          />
        </div>
      </div>
      <div v-if="showChangePhoneNumberModal" class="modal">
        <div class="modal-content">
          <div class="modal-header">
            <img
              src="@/../public/back.png"
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
          <div class="modal-header">
            <img
              src="@/../public/back.png"
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
          <div class="modal-header">
            <span class="close" @click="showLogoutModal = false">&times;</span>
          </div>
          <LogoutModal class="change-component" @close="closeLogoutModal" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import ChangeBasicUserInfo from '@/components/ChangeBasicUserInfo.vue';
  import ChangePhoneNumber from '@/components/ChangePhoneNumber.vue';
  import ChangePassword from '@/components/ChangePassword.vue';
  import LogoutModal from '@/components/LogoutModal.vue';
  
  export default {
    name: 'UserProfile',
    components: {
      ChangeBasicUserInfo,
      ChangePhoneNumber,
      ChangePassword,
      LogoutModal,
    },
    data() {
      return {
        isLoggedIn: false,
        username: '当前未登录',
        avatarUrl: require('@/../public/default-avatar.png'),
        showMenu: false,
        showChangeBasicUserInfoModal: false,
        showChangePhoneNumberModal: false,
        showChangePasswordModal: false,
        showLogoutModal: false,
      };
    },
    mounted() {
      this.fetchUserInfo();
      document.addEventListener('click', this.closeMenu);
    },
    beforeUnmount() {
      document.removeEventListener('click', this.closeMenu);
    },
    methods: {
      async fetchUserInfo() {
        const token = localStorage.getItem('token');
        console.log('fetchUserInfo token:', token);
        if (!token) {
          this.isLoggedIn = false;
          this.username = '当前未登录';
          this.avatarUrl = require('@/../public/default-avatar.png');
          console.log('No token, isLoggedIn:', this.isLoggedIn);
          return;
        }
  
        try {
          const response = await axios.get(
            'http://110.42.205.158:5000/api/account/getBasicUserInfo',
            {
              headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
              },
            }
          );
          console.log('fetchUserInfo response:', response.data);
          if (response.data.success) {
            this.isLoggedIn = true;
            this.username = response.data.response.username || '用户';
            this.avatarUrl = response.data.response.avatarUrl || this.avatarUrl;
          } else {
            this.isLoggedIn = false;
            this.username = '当前未登录';
            this.avatarUrl = require('@/../public/default-avatar.png');
          }
        } catch (error) {
          console.error('获取用户信息失败:', error);
          this.isLoggedIn = false;
          this.username = '当前未登录';
          this.avatarUrl = require('@/../public/default-avatar.png');
          if (error.response?.status === 401) {
            localStorage.removeItem('token');
            this.$router.push('/login');
          }
        }
        console.log('fetchUserInfo final state:', { isLoggedIn: this.isLoggedIn });
      },
      handleAvatarClick(event) {
        event.stopPropagation();
        if (!this.isLoggedIn) {
          this.$router.push('/login1');
        } else {
          this.toggleMenu();
        }
      },
      handleUsernameClick(event) {
        event.stopPropagation();
        if (!this.isLoggedIn) {
          this.$router.push('/login1');
        } else {
          this.toggleMenu();
        }
      },
      toggleMenu() {
        this.showMenu = !this.showMenu;
        console.log('toggleMenu:', { isLoggedIn: this.isLoggedIn, showMenu: this.showMenu });
      },
      closeMenu(event) {
        if (this.$el && !this.$el.contains(event.target)) {
          this.showMenu = false;
        }
      },
      clearToken() {
        localStorage.removeItem('token');
      },
      openChangeBasicUserInfoModal() {
        const token = localStorage.getItem('token');
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
      },
    },
  };
  </script>
  
<style scoped>
.user-profile {
  display: flex;
  align-items: center; /* 保持头像和用户名垂直居中 */
  padding: 15px 0px; /* 增大内边距 */
  border-top: 1px solid #e5e5e6;
  position: relative;
  width: 100%; /* 确保占满父容器宽度 */
  justify-content: flex-start; /* 左对齐 */
}
.avatar {
  width: 50px; /* 增大头像尺寸 */
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  cursor: pointer;
  margin-right: 15px; /* 增加与用户名的间距 */
  margin-left: 20px;
}
.avatar:hover {
  opacity: 0.8;
}
.username {
  font-size: 18px; /* 增大字体 */
  color: #333;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.menu {
  position: absolute;
  bottom: 80px; /* 调整菜单位置以适应更大的头像 */
  left: 10px;
  background-color: #fff;
  border: 1px solid #e5e5e6;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 220px;
  z-index: 9999;
}
.menu-item {
  padding: 8px 10px; /* 增大菜单项内边距 */
  font-size: 14px;
  text-align: left;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s;
}
.menu-item:hover {
  background-color: #C5D4FF;
}
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
.change-component {
  margin: 0 auto; /* 水平居中 */
  width: fit-content;
}
  </style>