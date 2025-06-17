import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia' // not needed since GMail-based authentication?

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia()) // not needed since GMail-based authentication?
app.use(router)

app.mount('#app')
