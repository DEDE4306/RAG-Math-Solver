<template>
    <div class="background">
        <img src="../assets/logo.png" class="logo">
        <div class="right-area">
            <div class="register-component">
                <RegisterComponent class="RegisterComponent"/>
            </div>
        </div>
    </div>
</template>

<script>
import RegisterComponent from '@/components/RegisterComponent.vue';

export default {
    components: {
        RegisterComponent // 注册组件
    }
};
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
html, body {
    height: 100%;
    width: 100%;
    overflow: hidden; /* 禁止任何滚动 */
}
.background {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    background: linear-gradient(to bottom right, #3f51b5, #7498ff);
    height: 100vh;
    width: 100vw;
    min-height: 100%; 
    position: fixed; /* 防止内容溢出导致的滚动 */
    top: 0;
    left: 0;
}
.logo {
    width: 33.33%;
    height: 100%;
}
.right-area {
    width: 66%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.register-component {
    width: 42.5%;
    height: 55%;
    transform: translateX(-10px); /* 向左偏移 10px */
}
</style>