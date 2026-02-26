// frontend/src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'

import './assets/main.css'
// import 'bootstrap/dist/css/bootstrap.min.css' // 부트스트랩 CSS (필요시 주석 해제)
// import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate) // 플러그인 등록

app.use(pinia)
app.use(router)

app.mount('#app')