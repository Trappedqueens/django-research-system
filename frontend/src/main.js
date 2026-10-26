import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css' // 必须引入 ElementPlus 样式

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')