<template>
    <div class="background">
        <div class="left-section">
            <div class="logo-container">
                <img src="../assets/logo2.png" class="logo" alt="Logo">
                <div class="logo-overlay">
                    <div class="welcome-text">
                        <p>MathSage</p>
                    </div>
                    <div class="decorative-elements">
                        <div class="floating-circle circle-1"></div>
                        <div class="floating-circle circle-2"></div>
                        <div class="floating-circle circle-3"></div>
                        <div class="floating-shape shape-1"></div>
                        <div class="floating-shape shape-2"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="right-section">
            <div class="register-container">
                <div class="glass-backdrop">
                    <RegisterComponent class="register-component"/>
                </div>
            </div>
            
            <!-- 背景装饰 -->
            <div class="background-decoration">
                <div class="floating-element element-1"></div>
                <div class="floating-element element-2"></div>
                <div class="floating-element element-3"></div>
                <div class="floating-element element-4"></div>
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
    overflow: hidden;
}

.background {
    display: flex;
    height: 100vh;
    width: 100vw;
    position: fixed;
    top: 0;
    left: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #3f51b5 100%);
    overflow: hidden;
}

/* 左侧区域 */
.left-section {
    width: 40%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(63, 81, 181, 0.9), rgba(116, 75, 162, 0.8));
    backdrop-filter: blur(20px);
}

.logo-container {
    position: relative;
    width: 80%;
    height: 80%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

.logo {
    max-width: 100%;
    max-height: 60%;
    object-fit: contain;
    filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.3));
    animation: logoFloat 6s ease-in-out infinite;
}

.logo-overlay {
    position: absolute;
    bottom: 20%;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    z-index: 10;
}

.welcome-text p {
    color: rgba(255, 255, 255, 0.9);
    margin-left: 10px;
    margin-right: 10px;
    font-size: 30px;
    font-weight: 600;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    opacity: 0;
    animation: fadeInUp 1s ease-out 0.8s forwards;
}

/* 装饰元素 */
.decorative-elements {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.floating-circle {
    position: absolute;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.circle-1 {
    width: 80px;
    height: 80px;
    top: 15%;
    left: -45%;
    animation: floatRotate 8s linear infinite;
}

.circle-2 {
    width: 60px;
    height: 60px;
    top: 70%;
    right: -25%;
    animation: floatRotate 10s linear infinite reverse;
}

.circle-3 {
    width: 40px;
    height: 40px;
    top: -30%;
    left: -25%;
    animation: floatBounce 6s ease-in-out infinite;
}

.floating-shape {
    position: absolute;
    background: linear-gradient(45deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.15);
}

.shape-1 {
    width: 50px;
    height: 50px;
    top: 25%;
    right: -30%;
    transform: rotate(45deg);
    animation: shapeFloat 7s ease-in-out infinite;
}

.shape-2 {
    width: 30px;
    height: 30px;
    bottom: 30%;
    left: -40%;
    transform: rotate(30deg);
    animation: shapeFloat 9s ease-in-out infinite reverse;
}

/* 右侧区域 */
.right-section {
    width: 60%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
    backdrop-filter: blur(10px);
}

.register-container {
    width: 85%;
    max-width: 480px;
    height: 80%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 10;
}

.glass-backdrop {
    width: 100%;
    height: auto;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 30px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 
        0 20px 60px rgba(0, 0, 0, 0.15),
        0 8px 32px rgba(63, 81, 181, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
    padding: 0;
    overflow: hidden;
    position: relative;
    animation: slideInRight 1s ease-out;
}

.glass-backdrop::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
}

.register-component {
    width: 100%;
    position: relative;
    z-index: 2;
}

/* 背景装饰 */
.background-decoration {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
}

.floating-element {
    position: absolute;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
    border-radius: 50%;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.element-1 {
    width: 120px;
    height: 120px;
    top: 10%;
    right: 10%;
    animation: floatSlow 12s ease-in-out infinite;
}

.element-2 {
    width: 80px;
    height: 80px;
    bottom: 15%;
    right: 25%;
    animation: floatSlow 15s ease-in-out infinite reverse;
}

.element-3 {
    width: 60px;
    height: 60px;
    top: 50%;
    right: 5%;
    animation: floatBounce 8s ease-in-out infinite;
}

.element-4 {
    width: 40px;
    height: 40px;
    bottom: 40%;
    left: 10%;
    animation: floatRotate 10s linear infinite;
}

/* 动画 */
@keyframes logoFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes floatRotate {
    from { transform: rotate(0deg) translateY(0px); }
    50% { transform: rotate(180deg) translateY(-10px); }
    to { transform: rotate(360deg) translateY(0px); }
}

@keyframes floatBounce {
    0%, 100% { transform: translateY(0px); }
    25% { transform: translateY(-8px); }
    50% { transform: translateY(-15px); }
    75% { transform: translateY(-8px); }
}

@keyframes shapeFloat {
    0%, 100% { transform: rotate(45deg) translateY(0px); }
    50% { transform: rotate(45deg) translateY(-12px); }
}

@keyframes floatSlow {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-20px) scale(1.05); }
}

/* 响应式设计 */
@media (max-width: 1200px) {
    .left-section {
        width: 45%;
    }
    
    .right-section {
        width: 55%;
    }
    
    .register-container {
        width: 90%;
    }
}

@media (max-width: 768px) {
    .background {
        flex-direction: column;
    }
    
    .left-section {
        width: 100%;
        height: 30%;
    }
    
    .right-section {
        width: 100%;
        height: 70%;
    }
    
    .logo-container {
        height: 100%;
    }
    
    .logo {
        max-height: 80%;
    }
    
    .welcome-text h2 {
        font-size: 20px;
    }
    
    .welcome-text p {
        font-size: 14px;
    }
    
    .register-container {
        width: 95%;
        height: 95%;
    }
}

@media (max-width: 480px) {
    .left-section {
        height: 25%;
    }
    
    .right-section {
        height: 75%;
    }
    
    .glass-backdrop {
        border-radius: 20px;
        margin: 10px;
    }
}
</style>