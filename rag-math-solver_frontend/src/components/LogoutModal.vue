<template>
    <div class="logout-container">        
        <h1>退出登录</h1>
        <h4>是否确认退出登录？</h4>
        <h4>退出登录将无法查看本账号历史提问记录。</h4>
        <div class="button-group">
            <button class="logout-button" @click="handleLogout">退出登录</button>
            <button class="cancel-button" @click="handleCancel">取消</button>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        handleLogout() {
            localStorage.removeItem('token');
            alert('退出登录成功');
            this.$router.go(0);
            this.$emit('close');
        },
        handleCancel() {
            this.$emit('close');
        }
    }
}
</script>

<style scoped>
.logout-container {
    display: flex;
    flex-direction: column;
    position: relative;
    align-items: center;
    padding-bottom: 30px;
    background-color: rgba(255, 255, 255, 0);
}
h1 {
    text-align: center;
    font-size: 30px;
    margin-bottom: 20px;
}
h4 {
    text-align: center;
    font-weight: normal;
    margin-top: 0;
    margin-bottom: 0;
}
.button-group {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 15px;
}
.logout-button {
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
.cancel-button {
    margin-top: 15px;
    width: 115px;
    height: 38px;
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background: #ccc; 
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: opacity 0.3s ease;
}
</style>